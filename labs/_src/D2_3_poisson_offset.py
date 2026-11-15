# %% [markdown]
# # Lab 2.3 · Leaks with an exposure
#
# Day 2 · Session 3 (Counts and exposure) · 25 min.
#
# Basil Al-Jowair, the pipe network engineer, has weekly leak reports for 1,200 pipe segments and a budget to renew some of them. He asks how the leak rate differs by material, age and pressure. Segments differ in length and some entered service mid-year, so a raw count compares unlike things. You turn the reports into counts with an exposure and fit a Poisson model with an offset.
#
# **Use and estimand.** Descriptive: leaks per kilometre per year by material, age and pressure, across Sahil's segments in 2026, as rate ratios.
#
# **AI policy.** AI-off for the model and its reading. The hint-only tutor may help with the aggregation and the stretch item.
#
# **Reference state.** `data/leaks.csv` and `data/segments.csv`, loaded fresh. Nothing from earlier labs is needed.
#
# **Tasks**
# - [ ] 1 · Weekly reports into one count per segment (5')
# - [ ] 2 · Exposure: kilometres times years in service (4')
# - [ ] 3 · The Poisson model with an offset (6')
# - [ ] 4 · Rate ratios with intervals (6')
# - [ ] 5 · Expected leaks for two segments (4')
# - [ ] ✱ Stretch · Fit length as a predictor in place of the offset and read its coefficient

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-301.git"
    if not Path("/content/ds-301").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-301"], check=True)
    os.chdir("/content/ds-301/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("sahil.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sahil as U
print("mode:", U.MODE)

weekly = U.leaks()
seg = U.segments()
print(f"{len(weekly)} weekly rows for {weekly['segment_id'].nunique()} segments; {weekly['leaks'].sum()} leaks in all")

# %% [markdown]
# ## 1 · Weekly reports into one count per segment (5')
#
# Each segment's predictors do not change from week to week, so one row per segment with its year's count loses nothing a model of these predictors could use.
#
# ✏️ **Exercise** · Return `seg` with a column `leaks`: the sum of the weekly counts of each segment (0 for a segment with no rows).

# %%
def add_counts(seg, weekly):
    # BEGIN SOLUTION
    tot = weekly.groupby("segment_id")["leaks"].sum()
    out = seg.copy()
    out["leaks"] = out["segment_id"].map(tot).fillna(0).astype(int)
    return out
    # END SOLUTION


# %%
try:
    s = add_counts(seg, weekly)
except NotImplementedError:
    print("↪ exercise not done yet: using U.segment_totals()")
    if U.STRICT:
        raise
    s = U.segment_totals()
print(s["leaks"].value_counts().sort_index().head(10).to_string())
U.check(s["leaks"].sum() == weekly["leaks"].sum() and len(s) == 1200, "1,200 segments and every leak counted once")

# %% [markdown]
# ## 2 · Exposure: kilometres times years in service (4')
#
# A 4 km main in service all year has 8 times the chances to leak of a 1 km main in service half the year. The **exposure** is length × weeks in service / 52, in kilometre-years.
#
# ✏️ **Exercise** · Add the column `km_years` to `s`.

# %%
def add_exposure(s):
    # BEGIN SOLUTION
    s = s.copy()
    s["km_years"] = s["length_km"] * s["weeks_in_service"] / 52
    return s
    # END SOLUTION


# %%
try:
    s = add_exposure(s)
except NotImplementedError:
    print("↪ exercise not done yet: computing the reference exposure")
    if U.STRICT:
        raise
    s["km_years"] = s["length_km"] * s["weeks_in_service"] / 52
print(s["km_years"].describe().round(2).to_string())
raw = s.groupby("material", observed=True).agg(leaks=("leaks", "sum"), km_years=("km_years", "sum"))
raw["per_km_year"] = raw["leaks"] / raw["km_years"]
print(raw.round(3).to_string())
U.check(s["km_years"].max() / s["km_years"].min() > 20, "exposures differ more than twentyfold between segments")

# %% [markdown]
# ## 3 · The Poisson model with an offset (6')
#
# log E[leaks] = log(km_years) + β₀ + β·x. The **offset** log(km_years) enters with a coefficient fixed at 1, so the β describe the rate per kilometre-year.
#
# ✏️ **Exercise** · Fit `leaks ~ material + age_years + pressure_bar` with `smf.glm(..., family=sm.families.Poisson(), offset=np.log(s["km_years"]))` and return the fit.

# %%
FORMULA = "leaks ~ material + age_years + pressure_bar"


def fit_poisson(s):
    # BEGIN SOLUTION
    return smf.glm(FORMULA, data=s, family=sm.families.Poisson(), offset=np.log(s["km_years"])).fit()
    # END SOLUTION


# %%
try:
    po = fit_poisson(s)
except NotImplementedError:
    print("↪ exercise not done yet: fitting the reference model so the cells below run")
    if U.STRICT:
        raise
    po = smf.glm(FORMULA, data=s, family=sm.families.Poisson(), offset=np.log(s["km_years"])).fit()
print(po.summary().tables[1])

# %% [markdown]
# ## 4 · Rate ratios with intervals (6')
#
# ✏️ **Exercise** · Return a DataFrame of rate ratios exp(β) with 95% intervals (columns `rate_ratio`, `low`, `high`), without the intercept. Express age per 10 years: the ratio for 10 years is exp(10 β).

# %%
def rate_ratios(po):
    # BEGIN SOLUTION
    ci = po.conf_int()
    scale = pd.Series(1.0, index=po.params.index)
    scale["age_years"] = 10.0
    out = pd.DataFrame({"rate_ratio": np.exp(po.params * scale), "low": np.exp(ci[0] * scale), "high": np.exp(ci[1] * scale)})
    out = out.drop(index="Intercept")
    return out.rename(index={"age_years": "age, per 10 years"})
    # END SOLUTION


# %%
try:
    rr = rate_ratios(po)
except NotImplementedError:
    rr = U.reference("d2_3", "rate_ratios")
U.keep("d2_3", "rate_ratios", rr)
print(rr.round(3).to_string())
U.check(rr.loc["material[T.asbestos_cement]", "low"] > 1.3 and rr.loc["age, per 10 years", "rate_ratio"] > 1.2,
        "asbestos cement and older mains leak at clearly higher rates")

# %% [markdown]
# ## 5 · Expected leaks for two segments (4')
#
# ✏️ **Exercise** · Predict next year's expected leaks for two 2 km segments in service all year: asbestos cement, 40 years, 5 bar; and PVC, 10 years, 4 bar. Pass the offset to `po.predict(new, offset=...)` and return the two numbers.

# %%
def two_segments(po):
    # BEGIN SOLUTION
    new = pd.DataFrame({"material": pd.Categorical(["asbestos_cement", "PVC"], categories=s["material"].cat.categories),
                        "age_years": [40.0, 10.0], "pressure_bar": [5.0, 4.0], "km_years": [2.0, 2.0]})
    return [float(v) for v in po.predict(new, offset=np.log(new["km_years"]))]
    # END SOLUTION


# %%
try:
    two = two_segments(po)
except NotImplementedError:
    two = U.reference("d2_3", "two")
U.keep("d2_3", "two", two)
print(f"expected leaks a year: {two[0]:.2f} for the old asbestos-cement main, {two[1]:.2f} for the young PVC main ({two[0] / two[1]:.1f} times)")
U.check(two[0] > 4 * two[1], "the old asbestos-cement main is expected to leak several times as often")

# %% [markdown]
# ## ✱ Stretch · Length as a predictor
#
# Fit the same model with `np.log(length_km)` as a predictor and no offset, on the segments in service all year. If leaks are proportional to length, its coefficient is close to 1.

# %%
def stretch():
    # BEGIN SOLUTION
    full = s[s["weeks_in_service"] == 52]
    f = smf.glm("leaks ~ material + age_years + pressure_bar + np.log(length_km)", data=full, family=sm.families.Poisson()).fit()
    lo, hi = f.conf_int().loc["np.log(length_km)"]
    print(f"coefficient of log length: {f.params['np.log(length_km)']:.3f} (95% interval {lo:.3f} to {hi:.3f})")
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
t = U.truth()["leaks"]
U.note(f"Checked against the truth: the generator's rate rises by {t['age_per_year']} per year of age on the log scale (a ratio of {np.exp(10 * t['age_per_year']):.2f} per 10 years) and asbestos cement adds {t['material']['asbestos_cement']}.",
       "Checked: the offset makes every segment's count comparable per kilometre-year.",
       "Not checked yet: whether the counts vary as much as a Poisson model allows. Lab 2.4 tests it.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is log(km_years) an offset and not just another predictor?
#    <details><summary>Answer</summary>Because the count is assumed proportional to exposure: its coefficient is fixed at 1, so the other coefficients describe a rate.</details>
# 2. The rate ratio for asbestos cement is 1.6. What does it say?
#    <details><summary>Answer</summary>Asbestos-cement mains have about 1.6 times the leaks per kilometre-year of PVC mains of the same age and pressure, in these data.</details>
# 3. What happens to segments with no leak this year?
#    <details><summary>Answer</summary>They stay in the model with a count of 0. Dropping them would make every rate look higher.</details>
#
# ## Carry forward
#
# Lab 2.4 tests whether these counts are more variable than a Poisson model allows.
