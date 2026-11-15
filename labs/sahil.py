"""Helpers for the DS-301 labs: the data of Sahil Water, effects with intervals, checks and safety nets.

    import sahil as U

NumPy, pandas, patsy and statsmodels. Nothing calls or downloads a model.

Environment variables
    DS301_QUICK=1      fewer simulations, repeats and bootstrap samples, for a fast run
    DS301_STRICT=1     solution runs: a failed check stops the run
    DS301_WRITE_REF=1  the trainer's run that writes data/reference/ (the safety nets read it)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

for _stream in (sys.stdout, sys.stderr):  # a Windows console or a redirected run may not default to UTF-8
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
REF = DATA / "reference"

QUICK = os.environ.get("DS301_QUICK", "0") == "1"
STRICT = os.environ.get("DS301_STRICT", "0") == "1"
WRITE_REF = os.environ.get("DS301_WRITE_REF", "0") == "1"
MODE = "quick" if QUICK else "full"
SEED = 301
BANDS = ["social", "standard", "villa"]


def pick(full, quick):
    """The full value, or the small one in quick mode."""
    return quick if QUICK else full


def rng(offset: int = 0) -> np.random.Generator:
    """A seeded generator. The same offset gives the same draws on every run."""
    return np.random.default_rng(SEED + offset)


# ---------------------------------------------------------------- checks and safety nets

def check(ok, what: str) -> bool:
    """Print a tick or a cross. In a solution run (DS301_STRICT=1) a cross stops the run."""
    ok = bool(ok)
    print(("✅ " if ok else "❌ ") + what)
    if STRICT and not ok:
        raise AssertionError(what)
    return ok


def _jsonable(v):
    if isinstance(v, pd.DataFrame):
        return {"__frame__": json.loads(v.to_json(orient="split"))}
    if isinstance(v, np.ndarray):
        return {"__array__": v.tolist()}
    if isinstance(v, (np.floating, np.integer, np.bool_)):
        return v.item()
    if isinstance(v, dict):
        return {str(k): _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    return v


def _unjson(v):
    if isinstance(v, dict):
        if "__array__" in v:
            return np.array(v["__array__"])
        if "__frame__" in v:
            f = v["__frame__"]
            return pd.DataFrame(f["data"], index=f["index"], columns=f["columns"])
        return {k: _unjson(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_unjson(x) for x in v]
    return v


def keep(lab: str, name: str, value):
    """Return value. In the trainer's run, also store it as the reference of this exercise."""
    if WRITE_REF:
        REF.mkdir(parents=True, exist_ok=True)
        path = REF / f"{lab}.{MODE}.json"
        store = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        store[name] = _jsonable(value)
        path.write_text(json.dumps(store, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return value


def reference(lab: str, name: str):
    """The reference result of an exercise, so the cells after it run when it is not done yet."""
    if STRICT:
        raise AssertionError(f"the solution run reached the safety net of {lab}/{name}")
    print(f"↪ exercise not done yet: using the reference result for {name}")
    return stored(lab, name)


def stored(lab: str, name: str, mode: str | None = None):
    """A stored reference result (the trainer's solution run), read without printing anything."""
    store = json.loads((REF / f"{lab}.{mode or MODE}.json").read_text(encoding="utf-8"))
    return _unjson(store[name])


# ---------------------------------------------------------------- the data of Sahil Water

def districts() -> pd.DataFrame:
    """30 districts: households, coastal, temperature offset, pressure management."""
    return pd.read_csv(DATA / "districts.csv")


def bills() -> pd.DataFrame:
    """40,000 household bills, one month each. household_key is a pseudonym, never a name or an address.

    consumption_m3 is the month's consumption; log_m3 is added here. tariff_band is a category with
    'standard' as the reference level.
    """
    b = pd.read_csv(DATA / "bills.csv")
    b["tariff_band"] = pd.Categorical(b["tariff_band"], categories=["standard", "social", "villa"])
    b["log_m3"] = np.log(b["consumption_m3"])
    return b


def segments() -> pd.DataFrame:
    """1,200 pipe segments: district, length_km, material, age_years, pressure_bar, weeks_in_service."""
    s = pd.read_csv(DATA / "segments.csv")
    s["material"] = pd.Categorical(s["material"], categories=["PVC", "ductile_iron", "asbestos_cement"])
    return s


def leaks() -> pd.DataFrame:
    """Weekly leak reports: one row per segment and week in service."""
    return pd.read_csv(DATA / "leaks.csv")


def segment_totals() -> pd.DataFrame:
    """One row per segment: the year's leaks and the exposure in kilometre-years."""
    s = segments()
    tot = leaks().groupby("segment_id")["leaks"].sum()
    s = s.merge(tot.rename("leaks").reset_index(), on="segment_id", how="left")
    s["leaks"] = s["leaks"].fillna(0).astype(int)
    s["km_years"] = s["length_km"] * s["weeks_in_service"] / 52
    return s


def district_leaks() -> pd.DataFrame:
    """Qusai's district summary of 2026, as he sent it."""
    return pd.read_csv(DATA / "qusai" / "district_leaks.csv")


def candidates() -> pd.DataFrame:
    """2,000 households with 126 candidate columns and next August's log consumption."""
    return pd.read_csv(DATA / "candidates.csv")


def js(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- effects with intervals, by simulation

def design(fit, newdata: pd.DataFrame) -> np.ndarray:
    """The model matrix of a formula fit for new rows (splines keep the knots of the fit).

    It is the same transformation statsmodels applies inside fit.predict(newdata).
    """
    exog, _ = fit._transform_predict_exog(newdata, transform=True)
    return np.asarray(exog, dtype=float)


def coef_draws(fit, n: int, gen: np.random.Generator | None = None, cov=None, k: int | None = None) -> np.ndarray:
    """n draws of the first k coefficients (the model matrix's columns) from their estimated sampling distribution."""
    gen = gen or rng(7)
    k = k or len(fit.model.exog_names)
    beta = np.asarray(fit.params)[:k]
    V = np.asarray(cov if cov is not None else fit.cov_params())[:k, :k]
    return gen.multivariate_normal(beta, V, size=n)


def _inverse(scale: str, fit):
    if scale == "link":
        return lambda eta: eta
    if scale == "m3":  # a model of log consumption, read on the mean scale (normal errors)
        s2 = float(fit.scale)
        return lambda eta: np.exp(eta + s2 / 2)
    if scale == "probability":
        return lambda eta: 1 / (1 + np.exp(-eta))
    if scale == "count":
        return np.exp
    raise ValueError(scale)


def contrast(fit, data: pd.DataFrame, var: str, low, high, scale: str, by: str | None = None,
             n: int | None = None, offset: np.ndarray | None = None, cov=None) -> pd.DataFrame:
    """Average difference in the prediction when var is set to high rather than low, for every row of data.

    scale: 'm3', 'probability', 'count' or 'link'. Returns the estimate and a 95% interval from
    simulation of the coefficients, overall or for each level of by.
    """
    n = n or pick(1000, 300)
    inv = _inverse(scale, fit)
    lo_d, hi_d = data.copy(), data.copy()
    lo_d[var] = low if not callable(low) else low(data[var])
    hi_d[var] = high if not callable(high) else high(data[var])
    X0, X1 = design(fit, lo_d), design(fit, hi_d)
    off = np.zeros(len(data)) if offset is None else np.asarray(offset, dtype=float)
    beta = np.asarray(fit.params)[: X0.shape[1]]
    B = coef_draws(fit, n, cov=cov, k=X0.shape[1])
    groups = [("all", np.ones(len(data), bool))] if by is None else [(g, (data[by] == g).to_numpy()) for g in pd.unique(data[by])]
    rows = []
    for g, m in groups:
        o = off[m]
        est = float(np.mean(inv(X1[m] @ beta + o) - inv(X0[m] @ beta + o)))
        sims = (inv(X1[m] @ B.T + o[:, None]) - inv(X0[m] @ B.T + o[:, None])).mean(axis=0)
        lo, hi = np.percentile(sims, [2.5, 97.5])
        rows.append({"group": g, "estimate": est, "low": float(lo), "high": float(hi), "rows": int(m.sum())})
    return pd.DataFrame(rows).set_index("group")


def predict_band(fit, newdata: pd.DataFrame, scale: str, n: int | None = None, offset=None) -> pd.DataFrame:
    """Predictions for new rows with a 95% interval for the mean, from simulation of the coefficients."""
    n = n or pick(1000, 300)
    inv = _inverse(scale, fit)
    X = design(fit, newdata)
    off = np.zeros(len(newdata)) if offset is None else np.asarray(offset, dtype=float)
    beta = np.asarray(fit.params)[: X.shape[1]]
    sims = inv(X @ coef_draws(fit, n, k=X.shape[1]).T + off[:, None])
    lo, hi = np.percentile(sims, [2.5, 97.5], axis=1)
    est = inv(X @ beta + off)
    return pd.DataFrame({"estimate": est, "low": lo, "high": hi}, index=newdata.index)


def binned_residuals(y, p, x, bins: int = 20) -> pd.DataFrame:
    """Gelman and Hill's binned residuals: mean of (observed minus predicted) in bins of x, with a 2-SE band."""
    d = pd.DataFrame({"r": np.asarray(y) - np.asarray(p), "p": np.asarray(p), "x": np.asarray(x)})
    if d["x"].nunique() <= bins:  # a predictor with few values: one bin per value
        d["bin"] = d["x"]
    else:
        d["bin"] = pd.qcut(d["x"].rank(method="first"), bins, labels=False)
    g = d.groupby("bin", observed=True)
    out = pd.DataFrame({"x_mean": g["x"].mean(), "resid_mean": g["r"].mean(), "n": g.size()})
    pbar = g["p"].mean()
    out["band"] = 2 * np.sqrt(pbar * (1 - pbar) / out["n"])
    out["outside"] = out["resid_mean"].abs() > out["band"]
    return out.reset_index(drop=True)


# ---------------------------------------------------------------- the marked sheet of lab 1.1

def mark_claims(sheet: dict) -> int:
    """Score {claim id: (stated use, supported True/False, reason)} against the key."""
    key = {x["id"]: x for x in js("claims_key.json")}
    score = 0
    for i in sorted(key):
        use, sup, reason = sheet.get(i, ("", None, ""))
        has_reason = len(str(reason).split()) >= 6
        ok = use == key[i]["stated_use"] and sup == key[i]["supported"] and has_reason
        score += ok
        print(f"{'✅' if ok else '❌'} claim {i}: you said {use or 'nothing'}, supported={sup}; key: {key[i]['stated_use']}, supported={key[i]['supported']}"
              + ("" if has_reason else "  (a reason of at least six words is part of the answer)"))
        print(f"   key: {key[i]['reason']}")
    print(f"score: {score} of {len(key)}")
    return score


# ---------------------------------------------------------------- the diagnosis log of Day 3 and the report of lab 4.4

LOG_KINDS = ["missing non-linear term", "influential districts", "overdispersion", "separation", "non-constant variance"]


def log_entry(kind: str, evidence: str, fix: str) -> dict:
    """One line of the diagnosis log: the problem, the evidence that shows it, and the correction."""
    assert kind in LOG_KINDS, f"kind is one of {LOG_KINDS}"
    return {"problem": kind, "evidence": evidence, "fix": fix}


ARTIFACTS = LABS / "artifacts"


def log_save(lab: str, entry: dict) -> None:
    """Add (or replace) this lab's line in artifacts/diagnosis_log.json, the log lab 3.4 assembles."""
    ARTIFACTS.mkdir(exist_ok=True)
    path = ARTIFACTS / "diagnosis_log.json"
    log = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    log[lab] = entry
    path.write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")


def log_read() -> dict:
    """The diagnosis log written so far on this computer (empty when no Day 3 lab has run here)."""
    path = ARTIFACTS / "diagnosis_log.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def qusai_models() -> dict:
    """The four models Qusai Al-Mufarrij left, as he specified them."""
    return js("qusai/models.json")


def text_check(text: str, numbers: dict, words: list[str], max_words: int | None = None) -> bool:
    """Does the text quote every number (as formatted) and use every required phrase?"""
    ok = True
    for name, shown in numbers.items():
        found = str(shown) in text
        ok &= found
        print(f"{'✅' if found else '❌'} quotes the {name}: {shown}")
    low = text.lower()
    for w in words:
        found = w.lower() in low
        ok &= found
        print(f"{'✅' if found else '❌'} says: {w}")
    n = len(text.split())
    print(f"length: {n} words")
    if max_words:
        ok &= n <= max_words
        print(f"{'✅' if n <= max_words else '❌'} at most {max_words} words")
    if STRICT and not ok:
        raise AssertionError("the text misses a number, a required statement or the length")
    return ok


# ---------------------------------------------------------------- plotting and tables

def plt():
    """matplotlib.pyplot with the course defaults; draws to nothing when run as a script."""
    import matplotlib
    if "ipykernel" not in sys.modules:
        import warnings
        matplotlib.use("Agg")
        warnings.filterwarnings("ignore", message=".*non-interactive.*")
    import matplotlib.pyplot as p
    p.rcParams.update({"figure.figsize": (7, 4), "axes.spines.top": False, "axes.spines.right": False,
                       "axes.grid": True, "grid.alpha": 0.25, "font.size": 11})
    return p


def table(header: list[str], rows: list[list], fmt: str = "{:.4g}") -> None:
    """Print a small aligned table."""
    cells = [[fmt.format(v) if isinstance(v, (float, np.floating)) else str(v) for v in r] for r in rows]
    widths = [max(len(h), *(len(r[i]) for r in cells)) for i, h in enumerate(header)]
    print("  ".join(h.ljust(w) for h, w in zip(header, widths)))
    for r in cells:
        print("  ".join(c.rjust(w) for c, w in zip(r, widths)))


def note(*lines: str) -> None:
    """The verification note that closes every lab: what was checked against the truth, and what was not."""
    print("VERIFICATION NOTE")
    for line in lines:
        print(" ·", line)


def truth() -> dict:
    """The generator's true parameters (the trainer's file; the notes at the end of each lab read it)."""
    return json.loads((LABS / "solutions" / "truth.json").read_text(encoding="utf-8"))
