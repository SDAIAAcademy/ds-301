# %% [markdown]
# # Lab 1.3 · A temperature spline
#
# Day 1 · Session 3 (Transformations and splines) · 25 min.
#
# Ghaliya plans supply month by month, and summer is where the network runs short. She asks how monthly consumption rises with temperature for a typical household. You fit log consumption with a straight temperature term, see what it misses, replace it with a spline, and draw the curve in cubic metres with its band.
#
# **Use and estimand.** Descriptive: the mean monthly consumption of a four-person household on the standard tariff, as a function of the month's temperature, among Sahil's billed households.
#
# **AI policy.** AI-off for the first fit and its reading. The hint-only tutor may help with plotting and the stretch item.
#
# **Reference state.** `data/bills.csv`, loaded fresh. Nothing from labs 1.1 or 1.2 is needed.
#
# **Tasks**
# - [ ] 1 · Log consumption against temperature (4')
# - [ ] 2 · The straight-line model and its residual pattern (5')
# - [ ] 3 · The spline model and the comparison (6')
# - [ ] 4 · The curve with its band (6')
# - [ ] 5 · Back to cubic metres: median and mean (4')
# - [ ] ✱ Stretch · Try three, five and eight degrees of freedom and pick one by cross-validated error

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
print(f"{len(b)} bills; temperature from {b['temperature_c'].min():.1f} to {b['temperature_c'].max():.1f} °C")

# %% [markdown]
# ## 1 · Log consumption against temperature (4')
#
# Consumption is skewed and effects on it are multiplicative: a hot month adds a share, not a fixed number of cubic metres, to every household. The log turns shares into differences.

# %%
bins = pd.cut(b["temperature_c"], np.arange(16, 44, 2))  # 16 to 42 °C; the few bills outside are left out of the bins
means = b.groupby(bins, observed=True)["log_m3"].agg(["mean", "size"])
print(means.round(3).to_string())
plt = U.plt()
fig, ax = plt.subplots()
ax.scatter(b["temperature_c"], b["log_m3"], s=2, alpha=0.08, color="#3a7ca5")
ax.plot([i.mid for i in means.index], means["mean"], color="#e4572e", marker="o")
ax.set(xlabel="month's temperature, °C", ylabel="log of cubic metres a month", title="Flat when mild, steep when hot")
plt.show()

# %% [markdown]
# ## 2 · The straight-line model and its residual pattern (5')
#
# ✏️ **Exercise** · Fit `log_m3 ~ household_size + tariff_band + temperature_c` and return the fit.

# %%
def fit_line(b):
    # BEGIN SOLUTION
    return smf.ols("log_m3 ~ household_size + tariff_band + temperature_c", data=b).fit()
    # END SOLUTION


# %%
f_line = None
try:
    f_line = fit_line(b)
    pattern = f_line.resid.groupby(bins, observed=True).mean()
    line_stats = {"aic": float(f_line.aic), "temp_pct": float(100 * (np.exp(f_line.params["temperature_c"]) - 1)),
                  "pattern": pattern.round(4).tolist()}
except NotImplementedError:
    line_stats = U.reference("d1_3", "line")
U.keep("d1_3", "line", line_stats)
print(f"straight line: each degree goes with {line_stats['temp_pct']:.1f}% more consumption, at every temperature")
print("mean residual by 2-degree bin:", np.round(line_stats["pattern"], 3))
U.check(line_stats["pattern"][0] > 0.02 and line_stats["pattern"][-1] > 0.02 and min(line_stats["pattern"]) < -0.02,
        "the residuals are positive at both ends and negative in the middle: the line misses a bend")

# %% [markdown]
# ## 3 · The spline model and the comparison (6')
#
# A **spline** is a smooth curve made of polynomial pieces joined at knots. `bs(temperature_c, df=5)` gives five columns; the model weights them. You choose how flexible (the degrees of freedom), not the shape.
#
# ✏️ **Exercise** · Fit `log_m3 ~ household_size + tariff_band + bs(temperature_c, df=5)` and return the fit.

# %%
def fit_spline(b):
    # BEGIN SOLUTION
    return smf.ols("log_m3 ~ household_size + tariff_band + bs(temperature_c, df=5)", data=b).fit()
    # END SOLUTION


# %%
try:
    f_spl = fit_spline(b)
except NotImplementedError:
    print("↪ exercise not done yet: fitting the reference spline model so the cells below run")
    if U.STRICT:
        raise
    f_spl = smf.ols("log_m3 ~ household_size + tariff_band + bs(temperature_c, df=5)", data=b).fit()
spl_pattern = f_spl.resid.groupby(bins, observed=True).mean()
spl_stats = {"aic": float(f_spl.aic), "sigma": float(np.sqrt(f_spl.scale)), "pattern": spl_pattern.round(4).tolist()}
U.keep("d1_3", "spline", spl_stats)
U.table(["model", "AIC", "largest bin residual"],
        [["straight temperature", line_stats["aic"], float(np.max(np.abs(line_stats["pattern"])))],
         ["spline, 5 df", spl_stats["aic"], float(np.max(np.abs(spl_stats["pattern"])))]], fmt="{:.4g}")
U.check(spl_stats["aic"] < line_stats["aic"] - 500 and np.max(np.abs(spl_stats["pattern"])) < 0.03,
        "the spline fits much better and its residuals have no pattern left in temperature")

# %% [markdown]
# ## 4 · The curve with its band (6')
#
# The band is the 95% interval for the **mean** at each temperature, from 1,000 simulations of the coefficients (`U.predict_band`). It is narrow: 40,000 bills pin the mean down. It is not the range of single households.
#
# ✏️ **Exercise** · Build `grid`: 53 rows with temperatures from 16 to 42 °C in steps of 0.5, `household_size` 4 and `tariff_band` "standard" (as a category with the same levels as `b`).

# %%
def make_grid(b):
    # BEGIN SOLUTION
    t = np.arange(16, 42.01, 0.5)
    return pd.DataFrame({"temperature_c": t, "household_size": 4,
                         "tariff_band": pd.Categorical(["standard"] * len(t), categories=b["tariff_band"].cat.categories)})
    # END SOLUTION


# %%
try:
    grid = make_grid(b)
except NotImplementedError:
    print("↪ exercise not done yet: using the reference grid")
    if U.STRICT:
        raise
    t = np.arange(16, 42.01, 0.5)
    grid = pd.DataFrame({"temperature_c": t, "household_size": 4,
                         "tariff_band": pd.Categorical(["standard"] * len(t), categories=b["tariff_band"].cat.categories)})
band = U.predict_band(f_spl, grid, scale="m3")
fig, ax = plt.subplots()
ax.fill_between(grid["temperature_c"], band["low"], band["high"], color="#3a7ca5", alpha=0.3, label="95% interval for the mean")
ax.plot(grid["temperature_c"], band["estimate"], color="#3a7ca5", label="spline")
ax.set(xlabel="month's temperature, °C", ylabel="cubic metres a month", title="Four people, standard tariff")
ax.legend()
plt.show()
at = band.set_index(grid["temperature_c"]).loc[[20.0, 30.0, 40.0]].round(1)
print(at.to_string())
U.keep("d1_3", "band_at", at)
U.check(at.loc[40.0, "estimate"] > 1.5 * at.loc[30.0, "estimate"] and at.loc[30.0, "estimate"] < 1.25 * at.loc[20.0, "estimate"],
        "the curve is flat when mild and climbs steeply above 30 °C")

# %% [markdown]
# ## 5 · Back to cubic metres: median and mean (4')
#
# exp(predicted log) is the **median** consumption, not the mean: the log of a mean is larger than the mean of the logs. With normal errors on the log scale, the mean is exp(prediction + σ²/2).
#
# ✏️ **Exercise** · Return `(median_30, mean_30)`: the two back-transformed predictions at 30 °C for the grid household, using `f_spl.predict` and `f_spl.scale`.

# %%
def back_transform(f, grid):
    # BEGIN SOLUTION
    row = grid[grid["temperature_c"] == 30.0]
    eta = float(np.asarray(f.predict(row))[0])
    return float(np.exp(eta)), float(np.exp(eta + f.scale / 2))
    # END SOLUTION


# %%
try:
    med30, mean30 = back_transform(f_spl, grid)
except NotImplementedError:
    med30, mean30 = U.reference("d1_3", "back")
U.keep("d1_3", "back", [med30, mean30])
near = b[(b["household_size"] == 4) & (b["tariff_band"] == "standard") & b["temperature_c"].between(29, 31)]
print(f"at 30 °C: median {med30:.1f} m³, mean {mean30:.1f} m³ ({100 * (mean30 / med30 - 1):.1f}% higher)")
print(f"observed: {len(near)} such bills between 29 and 31 °C, median {near['consumption_m3'].median():.1f}, mean {near['consumption_m3'].mean():.1f}")
U.check(mean30 > med30 and abs(mean30 - near["consumption_m3"].mean()) < abs(med30 - near["consumption_m3"].mean()) + 0.5,
        "the mean back-transform is the one to compare with the observed mean")

# %% [markdown]
# **Look at.** A supply plan adds up volumes, so it needs means. A plan built from exp(prediction) runs short by the percentage above, every month.

# %% [markdown]
# ## ✱ Stretch · How flexible?
#
# Fit the spline with 3, 5 and 8 degrees of freedom and compare their mean squared error on held-out bills (5 folds, `sklearn.model_selection.KFold`, `random_state=301`).

# %%
def stretch():
    # BEGIN SOLUTION
    from sklearn.model_selection import KFold
    out = {}
    for df in (3, 5, 8):
        errs = []
        for tr, te in KFold(5, shuffle=True, random_state=301).split(b):
            f = smf.ols(f"log_m3 ~ household_size + tariff_band + bs(temperature_c, df={df}, lower_bound=13, upper_bound=44)", data=b.iloc[tr]).fit()
            errs.append(float(np.mean((b["log_m3"].iloc[te] - f.predict(b.iloc[te])) ** 2)))
        out[df] = round(float(np.mean(errs)), 5)
    print("held-out mean squared error by degrees of freedom:", out)
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
t = U.truth()["consumption"]
print("the generator's temperature term:", t["temp_effect"])
U.note("Checked against the truth: the generator bends at 28 °C (a squared term above it); the spline found the bend without being told where.",
       f"Checked: the mean back-transform ({mean30:.1f} m³) is the one close to the observed mean of comparable bills.",
       "Not checked: temperatures outside 16 to 42 °C; a spline says nothing beyond its data.")

# %% [markdown]
# ## Checkpoint
#
# 1. The temperature coefficient of the straight model is 0.025. What does it say, and why is it misleading here?
#    <details><summary>Answer</summary>About 2.5% more per degree at every temperature. The data are flat when mild and much steeper when hot, so it is too steep in winter and too flat in summer.</details>
# 2. Why is the band so narrow when single bills scatter widely?
#    <details><summary>Answer</summary>It is an interval for the mean at each temperature, estimated from 40,000 bills. An interval for one household would be many times wider.</details>
# 3. A planner sums exp(prediction) over all households. What happens?
#    <details><summary>Answer</summary>The total is too low by about σ²/2, roughly 5% here, because exp(prediction) is a median.</details>
#
# ## Carry forward
#
# Lab 1.4 keeps this spline and adds an interaction.
