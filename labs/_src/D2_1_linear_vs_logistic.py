# %% [markdown]
# # Lab 2.1 · Linear against logistic
#
# Day 2 · Session 1 (Links and families) · 25 min.
#
# Nidal Al-Fadhli, billing and collections manager, wants to know which households are likely to pay late, to plan the collections desk. The outcome is a flag: late or not. You fit it twice, with a straight line and with a logistic model, and find where the straight line breaks.
#
# **Use and estimand.** Descriptive and predictive: the probability that a bill is paid late, given its band, size, amount, autopay and past late payments, among this month's bills.
#
# **AI policy.** AI-off for both fits and their reading. The hint-only tutor may help with the decile table and the stretch item.
#
# **Reference state.** `data/bills.csv`, loaded fresh. Nothing from Day 1 is needed.
#
# **Tasks**
# - [ ] 1 · Late-payment rates by band and autopay (4')
# - [ ] 2 · The linear probability model (5')
# - [ ] 3 · Predictions outside zero and one (4')
# - [ ] 4 · The logistic model (5')
# - [ ] 5 · Predicted against observed, by decile (7')
# - [ ] ✱ Stretch · Compare the two models' average difference for autopay

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
RHS = "bill_sar + autopay + tariff_band + prior_late_12m + household_size"
print(f"{len(b)} bills, {b['late'].mean():.1%} paid late")

# %% [markdown]
# ## 1 · Late-payment rates by band and autopay (4')

# %%
rates = b.pivot_table(index="tariff_band", columns="autopay", values="late", aggfunc="mean", observed=True)
rates.columns = ["no autopay", "autopay"]
print(rates.round(3).to_string())
U.keep("d2_1", "rates", rates)

# %% [markdown]
# **Look at.** Rates run from about 2% to about 34%. A probability is bounded by 0 and 1, and differences near the bounds are squeezed: autopay cannot cut 3% by 20 points.

# %% [markdown]
# ## 2 · The linear probability model (5')
#
# ✏️ **Exercise** · Fit `late ~ ` + `RHS` by ordinary least squares and return the fit.

# %%
def fit_lpm(b):
    # BEGIN SOLUTION
    return smf.ols("late ~ " + RHS, data=b).fit()
    # END SOLUTION


# %%
try:
    lpm = fit_lpm(b)
except NotImplementedError:
    print("↪ exercise not done yet: fitting the reference model so the cells below run")
    if U.STRICT:
        raise
    lpm = smf.ols("late ~ " + RHS, data=b).fit()
print(lpm.params.round(4).to_string())
p_lpm = np.asarray(lpm.fittedvalues)
U.check(-0.3 < lpm.params["autopay"] < -0.2, "the line says autopay goes with about 25 points less late payment, for every household")

# %% [markdown]
# ## 3 · Predictions outside zero and one (4')
#
# ✏️ **Exercise** · Return `(below, above, lowest, highest)`: how many fitted values are below 0 and above 1, and the smallest and largest.

# %%
def out_of_range(p):
    # BEGIN SOLUTION
    p = np.asarray(p)
    return int((p < 0).sum()), int((p > 1).sum()), float(p.min()), float(p.max())
    # END SOLUTION


# %%
try:
    oor = out_of_range(p_lpm)
except NotImplementedError:
    oor = U.reference("d2_1", "oor")
U.keep("d2_1", "oor", list(oor))
print(f"{oor[0]} bills with a predicted probability below 0 and {oor[1]} above 1; range {oor[2]:.3f} to {oor[3]:.3f}")
neg = b[p_lpm < 0]
print("who gets a negative probability:", neg["autopay"].mean().round(2), "share on autopay;", neg["tariff_band"].value_counts().to_dict())
U.check(oor[0] > 1000, "thousands of bills get a negative probability of being late")

# %% [markdown]
# ## 4 · The logistic model (5')
#
# The logistic model keeps a straight line on the **log odds** scale and maps it into (0, 1): p = 1 / (1 + e<sup>−η</sup>).
#
# ✏️ **Exercise** · Fit `late ~ ` + `RHS` with `smf.logit(...).fit(disp=0)` and return the fit.

# %%
def fit_logit(b):
    # BEGIN SOLUTION
    return smf.logit("late ~ " + RHS, data=b).fit(disp=0)
    # END SOLUTION


# %%
try:
    lg = fit_logit(b)
except NotImplementedError:
    print("↪ exercise not done yet: fitting the reference model so the cells below run")
    if U.STRICT:
        raise
    lg = smf.logit("late ~ " + RHS, data=b).fit(disp=0)
p_lg = np.asarray(lg.predict(b))
print(lg.params.round(4).to_string())
print(f"logistic predictions run from {p_lg.min():.4f} to {p_lg.max():.4f}")
U.keep("d2_1", "logit_params", lg.params.round(5).to_dict())
U.check(0 < p_lg.min() and p_lg.max() < 1, "every logistic prediction is a probability")

# %% [markdown]
# ## 5 · Predicted against observed, by decile (7')
#
# Sort bills by a model's predicted probability, cut them into ten equal groups, and compare the mean prediction with the observed late rate in each group.
#
# ✏️ **Exercise** · Write `by_decile(p, y)`: return a DataFrame with one row per decile of `p` and the columns `predicted` (mean of `p`) and `observed` (mean of `y`).

# %%
def by_decile(p, y):
    # BEGIN SOLUTION
    d = pd.DataFrame({"p": np.asarray(p), "y": np.asarray(y)})
    d["decile"] = pd.qcut(d["p"].rank(method="first"), 10, labels=range(1, 11))
    return d.groupby("decile", observed=True).agg(predicted=("p", "mean"), observed=("y", "mean"))
    # END SOLUTION


# %%
try:
    dec_lpm, dec_lg = by_decile(p_lpm, b["late"]), by_decile(p_lg, b["late"])
except NotImplementedError:
    dec_lpm, dec_lg = U.reference("d2_1", "deciles")
U.keep("d2_1", "deciles", [dec_lpm, dec_lg])
table = pd.concat({"linear": dec_lpm, "logistic": dec_lg}, axis=1).round(3)
print(table.to_string())
plt = U.plt()
fig, ax = plt.subplots(figsize=(5.5, 5))
ax.plot([0, 0.8], [0, 0.8], color="grey", linewidth=1)
ax.plot(dec_lpm["predicted"], dec_lpm["observed"], "o-", color="#e4572e", label="linear")
ax.plot(dec_lg["predicted"], dec_lg["observed"], "o-", color="#3a7ca5", label="logistic")
ax.set(xlabel="mean predicted probability", ylabel="observed late rate", title="By decile of the prediction")
ax.legend()
plt.show()
gap_lpm = float((dec_lpm["predicted"] - dec_lpm["observed"]).abs().max())
gap_lg = float((dec_lg["predicted"] - dec_lg["observed"]).abs().max())
print(f"largest gap: linear {gap_lpm:.3f}, logistic {gap_lg:.3f}")
U.check(gap_lpm > 2 * gap_lg, "the linear model misses by far more in its extreme deciles")

# %% [markdown]
# **Look at.** In its lowest decile the line predicts a negative mean probability while a few of those bills are still paid late. In the middle the two models agree. A straight line can describe an average difference; it cannot describe probabilities near the bounds.

# %% [markdown]
# ## ✱ Stretch · Autopay in both models
#
# The line says autopay goes with the same number of points for every bill. Compute the logistic model's **average** difference in probability (every bill with autopay set to 1, minus set to 0, averaged) with `U.contrast(lg, b, "autopay", 0, 1, scale="probability")` and compare it with the linear coefficient.

# %%
def stretch():
    # BEGIN SOLUTION
    ame = U.contrast(lg, b, "autopay", 0, 1, scale="probability")
    print(f"linear coefficient {lpm.params['autopay']:.3f}; logistic average difference {ame.loc['all', 'estimate']:.3f} ({ame.loc['all', 'low']:.3f} to {ame.loc['all', 'high']:.3f})")
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
t = U.truth()["late_payment"]
U.note(f"Checked against the truth: the generator is logistic (autopay {t['autopay']} on the log odds scale), so the line's out-of-range predictions are its own failure, not noise.",
       "Checked: the decile table shows where each model's predictions match the observed rates.",
       "Not checked: whether the logistic model's form is right in every predictor; Day 3, lab 3.1 checks the bill term.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why does the line give negative probabilities to autopay households with small bills?
#    <details><summary>Answer</summary>It subtracts the same 25 points for autopay from every bill, also from bills whose probability was already near zero.</details>
# 2. When is a linear probability model acceptable?
#    <details><summary>Answer</summary>When predictions stay well inside 0 to 1 and the question is one average difference; never for predicting probabilities near the bounds.</details>
# 3. What does the logistic link keep straight?
#    <details><summary>Answer</summary>The log odds. The probability itself curves, so differences on that scale depend on where a household starts.</details>
#
# ## Carry forward
#
# Lab 2.2 reads this logistic model on the probability scale for three households.
