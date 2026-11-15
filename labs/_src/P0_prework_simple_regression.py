# %% [markdown]
# # Pre-work · Simple regression
#
# About two hours, before Day 1 and the supervised entry quiz.
#
# This notebook revises what Day 1 assumes: fitting a line, reading its slope and intercept, its standard error and interval, its residuals, and the difference between an interval for a mean and an interval for one new household. It uses the bills of Sahil Water, the fictional utility of the course. Work through it at your own pace; each exercise has a stored answer, so the notebook runs to the end even if you skip one.
#
# **AI policy.** Work without an assistant: the entry quiz is supervised and asks the same things.
#
# **Reference state.** `data/bills.csv`, loaded fresh.
#
# **Tasks**
# - [ ] 1 · Look at the data before any model
# - [ ] 2 · Fit a line and read the slope
# - [ ] 3 · The standard error and the interval of the slope
# - [ ] 4 · Residuals: what the line leaves out
# - [ ] 5 · Two kinds of interval for a prediction
# - [ ] 6 · Simulate to see what a standard error means
# - [ ] ✱ Stretch · The same slope from a formula you write yourself

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
std = b[b["tariff_band"] == "standard"].reset_index(drop=True)
print(f"{len(std):,} households on the standard tariff")

# %% [markdown]
# ## 1 · Look at the data before any model
#
# ✏️ **Exercise** · Return the mean consumption in m³ for each household size from 1 to 8 on the standard tariff, as a Series indexed by size.

# %%
def mean_by_size(d):
    # BEGIN SOLUTION
    return d[d["household_size"].between(1, 8)].groupby("household_size")["consumption_m3"].mean()
    # END SOLUTION


# %%
try:
    by_size = mean_by_size(std)
except NotImplementedError:
    by_size = U.reference("p0", "by_size")
by_size = pd.Series(by_size)
by_size.index = by_size.index.astype(int)
U.keep("p0", "by_size", {int(k): float(v) for k, v in by_size.items()})
print(by_size.round(1).to_string())
plt = U.plt()
fig, ax = plt.subplots()
ax.scatter(std["household_size"] + np.random.default_rng(0).uniform(-0.2, 0.2, len(std)), std["consumption_m3"], s=2, alpha=0.15)
ax.plot(by_size.index, by_size.to_numpy(), color="black", marker="o")
ax.set(xlabel="household size (jittered)", ylabel="consumption, m³ a month")
plt.show()

# %% [markdown]
# **Look at.** The means rise roughly in a straight line, and the spread around them is wide: household size explains part of consumption, not most of it.

# %% [markdown]
# ## 2 · Fit a line and read the slope
#
# ✏️ **Exercise** · Fit `consumption_m3 ~ household_size` on `std` by least squares and return the fit.

# %%
def fit_line(d):
    # BEGIN SOLUTION
    return smf.ols("consumption_m3 ~ household_size", data=d).fit()
    # END SOLUTION


# %%
try:
    fit = fit_line(std)
except NotImplementedError:
    fit = smf.ols("consumption_m3 ~ household_size", data=std).fit()
    print("↪ exercise not done yet: fitting the reference model")
slope, icpt = fit.params["household_size"], fit.params["Intercept"]
print(f"intercept {icpt:.2f} m³, slope {slope:.2f} m³ per person, R² {fit.rsquared:.3f}")
U.keep("p0", "slope", float(slope))
U.check(1.5 < slope < 3.5, "the slope is about two to three cubic metres a month per extra person")

# %% [markdown]
# **Read it.** Households with one more member used, on average, about this many more cubic metres a month. It is a comparison between households of different sizes, not what happens when someone moves in. The intercept is the line's value at size 0, which no household has.

# %% [markdown]
# ## 3 · The standard error and the interval of the slope
#
# ✏️ **Exercise** · Return the 95% interval of the slope as a tuple `(low, high)`, computed as the estimate plus and minus 1.96 standard errors (`fit.bse`).

# %%
def slope_interval(fit):
    # BEGIN SOLUTION
    se = fit.bse["household_size"]
    return (fit.params["household_size"] - 1.96 * se, fit.params["household_size"] + 1.96 * se)
    # END SOLUTION


# %%
try:
    ci = slope_interval(fit)
except NotImplementedError:
    ci = U.reference("p0", "ci")
U.keep("p0", "ci", [float(ci[0]), float(ci[1])])
print(f"slope {slope:.2f} m³ per person (95% interval {ci[0]:.2f} to {ci[1]:.2f})")
U.check(abs(ci[0] - fit.conf_int().loc["household_size", 0]) < 0.01, "your interval matches the one statsmodels reports")

# %% [markdown]
# ## 4 · Residuals: what the line leaves out
#
# ✏️ **Exercise** · Return the residual standard deviation for each household size from 1 to 8, as a Series. Is the spread the same for every size?

# %%
def resid_sd_by_size(fit, d):
    # BEGIN SOLUTION
    r = pd.Series(np.asarray(fit.resid), index=d.index)
    keep = d["household_size"].between(1, 8)
    return r[keep].groupby(d.loc[keep, "household_size"]).std()
    # END SOLUTION


# %%
try:
    sd_by = resid_sd_by_size(fit, std)
except NotImplementedError:
    sd_by = U.reference("p0", "sd_by")
sd_by = pd.Series(sd_by)
sd_by.index = sd_by.index.astype(int)
U.keep("p0", "sd_by", {int(k): float(v) for k, v in sd_by.items()})
print(sd_by.round(1).to_string())
U.check(sd_by.iloc[-1] > sd_by.iloc[0], "the spread grows with household size")

# %% [markdown]
# **Look at.** Larger households vary more. A constant spread is one of the assumptions behind the standard error you just computed; Day 1 fits the model on the log scale, where the spread is nearly constant, and Day 3 shows what to do when it is not.

# %% [markdown]
# ## 5 · Two kinds of interval for a prediction
#
# ✏️ **Exercise** · For a household of 5 people, return a dict with the predicted mean, the 95% interval for the **mean** of all such households (`mean_ci_lower`, `mean_ci_upper`) and the 95% interval for **one new** household (`obs_ci_lower`, `obs_ci_upper`), from `fit.get_prediction(...).summary_frame(alpha=0.05)`.

# %%
def predict_five(fit):
    # BEGIN SOLUTION
    f = fit.get_prediction(pd.DataFrame({"household_size": [5]})).summary_frame(alpha=0.05).iloc[0]
    return {"mean": float(f["mean"]), "mean_lo": float(f["mean_ci_lower"]), "mean_hi": float(f["mean_ci_upper"]),
            "obs_lo": float(f["obs_ci_lower"]), "obs_hi": float(f["obs_ci_upper"])}
    # END SOLUTION


# %%
try:
    p5 = predict_five(fit)
except NotImplementedError:
    p5 = U.reference("p0", "p5")
U.keep("p0", "p5", p5)
print(f"mean of 5-person households: {p5['mean']:.1f} m³ ({p5['mean_lo']:.1f} to {p5['mean_hi']:.1f})")
print(f"one new 5-person household:  {p5['obs_lo']:.1f} to {p5['obs_hi']:.1f} m³")
U.check(p5["obs_hi"] - p5["obs_lo"] > 10 * (p5["mean_hi"] - p5["mean_lo"]), "one household is far less predictable than the mean of many")

# %% [markdown]
# **Read it.** The first interval is about the average and shrinks with more data; the second is about one household and never shrinks below the spread of households. A supply plan uses the first; a bill estimate for one customer needs the second.

# %% [markdown]
# ## 6 · Simulate to see what a standard error means
#
# Draw 200 samples of 500 households each from `std`, fit the line in each, and look at the spread of the 200 slopes. It should be close to the standard error a fit on 500 households reports.
#
# ✏️ **Exercise** · Return an array of the 200 slopes.

# %%
def sample_slopes(d, n, reps, gen):
    # BEGIN SOLUTION
    out = []
    for _ in range(reps):
        s = d.iloc[gen.choice(len(d), n, replace=False)]
        out.append(smf.ols("consumption_m3 ~ household_size", data=s).fit().params["household_size"])
    return np.array(out)
    # END SOLUTION


# %%
REPS = U.pick(200, 50)
try:
    slopes = sample_slopes(std, 500, REPS, U.rng(1))
except NotImplementedError:
    slopes = np.asarray(U.reference("p0", "slopes"))
U.keep("p0", "slopes", [float(v) for v in slopes])
one = smf.ols("consumption_m3 ~ household_size", data=std.sample(500, random_state=2)).fit()
print(f"SD of {len(slopes)} sample slopes: {np.std(slopes, ddof=1):.3f}; the standard error one sample of 500 reports: {one.bse['household_size']:.3f}")
U.check(0.5 < np.std(slopes, ddof=1) / one.bse["household_size"] < 1.6, "the standard error describes how much the slope varies from sample to sample")

# %% [markdown]
# **Look at.** The two numbers are of the same size, and the reported one is somewhat smaller. The classical standard error assumes one spread for every household; step 4 showed that the spread grows with household size. Day 3 repairs exactly this.

# %% [markdown]
# ## ✱ Stretch · The slope from a formula
#
# The least-squares slope is cov(x, y) / var(x). Compute it with NumPy and compare it with the fit.

# %%
def stretch():
    # BEGIN SOLUTION
    x, y = std["household_size"].to_numpy(), std["consumption_m3"].to_numpy()
    s = np.cov(x, y)[0, 1] / np.var(x, ddof=1)
    print(f"cov/var slope {s:.4f}; statsmodels {slope:.4f}")
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked: the interval you computed matches statsmodels', and the spread of slopes over repeated samples is of the size of the reported standard error, about a quarter larger because the spread is not constant.",
       "Not checked: whether the line is the right shape. Day 1 asks that question, on the log scale and with a spline for temperature.")

# %% [markdown]
# ## Before the entry quiz
#
# 1. What does the slope say, and what does it not say?
#    <details><summary>Answer</summary>It compares the average consumption of households that differ by one member; it does not say what adding a member to a household would do.</details>
# 2. Why is the interval for one new household so much wider than the interval for the mean?
#    <details><summary>Answer</summary>It includes the spread of households around their mean, which no amount of data removes.</details>
# 3. What does a standard error of 0.05 on a slope mean?
#    <details><summary>Answer</summary>Across repeated samples of the same size, the estimated slope would typically vary by about 0.05.</details>
