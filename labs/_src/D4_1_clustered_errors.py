# %% [markdown]
# # Lab 4.1 · Clustered standard errors
#
# Day 4 · Session 1 (Clustered data) · 25 min.
#
# Ghaliya wants to know whether the 13 districts in the pressure management programme use less water than the other 17, at equal household size, band and temperature. The consumption model has 40,000 bills, and its naive standard error for the programme is tiny. But the programme is decided for a whole district: households in one district share their pressure, their network and their neighbourhood. You compute standard errors clustered by district and see which intervals change, and by how much.
#
# **Use and estimand.** Descriptive: the difference in mean log consumption between households in programme districts and others, at equal household size, band and temperature, reported as a percentage. Districts chose to join the programme, so this is a comparison, not the effect of joining.
#
# **AI policy.** AI-off for the fits and the explanation of the change, with every standard error checked against the printed table. The hint-only tutor may help with the bootstrap of the stretch item; it never writes model code.
#
# **Reference state.** `data/bills.csv` and `data/districts.csv`, loaded fresh; the formula is the consumption model of Day 1 with the programme flag added. Nothing from Day 3 is needed.
#
# **Tasks**
# - [ ] 1 · Which predictors vary by household and which by district (4')
# - [ ] 2 · The naive fit (4')
# - [ ] 3 · Errors clustered by district (6')
# - [ ] 4 · The ratio of standard errors, term by term (6')
# - [ ] 5 · Two sentences that explain the change (5')
# - [ ] ✱ Stretch · Resample whole districts and compare the bootstrap interval

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

import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import sahil as U
warnings.filterwarnings("ignore", category=RuntimeWarning)
print("mode:", U.MODE)

b = U.bills()
FORMULA = "log_m3 ~ tariff_band * household_size + bs(temperature_c, df=5) + pressure_managed"
TERMS = ["pressure_managed", "household_size", "tariff_band[T.social]", "tariff_band[T.villa]"]
print(f"{len(b):,} bills in {b['district'].nunique()} districts; bills per district from {b.groupby('district').size().min()} to {b.groupby('district').size().max():,}")

# %% [markdown]
# ## 1 · Which predictors vary by household and which by district (4')
#
# A predictor that is the same for every household of a district carries information only from the 30 districts, however many households there are.
#
# ✏️ **Exercise** · Return a dict `{column: "district" or "household"}` for `household_size`, `tariff_band`, `temperature_c` and `pressure_managed`: `"district"` when the column takes one value in every district.

# %%
def level_of(b, cols):
    # BEGIN SOLUTION
    return {c: "district" if (b.groupby("district")[c].nunique() == 1).all() else "household" for c in cols}
    # END SOLUTION


# %%
COLS = ["household_size", "tariff_band", "temperature_c", "pressure_managed"]
try:
    levels = level_of(b, COLS)
except NotImplementedError:
    levels = U.reference("d4_1", "levels")
U.keep("d4_1", "levels", levels)
print(levels)
U.check(levels["pressure_managed"] == "district" and levels["household_size"] == "household",
        "the programme flag varies only between districts; household size varies within them")

# %% [markdown]
# ## 2 · The naive fit (4')
#
# ✏️ **Exercise** · Fit `FORMULA` by least squares with classical standard errors and return the fit.

# %%
def naive_fit(b):
    # BEGIN SOLUTION
    return smf.ols(FORMULA, data=b).fit()
    # END SOLUTION


# %%
try:
    naive = naive_fit(b)
except NotImplementedError:
    naive = smf.ols(FORMULA, data=b).fit()
    print("↪ exercise not done yet: fitting the reference model")
pm = naive.params["pressure_managed"]
print(f"programme districts: {pm:.4f} on the log scale, {100 * (np.exp(pm) - 1):.1f}% (naive SE {naive.bse['pressure_managed']:.4f})")

# %% [markdown]
# ## 3 · Errors clustered by district (6')
#
# Clustered (sandwich) errors let the residuals of households in one district be correlated in any way, and assume only that districts are independent.
#
# ✏️ **Exercise** · Refit with `cov_type="cluster"` and `cov_kwds={"groups": ...}`, where the groups are integer codes of the district (`pd.factorize(b["district"])[0]`). Return the fit.

# %%
def clustered_fit(b):
    # BEGIN SOLUTION
    return smf.ols(FORMULA, data=b).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(b["district"])[0]})
    # END SOLUTION


# %%
try:
    clus = clustered_fit(b)
except NotImplementedError:
    clus = smf.ols(FORMULA, data=b).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(b["district"])[0]})
    print("↪ exercise not done yet: fitting the reference model")
ci_n = naive.conf_int().loc["pressure_managed"]
ci_c = clus.conf_int().loc["pressure_managed"]
print(f"programme, naive interval:     {100 * (np.exp(ci_n[0]) - 1):.1f}% to {100 * (np.exp(ci_n[1]) - 1):.1f}%")
print(f"programme, clustered interval: {100 * (np.exp(ci_c[0]) - 1):.1f}% to {100 * (np.exp(ci_c[1]) - 1):.1f}%")
U.check(abs(clus.params["pressure_managed"] - pm) < 1e-10, "the estimate is the same; only its standard error changed")

# %% [markdown]
# ## 4 · The ratio of standard errors, term by term (6')
#
# ✏️ **Exercise** · Return a DataFrame indexed by `TERMS` with columns `estimate`, `naive_se`, `cluster_se` and `ratio` (clustered over naive).

# %%
def se_ratios(naive, clus):
    # BEGIN SOLUTION
    t = pd.DataFrame({"estimate": naive.params[TERMS], "naive_se": naive.bse[TERMS], "cluster_se": clus.bse[TERMS]})
    t["ratio"] = t["cluster_se"] / t["naive_se"]
    return t
    # END SOLUTION


# %%
try:
    ratios = se_ratios(naive, clus)
except NotImplementedError:
    ratios = U.reference("d4_1", "ratios")
U.keep("d4_1", "ratios", ratios)
print(ratios.round(4).to_string())
U.check(ratios.loc["pressure_managed", "ratio"] > 5 and ratios.loc["household_size", "ratio"] < 1.5,
        "clustering widens the district-level term many times and the household-level term hardly at all")

# %% [markdown]
# **Look at.** The programme's standard error grows more than tenfold; household size's barely moves. A household-level predictor is compared within every district, so the district effects largely cancel; a district-level one has only 30 districts behind it, each with its own level of consumption.

# %% [markdown]
# ## 5 · Two sentences that explain the change (5')
#
# ✏️ **Exercise** · Complete `write_explain()` to return two sentences for Ghaliya: quote the naive and clustered standard errors of the programme (as printed, four decimals) and use the words "district" and "independent".

# %%
def write_explain():
    # BEGIN SOLUTION
    return (f"The naive standard error of the programme, {ratios.loc['pressure_managed', 'naive_se']:.4f}, treats 40,000 bills as independent pieces of evidence, "
               f"but the programme is set per district, and households in one district share more than the model knows. "
               f"Counting districts rather than bills, the clustered standard error is {ratios.loc['pressure_managed', 'cluster_se']:.4f}, "
               f"so the difference could be anywhere from a clear saving to none.")
    # END SOLUTION

# %%
try:
    EXPLAIN = write_explain()
except NotImplementedError:
    EXPLAIN = U.reference("d4_1", "explain")
U.keep("d4_1", "explain", EXPLAIN)
print(EXPLAIN)
U.text_check(EXPLAIN, {"naive SE": f"{ratios.loc['pressure_managed', 'naive_se']:.4f}",
                       "clustered SE": f"{ratios.loc['pressure_managed', 'cluster_se']:.4f}"},
             ["district", "independent"], max_words=90)

# %% [markdown]
# ## ✱ Stretch · Resample whole districts
#
# Draw 30 districts with replacement, keep all their bills, refit, and repeat. The spread of the programme's estimate is a bootstrap standard error that makes no formula assumption at all.

# %%
def stretch():
    # BEGIN SOLUTION
    gen = U.rng(41)
    groups = {d: g for d, g in b.groupby("district")}
    names = list(groups)
    est = []
    for _ in range(U.pick(200, 30)):
        pick = gen.choice(names, len(names), replace=True)
        s = pd.concat([groups[d] for d in pick], ignore_index=True)
        if s["pressure_managed"].nunique() < 2:
            continue
        est.append(smf.ols(FORMULA, data=s).fit().params["pressure_managed"])
    print(f"district bootstrap SE of the programme: {np.std(est, ddof=1):.4f} over {len(est)} samples (clustered {ratios.loc['pressure_managed', 'cluster_se']:.4f})")
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
tr = U.truth()["consumption"]
U.note(f"Checked against the truth: the generator gives the programme {tr['pressure_managed']} on the log scale and each district its own level with SD {tr['sd_district']}; the naive interval excludes the truth, the clustered one contains it.",
       "Checked: the estimates are identical in both fits; only the standard errors change.",
       "Not checked: with 30 clusters, clustered errors are themselves a little too small; the bootstrap of the stretch item is one way to see by how much.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why does clustering widen the programme's interval so much more than household size's?
#    <details><summary>Answer</summary>The programme varies only between districts, so its evidence is 30 districts; household size varies within every district, so district effects cancel in its comparison.</details>
# 2. Did clustering change the estimate of the programme?
#    <details><summary>Answer</summary>No. It changes the standard errors only.</details>
# 3. The naive interval for the programme was about −8.3% to −7.2%. What would a planner have concluded from it?
#    <details><summary>Answer</summary>That the programme districts certainly use about 8% less water, a certainty the 30 districts do not support.</details>
#
# ## Carry forward
#
# The naive and clustered rows of the programme feed the three-way table of lab 4.2.
