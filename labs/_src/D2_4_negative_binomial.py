# %% [markdown]
# # Lab 2.4 · Dispersion and the negative binomial
#
# Day 2 · Session 4 (Overdispersion) · 25 min.
#
# Basil wants to choose mains for renewal from the rate ratios of lab 2.3. Before he does, you check the Poisson model's promise that a count's variance equals its mean. Some mains leak far more than others of the same kind, so the counts vary more, and the Poisson intervals are too narrow. You test the dispersion, refit with a negative binomial model and set the two side by side.
#
# **Use and estimand.** Descriptive: leaks per kilometre-year by material, age and pressure across Sahil's segments in 2026, as rate ratios and as expected counts, with honest intervals.
#
# **AI policy.** AI-off for the dispersion check and the refit. The hint-only tutor may help with the table and the stretch item.
#
# **Reference state.** `data/leaks.csv` and `data/segments.csv` through `U.segment_totals()`, which returns one row per segment with its count and exposure (the result of lab 2.3, steps 1 and 2).
#
# **Tasks**
# - [ ] 1 · Variance against mean in groups (5')
# - [ ] 2 · The Pearson dispersion statistic (4')
# - [ ] 3 · The negative binomial fit (5')
# - [ ] 4 · Standard errors and intervals side by side (6')
# - [ ] 5 · Effects on the count scale (5')
# - [ ] ✱ Stretch · Run the auxiliary-regression test of dispersion

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
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sahil as U
warnings.filterwarnings("ignore", category=RuntimeWarning)
print("mode:", U.MODE)

s = U.segment_totals()
FORMULA = "leaks ~ material + age_years + pressure_bar"
po = smf.glm(FORMULA, data=s, family=sm.families.Poisson(), offset=np.log(s["km_years"])).fit()
mu = np.asarray(po.fittedvalues)

# %% [markdown]
# ## 1 · Variance against mean in groups (5')
#
# Sort segments by their fitted mean, cut them into ten groups and compare, in each group, the mean of the observed counts with their variance. Under the Poisson model the two are about equal.
#
# ✏️ **Exercise** · Return a DataFrame with one row per decile of `mu` and columns `mean` and `variance` of the observed `leaks`.

# %%
def mean_variance(s, mu):
    # BEGIN SOLUTION
    d = pd.DataFrame({"y": s["leaks"].to_numpy(), "mu": mu})
    d["group"] = pd.qcut(d["mu"].rank(method="first"), 10, labels=range(1, 11))
    return d.groupby("group", observed=True)["y"].agg(mean="mean", variance="var")
    # END SOLUTION


# %%
try:
    mv = mean_variance(s, mu)
except NotImplementedError:
    mv = U.reference("d2_4", "mean_variance")
U.keep("d2_4", "mean_variance", mv)
mv["ratio"] = mv["variance"] / mv["mean"]
print(mv.round(2).to_string())
U.check((mv["ratio"] > 1.3).sum() >= 7, "in most groups the variance is well above the mean")

# %% [markdown]
# ## 2 · The Pearson dispersion statistic (4')
#
# The sum of squared Pearson residuals, (y − μ)² / μ, divided by the residual degrees of freedom, is about 1 for a Poisson model that fits.
#
# ✏️ **Exercise** · Return the dispersion statistic of `po`.

# %%
def dispersion(po):
    # BEGIN SOLUTION
    return float(po.pearson_chi2 / po.df_resid)
    # END SOLUTION


# %%
try:
    phi = dispersion(po)
except NotImplementedError:
    phi = U.reference("d2_4", "phi")
U.keep("d2_4", "phi", phi)
print(f"Pearson dispersion: {phi:.2f}")
U.check(phi > 1.5, "the counts are overdispersed: about twice the variance a Poisson model allows")

# %% [markdown]
# ## 3 · The negative binomial fit (5')
#
# The negative binomial model lets each segment have its own hidden leakiness: variance = μ + α μ². With α = 0 it is the Poisson model.
#
# ✏️ **Exercise** · Fit `FORMULA` with `smf.negativebinomial(FORMULA, data=s, exposure=s["km_years"]).fit(disp=0)` and return the fit.

# %%
def fit_nb(s):
    # BEGIN SOLUTION
    return smf.negativebinomial(FORMULA, data=s, exposure=s["km_years"]).fit(disp=0)
    # END SOLUTION


# %%
try:
    nb = fit_nb(s)
except NotImplementedError:
    print("↪ exercise not done yet: fitting the reference model so the cells below run")
    if U.STRICT:
        raise
    nb = smf.negativebinomial(FORMULA, data=s, exposure=s["km_years"]).fit(disp=0)
alpha = float(nb.params["alpha"])
lo_a, hi_a = nb.conf_int().loc["alpha"]
print(f"alpha {alpha:.3f} (95% interval {lo_a:.3f} to {hi_a:.3f}); AIC Poisson {po.aic:.0f}, negative binomial {nb.aic:.0f}")
U.keep("d2_4", "alpha", [alpha, float(lo_a), float(hi_a), float(po.aic), float(nb.aic)])
U.check(lo_a > 0.2 and nb.aic < po.aic, "alpha is clearly above zero and the negative binomial fits better")

# %% [markdown]
# ## 4 · Standard errors and intervals side by side (6')
#
# ✏️ **Exercise** · Return a DataFrame indexed by the terms (without the intercept and `alpha`) with the rate ratio and 95% interval of each model: columns `poisson`, `poisson_low`, `poisson_high`, `nb`, `nb_low`, `nb_high`, and `se_ratio` (negative binomial standard error over Poisson's).

# %%
def side_by_side(po, nb):
    # BEGIN SOLUTION
    terms = [t for t in po.params.index if t != "Intercept"]
    cp, cn = po.conf_int(), nb.conf_int()
    return pd.DataFrame({
        "poisson": np.exp(po.params[terms]), "poisson_low": np.exp(cp.loc[terms, 0]), "poisson_high": np.exp(cp.loc[terms, 1]),
        "nb": np.exp(nb.params[terms]), "nb_low": np.exp(cn.loc[terms, 0]), "nb_high": np.exp(cn.loc[terms, 1]),
        "se_ratio": nb.bse[terms] / po.bse[terms]})
    # END SOLUTION


# %%
try:
    sbs = side_by_side(po, nb)
except NotImplementedError:
    sbs = U.reference("d2_4", "side_by_side")
U.keep("d2_4", "side_by_side", sbs)
print(sbs.round(3).to_string())
U.check(sbs["se_ratio"].min() > 1.3, "every negative binomial standard error is at least a third larger")

# %% [markdown]
# **Look at.** The rate ratios barely move; their intervals widen by about the square root of the dispersion. A renewal list built on the Poisson intervals would treat small differences between materials as settled.

# %% [markdown]
# ## 5 · Effects on the count scale (5')
#
# The evidence asks for effects on the count scale. Basil thinks in leaks a year on 10 km of main.
#
# ✏️ **Exercise** · Using `U.contrast` with `scale="count"` and `offset=np.log(np.full(len(s), 10.0))`, return the average difference in expected leaks a year on 10 km between asbestos cement and PVC, over all segments' ages and pressures, for both models, as `{"poisson": (estimate, low, high), "nb": (...)}`.

# %%
def count_scale(po, nb):
    # BEGIN SOLUTION
    off = np.log(np.full(len(s), 10.0))
    out = {}
    for name, f in (("poisson", po), ("nb", nb)):
        c = U.contrast(f, s, "material", "PVC", "asbestos_cement", scale="count", offset=off)
        out[name] = tuple(float(c.loc["all", k]) for k in ("estimate", "low", "high"))
    return out
    # END SOLUTION


# %%
try:
    cs = count_scale(po, nb)
except NotImplementedError:
    cs = U.reference("d2_4", "count_scale")
cs = {k: tuple(v) for k, v in cs.items()}
U.keep("d2_4", "count_scale", cs)
for k, (e, lo, hi) in cs.items():
    print(f"{k:8s} asbestos cement minus PVC, per 10 km a year: {e:.1f} leaks (95% interval {lo:.1f} to {hi:.1f})")
U.check((cs["nb"][2] - cs["nb"][1]) > 1.3 * (cs["poisson"][2] - cs["poisson"][1]), "the negative binomial interval on the count scale is wider")

# %% [markdown]
# ## ✱ Stretch · The auxiliary-regression test
#
# Cameron and Trivedi's test: regress ((y − μ)² − y) / μ on μ without an intercept, using the Poisson μ. The slope estimates α; a t statistic far above 2 rejects equal mean and variance.

# %%
def stretch():
    # BEGIN SOLUTION
    y = s["leaks"].to_numpy()
    aux = sm.OLS(((y - mu) ** 2 - y) / mu, mu).fit()
    print(f"auxiliary slope {aux.params[0]:.3f}, t = {aux.tvalues[0]:.1f}")
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
t = U.truth()["leaks"]
U.note(f"Checked against the truth: each segment's hidden leakiness is gamma with shape {t['segment_frailty'].split('shape ')[1].split(',')[0]}, which implies alpha {t['implied_nb_alpha']}; your estimate is {alpha:.2f}.",
       "Checked: the rate ratios hardly change between models; their intervals do.",
       "Not checked yet: whether the negative binomial reproduces features of the data such as the share of zeros. Lab 3.3 simulates from both fits.")

# %% [markdown]
# ## Checkpoint
#
# 1. The dispersion statistic is 2.3. What happens to the Poisson standard errors?
#    <details><summary>Answer</summary>They are too small, by about the square root of 2.3, so intervals are about two thirds of the width they should have.</details>
# 2. Why do the rate ratios hardly move?
#    <details><summary>Answer</summary>Both models describe the same mean; they disagree about the variance, which shows in the intervals.</details>
# 3. A quasi-Poisson fit would scale the standard errors by the dispersion. When is the negative binomial the better choice?
#    <details><summary>Answer</summary>When you need the whole distribution of counts, for example to simulate data or to predict the share of zero-leak segments (lab 3.3).</details>
#
# ## Carry forward
#
# The side-by-side table is the evidence of LO2 on the count scale, with lab 2.2's probability differences.
