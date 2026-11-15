# %% [markdown]
# # Lab 3.4 · Separation and robust errors
#
# Day 3 · Session 4 (Separation and error structure) · 25 min.
#
# Two of Qusai's models remain. His "improved" late-payment model was reported as fitting almost perfectly; one of its coefficients is 26 with a standard error in the thousands. His consumption model for the supply plan uses classical standard errors on a scale where the spread grows with the bill. You repair both, then assemble the diagnosis log of the day with its corrected models.
#
# **Use and estimand.** Predictive (late payment) and descriptive (consumption in cubic metres). The question here is whether each model's form and standard errors can be trusted.
#
# **AI policy.** AI-off for the diagnosis and the repair. The hint-only tutor may help with the log table and the stretch item.
#
# **Reference state.** `data/bills.csv` and `data/qusai/models.json` (`late_v2` and `consumption`). The log assembled in step 5 takes your entries from labs 3.1 to 3.3 when they ran on this computer, and the reference entries otherwise.
#
# **Tasks**
# - [ ] 1 · The separated fit and its symptoms (5')
# - [ ] 2 · The cross-table that explains it, and the repair (5')
# - [ ] 3 · The funnel in the consumption model (5')
# - [ ] 4 · Classical against robust standard errors (5')
# - [ ] 5 · The full diagnosis log and the corrected models (5')
# - [ ] ✱ Stretch · Fit the separated model with a small penalty and compare

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
print("mode:", U.MODE)

b = U.bills()
models = U.qusai_models()
print(models["late_v2"]["formula"])
print(models["consumption"]["formula"])

# %% [markdown]
# ## 1 · The separated fit and its symptoms (5')

# %%
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    v2 = smf.logit(models["late_v2"]["formula"], data=b).fit(disp=0, maxiter=200)
print("warnings:", sorted({type(w.message).__name__ for w in caught}) or "none")
print(pd.DataFrame({"coef": v2.params, "se": v2.bse}).round(3).to_string())

# %% [markdown]
# ✏️ **Exercise** · Return, as a list, the names of the terms whose standard error is more than 100 times the median standard error of the model (`v2.bse`).

# %%
def suspicious_terms(fit):
    # BEGIN SOLUTION
    se = fit.bse
    return [t for t in se.index if se[t] > 100 * se.median()]
    # END SOLUTION


# %%
try:
    sus = suspicious_terms(v2)
except NotImplementedError:
    sus = U.reference("d3_4", "suspicious")
U.keep("d3_4", "suspicious", sus)
sep = {"coef": float(v2.params["notice_sent"]), "se": float(v2.bse["notice_sent"])}
U.keep("d3_4", "separation", sep)
print(sus, sep)
U.check(sus == ["notice_sent"], "one term, notice_sent, has a huge coefficient and a standard error in the thousands")

# %% [markdown]
# ## 2 · The cross-table that explains it, and the repair (5')
#
# **Separation**: a predictor, or a combination, splits the outcome perfectly for some rows. The likelihood keeps rising as the coefficient grows, so the estimate runs off towards infinity and its standard error with it.

# %%
xt = pd.crosstab(b["notice_sent"], b["late"])
print(xt.to_string())

# %% [markdown]
# Every bill with a notice was late: the notice is sent **after** a bill is more than 30 days late. It is a consequence of the outcome, so it can never be a predictor of it, whatever a penalty does to its coefficient.
#
# ✏️ **Exercise** · Fit `late_v2` without `notice_sent` and return the fit.

# %%
def repair_v2(b):
    # BEGIN SOLUTION
    return smf.logit(models["late_v2"]["formula"].replace(" + notice_sent", ""), data=b).fit(disp=0)
    # END SOLUTION


# %%
try:
    v2r = repair_v2(b)
except NotImplementedError:
    print("↪ exercise not done yet: fitting the reference model so the cells below run")
    if U.STRICT:
        raise
    v2r = smf.logit(models["late_v2"]["formula"].replace(" + notice_sent", ""), data=b).fit(disp=0)
print(f"largest standard error now {v2r.bse.max():.3f}; AIC {v2r.aic:.0f} (with the notice {v2.aic:.0f}, which looked better only because it used the answer)")
U.check(xt.loc[1, 0] == 0 and v2r.bse.max() < 1, "no notice bill was paid on time; without the flag every standard error is ordinary")

# %% [markdown]
# ## 3 · The funnel in the consumption model (5')
#
# Qusai modelled cubic metres directly. Households that use more vary more, so the spread of the residuals grows with the fitted value.
#
# ✏️ **Exercise** · Fit `models["consumption"]["formula"]` by ordinary least squares and return the ratio of the residual standard deviation in the top decile of fitted values to that in the bottom decile.

# %%
cons = smf.ols(models["consumption"]["formula"], data=b).fit()


def funnel_ratio(fit):
    # BEGIN SOLUTION
    d = pd.DataFrame({"f": np.asarray(fit.fittedvalues), "r": np.asarray(fit.resid)})
    d["dec"] = pd.qcut(d["f"].rank(method="first"), 10, labels=False)
    sd = d.groupby("dec")["r"].std()
    return float(sd.iloc[-1] / sd.iloc[0])
    # END SOLUTION


# %%
try:
    funnel = funnel_ratio(cons)
except NotImplementedError:
    funnel = U.reference("d3_4", "funnel")
U.keep("d3_4", "funnel", funnel)
plt = U.plt()
fig, ax = plt.subplots()
ax.scatter(cons.fittedvalues, cons.resid, s=2, alpha=0.08, color="#3a7ca5")
ax.axhline(0, color="black", linewidth=1)
ax.set(xlabel="fitted m³ a month", ylabel="residual, m³", title="The spread grows with the fitted value")
plt.show()
print(f"residual spread in the top decile of fitted values is {funnel:.1f} times that of the bottom decile")
U.check(funnel > 2.5, "a clear funnel: the classical standard errors assume one spread for all bills")

# %% [markdown]
# ## 4 · Classical against robust standard errors (5')
#
# Heteroskedasticity-consistent (HC3) standard errors estimate each coefficient's variance from the residuals as they are, without assuming one spread.
#
# ✏️ **Exercise** · Return a DataFrame for the terms `household_size`, `tariff_band[T.social]` and `tariff_band[T.villa]` with columns `estimate`, `se_classical`, `se_hc3` and `ratio`, using `cons.get_robustcov_results("HC3")` or a refit with `cov_type="HC3"`.

# %%
TERMS = ["household_size", "tariff_band[T.social]", "tariff_band[T.villa]"]


def compare_se(cons):
    # BEGIN SOLUTION
    hc = smf.ols(models["consumption"]["formula"], data=b).fit(cov_type="HC3")
    out = pd.DataFrame({"estimate": cons.params[TERMS], "se_classical": cons.bse[TERMS], "se_hc3": hc.bse[TERMS]})
    out["ratio"] = out["se_hc3"] / out["se_classical"]
    return out
    # END SOLUTION


# %%
try:
    se_tab = compare_se(cons)
except NotImplementedError:
    se_tab = U.reference("d3_4", "se_table")
U.keep("d3_4", "se_table", se_tab)
print(se_tab.round(4).to_string())
U.check(se_tab["ratio"].max() > 1.25, "the robust standard errors are up to a third or more larger")

# %% [markdown]
# **Look at.** The estimates do not change; only their uncertainty does. The log model of Day 1 is the other repair: on the log scale the spread is nearly constant, and effects are read back in cubic metres.

# %% [markdown]
# ## 5 · The full diagnosis log and the corrected models (5')
#
# ✏️ **Exercise** · Write the two entries of this lab with `U.log_entry`, one for `"separation"` and one for `"non-constant variance"`, and return them as a list.

# %%
def my_entries():
    # BEGIN SOLUTION
    return [U.log_entry("separation",
                        f"late_v2: notice_sent has coefficient {sep['coef']:.0f} with standard error {sep['se']:.0f}; all {xt.loc[1, 1]} bills with a notice were late",
                        "remove notice_sent: it is sent after a bill is 30 days late, a consequence of the outcome; every standard error is then ordinary"),
            U.log_entry("non-constant variance",
                        f"consumption: residual spread {funnel:.1f} times larger in the top decile of fitted m³ than in the bottom one",
                        f"HC3 standard errors (up to {se_tab['ratio'].max():.2f} times the classical ones), or model log consumption and read effects in m³ as on Day 1")]
    # END SOLUTION


# %%
try:
    mine = my_entries()
except NotImplementedError:
    mine = U.reference("d3_4", "entries")
U.keep("d3_4", "entries", mine)
U.log_save("3.4a", mine[0])
U.log_save("3.4b", mine[1])
saved = U.log_read()
log = []
for lab, ref in (("3.1", "d3_1"), ("3.2", "d3_2"), ("3.3", "d3_3")):
    if lab in saved:
        log.append({**saved[lab], "source": f"your lab {lab}"})
    else:
        log.append({**U.stored(ref, "entry"), "source": f"reference of lab {lab}"})
log += [{**mine[0], "source": "this lab"}, {**mine[1], "source": "this lab"}]
for i, e in enumerate(log, 1):
    print(f"{i}. {e['problem'].upper()} ({e['source']})\n   evidence: {e['evidence']}\n   fix: {e['fix']}")
corrected = {
    "late": "late ~ np.log(bill_sar) + autopay + tariff_band + prior_late_12m + household_size (logistic; no notice_sent)",
    "district_leaks": "the same formula on kilometres recomputed from the segments; reported with and without D30",
    "leaks": "negative binomial, leaks ~ material + age_years + pressure_bar, exposure km_years",
    "consumption": "log_m3 ~ household_size + tariff_band + bs(temperature_c, df=5), effects in m³ by simulation; or the m³ model with HC3 errors",
}
print("\nCORRECTED MODELS")
for k, v in corrected.items():
    print(f" · {k}: {v}")
U.keep("d3_4", "log", log)
U.check(len({e["problem"] for e in log}) >= 4, "the diagnosis log names at least four different problems, with evidence and a fix for each")

# %% [markdown]
# ## ✱ Stretch · A small penalty
#
# Fit `late_v2` with the notice flag and an L2 penalty (`smf.logit(...).fit_regularized(method="l1", alpha=...)` is L1; use `sklearn.linear_model.LogisticRegression(C=1.0)` on the model matrix for L2). The coefficient becomes finite. Does that make the notice a valid predictor?

# %%
def stretch():
    # BEGIN SOLUTION
    from sklearn.linear_model import LogisticRegression
    X = pd.get_dummies(b[["autopay", "tariff_band", "prior_late_12m", "household_size", "notice_sent"]], drop_first=True).astype(float)
    X["log_bill"] = np.log(b["bill_sar"])
    m = LogisticRegression(C=1.0, max_iter=2000).fit(X, b["late"])
    print(f"penalised coefficient of notice_sent: {dict(zip(X.columns, m.coef_[0]))['notice_sent']:.2f}; finite, and still a consequence of the outcome")
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked against the truth: the generator sends a notice only for late bills, and draws consumption with a constant spread on the log scale, which is a funnel in m³.",
       f"Checked: the log names {len({e['problem'] for e in log})} problems; LO3 asks for at least four, with the corrected models.",
       "Not checked: errors that are correlated within districts; Day 4 takes them up.")

# %% [markdown]
# ## Checkpoint
#
# 1. A coefficient of 26 with a standard error of 4,000. What do you look at first?
#    <details><summary>Answer</summary>The cross-table of that predictor with the outcome: an empty cell means separation.</details>
# 2. A penalty would make the notice's coefficient finite. Why is removing it still the repair?
#    <details><summary>Answer</summary>The notice is sent after the outcome; no estimation method turns a consequence into a predictor.</details>
# 3. HC3 widened the household-size standard error. Did the estimate change?
#    <details><summary>Answer</summary>No. Robust standard errors change the uncertainty, not the coefficients.</details>
#
# ## Carry forward
#
# The diagnosis log and the corrected models are the evidence of LO3. The capstone report has a diagnostics section in the same form.
