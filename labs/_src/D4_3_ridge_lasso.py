# %% [markdown]
# # Lab 4.3 · Ridge and lasso
#
# Day 4 · Session 3 (Penalised regression) · 25 min.
#
# For next summer's supply plan, Ghaliya wants to predict each household's August consumption. Nidal from billing has exported 126 candidate columns for 2,000 households: twelve months of past consumption, property details, appliance survey answers, area climate, and some columns nobody asked for. Before any model, you remove the columns a water utility cannot justify using for supply planning. Then you fit ridge and lasso on the remaining 120 predictors, tune their penalties by cross-validation, and check how stable the lasso's choice of predictors is.
#
# **Use and estimand.** Predictive: next August's log consumption of a household, from data held at the end of June. Coefficients here serve the prediction; none is an effect.
#
# **AI policy.** AI-off for the minimisation decision in step 1, the first ridge and lasso fits and the reading in step 5. The hint-only tutor may help with the paths plot, the bootstrap loop and the stretch item; it never writes model code.
#
# **Reference state.** `data/candidates.csv`, loaded fresh, and `data/candidates_key.json`, which states the purpose the data were collected for. Nothing from labs 4.1 or 4.2 is needed.
#
# **Tasks**
# - [ ] 1 · Remove the columns that fail data minimisation (4')
# - [ ] 2 · Ridge path and cross-validated penalty (5')
# - [ ] 3 · Lasso path and cross-validated penalty (5')
# - [ ] 4 · Selection frequency over bootstrap samples (7')
# - [ ] 5 · Which selections to trust (4')
# - [ ] ✱ Stretch · Fit ordinary least squares on half the data after selecting on the other half

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
from sklearn.linear_model import LassoCV, RidgeCV, Lasso, Ridge
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
import sahil as U
warnings.filterwarnings("ignore")
print("mode:", U.MODE)

c = U.candidates()
TARGET = "next_august_log_m3"
print(f"{len(c):,} households; {c.shape[1] - 2} candidate columns")
print("purpose of collection:", U.js("candidates_key.json")["purpose"])
print([col for col in c.columns if not col.startswith(("lag_", "prop_", "use_", "area_", "survey_"))])

# %% [markdown]
# ## 1 · Remove the columns that fail data minimisation (4')
#
# The PDPL asks that personal data be limited to the minimum needed for the purpose for which it was collected (Article 11). A health condition is sensitive data, and income, nationality, employer, phone brand and marital status are neither needed for, nor expected in, a supply forecast.
#
# ✏️ **Exercise** · Return the list of columns to remove before modelling. Decide from the column names and the purpose; do not look at whether they predict.

# %%
def to_remove(c):
    # BEGIN SOLUTION
    return ["member_chronic_condition", "nationality_group", "monthly_income_band", "employer_sector", "phone_brand", "head_marital_status"]
    # END SOLUTION


# %%
try:
    removed = to_remove(c)
except NotImplementedError:
    removed = U.reference("d4_3", "removed")
U.keep("d4_3", "removed", removed)
key = U.js("candidates_key.json")["flagged"]
U.check(set(removed) == set(key), "the six personal columns that supply planning cannot justify are removed, and nothing else")
X = c.drop(columns=["household_key", TARGET] + list(removed))
y = c[TARGET].to_numpy()
names = X.columns
Z = StandardScaler().fit_transform(X)
print(f"{X.shape[1]} predictors remain; the six lag months nearest August are correlated at about 0.9")

# %% [markdown]
# ## 2 · Ridge path and cross-validated penalty (5')
#
# Ridge shrinks every coefficient towards zero, more as the penalty grows; it never sets one exactly to zero. The predictors are standardised so that one penalty treats them alike.
#
# ✏️ **Exercise** · Fit `RidgeCV(alphas=ALPHAS_RIDGE)` on `Z, y` and return it.

# %%
ALPHAS_RIDGE = np.logspace(-2, 4, 40)
CV = KFold(5, shuffle=True, random_state=301)


def ridge_cv(Z, y):
    # BEGIN SOLUTION
    return RidgeCV(alphas=ALPHAS_RIDGE).fit(Z, y)
    # END SOLUTION


# %%
try:
    rid = ridge_cv(Z, y)
    ridge_alpha = float(rid.alpha_)
except NotImplementedError:
    ridge_alpha = U.reference("d4_3", "ridge_alpha")
U.keep("d4_3", "ridge_alpha", ridge_alpha)
paths_r = np.array([Ridge(alpha=a).fit(Z, y).coef_ for a in ALPHAS_RIDGE])
print(f"ridge penalty chosen by cross-validation: {ridge_alpha:.1f}; nonzero coefficients: {int((Ridge(alpha=ridge_alpha).fit(Z, y).coef_ != 0).sum())} of {Z.shape[1]}")

# %% [markdown]
# ## 3 · Lasso path and cross-validated penalty (5')
#
# The lasso's penalty sets coefficients exactly to zero, so it selects. Its cross-validated penalty is chosen for prediction, not for finding the true predictors.
#
# ✏️ **Exercise** · Fit `LassoCV(cv=CV, random_state=301)` on `Z, y` and return it.

# %%
def lasso_cv(Z, y):
    # BEGIN SOLUTION
    return LassoCV(cv=CV, random_state=301).fit(Z, y)
    # END SOLUTION


# %%
try:
    las = lasso_cv(Z, y)
    lasso_alpha = float(las.alpha_)
    selected = list(names[las.coef_ != 0])
except NotImplementedError:
    lasso_alpha = U.reference("d4_3", "lasso_alpha")
    selected = U.reference("d4_3", "selected")
U.keep("d4_3", "lasso_alpha", lasso_alpha)
U.keep("d4_3", "selected", selected)
print(f"lasso penalty: {lasso_alpha:.5f}; {len(selected)} predictors selected:")
print(selected)
plt = U.plt()
alphas_l = np.logspace(np.log10(lasso_alpha) - 1.5, np.log10(lasso_alpha) + 1.5, 30)
paths_l = np.array([Lasso(alpha=a).fit(Z, y).coef_ for a in alphas_l])
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(ALPHAS_RIDGE, paths_r, color="#3a7ca5", linewidth=0.6)
axes[0].axvline(ridge_alpha, color="black", linestyle="--")
axes[0].set(xscale="log", title="ridge", xlabel="penalty", ylabel="standardised coefficient")
axes[1].plot(alphas_l, paths_l, color="#e4572e", linewidth=0.6)
axes[1].axvline(lasso_alpha, color="black", linestyle="--")
axes[1].set(xscale="log", title="lasso", xlabel="penalty")
plt.show()

# %% [markdown]
# ## 4 · Selection frequency over bootstrap samples (7')
#
# Would the lasso pick the same predictors from a slightly different sample of households? Resample the households, refit the lasso at the cross-validated penalty, and count how often each predictor is selected.
#
# ✏️ **Exercise** · Return a Series indexed by predictor name: the share of `B` bootstrap samples in which the predictor's coefficient is nonzero.

# %%
B = U.pick(100, 20)


def selection_frequency(Z, y, alpha, B, gen):
    # BEGIN SOLUTION
    count = np.zeros(Z.shape[1])
    for _ in range(B):
        i = gen.integers(0, len(y), len(y))
        count += Lasso(alpha=alpha).fit(Z[i], y[i]).coef_ != 0
    return pd.Series(count / B, index=names)
    # END SOLUTION


# %%
try:
    freq = selection_frequency(Z, y, lasso_alpha, B, U.rng(43))
except NotImplementedError:
    freq = U.reference("d4_3", "frequency")
freq = pd.Series(freq).sort_values(ascending=False)
U.keep("d4_3", "frequency", {k: float(v) for k, v in freq.items()})
print(f"selected in every one of {B} samples: {list(freq[freq >= 0.999].index)}")
print(f"selected in 10% to 90% of samples: {int(((freq > 0.1) & (freq < 0.9)).sum())} predictors")
fig, ax = plt.subplots(figsize=(12, 3.5))
ax.bar(range(len(freq)), freq.to_numpy(), color=["#3a7ca5" if f >= 0.999 else "#e4572e" for f in freq])
ax.set(xlabel="predictors, most often selected first", ylabel="share of bootstrap samples")
plt.show()

# %% [markdown]
# ## 5 · Which selections to trust (4')
#
# ✏️ **Exercise** · Return the list of predictors you would report to Ghaliya as stable: those selected in every bootstrap sample. Then complete `write_reading()` to say, in at most 60 words, why the others should not be reported as "the drivers of August consumption". Use the word "unstable".

# %%
def stable(freq):
    # BEGIN SOLUTION
    return sorted(freq[freq >= 0.999].index)
    # END SOLUTION


def write_reading():
    # BEGIN SOLUTION
    return ("The other selected predictors are unstable: each enters in some bootstrap samples and not in others, because many are correlated "
               "and the lasso picks one of a group almost at random. They help the prediction a little, but they are not evidence that a "
               "predictor matters.")
    # END SOLUTION

# %%
try:
    keep = stable(freq)
except NotImplementedError:
    keep = U.reference("d4_3", "stable")
try:
    READING = write_reading()
except NotImplementedError:
    READING = U.reference("d4_3", "reading")
U.keep("d4_3", "stable", keep)
U.keep("d4_3", "reading", READING)
print("stable:", keep)
print(READING)
U.text_check(READING, {}, ["unstable"], max_words=60)
U.check(len(keep) <= len(selected), "the stable set is a subset of what one lasso fit selects")

# %% [markdown]
# **Look at.** The six columns of step 1 were never offered to the model, so the question "would they have helped?" never arises. Minimisation comes before modelling.

# %% [markdown]
# ## ✱ Stretch · Select on one half, estimate on the other
#
# Coefficients refitted by least squares on the same data that chose them are too large in magnitude and their intervals too narrow. Split the households in two, select with the lasso on one half, and fit ordinary least squares on the other half with only the stable predictors.

# %%
def stretch():
    # BEGIN SOLUTION
    import statsmodels.api as sm
    gen = U.rng(44)
    half = gen.permutation(len(y)) < len(y) // 2
    l = LassoCV(cv=CV, random_state=301).fit(Z[half], y[half])
    chosen = list(names[l.coef_ != 0])
    ols = sm.OLS(y[~half], sm.add_constant(X.loc[~half, chosen])).fit()
    print(f"{len(chosen)} predictors chosen on the first half; on the second half, intervals that exclude zero:")
    ci = ols.conf_int().drop(index="const")
    print(sorted(ci.index[(ci[0] > 0) | (ci[1] < 0)]))
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
true_terms = U.truth()["candidates"]["true_terms"]
U.note(f"Checked against the truth: the generator uses {len(true_terms)} predictors; the stable set has {len(keep)}, and {len(set(keep) & set(true_terms))} of them are true ones.",
       f"Checked: one lasso fit selected {len(selected)}, so about {len(selected) - len(set(selected) & set(true_terms))} of its choices were noise.",
       "Not checked: the prediction error on households of another year; cross-validation here mixes households of one year.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why remove the six columns before checking whether they predict?
#    <details><summary>Answer</summary>Minimisation is decided by the purpose, not by predictive power; a column that cannot be justified for supply planning should not be processed for it at all.</details>
# 2. The lasso selected lag_m10 in most samples but not all. Should Ghaliya hear that October's consumption drives August's?
#    <details><summary>Answer</summary>No. The lag months are correlated at about 0.9; the lasso's choice among them is unstable, and the coefficients serve prediction, not explanation.</details>
# 3. Ridge kept all 120 predictors. Is that a problem for prediction?
#    <details><summary>Answer</summary>Not necessarily: ridge often predicts as well as the lasso with correlated predictors; it simply does not select.</details>
#
# ## Carry forward
#
# The stable set and the minimisation step are the evidence of LO5.
