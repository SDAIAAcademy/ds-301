# %% [markdown]
# # Lab 1.4 · Interaction and marginal effects
#
# Day 1 · Session 4 (Interactions and marginal effects) · 25 min.
#
# Ghaliya's next question: how much more water does one more person in a household mean, in cubic metres a month, and is it the same on every tariff band? You let the size slope differ by band with an interaction, then turn the log-scale coefficients into the number she asked for: an average marginal effect in cubic metres, with an interval, for each band.
#
# **Use and estimand.** Descriptive: among Sahil's billed households, the average difference in monthly consumption between a household and the same household with one more person, by tariff band. It compares households; it is not what happens when someone moves in.
#
# **AI policy.** AI-off for the fit and the first reading of the interaction. The hint-only tutor may help with the plot and the stretch item.
#
# **Reference state.** `data/bills.csv`, loaded fresh; the spline of lab 1.3 is written into the formula below.
#
# **Tasks**
# - [ ] 1 · Fit the interaction model (4')
# - [ ] 2 · Read the slope of each band on the log scale (5')
# - [ ] 3 · One more person, in cubic metres, for each household (6')
# - [ ] 4 · Average marginal effects by band with intervals (6')
# - [ ] 5 · The effect plot and the interval table (4')
# - [ ] ✱ Stretch · Check the course function against the marginaleffects package

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

b = U.bills()
FORMULA = "log_m3 ~ tariff_band * household_size + bs(temperature_c, df=5)"

# %% [markdown]
# ## 1 · Fit the interaction model (4')
#
# `tariff_band * household_size` expands to both main terms and their product: one size slope for the reference band (standard) and a difference in slope for each other band.
#
# ✏️ **Exercise** · Fit `FORMULA` with `smf.ols` and return the fit.

# %%
def fit_interaction(b):
    # BEGIN SOLUTION
    return smf.ols(FORMULA, data=b).fit()
    # END SOLUTION


# %%
try:
    f = fit_interaction(b)
except NotImplementedError:
    print("↪ exercise not done yet: fitting the reference model so the cells below run")
    if U.STRICT:
        raise
    f = smf.ols(FORMULA, data=b).fit()
print(f.params.filter(like="household_size").round(4).to_string())

# %% [markdown]
# ## 2 · Read the slope of each band on the log scale (5')
#
# ✏️ **Exercise** · Return a dictionary `{band: slope}`: the size slope of each band on the log scale (the main slope plus the band's interaction term), and convert each to percent per person, 100 × (exp(slope) − 1).

# %%
def band_slopes(f):
    # BEGIN SOLUTION
    base = f.params["household_size"]
    return {"standard": float(base),
            "social": float(base + f.params["tariff_band[T.social]:household_size"]),
            "villa": float(base + f.params["tariff_band[T.villa]:household_size"])}
    # END SOLUTION


# %%
try:
    slopes = band_slopes(f)
except NotImplementedError:
    slopes = U.reference("d1_4", "slopes")
U.keep("d1_4", "slopes", slopes)
for k, v in slopes.items():
    print(f"{k:9s} slope {v:.4f} on the log scale: {100 * (np.exp(v) - 1):.1f}% more per person")
U.check(slopes["social"] < slopes["standard"] < slopes["villa"], "the percentage per person differs by band: smallest on social, largest on villa")

# %% [markdown]
# **Look at.** The coefficient `tariff_band[T.social]:household_size` is not "the effect of size on social": it is the difference between the social and standard slopes. And a percentage is not what Ghaliya asked for: 9% of a villa's bill is many more cubic metres than 9% of a small flat's.

# %% [markdown]
# ## 3 · One more person, in cubic metres, for each household (6')
#
# For every bill: predict with its own size, predict again with one more person, and take the difference on the cubic-metre scale (the mean back-transform of lab 1.3: exp(prediction + σ²/2)).
#
# ✏️ **Exercise** · Write `effect_each(f, b)`: return an array with that difference for every row of `b`.

# %%
def effect_each(f, b):
    # BEGIN SOLUTION
    b1 = b.copy()
    b1["household_size"] = b1["household_size"] + 1
    adj = np.exp(f.scale / 2)
    return (np.exp(np.asarray(f.predict(b1))) - np.exp(np.asarray(f.predict(b)))) * adj
    # END SOLUTION


# %%
try:
    each = effect_each(f, b)
except NotImplementedError:
    each = None
    ame_point = U.reference("d1_4", "ame_point")
if each is not None:
    ame_point = pd.Series(each).groupby(b["tariff_band"].to_numpy()).mean().to_dict()
ame_point = {k: float(v) for k, v in ame_point.items()}
U.keep("d1_4", "ame_point", ame_point)
print({k: round(v, 2) for k, v in ame_point.items()})
U.check(ame_point["villa"] > 2 * ame_point["social"], "in cubic metres the band difference is far larger than in percent")

# %% [markdown]
# ## 4 · Average marginal effects by band with intervals (6')
#
# `U.contrast` does the same computation for 1,000 draws of the coefficients from their sampling distribution and takes the 2.5th and 97.5th percentiles of the average: an interval for the average marginal effect. Its estimate must equal yours.

# %%
ame = U.contrast(f, b, "household_size", low=lambda x: x, high=lambda x: x + 1, scale="m3", by="tariff_band")
ame = ame.loc[["social", "standard", "villa"]]
print(ame.round(3).to_string())
U.keep("d1_4", "ame_table", ame)
U.check(all(abs(ame.loc[k, "estimate"] - ame_point[k]) < 1e-6 for k in ame_point), "your per-household effects average to the function's estimates")

# %% [markdown]
# ## 5 · The effect plot and the interval table (4')
#
# The outcome's evidence: an interval table that matches the reference of the trainer's run, and the effect plot.

# %%
plt = U.plt()
fig, ax = plt.subplots(figsize=(6, 3.5))
y = np.arange(len(ame))
ax.errorbar(ame["estimate"], y, xerr=[ame["estimate"] - ame["low"], ame["high"] - ame["estimate"]], fmt="o", color="#3a7ca5", capsize=4)
ax.set_yticks(y, ame.index)
ax.set(xlabel="cubic metres a month for one more person", title="Average marginal effect of household size, by band")
plt.show()
try:
    ref = U.stored("d1_4", "ame_table")
    ok = np.allclose(ame[["estimate", "low", "high"]].to_numpy(dtype=float), ref.loc[ame.index, ["estimate", "low", "high"]].to_numpy(dtype=float), atol=0.05)
except (FileNotFoundError, KeyError):
    ok = U.WRITE_REF
U.check(ok, "the interval table matches the reference within 0.05 m³")

# %% [markdown]
# ## ✱ Stretch · Check against marginaleffects
#
# `marginaleffects.avg_slopes(f, variables="household_size", by="tariff_band")` gives the average slope on the scale of the model's prediction, here the log scale. Compare it with your band slopes of step 2.

# %%
def stretch():
    # BEGIN SOLUTION
    try:
        import marginaleffects as me
    except ImportError:
        print("marginaleffects is not installed here")
        return
    out = me.avg_slopes(f, variables="household_size", by="tariff_band")
    print(out)
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
t = U.truth()["consumption"]["size_slope_by_band"]
U.note(f"Checked against the truth: the generator's size slopes on the log scale are {t}; yours: " + ", ".join(f"{k} {v:.3f}" for k, v in slopes.items()) + ".",
       "Checked: the course function's estimates equal your own per-household computation.",
       "Not checked: whether a household that grows by one person changes its use by this amount; these are comparisons between households.")

# %% [markdown]
# ## Checkpoint
#
# 1. The interaction term for villas is 0.04. What is the villa size slope on the log scale?
#    <details><summary>Answer</summary>The standard slope plus 0.04. The interaction term alone is a difference between slopes.</details>
# 2. Why is the average marginal effect for villas so much larger in cubic metres than the percentages suggest?
#    <details><summary>Answer</summary>The same percentage applies to a larger base: villas use more, so each percent is more cubic metres.</details>
# 3. Ghaliya writes: "adding a person to a social-tariff home adds 2.5 m³." What do you change?
#    <details><summary>Answer</summary>"Social-tariff households with one more person use about 2.5 m³ more a month, with an interval", a comparison of households, not the effect of adding a person.</details>
#
# ## Carry forward
#
# The interval table of this lab is the evidence of LO1 and returns in the model report of lab 4.4.
