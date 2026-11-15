# %% [markdown]
# # Lab 1.2 · Fake data first
#
# Day 1 · Session 2 (Fake data first) · 25 min.
#
# Before you fit Sahil Water's real bills, you fit bills you made yourself. You keep the real households' size, band and temperature, invent their consumption from a model whose coefficients you chose, and fit it. If the fit cannot give back what you planted, the problem is in your code or your design, and the real data would never have told you.
#
# **AI policy.** AI-off for the simulator and the first fit. The hint-only tutor may help with the stretch item.
#
# **Reference state.** `data/bills.csv` (only its predictors are used) and the coefficients in the cell below. Nothing from lab 1.1 is needed.
#
# **Tasks**
# - [ ] 1 · Write the simulator with known coefficients (7')
# - [ ] 2 · Fit and compare estimates with the truth (4')
# - [ ] 3 · Coverage of the size interval over repeated simulations (7')
# - [ ] 4 · Leave out the band and watch the size coefficient (5')
# - [ ] 5 · Write the recovery table (2')
# - [ ] ✱ Stretch · Make the error spread grow with household size and repeat the coverage count

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
X = b[["household_size", "tariff_band", "temperature_c"]].copy()
if U.QUICK:
    X = X.iloc[:8000].copy()
print(f"{len(X)} households: real sizes, bands and temperatures; consumption will be invented")

# The model you plant: log of monthly cubic metres
TRUE = {"Intercept": 2.00, "household_size": 0.095, "social": -0.45, "villa": 0.40, "temperature_c": 0.030, "sigma": 0.30}
FORMULA = "log_m3 ~ household_size + C(tariff_band) + temperature_c"

# %% [markdown]
# ## 1 · Write the simulator with known coefficients (7')
#
# The model: log consumption = intercept + size × households size + a shift for the social and villa bands + temperature × degrees + a normal error with standard deviation sigma.
#
# ✏️ **Exercise** · Write `simulate(X, p, gen)`: return an array of simulated `log_m3`, one per row of `X`, using the coefficients in `p` and the generator `gen` for the errors.

# %%
def simulate(X, p, gen):
    # BEGIN SOLUTION
    shift = np.select([X["tariff_band"] == "social", X["tariff_band"] == "villa"], [p["social"], p["villa"]], 0.0)
    mean = p["Intercept"] + p["household_size"] * X["household_size"].to_numpy() + shift + p["temperature_c"] * X["temperature_c"].to_numpy()
    return mean + gen.normal(0, p["sigma"], len(X))
    # END SOLUTION


# %%
def fake(gen):
    d = X.copy()
    try:
        d["log_m3"] = simulate(d, TRUE, gen)
    except NotImplementedError:
        shift = np.select([d["tariff_band"] == "social", d["tariff_band"] == "villa"], [TRUE["social"], TRUE["villa"]], 0.0)
        d["log_m3"] = (TRUE["Intercept"] + TRUE["household_size"] * d["household_size"] + shift
                       + TRUE["temperature_c"] * d["temperature_c"] + gen.normal(0, TRUE["sigma"], len(d)))
    return d


d0 = fake(U.rng(12))
print(d0["log_m3"].describe().round(3).to_string())
U.check(abs(d0["log_m3"].std() - 0.45) < 0.15, "the simulated log consumption has a plausible spread")

# %% [markdown]
# ## 2 · Fit and compare estimates with the truth (4')
#
# ✏️ **Exercise** · Fit `FORMULA` to `d0` with `smf.ols(...).fit()` and return the fit.

# %%
def fit_fake(d):
    # BEGIN SOLUTION
    return smf.ols(FORMULA, data=d).fit()
    # END SOLUTION


# %%
names = {"Intercept": "Intercept", "household_size": "household_size", "social": "C(tariff_band)[T.social]",
         "villa": "C(tariff_band)[T.villa]", "temperature_c": "temperature_c"}
try:
    f0 = fit_fake(d0)
    est0 = {k: float(f0.params[v]) for k, v in names.items()}
    se0 = {k: float(f0.bse[v]) for k, v in names.items()}
    est0["sigma"] = float(np.sqrt(f0.scale))
except NotImplementedError:
    est0, se0 = U.reference("d1_2", "est0")
U.keep("d1_2", "est0", [est0, se0])
rows = [[k, TRUE[k], est0[k], se0.get(k, float("nan"))] for k in TRUE]
U.table(["term", "planted", "estimate", "std error"], rows)
U.check(all(abs(est0[k] - TRUE[k]) < 4 * se0[k] for k in names), "every estimate within four standard errors of what was planted")

# %% [markdown]
# **Look at.** The estimates are not equal to the truth: one simulated data set is one draw. Whether the interval is honest is a question about many draws.

# %% [markdown]
# ## 3 · Coverage of the size interval over repeated simulations (7')
#
# ✏️ **Exercise** · Write `coverage(reps)`: simulate `reps` new data sets (use `U.rng(100 + r)` for repeat `r`), fit each, and return the share of 95% intervals for `household_size` that contain 0.095, with the list of estimates.

# %%
def coverage(reps):
    # BEGIN SOLUTION
    hits, ests = 0, []
    for r in range(reps):
        f = smf.ols(FORMULA, data=fake(U.rng(100 + r))).fit()
        lo, hi = f.conf_int().loc["household_size"]
        hits += lo <= TRUE["household_size"] <= hi
        ests.append(float(f.params["household_size"]))
    return hits / reps, ests
    # END SOLUTION


# %%
REPS = U.pick(200, 40)
try:
    cov, ests = coverage(REPS)
except NotImplementedError:
    cov, ests = U.reference("d1_2", "coverage")
U.keep("d1_2", "coverage", [cov, ests])
ests = np.asarray(ests)
print(f"{REPS} simulated data sets: {cov:.1%} of the 95% intervals contain the planted 0.095")
print(f"spread of the estimates {ests.std():.5f}; the standard error of one fit said {se0['household_size']:.5f}")
plt = U.plt()
fig, ax = plt.subplots()
ax.hist(ests, bins=25, color="#3a7ca5")
ax.axvline(TRUE["household_size"], color="#e4572e", linewidth=2)
ax.set(xlabel="estimated coefficient of household size", ylabel="data sets", title="Estimates over repeated fake data")
plt.show()
U.check(abs(cov - 0.95) < U.pick(0.04, 0.10), "coverage close to 95%: the interval is honest when the model is right")

# %% [markdown]
# ## 4 · Leave out the band and watch the size coefficient (5')
#
# Social-tariff households are larger and use less; villas are mid-sized and use more. Fit a model without the band to the same fake data.
#
# ✏️ **Exercise** · Fit `log_m3 ~ household_size + temperature_c` on `d0` and return the coefficient of `household_size`.

# %%
def size_without_band(d):
    # BEGIN SOLUTION
    return float(smf.ols("log_m3 ~ household_size + temperature_c", data=d).fit().params["household_size"])
    # END SOLUTION


# %%
try:
    s_short = size_without_band(d0)
except NotImplementedError:
    s_short = U.reference("d1_2", "s_short")
U.keep("d1_2", "s_short", s_short)
by_band = X.groupby("tariff_band", observed=True)["household_size"].mean()
print("mean household size by band:", by_band.round(2).to_dict())
print(f"size coefficient: {est0['household_size']:.4f} with the band, {s_short:.4f} without it (planted 0.095)")
U.check(abs(s_short - TRUE["household_size"]) > 0.005, "leaving out the band moves the size coefficient away from what was planted")

# %% [markdown]
# **Look at.** No warning appears. The short model fits, its interval is narrow and it is wrong for the planted quantity. Only fake data, where you know the answer, shows this.

# %% [markdown]
# ## 5 · Write the recovery table (2')

# %%
recovery = pd.DataFrame({"planted": TRUE, "estimate": est0}).round(4)
recovery.loc["coverage of size interval", ["planted", "estimate"]] = [0.95, round(cov, 3)]
recovery.loc["size, band left out", ["planted", "estimate"]] = [TRUE["household_size"], round(s_short, 4)]
print(recovery.to_string())
U.keep("d1_2", "recovery", recovery)

# %% [markdown]
# ## ✱ Stretch · An error that grows with household size
#
# Change the simulator so that sigma is 0.15 + 0.04 × household size, run the coverage count again, and compare the classical interval with one from `fit(cov_type="HC3")`.

# %%
def stretch():
    # BEGIN SOLUTION
    hits = {"classical": 0, "HC3": 0}
    reps = U.pick(100, 20)
    for r in range(reps):
        gen = U.rng(500 + r)
        d = fake(gen)
        d["log_m3"] += gen.normal(0, 1, len(d)) * (0.04 * d["household_size"] - 0.15)
        for kind in hits:
            f = smf.ols(FORMULA, data=d).fit(**({} if kind == "classical" else {"cov_type": "HC3"}))
            lo, hi = f.conf_int().loc["household_size"]
            hits[kind] += lo <= TRUE["household_size"] <= hi
    print({k: v / reps for k, v in hits.items()})
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: you planted the coefficients, so each estimate is compared with its known value; coverage {cov:.1%} over {REPS} data sets.",
       "Checked: leaving out a term tied to household size biases its coefficient without any warning from the fit.",
       "Not checked: whether the real bills follow this model. Fake data test the method, never the world.")

# %% [markdown]
# ## Checkpoint
#
# 1. Your fit recovers every planted coefficient. What have you shown?
#    <details><summary>Answer</summary>That the code and the estimator work when the model is right. Nothing about whether the real data follow the model.</details>
# 2. Coverage over 200 data sets is 95%. What would 80% mean?
#    <details><summary>Answer</summary>The intervals are too narrow: the standard error or the model is wrong for these data.</details>
# 3. Why did the short model's size coefficient move?
#    <details><summary>Answer</summary>The band is related to both household size and consumption, so without it the size coefficient absorbs part of the band's shift.</details>
#
# ## Carry forward
#
# Labs 1.3 and 1.4 fit the real bills. Before a new model in the capstone, simulate from it once.
