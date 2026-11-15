"""Write the synthetic data of Sahil Water (شركة ساحل للمياه) for the DS-301 labs.

    uv run python prepare_data.py

Fixed seed 301: the same files on every run. Nothing here describes a real utility, household,
district or person. Household keys are pseudonyms. The true parameters go to solutions/truth.json,
for the trainer; what is planted and which lab finds it is in solutions/answer_key.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
CAP = LABS / "capstone" / "data"
SEED = 301

TRUTH: dict = {}

MONTH_TEMP = [19.0, 21.0, 24.0, 28.0, 32.0, 35.0, 37.0, 37.0, 34.0, 30.0, 25.0, 21.0]
BANDS = ["social", "standard", "villa"]
PRICE = {"social": 3.0, "standard": 5.0, "villa": 7.5}  # SAR per cubic metre, fictional
FIXED_FEE = 15.0

# the consumption model, on the log of cubic metres a month
B0 = 2.55
BAND_SHIFT = {"social": -0.12, "standard": 0.0, "villa": 0.40}
SIZE_SLOPE = {"social": 0.075, "standard": 0.095, "villa": 0.115}
PRESSURE_EFFECT = -0.06
SD_DISTRICT = 0.10
SD_HOUSEHOLD = 0.30


def temp_effect(t):
    t = np.asarray(t, dtype=float)
    return 0.012 * (t - 25.0) + 0.0035 * np.maximum(t - 28.0, 0.0) ** 2


def write_csv(df: pd.DataFrame, path: Path, decimals: dict | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df = df.copy()
    for col, d in (decimals or {}).items():
        df[col] = df[col].round(d)
    df.to_csv(path, index=False, lineterminator="\n")


def write_json(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")


# ------------------------------------------------------------------ districts

def make_districts(rng: np.random.Generator) -> pd.DataFrame:
    raw = np.exp(rng.normal(0.0, 1.05, 30))
    sizes = np.maximum(np.round(raw / raw.sum() * 40000), 40).astype(int)
    sizes[-1] = 60  # D30, a new development on the edge of the city
    sizes[int(np.argmax(sizes))] += 40000 - sizes.sum()
    coastal = (rng.uniform(size=30) < 0.45).astype(int)
    temp_offset = np.where(coastal == 1, rng.uniform(-1.8, -0.2, 30), rng.uniform(0.5, 2.8, 30))
    managed = np.zeros(30, dtype=int)
    managed[rng.choice(29, size=13, replace=False)] = 1
    u = rng.normal(0.0, SD_DISTRICT, 30)
    d = pd.DataFrame({
        "district": [f"D{i + 1:02d}" for i in range(30)],
        "households": sizes,
        "coastal": coastal,
        "temp_offset_c": temp_offset.round(2),
        "pressure_managed": managed,
        "social_share": rng.uniform(0.10, 0.40, 30).round(3),
        "villa_share": rng.uniform(0.05, 0.35, 30).round(3),
    })
    d.loc[29, ["social_share", "villa_share", "pressure_managed"]] = [0.05, 0.60, 0]
    TRUTH["district_effect"] = dict(zip(d["district"], u.round(4).tolist()))
    d["_u"] = u
    return d


# ------------------------------------------------------------------ bills

def make_bills(rng: np.random.Generator, dist: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in dist.iterrows():
        n = int(r["households"])
        p = np.array([r["social_share"], 1 - r["social_share"] - r["villa_share"], r["villa_share"]])
        band = rng.choice(BANDS, size=n, p=p)
        lam = np.select([band == "social", band == "villa"], [4.5, 4.0], 3.2)
        size = np.minimum(1 + rng.poisson(lam), 12)
        month = rng.integers(1, 13, n)
        temp = np.array(MONTH_TEMP)[month - 1] + r["temp_offset_c"] + rng.normal(0, 1.0, n)
        rows.append(pd.DataFrame({"district": r["district"], "tariff_band": band, "household_size": size,
                                  "bill_month": month, "temperature_c": temp,
                                  "_u": r["_u"], "pressure_managed": r["pressure_managed"]}))
    b = pd.concat(rows, ignore_index=True)
    shift = b["tariff_band"].map(BAND_SHIFT)
    slope = b["tariff_band"].map(SIZE_SLOPE)
    log_m3 = (B0 + shift + slope * b["household_size"] + temp_effect(b["temperature_c"]) + b["_u"]
              + PRESSURE_EFFECT * b["pressure_managed"] + rng.normal(0, SD_HOUSEHOLD, len(b)))
    b["consumption_m3"] = np.exp(log_m3).round(1)
    b["bill_sar"] = (FIXED_FEE + b["consumption_m3"] * b["tariff_band"].map(PRICE)).round(2)

    # late payment: the true model uses the log of the bill
    social = (b["tariff_band"] == "social").astype(float)
    villa = (b["tariff_band"] == "villa").astype(float)
    p_auto = np.select([social == 1, villa == 1], [0.10, 0.55], 0.35)
    b["autopay"] = (rng.uniform(size=len(b)) < p_auto).astype(int)
    lam_prior = np.select([social == 1, villa == 1], [1.1, 0.4], 0.6)
    b["prior_late_12m"] = np.minimum(rng.poisson(lam_prior), 8)
    eta = (-1.75 + 0.90 * np.log(b["bill_sar"] / 100) + 0.50 * social - 2.20 * b["autopay"]
           + 0.45 * b["prior_late_12m"] + 0.04 * b["household_size"])
    b["late"] = (rng.uniform(size=len(b)) < 1 / (1 + np.exp(-eta))).astype(int)
    # planted: a disconnection notice goes out only after a bill is more than 30 days late
    b["notice_sent"] = ((b["late"] == 1) & (rng.uniform(size=len(b)) < 0.30)).astype(int)

    order = rng.permutation(len(b))
    b = b.iloc[order].reset_index(drop=True)
    keys = rng.choice(16 ** 6, size=len(b), replace=False)
    b.insert(0, "household_key", [f"H{k:06x}" for k in keys])
    TRUTH["consumption"] = {"intercept": B0, "band_shift": BAND_SHIFT, "size_slope_by_band": SIZE_SLOPE,
                            "temp_effect": "0.012*(t-25) + 0.0035*max(t-28,0)^2", "pressure_managed": PRESSURE_EFFECT,
                            "sd_district": SD_DISTRICT, "sd_household": SD_HOUSEHOLD}
    TRUTH["late_payment"] = {"intercept": -1.75, "log_bill_over_100": 0.90, "social": 0.50, "autopay": -2.20,
                             "prior_late_12m": 0.45, "household_size": 0.04,
                             "notice_sent": "sent for 30% of late bills only: a consequence of the outcome"}
    TRUTH["late_rate"] = round(float(b["late"].mean()), 4)
    cols = ["household_key", "district", "tariff_band", "household_size", "bill_month", "temperature_c",
            "pressure_managed", "consumption_m3", "bill_sar", "autopay", "prior_late_12m", "late", "notice_sent"]
    return b[cols]


# ------------------------------------------------------------------ pipe segments and weekly leak reports

MATERIAL = {"PVC": 0.0, "ductile_iron": 0.15, "asbestos_cement": 0.55}
LEAK_B0, LEAK_AGE, LEAK_PRESSURE, LEAK_SHAPE = -4.2, 0.03, 0.20, 1.5


def make_segments(rng: np.random.Generator, dist: pd.DataFrame):
    w = np.sqrt(dist["households"].to_numpy())
    counts = np.maximum(np.round(w / w.sum() * 1200), 12).astype(int)
    counts[int(np.argmax(counts))] += 1200 - counts.sum()
    segs = []
    for (_, r), k in zip(dist.iterrows(), counts):
        mat = rng.choice(list(MATERIAL), size=k, p=[0.5, 0.3, 0.2])
        age = np.select([mat == "PVC", mat == "ductile_iron"],
                        [rng.uniform(2, 25, k), rng.uniform(5, 40, k)], rng.uniform(30, 55, k))
        pmean = 3.8 if r["pressure_managed"] else 4.6
        pressure = rng.normal(pmean, 0.5, k)
        if r["district"] == "D30":  # new development: young PVC mains at high pressure
            mat = np.array(["PVC"] * k)
            age = rng.uniform(1, 4, k)
            pressure = rng.normal(6.4, 0.3, k)
        length = np.clip(np.exp(rng.normal(0.0, 0.7, k)), 0.1, 8.0)
        weeks = np.where(rng.uniform(size=k) < 0.9, 52, rng.integers(10, 52, k))
        segs.append(pd.DataFrame({"district": r["district"], "length_km": length, "material": mat,
                                  "age_years": age, "pressure_bar": pressure, "weeks_in_service": weeks}))
    s = pd.concat(segs, ignore_index=True)
    s.insert(0, "segment_id", [f"S{i + 1:04d}" for i in range(len(s))])
    s["length_km"] = s["length_km"].round(2)
    s["age_years"] = s["age_years"].round(1)
    s["pressure_bar"] = s["pressure_bar"].round(2)
    frailty = rng.gamma(LEAK_SHAPE, 1 / LEAK_SHAPE, len(s))
    rate = np.exp(LEAK_B0 + LEAK_AGE * s["age_years"] + s["material"].map(MATERIAL)
                  + LEAK_PRESSURE * (s["pressure_bar"] - 4.5)) * frailty  # leaks per km per week
    rows = []
    for i, r in s.iterrows():
        n = int(r["weeks_in_service"])
        start = 53 - n
        counts_w = rng.poisson(rate[i] * r["length_km"], n)
        rows.append(pd.DataFrame({"segment_id": r["segment_id"], "week": np.arange(start, 53), "leaks": counts_w}))
    leaks = pd.concat(rows, ignore_index=True)
    TRUTH["leaks"] = {"intercept_per_km_week": LEAK_B0, "age_per_year": LEAK_AGE, "material": MATERIAL,
                      "pressure_per_bar_above_4_5": LEAK_PRESSURE, "segment_frailty": f"gamma, shape {LEAK_SHAPE}, mean 1",
                      "implied_nb_alpha": round(1 / LEAK_SHAPE, 4)}
    return s, leaks


def make_district_leaks(seg: pd.DataFrame, leaks: pd.DataFrame) -> pd.DataFrame:
    tot = leaks.groupby("segment_id")["leaks"].sum()
    s = seg.set_index("segment_id").join(tot.rename("leaks"))
    s["km_weeks"] = s["length_km"] * s["weeks_in_service"] / 52
    g = s.groupby("district")
    d = pd.DataFrame({
        "km_of_pipe": g["km_weeks"].sum(),
        "leaks_2026": g["leaks"].sum(),
        "mean_age_years": g.apply(lambda x: np.average(x["age_years"], weights=x["length_km"]), include_groups=False),
        "mean_pressure_bar": g.apply(lambda x: np.average(x["pressure_bar"], weights=x["length_km"]), include_groups=False),
    }).reset_index()
    # planted: two districts whose kilometres were keyed in tens of kilometres
    for dd in ["D08", "D21"]:
        d.loc[d["district"] == dd, "km_of_pipe"] /= 10
    d["leaks_per_100km"] = 100 * d["leaks_2026"] / d["km_of_pipe"]
    TRUTH["district_leaks_planted"] = {"unit_error": ["D08", "D21"], "genuine_new_district": "D30"}
    return d.round({"km_of_pipe": 2, "mean_age_years": 1, "mean_pressure_bar": 2, "leaks_per_100km": 1})


# ------------------------------------------------------------------ 120 candidate predictors (lab 4.3)

def make_candidates(rng: np.random.Generator, bills: pd.DataFrame) -> pd.DataFrame:
    n = 2000
    pool = bills[bills["tariff_band"] != "social"].sample(n, random_state=SEED).reset_index(drop=True)
    level = np.log(pool["consumption_m3"].to_numpy()) - temp_effect(pool["temperature_c"].to_numpy())
    level = (level - level.mean()) / level.std()
    cols: dict[str, np.ndarray] = {}
    season = np.array(MONTH_TEMP)
    for m in range(12):
        cols[f"lag_m{m + 1:02d}"] = 3.1 + 0.30 * level + temp_effect(season[m]) + rng.normal(0, 0.10, n)
    size_f = rng.normal(0, 1, n) + 0.5 * level
    prop = ["floor_area_m2", "rooms", "bathrooms", "garden_m2", "pool", "floors", "building_age", "roof_tank_l",
            "ground_tank_l", "parking_spaces", "balconies", "kitchens", "maid_room", "majlis_rooms", "laundry_room",
            "plot_area_m2", "shaded_area_m2", "trees", "fountain", "car_wash_bay"]
    for j, name in enumerate(prop):
        cols[f"prop_{name}"] = 0.7 * size_f + rng.normal(0, 0.7, n) + (0.3 * level if j in (3, 4, 15) else 0)
    use_f = rng.normal(0, 1, n) + 0.4 * level
    app = ["ac_units", "washer_loads_week", "dishwasher", "irrigation_timer", "drip_irrigation", "sprinklers",
           "water_heater_l", "showers_day", "baths_week", "low_flow_taps", "dual_flush", "filter_unit",
           "car_washes_month", "pool_refills_year", "garden_hours_week", "cleaning_days_week", "guests_week",
           "ramadan_guests", "summer_away_weeks", "home_office", "cooler_units", "ice_maker", "aquarium",
           "pets", "laundry_service", "maid_live_in", "leak_reported_last_year", "meter_checks_year",
           "app_logins_month", "bill_queries_year"]
    for j, name in enumerate(app):
        cols[f"use_{name}"] = 0.6 * use_f + rng.normal(0, 0.8, n)
    dtemp = pool["district"].map(lambda d: int(d[1:])).to_numpy()
    base_w = rng.normal(0, 1, 31)[dtemp]
    wx = ["summer_mean_c", "summer_max_c", "humidity_pct", "dust_days", "rain_mm", "wind_ms", "night_min_c",
          "heatwave_days", "elevation_m", "distance_sea_km", "green_cover_pct", "density_hh_km2",
          "new_build_share", "network_age_years", "pressure_bar", "outage_hours", "tanker_calls",
          "mosques_km2", "schools_km2", "shops_km2"]
    for name in wx:
        cols[f"area_{name}"] = 0.8 * base_w + rng.normal(0, 0.6, n)
    for q in range(38):
        cols[f"survey_q{q + 1:02d}"] = rng.normal(0, 1, n)
    X = pd.DataFrame(cols)
    y = (0.10 + 0.25 * X["lag_m06"] + 0.30 * X["lag_m07"] + 0.25 * X["lag_m08"]
         + 0.06 * X["prop_garden_m2"] + 0.05 * X["prop_pool"] + 0.04 * X["use_ac_units"]
         + 0.03 * X["use_irrigation_timer"] + 0.03 * X["area_summer_max_c"] + rng.normal(0, 0.12, n))
    TRUTH["candidates"] = {"true_terms": {"lag_m06": 0.25, "lag_m07": 0.30, "lag_m08": 0.25, "prop_garden_m2": 0.06,
                                          "prop_pool": 0.05, "use_ac_units": 0.04, "use_irrigation_timer": 0.03,
                                          "area_summer_max_c": 0.03}, "noise_sd": 0.12}
    flagged = pd.DataFrame({
        "member_chronic_condition": (rng.uniform(size=n) < 0.12).astype(int),
        "nationality_group": rng.choice(["A", "B", "C", "D"], n),
        "monthly_income_band": np.clip(np.round(2.5 + 0.8 * size_f + rng.normal(0, 1, n)), 1, 6).astype(int),
        "employer_sector": rng.choice(["government", "private", "self", "none"], n),
        "phone_brand": rng.choice(["P", "Q", "R"], n),
        "head_marital_status": rng.choice(["married", "single", "other"], n, p=[0.7, 0.2, 0.1]),
    })
    out = pd.concat([pd.DataFrame({"household_key": pool["household_key"]}), flagged, X.round(3),
                     pd.DataFrame({"next_august_log_m3": y.round(3)})], axis=1)
    return out


# ------------------------------------------------------------------ five claims (lab 1.1)

CLAIMS = [
    {"id": 1, "source": "A daily newspaper, on the region's water bills",
     "text": "Households on the social tariff use 12% less water than other households. The social tariff is teaching low-income families to save water.",
     "evidence": "a comparison of one month of bills across 40,000 households"},
    {"id": 2, "source": "A utility's annual report",
     "text": "Our demand model, fitted on three years of bills, forecast last summer's peak demand in each district within 6%.",
     "evidence": "forecasts made before the summer, checked against the summer's meter readings"},
    {"id": 3, "source": "A ministry dashboard note",
     "text": "Districts in the pressure management programme reported 18% fewer leaks per kilometre of main than the other districts in 2026.",
     "evidence": "leak reports and network lengths for all districts in one year"},
    {"id": 4, "source": "A research abstract",
     "text": "Households randomly chosen to receive a monthly usage letter used 4% less water over six months (95% interval 2% to 6%) than households that were not.",
     "evidence": "a randomised trial in 1,200 households"},
    {"id": 5, "source": "A software vendor's brochure",
     "text": "Our model flags the customers who will pay late with 85% accuracy, and reminders sent to flagged customers cut late payment in half.",
     "evidence": "a model scored on past bills; no reminders were sent while it was tested"},
]
CLAIMS_KEY = [
    {"id": 1, "stated_use": "causal", "supported": False,
     "reason": "a comparison of different households cannot separate the tariff from income, size and housing"},
    {"id": 2, "stated_use": "predictive", "supported": True,
     "reason": "forecasts were made before the outcome and checked against it, which is what a predictive claim needs"},
    {"id": 3, "stated_use": "descriptive", "supported": True,
     "reason": "it reports a difference between groups in one year and claims nothing about what caused it"},
    {"id": 4, "stated_use": "causal", "supported": True,
     "reason": "random assignment makes the two groups alike except for the letter, so the difference estimates its effect"},
    {"id": 5, "stated_use": "causal", "supported": False,
     "reason": "accuracy supports the prediction, but no reminders were sent, so the halving is not evidence of an effect"},
]


# ------------------------------------------------------------------ capstone datasets

def make_capstone(rng: np.random.Generator, dist: pd.DataFrame) -> list[dict]:
    # C1: low-pressure complaints per district and month
    rows = []
    for _, r in dist.iterrows():
        for m in range(1, 13):
            cust = int(r["households"] * rng.uniform(0.97, 1.03))
            t = MONTH_TEMP[m - 1] + r["temp_offset_c"]
            mu = cust / 1000 * np.exp(0.2 + 0.05 * (t - 28) + 0.35 * r["pressure_managed"]) * rng.gamma(2.0, 0.5)
            rows.append({"district": r["district"], "month": m, "customers": cust, "mean_temp_c": round(t, 1),
                         "pressure_managed": int(r["pressure_managed"]), "complaints": int(rng.poisson(mu))})
    c1 = pd.DataFrame(rows)
    c1.loc[(c1["district"] == "D05") & (c1["month"] == 7), "complaints"] *= 6  # planted: a burst main week logged as complaints
    write_csv(c1, CAP / "c1_pressure_complaints.csv")

    # C2: the water-saving kit offer, channel randomised
    n = 6000
    band = rng.choice(BANDS, n, p=[0.3, 0.5, 0.2])
    size = np.minimum(1 + rng.poisson(3.6, n), 12)
    district = rng.choice(dist["district"].to_numpy(), n, p=(dist["households"] / dist["households"].sum()).to_numpy())
    cons = np.exp(2.6 + 0.09 * size + np.vectorize(BAND_SHIFT.get)(band) + rng.normal(0, 0.3, n))
    channel = rng.choice(["letter", "sms"], n)
    eta = -1.6 + 0.35 * (channel == "sms") + 0.25 * (band == "villa") * (channel == "sms") + 0.02 * cons - 0.3 * (band == "social")
    took = (rng.uniform(size=n) < 1 / (1 + np.exp(-eta))).astype(int)
    c2 = pd.DataFrame({"household_key": [f"K{k:06x}" for k in rng.choice(16 ** 6, n, replace=False)], "district": district,
                       "tariff_band": band, "household_size": size, "consumption_m3": cons.round(1),
                       "channel": channel, "took_kit": took})
    write_csv(c2, CAP / "c2_kit_offer.csv")

    # C3: villa peak-month consumption
    n = 3000
    district = rng.choice(dist["district"].to_numpy(), n)
    off = dist.set_index("district").loc[district, "temp_offset_c"].to_numpy()
    u = dist.set_index("district").loc[district, "_u"].to_numpy()
    garden = np.exp(rng.normal(5.0, 0.7, n))
    pool = (rng.uniform(size=n) < 0.3).astype(int)
    timer = (rng.uniform(size=n) < 0.4).astype(int)
    t = 37 + off + rng.normal(0, 1, n)
    y = np.exp(3.2 + 0.25 * np.log(garden / 150) + 0.30 * pool - 0.12 * timer * np.log(garden / 50) + temp_effect(t) + u + rng.normal(0, 0.28, n))
    c3 = pd.DataFrame({"villa_key": [f"V{k:06x}" for k in rng.choice(16 ** 6, n, replace=False)], "district": district,
                       "garden_m2": garden.round(0), "pool": pool, "irrigation_timer": timer,
                       "peak_temp_c": t.round(1), "peak_month_m3": y.round(1)})
    c3.loc[rng.choice(n, 9, replace=False), "garden_m2"] = 0  # planted: nine gardens recorded as zero, not missing
    write_csv(c3, CAP / "c3_villa_peak.csv")
    briefs = [
        {"id": "C1", "file": "c1_pressure_complaints.csv", "title": "Low-pressure complaints",
         "brief": "Ghaliya asks how low-pressure complaints per 1,000 customers move with temperature, and whether districts in the pressure management programme report more of them. The planning committee wants to know which districts to watch next summer.",
         "family_hint": "counts with an exposure", "grouping": "12 months in each of 30 districts"},
        {"id": "C2", "file": "c2_kit_offer.csv", "title": "The water-saving kit offer",
         "brief": "6,000 households were offered a free water-saving kit by a letter or a text message, the channel chosen at random. Ghaliya asks which channel the next offer should use, and whether the answer differs by tariff band.",
         "family_hint": "a binary outcome", "grouping": "households in 30 districts"},
        {"id": "C3", "file": "c3_villa_peak.csv", "title": "Villa peak demand",
         "brief": "Ghaliya asks how much a villa's peak-month consumption rises with garden size and with temperature, and whether an irrigation timer changes the garden effect, to size the summer supply of the villa districts.",
         "family_hint": "a positive continuous outcome", "grouping": "villas in 30 districts"},
    ]
    write_json(briefs, LABS / "capstone" / "briefs.json")
    TRUTH["capstone"] = {"C1": {"planted": "D05 in month 7 has six times its complaints: a burst main logged as complaints",
                                "truth": "log rate = 0.2 + 0.05*(temp-28) + 0.35*managed, gamma frailty shape 2 per district-month"},
                         "C2": {"planted": "the sms effect is larger for villas (interaction 0.25 on the logit)",
                                "truth": "logit = -1.6 + 0.35*sms + 0.25*villa*sms + 0.02*consumption - 0.3*social"},
                         "C3": {"planted": "nine gardens recorded as 0; the timer reduces the garden slope; district effects",
                                "truth": "log y = 3.2 + 0.25 log(garden/150) + 0.30 pool - 0.12 timer*log(garden/50) + temp effect + district"}}
    return briefs


def main() -> None:
    rng = np.random.default_rng(SEED)
    dist = make_districts(rng)
    bills = make_bills(rng, dist)
    seg, leaks = make_segments(rng, dist)
    dleaks = make_district_leaks(seg, leaks)
    cand = make_candidates(rng, bills)
    make_capstone(np.random.default_rng(SEED + 1000), dist)

    write_csv(dist.drop(columns=["_u", "social_share", "villa_share"]), DATA / "districts.csv")
    write_csv(bills, DATA / "bills.csv", {"temperature_c": 1})
    write_csv(seg, DATA / "segments.csv")
    write_csv(leaks, DATA / "leaks.csv")
    write_csv(dleaks, DATA / "qusai" / "district_leaks.csv")
    write_csv(cand, DATA / "candidates.csv")
    write_json(CLAIMS, DATA / "claims.json")
    write_json(CLAIMS_KEY, DATA / "claims_key.json")
    write_json({"flagged": ["member_chronic_condition", "nationality_group", "monthly_income_band", "employer_sector",
                            "phone_brand", "head_marital_status"],
                "purpose": "planning next summer's supply, from data collected for billing"}, DATA / "candidates_key.json")
    write_json(TRUTH, LABS / "solutions" / "truth.json")
    print(f"bills {len(bills)}, late rate {bills['late'].mean():.3f}; segments {len(seg)}, weekly rows {len(leaks)}, "
          f"leaks {leaks['leaks'].sum()}; candidates {cand.shape}")


if __name__ == "__main__":
    main()
