# %% [markdown]
# # Lab 3.3 · The share of zeros
#
# Day 3 · Session 3 (Simulation-based checks) · 25 min.
#
# Qusai's renewal plan used a Poisson model of leaks per segment. Basil asks a practical question: how many mains will have no leak next year, and how bad can the worst main get? A model that fits should be able to produce data that look like Sahil's. You simulate many replicate years from the Poisson fit and from a negative binomial fit, and compare the share of zero-leak segments and the largest count with what was observed.
#
# **Use and estimand.** Predictive: the share of segments with no leak in a year, and the largest count on one segment, as the model reproduces them.
#
# **AI policy.** AI-off for the simulation and its reading. The hint-only tutor may help with plotting and the stretch item.
#
# **Reference state.** `data/segments.csv` and `data/leaks.csv` through `U.segment_totals()`; both models are fitted in the setup cell. Nothing from Day 2 is needed.
#
# **Tasks**
# - [ ] 1 · Observed share of zeros and largest count (3')
# - [ ] 2 · Simulate from the Poisson fit (7')
# - [ ] 3 · Simulate from the negative binomial fit (6')
# - [ ] 4 · Where the observed values fall (5')
# - [ ] 5 · The third line of the diagnosis log (4')
# - [ ] ✱ Stretch · Add the uncertainty of the coefficients to the simulation

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
FORMULA = U.qusai_models()["leaks"]["formula"]
po = smf.glm(FORMULA, data=s, family=sm.families.Poisson(), offset=np.log(s["km_years"])).fit()
nb = smf.negativebinomial(FORMULA, data=s, exposure=s["km_years"]).fit(disp=0)
mu_po = np.asarray(po.fittedvalues)
mu_nb = np.asarray(nb.predict(s, exposure=s["km_years"]))
alpha = float(nb.params["alpha"])
R = U.pick(1000, 200)
y = s["leaks"].to_numpy()
print(f"{len(s)} segments; {R} replicate years per model; alpha {alpha:.3f}")

# %% [markdown]
# ## 1 · Observed share of zeros and largest count (3')
#
# Choose statistics that matter to the question, not the ones the model was fitted to match: a Poisson model reproduces the total count by construction, so the total tells you nothing.

# %%
obs = {"zeros": float((y == 0).mean()), "max": int(y.max()), "total": int(y.sum())}
print(obs)
U.keep("d3_3", "observed", obs)

# %% [markdown]
# ## 2 · Simulate from the Poisson fit (7')
#
# One replicate year: draw a count for each segment from Poisson(μ̂), using the fitted means. Repeat `R` times.
#
# ✏️ **Exercise** · Write `replicate_poisson(mu, R, gen)`: return an array of shape `(R, n)` of simulated counts.

# %%
def replicate_poisson(mu, R, gen):
    # BEGIN SOLUTION
    return gen.poisson(mu, size=(R, len(mu)))
    # END SOLUTION


# %%
def stats(sim):
    return {"zeros": (sim == 0).mean(axis=1), "max": sim.max(axis=1), "total": sim.sum(axis=1)}


try:
    sim_po = replicate_poisson(mu_po, R, U.rng(33))
    st_po = stats(sim_po)
except NotImplementedError:
    st_po = U.reference("d3_3", "stats_poisson")
st_po = {k: np.asarray(v) for k, v in st_po.items()}
U.keep("d3_3", "stats_poisson", st_po)
print(f"Poisson replicates: share of zeros {st_po['zeros'].mean():.3f} (range {st_po['zeros'].min():.3f} to {st_po['zeros'].max():.3f}); observed {obs['zeros']:.3f}")
print(f"largest count: median {np.median(st_po['max']):.0f} (range {st_po['max'].min()} to {st_po['max'].max()}); observed {obs['max']}")
print(f"total: median {np.median(st_po['total']):.0f}; observed {obs['total']} (fitted by construction)")

# %% [markdown]
# ## 3 · Simulate from the negative binomial fit (6')
#
# A negative binomial count is a Poisson count whose mean is first multiplied by a gamma draw with mean 1 and variance α: gamma(shape = 1/α, scale = α).
#
# ✏️ **Exercise** · Write `replicate_nb(mu, alpha, R, gen)`: return an array of shape `(R, n)`.

# %%
def replicate_nb(mu, alpha, R, gen):
    # BEGIN SOLUTION
    lam = mu * gen.gamma(1 / alpha, alpha, size=(R, len(mu)))
    return gen.poisson(lam)
    # END SOLUTION


# %%
try:
    sim_nb = replicate_nb(mu_nb, alpha, R, U.rng(34))
    st_nb = stats(sim_nb)
except NotImplementedError:
    st_nb = U.reference("d3_3", "stats_nb")
st_nb = {k: np.asarray(v) for k, v in st_nb.items()}
U.keep("d3_3", "stats_nb", st_nb)
print(f"negative binomial replicates: share of zeros {st_nb['zeros'].mean():.3f} (range {st_nb['zeros'].min():.3f} to {st_nb['zeros'].max():.3f})")
print(f"largest count: median {np.median(st_nb['max']):.0f} (range {st_nb['max'].min()} to {st_nb['max'].max()})")

# %% [markdown]
# ## 4 · Where the observed values fall (5')
#
# The check's p-value is the share of replicates at least as extreme as the data. Values near 0 or 1 say the model cannot produce what you observed.
#
# ✏️ **Exercise** · Return `{model: {"zeros": share of replicates with at least the observed share of zeros, "max": share with a largest count at least the observed one}}` for `"poisson"` and `"nb"`.

# %%
def tail_shares(st_po, st_nb, obs):
    # BEGIN SOLUTION
    return {name: {"zeros": float((st["zeros"] >= obs["zeros"]).mean()), "max": float((st["max"] >= obs["max"]).mean())}
            for name, st in (("poisson", st_po), ("nb", st_nb))}
    # END SOLUTION


# %%
try:
    tails = tail_shares(st_po, st_nb, obs)
except NotImplementedError:
    tails = U.reference("d3_3", "tails")
U.keep("d3_3", "tails", tails)
print(tails)
plt = U.plt()
fig, axes = plt.subplots(1, 2, figsize=(12, 3.8))
for ax, key, label in ((axes[0], "zeros", "share of segments with no leak"), (axes[1], "max", "largest count on one segment")):
    ax.hist(st_po[key], bins=30, alpha=0.6, color="#e4572e", label="Poisson")
    ax.hist(st_nb[key], bins=30, alpha=0.6, color="#3a7ca5", label="negative binomial")
    ax.axvline(obs[key], color="black", linewidth=2)
    ax.set(xlabel=label)
axes[0].legend()
plt.show()
U.check(tails["poisson"]["zeros"] < 0.01 and 0.05 < tails["nb"]["zeros"] < 0.95,
        "the Poisson model cannot produce as many zero-leak segments as Sahil has; the negative binomial can")

# %% [markdown]
# **Look at.** No test statistic was needed beyond counting. The check works for any model you can simulate from, and it answers in Basil's terms: how many mains with no leak, how bad the worst one.

# %% [markdown]
# ## 5 · The third line of the diagnosis log (4')
#
# ✏️ **Exercise** · Return `U.log_entry("overdispersion", evidence, fix)` quoting the observed share of zeros and the Poisson replicates' range.

# %%
def my_entry():
    # BEGIN SOLUTION
    return U.log_entry("overdispersion",
                       f"leaks: {100 * obs['zeros']:.1f}% of segments had no leak; in {R} Poisson replicate years the share ran from {100 * st_po['zeros'].min():.1f}% to {100 * st_po['zeros'].max():.1f}% (Pearson dispersion about 2.3 in lab 2.4)",
                       f"negative binomial with the same offset (alpha {alpha:.2f}): its replicates put the observed share inside their range (tail share {tails['nb']['zeros']:.2f})")
    # END SOLUTION


# %%
try:
    entry = my_entry()
except NotImplementedError:
    entry = U.reference("d3_3", "entry")
U.keep("d3_3", "entry", entry)
U.log_save("3.3", entry)
print(entry)
U.check(f"{100 * obs['zeros']:.1f}" in entry["evidence"], "the evidence quotes the observed share of zeros")

# %% [markdown]
# ## ✱ Stretch · Uncertainty in the coefficients
#
# The replicates above use the fitted coefficients as if they were known. Draw a coefficient vector for each replicate (`U.coef_draws(nb, R, k=...)`), recompute the means and simulate again. Does the conclusion change?

# %%
def stretch():
    # BEGIN SOLUTION
    X = U.design(nb, s)
    B = U.coef_draws(nb, R, k=X.shape[1])
    mu = np.exp(X @ B.T + np.log(s["km_years"].to_numpy())[:, None]).T
    gen = U.rng(35)
    sim = gen.poisson(mu * gen.gamma(1 / alpha, alpha, size=mu.shape))
    z = (sim == 0).mean(axis=1)
    print(f"with coefficient uncertainty: share of zeros {z.mean():.3f} (range {z.min():.3f} to {z.max():.3f}); tail share {(z >= obs['zeros']).mean():.2f}")
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked against the truth: the generator gives each segment a gamma leakiness, so the negative binomial is the right family; the Poisson model was misspecified, not unlucky.",
       "Checked: both models reproduce the total, which is why the total is useless as a check.",
       "Not checked: a zero-inflated model. With the negative binomial reproducing the zeros, the data give no reason for one.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is the total number of leaks a poor statistic for this check?
#    <details><summary>Answer</summary>A Poisson model with an intercept reproduces the observed total by construction, so every replicate is close to it.</details>
# 2. The observed share of zeros falls above every Poisson replicate. What does that say?
#    <details><summary>Answer</summary>The Poisson model cannot produce data like these: there is more variation between segments than it allows.</details>
# 3. Would a model with excess zeros (zero-inflated) be the next step?
#    <details><summary>Answer</summary>Only if the negative binomial also failed to reproduce the zeros. Here it does reproduce them, so the simpler model stands.</details>
#
# ## Carry forward
#
# The third line of the diagnosis log is saved; lab 3.4 assembles the log.
