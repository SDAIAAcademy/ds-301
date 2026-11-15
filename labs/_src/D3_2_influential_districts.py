# %% [markdown]
# # Lab 3.2 · Influential districts
#
# Day 3 · Session 2 (Influential observations) · 25 min.
#
# Qusai's district model says older mains do not leak more: its age coefficient is negative. It rests on 30 points, one per district, and a few points can carry a fit of 30. You measure each district's leverage and influence, refit without the three most influential, then trace them before deciding what to do: two are a data error, one is a real district unlike the others.
#
# **Use and estimand.** Descriptive: how district leak rates per 100 km move with the mean age and pressure of their mains, across Sahil's 30 districts in 2026.
#
# **AI policy.** AI-off for the influence measures and the decision. The hint-only tutor may help with the table and the stretch item.
#
# **Reference state.** `data/qusai/district_leaks.csv` as Qusai sent it, and `data/segments.csv` and `data/leaks.csv` for the check in step 4. Nothing from earlier labs is needed.
#
# **Tasks**
# - [ ] 1 · Fit the district model (3')
# - [ ] 2 · Leverage and Cook's distance (6')
# - [ ] 3 · The three districts and the refit without them (6')
# - [ ] 4 · Recompute the kilometres from the segment table (6')
# - [ ] 5 · The second line of the diagnosis log (4')
# - [ ] ✱ Stretch · Compute DFBETA for the age coefficient

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
import statsmodels.formula.api as smf
import sahil as U
print("mode:", U.MODE)

d = U.district_leaks()
spec = U.qusai_models()["district_leaks"]
print(spec["what"], "\n", spec["formula"])

# %% [markdown]
# ## 1 · Fit the district model (3')

# %%
fit = smf.ols(spec["formula"], data=d).fit()
print(fit.summary().tables[1])
U.keep("d3_2", "qusai_fit", fit.params.round(3).to_dict())

# %% [markdown]
# **Look at.** Leak rates falling with age contradicts lab 2.3, where each 10 years of age went with about 38% more leaks per kilometre. Something in these 30 points is pulling the line.

# %% [markdown]
# ## 2 · Leverage and Cook's distance (6')
#
# **Leverage** (the hat value) measures how unusual a district's predictors are; **Cook's distance** combines leverage with the size of its residual into how much all the fitted values move when it is left out.
#
# ✏️ **Exercise** · Return a DataFrame indexed by district with columns `leverage` and `cooks_d`, from `fit.get_influence()` (`hat_matrix_diag`, `cooks_distance[0]`), sorted by `cooks_d`, largest first.

# %%
def influence_table(fit, d):
    # BEGIN SOLUTION
    inf = fit.get_influence()
    out = pd.DataFrame({"leverage": inf.hat_matrix_diag, "cooks_d": inf.cooks_distance[0]}, index=d["district"])
    return out.sort_values("cooks_d", ascending=False)
    # END SOLUTION


# %%
try:
    infl = influence_table(fit, d)
except NotImplementedError:
    infl = U.reference("d3_2", "influence")
U.keep("d3_2", "influence", infl)
show = infl.head(6).join(d.set_index("district")[["km_of_pipe", "leaks_2026", "mean_age_years", "mean_pressure_bar", "leaks_per_100km"]])
print(show.round(3).to_string())
print(f"mean leverage is {3 / len(d):.2f}; a common flag for Cook's distance is 4/n = {4 / len(d):.2f}")
top3 = list(infl.index[:3])
U.check(set(top3) == {"D08", "D21", "D30"}, "three districts stand out: D21 and D08 by their residuals, D30 by its leverage")

# %% [markdown]
# ## 3 · The three districts and the refit without them (6')
#
# ✏️ **Exercise** · Refit the model without the three districts of `top3` and return the fit.

# %%
def refit_without(d, drop):
    # BEGIN SOLUTION
    return smf.ols(spec["formula"], data=d[~d["district"].isin(drop)]).fit()
    # END SOLUTION


# %%
try:
    f3 = refit_without(d, top3)
    without = {"age": float(f3.params["mean_age_years"]), "age_se": float(f3.bse["mean_age_years"]),
               "pressure": float(f3.params["mean_pressure_bar"])}
except NotImplementedError:
    without = U.reference("d3_2", "without")
U.keep("d3_2", "without", without)
print(f"age coefficient: {fit.params['mean_age_years']:.2f} with all 30 districts, {without['age']:.2f} without the three (standard error {without['age_se']:.2f})")
U.check(fit.params["mean_age_years"] < 0 < without["age"], "the sign of the age coefficient turns on three districts")

# %% [markdown]
# **Stop before deleting.** Dropping points until the fit looks right is how wrong models get published. Ask what each district is.

# %% [markdown]
# ## 4 · Recompute the kilometres from the segment table (6')
#
# ✏️ **Exercise** · From `U.segment_totals()`, compute each district's kilometre-years (sum of `km_years`) and leaks, and return a DataFrame indexed by district with `km_recomputed`, `leaks_recomputed` and `km_ratio` (Qusai's `km_of_pipe` divided by yours).

# %%
def recompute(d):
    # BEGIN SOLUTION
    s = U.segment_totals()
    g = s.groupby("district").agg(km_recomputed=("km_years", "sum"), leaks_recomputed=("leaks", "sum"))
    g["km_ratio"] = d.set_index("district")["km_of_pipe"] / g["km_recomputed"]
    return g
    # END SOLUTION


# %%
try:
    rc = recompute(d)
except NotImplementedError:
    rc = U.reference("d3_2", "recomputed")
U.keep("d3_2", "recomputed", rc)
print(rc.loc[top3].round(3).to_string())
print("districts whose kilometres differ by more than 1%:", list(rc.index[(rc["km_ratio"] - 1).abs() > 0.01]))
fixed = d.copy().set_index("district")
fixed["km_of_pipe"] = rc["km_recomputed"]
fixed["leaks_per_100km"] = 100 * fixed["leaks_2026"] / fixed["km_of_pipe"]
fixed = fixed.reset_index()
ff = smf.ols(spec["formula"], data=fixed).fit()
ff30 = smf.ols(spec["formula"], data=fixed[fixed["district"] != "D30"]).fit()
corrected = {"age": float(ff.params["mean_age_years"]), "age_low": float(ff.conf_int().loc["mean_age_years", 0]),
             "age_high": float(ff.conf_int().loc["mean_age_years", 1]), "age_without_D30": float(ff30.params["mean_age_years"]),
             "cooks_D30": float(ff.get_influence().cooks_distance[0][fixed.index[fixed["district"] == "D30"][0]])}
U.keep("d3_2", "corrected", corrected)
print(f"with the two lengths corrected: age {corrected['age']:.2f} per year (95% interval {corrected['age_low']:.2f} to {corrected['age_high']:.2f}); without D30: {corrected['age_without_D30']:.2f}")
print(f"D30 after the correction: Cook's distance {corrected['cooks_D30']:.2f}, mean age {d.set_index('district').loc['D30', 'mean_age_years']} years, pressure {d.set_index('district').loc['D30', 'mean_pressure_bar']} bar")
U.check(set(rc.index[(rc["km_ratio"] - 1).abs() > 0.01]) == {"D08", "D21"} and corrected["age"] > 0,
        "D08 and D21 have their kilometres keyed a tenth too small; corrected, older mains leak more")

# %% [markdown]
# **Look at.** D30 is not an error: it is the new development on the edge of the city, with young mains at high pressure, far from every other district. Keep it, and report the model with and without it: its pressure is outside the range of the other 29, so the pressure coefficient leans on one district.

# %% [markdown]
# ## 5 · The second line of the diagnosis log (4')
#
# ✏️ **Exercise** · Return `U.log_entry("influential districts", evidence, fix)`: the evidence names the three districts and the sign change; the fix says what was corrected and what was kept.

# %%
def my_entry():
    # BEGIN SOLUTION
    return U.log_entry("influential districts",
                       f"district_leaks: Cook's distance flags {', '.join(top3)}; without them the age coefficient turns from {fit.params['mean_age_years']:.1f} to {without['age']:.1f}",
                       f"D08 and D21 had kilometres keyed a tenth too small: recomputed from the segment table. D30, a new high-pressure district, is real: kept and reported with and without (age {corrected['age']:.1f} and {corrected['age_without_D30']:.1f})")
    # END SOLUTION


# %%
try:
    entry = my_entry()
except NotImplementedError:
    entry = U.reference("d3_2", "entry")
U.keep("d3_2", "entry", entry)
U.log_save("3.2", entry)
print(entry)
U.check(all(k in entry["evidence"] + entry["fix"] for k in ("D08", "D21", "D30")), "the entry names all three districts")

# %% [markdown]
# ## ✱ Stretch · DFBETA for age
#
# DFBETA is how many standard errors a coefficient moves when one point is left out. Print the three largest for the age coefficient in Qusai's fit and in the corrected fit.

# %%
def stretch():
    # BEGIN SOLUTION
    for name, f, dd in (("Qusai's", fit, d), ("corrected", ff, fixed)):
        dfb = pd.Series(f.get_influence().dfbetas[:, 1], index=dd["district"]).abs().sort_values(ascending=False)
        print(name, dfb.head(3).round(2).to_dict())
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked against the truth: the generator keyed D08 and D21 a tenth too small in Qusai's summary and built D30 as a new district of young mains at high pressure.",
       "Checked: the recomputed kilometres match the segment table for the other 28 districts.",
       "Not checked: whether 30 district means can separate age from pressure well; the segment-level model of lab 2.3 has far more information.")

# %% [markdown]
# ## Checkpoint
#
# 1. D30 has high leverage and a modest residual. Why can it still be influential?
#    <details><summary>Answer</summary>Its predictors are far from the others', so the line must pass near it; moving it moves the line.</details>
# 2. When is deleting an influential point justified?
#    <details><summary>Answer</summary>When it is shown to be an error that cannot be corrected. A real unusual unit stays, and the result is reported with and without it.</details>
# 3. Why do 30 district points carry less information than 1,200 segments?
#    <details><summary>Answer</summary>Averaging inside districts throws away the variation between segments, and with 30 points a few can carry the fit.</details>
#
# ## Carry forward
#
# The second line of the diagnosis log is saved; lab 3.4 assembles the log.
