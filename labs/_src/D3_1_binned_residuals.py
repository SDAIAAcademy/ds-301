# %% [markdown]
# # Lab 3.1 · Binned residuals
#
# Day 3 · Session 1 (Residuals that tell you something) · 25 min.
#
# Qusai Al-Mufarrij, the analyst who left, built the late-payment forecast the collections desk still uses. Before anyone trusts it again, you check it. Raw residuals of a yes-or-no model are two useless bands; binned residuals, against each predictor, show what the model misses. You find the bill term that belongs on the log scale, repair it and write the first line of the diagnosis log.
#
# **Use and estimand.** Predictive and descriptive: the probability that a bill is paid late. The question here is whether the model's form fits the data.
#
# **AI policy.** AI-off for the diagnosis: you read the plots yourself. The hint-only tutor may help with plotting and the stretch item.
#
# **Reference state.** `data/bills.csv` and `data/qusai/models.json` (Qusai's model `late_v1`), loaded fresh. Nothing from Day 2 is needed.
#
# **Tasks**
# - [ ] 1 · Fit Qusai's model as he wrote it (3')
# - [ ] 2 · Raw residuals, and why they do not help (3')
# - [ ] 3 · Binned residuals against each predictor (8')
# - [ ] 4 · Add the log term and refit (6')
# - [ ] 5 · The first line of the diagnosis log (5')
# - [ ] ✱ Stretch · Draw binned residuals against the fitted probability

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
spec = U.qusai_models()["late_v1"]
print(spec["what"], "\n", spec["formula"])

# %% [markdown]
# ## 1 · Fit Qusai's model as he wrote it (3')
#
# ✏️ **Exercise** · Fit `spec["formula"]` with `smf.logit(...).fit(disp=0)` and return the fit.

# %%
def fit_v1(b):
    # BEGIN SOLUTION
    return smf.logit(spec["formula"], data=b).fit(disp=0)
    # END SOLUTION


# %%
try:
    v1 = fit_v1(b)
except NotImplementedError:
    print("↪ exercise not done yet: fitting the reference model so the cells below run")
    if U.STRICT:
        raise
    v1 = smf.logit(spec["formula"], data=b).fit(disp=0)
p1 = np.asarray(v1.predict(b))
print(f"AIC {v1.aic:.0f}; every coefficient looks sensible:")
print(v1.params.round(4).to_string())

# %% [markdown]
# ## 2 · Raw residuals, and why they do not help (3')
#
# A residual of a yes-or-no outcome is either 1 − p or 0 − p. Plotted against anything, it makes two bands, whatever the model.

# %%
plt = U.plt()
r1 = b["late"].to_numpy() - p1
fig, ax = plt.subplots()
ax.scatter(p1, r1, s=2, alpha=0.1, color="#3a7ca5")
ax.set(xlabel="fitted probability", ylabel="observed minus fitted", title="Raw residuals: two bands, no information")
plt.show()

# %% [markdown]
# ## 3 · Binned residuals against each predictor (8')
#
# Sort the bills by a predictor, cut them into 20 bins (or one bin per value when it has few), and plot the mean residual of each bin with a band of ±2 standard errors. If the model's form is right, about 19 of 20 bins sit inside the band and the means show no pattern.
#
# ✏️ **Exercise** · For each predictor in `["bill_sar", "household_size", "prior_late_12m"]`, compute `U.binned_residuals(b["late"], p1, b[x])` and return `{x: number of bins outside the band}`.

# %%
PREDICTORS = ["bill_sar", "household_size", "prior_late_12m"]


def outside_by_predictor(p):
    # BEGIN SOLUTION
    return {x: int(U.binned_residuals(b["late"], p, b[x])["outside"].sum()) for x in PREDICTORS}
    # END SOLUTION


# %%
try:
    outside = outside_by_predictor(p1)
except NotImplementedError:
    outside = U.reference("d3_1", "outside_v1")
U.keep("d3_1", "outside_v1", outside)
fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
for ax, x in zip(axes, PREDICTORS):
    br = U.binned_residuals(b["late"], p1, b[x])
    ax.fill_between(br["x_mean"], -br["band"], br["band"], color="grey", alpha=0.2)
    ax.plot(br["x_mean"], br["resid_mean"], "o", color="#e4572e")
    ax.axhline(0, color="black", linewidth=1)
    ax.set(xlabel=x, title=f"{outside[x]} bins outside the band")
axes[0].set_ylabel("mean residual")
plt.show()
print(outside)
U.check(outside["bill_sar"] >= 4 and outside["bill_sar"] > max(outside["household_size"], outside["prior_late_12m"]),
        "the bill term is where the model misses: residuals below zero for small bills, above in the middle")

# %% [markdown]
# **Look at.** Small bills are late less often than the model says, middle bills more often. A straight line in the bill on the log odds scale rises too slowly at first and too fast later: the shape of a log.

# %% [markdown]
# ## 4 · Add the log term and refit (6')
#
# ✏️ **Exercise** · Fit the same model with `np.log(bill_sar)` in place of `bill_sar` and return the fit.

# %%
def fit_log(b):
    # BEGIN SOLUTION
    return smf.logit(spec["formula"].replace("bill_sar", "np.log(bill_sar)"), data=b).fit(disp=0)
    # END SOLUTION


# %%
try:
    v1b = fit_log(b)
except NotImplementedError:
    print("↪ exercise not done yet: fitting the reference model so the cells below run")
    if U.STRICT:
        raise
    v1b = smf.logit(spec["formula"].replace("bill_sar", "np.log(bill_sar)"), data=b).fit(disp=0)
p2 = np.asarray(v1b.predict(b))
br2 = U.binned_residuals(b["late"], p2, b["bill_sar"])
repair = {"aic_before": float(v1.aic), "aic_after": float(v1b.aic), "outside_after": int(br2["outside"].sum()),
          "outside_before": int(outside["bill_sar"])}
U.keep("d3_1", "repair", repair)
print(repair)
U.check(repair["aic_after"] < repair["aic_before"] - 50 and repair["outside_after"] <= 2, "with the log term the binned residuals sit inside the band and AIC falls")

# %% [markdown]
# ## 5 · The first line of the diagnosis log (5')
#
# The log of Day 3 names each problem, the evidence that shows it and the correction. Lab 3.4 assembles it.
#
# ✏️ **Exercise** · Return `U.log_entry("missing non-linear term", evidence, fix)` with an evidence sentence that quotes the number of bins outside the band before and after, and a fix sentence.

# %%
def my_entry():
    # BEGIN SOLUTION
    return U.log_entry("missing non-linear term",
                       f"late_v1: binned residuals against bill_sar had {repair['outside_before']} of 20 bins outside the 2-SE band, negative for small bills and positive in the middle",
                       f"use np.log(bill_sar): {repair['outside_after']} bins outside, AIC from {repair['aic_before']:.0f} to {repair['aic_after']:.0f}")
    # END SOLUTION


# %%
try:
    entry = my_entry()
except NotImplementedError:
    entry = U.reference("d3_1", "entry")
U.keep("d3_1", "entry", entry)
U.log_save("3.1", entry)
print(entry)
U.check(str(repair["outside_before"]) in entry["evidence"], "the evidence quotes the number of bins outside the band")

# %% [markdown]
# ## ✱ Stretch · Against the fitted probability
#
# Draw binned residuals against the fitted probability for both models. Would this plot alone have found the problem?

# %%
def stretch():
    # BEGIN SOLUTION
    for name, p in (("bill_sar", p1), ("log bill", p2)):
        br = U.binned_residuals(b["late"], p, p)
        print(f"{name}: {int(br['outside'].sum())} bins outside the band against the fitted probability")
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the truth: the generator uses log(bill / 100) with coefficient {U.truth()['late_payment']['log_bill_over_100']}; your repaired coefficient is {v1b.params['np.log(bill_sar)']:.2f}.",
       "Checked: after the repair, the binned residuals against the bill sit inside their band.",
       "Not checked: interactions between predictors; a binned plot against one predictor cannot see them.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why are raw residuals of a logistic model plotted against the fit uninformative?
#    <details><summary>Answer</summary>Each is 1 − p or −p, so they form two bands whatever the model; only averages over many bills carry information.</details>
# 2. About how many bins out of 20 fall outside a 2-SE band when the model is right?
#    <details><summary>Answer</summary>About one: the band holds about 95% of bin means.</details>
# 3. The pattern was negative for small bills, positive in the middle, negative again for the largest. Why a log and not a quadratic?
#    <details><summary>Answer</summary>Either can remove the pattern; the log is simpler, stays monotone and matches how a bill's burden grows. Compare both by AIC and by the plot.</details>
#
# ## Carry forward
#
# The first line of the diagnosis log is saved in `artifacts/diagnosis_log.json`; lab 3.4 assembles the log.
