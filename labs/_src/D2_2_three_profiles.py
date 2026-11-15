# %% [markdown]
# # Lab 2.2 · Three household profiles
#
# Day 2 · Session 2 (Reading a logistic model) · 25 min.
#
# Nidal asks a plain question: "How much lower is late payment with autopay?" The logistic model has one autopay coefficient and one odds ratio. On the probability scale, which is the scale Nidal thinks in, the answer depends on the household. You compute it for three households he recognises, with intervals, and write one careful sentence for each.
#
# **Use and estimand.** Descriptive: for three stated household profiles, the difference in the probability of a late bill between households with and without autopay, other listed characteristics equal. Households chose autopay themselves, so this is not what promoting autopay would do.
#
# **AI policy.** AI-off for the reading of the coefficients. The hint-only tutor may help with the profile table and the stretch item.
#
# **Reference state.** `data/bills.csv`, loaded fresh; the model formula of lab 2.1 is written below.
#
# **Tasks**
# - [ ] 1 · Fit the model and read the odds ratios (5')
# - [ ] 2 · Describe the three profiles (3')
# - [ ] 3 · Predicted probabilities with and without autopay (6')
# - [ ] 4 · Differences with intervals (6')
# - [ ] 5 · One sentence per profile, without causal words (5')
# - [ ] ✱ Stretch · Compute the average marginal effect of autopay over all bills

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
FORMULA = "late ~ bill_sar + autopay + tariff_band + prior_late_12m + household_size"
lg = smf.logit(FORMULA, data=b).fit(disp=0)

# %% [markdown]
# ## 1 · Fit the model and read the odds ratios (5')
#
# A coefficient is a change in the **log odds** for one unit of its variable; exp(coefficient) is an **odds ratio**.
#
# ✏️ **Exercise** · Return a DataFrame with the odds ratio of every term except the intercept and its 95% interval (exp of `lg.conf_int()`), columns `odds_ratio`, `low`, `high`.

# %%
def odds_ratios(lg):
    # BEGIN SOLUTION
    ci = np.exp(lg.conf_int())
    out = pd.DataFrame({"odds_ratio": np.exp(lg.params), "low": ci[0], "high": ci[1]})
    return out.drop(index="Intercept")
    # END SOLUTION


# %%
try:
    ors = odds_ratios(lg)
except NotImplementedError:
    ors = U.reference("d2_2", "odds_ratios")
U.keep("d2_2", "odds_ratios", ors)
print(ors.round(3).to_string())
U.check(ors.loc["autopay", "high"] < 0.2, "autopay goes with odds of late payment about a tenth as large")

# %% [markdown]
# **Look at.** "Odds about a tenth as large" is exact and almost useless to Nidal: odds are not how people think, and a tenth of small odds is a small change in probability.

# %% [markdown]
# ## 2 · Describe the three profiles (3')
#
# | Profile | Band | People | Bill (SAR) | Late payments in the past 12 months |
# |---|---|---|---|---|
# | A | social | 7 | 180 | 3 |
# | B | standard | 4 | 120 | 0 |
# | C | villa | 3 | 400 | 1 |
#
# ✏️ **Exercise** · Build `profiles`: a DataFrame with these three rows, index `A`, `B`, `C`, the columns of the formula, `autopay` 0, and `tariff_band` as a category with the levels of `b`.

# %%
def make_profiles(b):
    # BEGIN SOLUTION
    cats = b["tariff_band"].cat.categories
    return pd.DataFrame({"tariff_band": pd.Categorical(["social", "standard", "villa"], categories=cats),
                         "household_size": [7, 4, 3], "bill_sar": [180.0, 120.0, 400.0],
                         "prior_late_12m": [3, 0, 1], "autopay": [0, 0, 0]}, index=["A", "B", "C"])
    # END SOLUTION


# %%
try:
    profiles = make_profiles(b)
except NotImplementedError:
    print("↪ exercise not done yet: using the reference profiles")
    if U.STRICT:
        raise
    cats = b["tariff_band"].cat.categories
    profiles = pd.DataFrame({"tariff_band": pd.Categorical(["social", "standard", "villa"], categories=cats),
                             "household_size": [7, 4, 3], "bill_sar": [180.0, 120.0, 400.0],
                             "prior_late_12m": [3, 0, 1], "autopay": [0, 0, 0]}, index=["A", "B", "C"])
print(profiles.to_string())

# %% [markdown]
# ## 3 · Predicted probabilities with and without autopay (6')
#
# ✏️ **Exercise** · Return a DataFrame with index A, B, C and columns `without` and `with`: the predicted probability with `autopay` 0 and 1.

# %%
def with_without(lg, profiles):
    # BEGIN SOLUTION
    p0 = profiles.assign(autopay=0)
    p1 = profiles.assign(autopay=1)
    return pd.DataFrame({"without": np.asarray(lg.predict(p0)), "with": np.asarray(lg.predict(p1))}, index=profiles.index)
    # END SOLUTION


# %%
try:
    ww = with_without(lg, profiles)
except NotImplementedError:
    ww = U.reference("d2_2", "with_without")
U.keep("d2_2", "with_without", ww)
ww["difference, points"] = 100 * (ww["with"] - ww["without"])
print(ww.round(3).to_string())
U.check(ww["difference, points"].max() - ww["difference, points"].min() > 20, "one coefficient, differences that range over more than 20 points")

# %% [markdown]
# ## 4 · Differences with intervals (6')
#
# `U.contrast` repeats the difference for 1,000 draws of the coefficients. For one profile it gives that profile's difference with an interval.

# %%
rows = []
for k in profiles.index:
    c = U.contrast(lg, profiles.loc[[k]], "autopay", 0, 1, scale="probability")
    rows.append([k, 100 * c.loc["all", "estimate"], 100 * c.loc["all", "low"], 100 * c.loc["all", "high"]])
diffs = pd.DataFrame(rows, columns=["profile", "points", "low", "high"]).set_index("profile")
U.keep("d2_2", "diffs", diffs)
print(diffs.round(1).to_string())
U.check(all(abs(diffs.loc[k, "points"] - ww.loc[k, "difference, points"]) < 1e-6 for k in "ABC"),
        "the function's estimates equal your differences")

# %% [markdown]
# ## 5 · One sentence per profile, without causal words (5')
#
# Households chose autopay; those who choose it may differ in ways the model does not see (income, how they manage bills). Write each sentence as a comparison: "households like A with autopay ... than those without". Avoid the words *reduces*, *cuts*, *causes*, *effect*, *would*.
#
# ✏️ **Exercise** · Return a dictionary `{profile: sentence}` that quotes the difference in points (rounded to a whole number) and its interval.

# %%
def sentences():
    # BEGIN SOLUTION
    out = {}
    for k, who in zip("ABC", ["large social-tariff households with past late payments", "four-person standard households with no late payments", "small villa households with large bills"]):
        r = diffs.loc[k]
        out[k] = (f"Among {who} (profile {k}), bills on autopay were late about {abs(r['points']):.0f} percentage points less often than bills without it "
                  f"(95% interval {abs(r['high']):.0f} to {abs(r['low']):.0f} points), a comparison of households that chose differently.")
    return out
    # END SOLUTION


# %%
try:
    sent = sentences()
except NotImplementedError:
    sent = U.reference("d2_2", "sentences")
U.keep("d2_2", "sentences", sent)
banned = ["reduce", "cuts", "cause", "effect", "would"]
ok = True
for k, s in sent.items():
    print(f"{k}: {s}")
    found = [w for w in banned if w in s.lower()]
    ok &= not found and f"{abs(diffs.loc[k, 'points']):.0f}" in s
    if found:
        print("   causal words:", found)
U.check(ok, "every sentence quotes its difference and uses no causal word")

# %% [markdown]
# ## ✱ Stretch · The average marginal effect of autopay
#
# Average the autopay difference over all 40,000 bills, and over the bills of each band.

# %%
def stretch():
    # BEGIN SOLUTION
    for by in (None, "tariff_band"):
        c = U.contrast(lg, b, "autopay", 0, 1, scale="probability", by=by)
        c[["estimate", "low", "high"]] *= 100
        print(c.round(1).to_string())
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked: the profile differences equal the simulation function's estimates; the intervals come from 1,000 coefficient draws.",
       f"Checked against the generator: autopay is {U.truth()['late_payment']['autopay']} on the log odds scale for every bill; the probability differences vary only because the starting probabilities vary.",
       "Not checked, and not checkable here: whether autopay changes anyone's behaviour. Households chose it.")

# %% [markdown]
# ## Checkpoint
#
# 1. One odds ratio, three different differences in points. Which is "the" effect of autopay?
#    <details><summary>Answer</summary>None alone. On the probability scale the difference depends on the starting probability; report it for stated profiles, or averaged over the bills you describe.</details>
# 2. Why is profile B's difference small?
#    <details><summary>Answer</summary>Its probability without autopay is already low; a large change in odds near zero is a small change in points.</details>
# 3. Nidal wants to promote autopay to profile A households. What does the model tell him?
#    <details><summary>Answer</summary>That A-like households already on autopay are late less often. Whether promoting it would change their payments needs a trial: offer it at random and compare.</details>
#
# ## Carry forward
#
# Lab 3.1 checks this model's bill term with binned residuals.
