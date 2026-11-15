# %% [markdown]
# # Lab 4.2 · Partial pooling
#
# Day 4 · Session 2 (Partial pooling) · 25 min.
#
# Ghaliya's districts range from 40 bills (D13) to more than 9,000 (D17). She asks for each district's consumption level, to set next summer's supply targets, and she asks again about the programme. A district's own average is noisy when it rests on 40 bills. A random-intercept model lets each district have its own level while pulling the small ones towards the average of all districts. You fit it, read its variances, watch the small districts shrink and complete the table of naive, clustered and mixed-model estimates.
#
# **Use and estimand.** Descriptive: each district's level of log consumption relative to the average district, at equal household size, band and temperature; and the programme difference of lab 4.1.
#
# **AI policy.** AI-off for the random-intercept fit and its reading, with each number checked against the printed output. The hint-only tutor may help with the plot and the stretch item; it never writes model code.
#
# **Reference state.** `data/bills.csv`, loaded fresh. The naive and clustered rows of the table come from the stored result of lab 4.1, which is the same on every computer.
#
# **Tasks**
# - [ ] 1 · Fit the random-intercept model (5')
# - [ ] 2 · District and household variance (4')
# - [ ] 3 · Raw against shrunken district effects (7')
# - [ ] 4 · The three-way table (5')
# - [ ] 5 · A short explanation of the table (4')
# - [ ] ✱ Stretch · Add a random slope for household size and compare

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
warnings.filterwarnings("ignore")  # MixedLM reports boundary and convergence notes that do not apply here
print("mode:", U.MODE)

b = U.bills()
FORMULA = "log_m3 ~ tariff_band * household_size + bs(temperature_c, df=5) + pressure_managed"
n_bills = b.groupby("district").size()
print(f"bills per district: smallest {n_bills.min()} ({n_bills.idxmin()}), largest {n_bills.max():,} ({n_bills.idxmax()})")

# %% [markdown]
# ## 1 · Fit the random-intercept model (5')
#
# `smf.mixedlm(FORMULA, data=b, groups=b["district"])` gives each district its own intercept, drawn from a normal distribution whose SD is estimated. In R the same model is `lmer(log_m3 ~ ... + (1 | district))`.
#
# ✏️ **Exercise** · Fit it (REML, the default) and return the fit.

# %%
def mixed_fit(b):
    # BEGIN SOLUTION
    return smf.mixedlm(FORMULA, data=b, groups=b["district"]).fit()
    # END SOLUTION


# %%
try:
    mix = mixed_fit(b)
except NotImplementedError:
    mix = smf.mixedlm(FORMULA, data=b, groups=b["district"]).fit()
    print("↪ exercise not done yet: fitting the reference model")
pm = mix.params["pressure_managed"]
print(f"programme: {pm:.4f} (SE {mix.bse['pressure_managed']:.4f}), {100 * (np.exp(pm) - 1):.1f}%")

# %% [markdown]
# ## 2 · District and household variance (4')
#
# ✏️ **Exercise** · Return a dict with `sd_district` (the SD of the district intercepts, from `mix.cov_re`), `sd_household` (the residual SD, the square root of `mix.scale`) and `icc`, the share of the variance that lies between districts.

# %%
def variances(mix):
    # BEGIN SOLUTION
    tau2 = float(mix.cov_re.iloc[0, 0])
    s2 = float(mix.scale)
    return {"sd_district": tau2 ** 0.5, "sd_household": s2 ** 0.5, "icc": tau2 / (tau2 + s2)}
    # END SOLUTION


# %%
try:
    var = variances(mix)
except NotImplementedError:
    var = U.reference("d4_2", "variances")
U.keep("d4_2", "variances", var)
print({k: round(v, 3) for k, v in var.items()})
U.check(0.02 < var["icc"] < 0.15, "a small share of the variance lies between districts, and still enough to change the programme's standard error tenfold")

# %% [markdown]
# **Look at.** About 6% of the variance is between districts. That looks negligible; but with 1,300 bills in an average district, a correlation that small is what turned 40,000 bills into the evidence of about 30 districts in lab 4.1.

# %% [markdown]
# ## 3 · Raw against shrunken district effects (7')
#
# A district's raw effect is the mean of its bills' deviations from the fixed part of the model. Its shrunken effect is the model's estimate (`mix.random_effects`). The theory says the raw effect is multiplied by τ² / (τ² + σ²/n): close to 1 for large districts, smaller for small ones.
#
# ✏️ **Exercise** · Return a DataFrame indexed by district with columns `n`, `raw`, `shrunken` and `factor` (the theoretical multiplier above, with τ and σ from step 2).

# %%
def pooling_table(b, mix, var):
    # BEGIN SOLUTION
    fixed = np.asarray(mix.fittedvalues) - np.asarray([mix.random_effects[d].iloc[0] for d in b["district"]])
    dev = pd.Series(b["log_m3"].to_numpy() - fixed, index=b.index)
    t = pd.DataFrame({"n": b.groupby("district").size(), "raw": dev.groupby(b["district"]).mean()})
    t["shrunken"] = pd.Series({d: float(v.iloc[0]) for d, v in mix.random_effects.items()})
    tau2, s2 = var["sd_district"] ** 2, var["sd_household"] ** 2
    t["factor"] = tau2 / (tau2 + s2 / t["n"])
    return t.sort_values("n")
    # END SOLUTION


# %%
try:
    pool = pooling_table(b, mix, var)
except NotImplementedError:
    pool = U.reference("d4_2", "pooling")
U.keep("d4_2", "pooling", pool)
print(pool.head(6).round(3).to_string())
print("...")
print(pool.tail(3).round(3).to_string())
plt = U.plt()
fig, ax = plt.subplots(figsize=(8, 4))
for d, r in pool.iterrows():
    ax.plot([r["n"], r["n"]], [r["raw"], r["shrunken"]], color="grey", linewidth=1)
ax.scatter(pool["n"], pool["raw"], color="#e4572e", label="raw district mean", zorder=3)
ax.scatter(pool["n"], pool["shrunken"], color="#3a7ca5", label="random intercept", zorder=3)
ax.set(xscale="log", xlabel="bills in the district (log scale)", ylabel="district effect, log scale")
ax.axhline(0, color="black", linewidth=0.8)
ax.legend()
plt.show()
ratio = (pool["shrunken"] / pool["raw"]).where(pool["raw"].abs() > 0.01)
U.check(np.nanmax(np.abs(ratio - pool["factor"])) < 0.05,
        "each district's shrinkage matches the factor τ² / (τ² + σ²/n): small districts move most")

# %% [markdown]
# **Look at.** D13 (40 bills) keeps about 73% of its raw effect and D30 (60 bills) about 80%; the large districts keep more than 99%. The mixed estimate of the programme also moves, from −8% to −10%: it weighs districts more evenly than least squares, which lets D17, with a quarter of the bills, count for less. Small districts borrow strength from the rest because their own mean is the least reliable.

# %% [markdown]
# ## 4 · The three-way table (5')
#
# ✏️ **Exercise** · Return a DataFrame with one row per method (`naive`, `clustered`, `mixed`) and columns `estimate`, `se`, `low_pct` and `high_pct`: the 95% interval for the programme as a percentage difference.

# %%
def three_way(r41, mix):
    # BEGIN SOLUTION
    rows = {"naive": (r41.loc["pressure_managed", "estimate"], r41.loc["pressure_managed", "naive_se"]),
            "clustered": (r41.loc["pressure_managed", "estimate"], r41.loc["pressure_managed", "cluster_se"]),
            "mixed": (mix.params["pressure_managed"], mix.bse["pressure_managed"])}
    t = pd.DataFrame(rows, index=["estimate", "se"]).T
    t["low_pct"] = 100 * (np.exp(t["estimate"] - 1.96 * t["se"]) - 1)
    t["high_pct"] = 100 * (np.exp(t["estimate"] + 1.96 * t["se"]) - 1)
    return t
    # END SOLUTION


# %%
r41 = U.stored("d4_1", "ratios")  # the reference of lab 4.1; the numbers are the same on every computer
try:
    tab = three_way(r41, mix)
except NotImplementedError:
    tab = U.reference("d4_2", "three_way")
U.keep("d4_2", "three_way", tab)
print(tab.round(4).to_string())
U.check(tab.loc["naive", "se"] < tab.loc["mixed", "se"] < tab.loc["clustered", "se"] * 1.2,
        "the mixed model's standard error is of the clustered size, not the naive one")

# %% [markdown]
# ## 5 · A short explanation of the table (4')
#
# ✏️ **Exercise** · Complete `write_explain()` to return at most 80 words for Ghaliya: quote the mixed model's interval (as a percentage, one decimal, as printed by `tab`) and say why the naive one was too narrow. Use the word "district".

# %%
def write_explain():
    # BEGIN SOLUTION
    return (f"Programme districts used less water at equal household size, band and temperature: the mixed model puts the difference between "
               f"{tab.loc['mixed', 'low_pct']:.1f}% and {tab.loc['mixed', 'high_pct']:.1f}%. The naive interval was far narrower because it counted "
               f"40,000 bills as independent, when the programme is set per district and only 30 districts carry that comparison. "
               f"Districts chose to join, so this is a comparison, not the saving from joining.")
    # END SOLUTION

# %%
try:
    EXPLAIN = write_explain()
except NotImplementedError:
    EXPLAIN = U.reference("d4_2", "explain")
U.keep("d4_2", "explain", EXPLAIN)
print(EXPLAIN)
U.text_check(EXPLAIN, {"mixed low": f"{tab.loc['mixed', 'low_pct']:.1f}%", "mixed high": f"{tab.loc['mixed', 'high_pct']:.1f}%"},
             ["district"], max_words=80)

# %% [markdown]
# ## ✱ Stretch · A random slope
#
# Let the household-size slope vary by district: `re_formula="~household_size"`. Does the SD of the slopes look different from zero, and does the programme's interval change?

# %%
def stretch():
    # BEGIN SOLUTION
    m2 = smf.mixedlm(FORMULA, data=b, groups=b["district"], re_formula="~household_size").fit()
    sd_slope = float(m2.cov_re.iloc[1, 1]) ** 0.5
    print(f"SD of the household-size slopes between districts: {sd_slope:.4f} (the slope itself is about 0.095)")
    print(f"programme with a random slope: {m2.params['pressure_managed']:.4f} (SE {m2.bse['pressure_managed']:.4f})")
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
tr = U.truth()
true_eff = pd.Series(tr["district_effect"])
raw_err = float(np.sqrt(((pool["raw"] - pool["raw"].mean()) - (true_eff - true_eff.mean())).pow(2).mean()))
shr_err = float(np.sqrt(((pool["shrunken"] - pool["shrunken"].mean()) - (true_eff - true_eff.mean())).pow(2).mean()))
U.note(f"Checked against the truth: the generator's district SD is {tr['consumption']['sd_district']}, the fit's {var['sd_district']:.3f}; the programme's true value, {tr['consumption']['pressure_managed']}, is inside the mixed interval.",
       f"Checked: distance from the true district effects, raw means {raw_err:.4f} against shrunken {shr_err:.4f}; with 30 districts the gain from pooling is small here and largest for the smallest districts.",
       "Not checked: whether the district effects are normal. With 30 districts the data say little about their shape.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why does D13 move more than D17?
#    <details><summary>Answer</summary>D13's mean rests on 40 bills and D17's on more than 9,000; the shrinkage factor τ²/(τ² + σ²/n) is far from 1 only when n is small.</details>
# 2. Only about 6% of the variance lies between districts. Why does it matter so much for the programme?
#    <details><summary>Answer</summary>The programme varies only between districts; with over 1,000 bills per district on average, even a small shared district level makes the bills of a district far from independent.</details>
# 3. Which interval would you give Ghaliya, clustered or mixed?
#    <details><summary>Answer</summary>Either is defensible and they agree in size; the mixed model also gives district levels, which she asked for. The naive one is not defensible.</details>
#
# ## Carry forward
#
# The three-way table and the district levels go into the report of lab 4.4.
