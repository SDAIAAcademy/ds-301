# %% [markdown]
# # Lab 1.1 · Three uses of a regression
#
# Day 1 · Session 1 (A regression answers a question) · 25 min.
#
# Ghaliya Al-Muhairi, head of network and demand planning at Sahil Water, keeps a folder of regression results that people send her. Before you fit anything this week, you sort five of them: does each claim describe, predict or explain a cause, and does the evidence it names support that use? Then you write the estimand of two of them: the quantity the claim is about, before any model.
#
# **AI policy.** AI-off: this lab is a first interpretation, so no assistant. The stretch item may use the hint-only tutor.
#
# **Reference state.** `data/claims.json`, five short claims written for this course in the style of published ones (a newspaper, an annual report, a dashboard, a research abstract, a brochure). Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Read the five claims and the evidence each names (4')
# - [ ] 2 · Label the use each claim states (6')
# - [ ] 3 · Decide whether the evidence supports it, with a reason (7')
# - [ ] 4 · Write the estimand of claims 1 and 3 (5')
# - [ ] 5 · Mark the sheet against the key (3')
# - [ ] ✱ Stretch · Rewrite claim 1 so that the evidence supports it

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

import sahil as U
print("mode:", U.MODE)

# %% [markdown]
# ## 1 · Read the five claims and the evidence each names (4')
#
# Read each claim twice: once for what it **says** (its verbs: "is", "predicts", "makes", "cuts") and once for what it **rests on** (the evidence line).

# %%
claims = U.js("claims.json")
for c in claims:
    print(f"[{c['id']}] {c['source']}\n    \"{c['text']}\"\n    evidence: {c['evidence']}\n")

# %% [markdown]
# ## 2 · Label the use each claim states (6')
#
# Three uses:
#
# | Use | The claim says | What it needs |
# |---|---|---|
# | **descriptive** | how a quantity differs between groups, or moves with another, in a stated population | a fair sample of that population |
# | **predictive** | what an outcome will be for new cases | checked predictions on cases the model did not see |
# | **causal** | what would change if someone acted (a tariff, a letter, a reminder) | a design that makes the compared groups alike apart from the action |
#
# Label the use the claim **states**, not the one its evidence could support. A claim that predicts and then promises an effect states a causal use.
#
# ✏️ **Exercise** · Fill `stated_use` with `"descriptive"`, `"predictive"` or `"causal"` for each claim id.

# %%
def stated_use():
    # BEGIN SOLUTION
    return {1: "causal", 2: "predictive", 3: "descriptive", 4: "causal", 5: "causal"}
    # END SOLUTION


# %%
try:
    uses = stated_use()
except NotImplementedError:
    uses = U.reference("d1_1", "uses")
uses = {int(k): v for k, v in uses.items()}
U.keep("d1_1", "uses", uses)
U.check(set(uses) == {1, 2, 3, 4, 5} and set(uses.values()) <= {"descriptive", "predictive", "causal"},
        "one of the three uses for each of the five claims")

# %% [markdown]
# ## 3 · Decide whether the evidence supports it, with a reason (7')
#
# For each claim: `True` if the evidence named is the kind that use needs, `False` if not, and a reason of at least six words that names what is missing or what makes it enough.
#
# ✏️ **Exercise** · Fill `supported()` with `{id: (True or False, "reason")}`.

# %%
def supported():
    # BEGIN SOLUTION
    return {
        1: (False, "different households differ in income, size and housing, not only in tariff"),
        2: (True, "the forecasts were made before the summer and checked against it"),
        3: (True, "it only reports a difference between districts in one year"),
        4: (True, "the letter was assigned at random, so the groups are otherwise alike"),
        5: (False, "no reminders were sent, so nothing measured what reminders do"),
    }
    # END SOLUTION


# %%
try:
    sup = supported()
except NotImplementedError:
    sup = U.reference("d1_1", "supported")
sup = {int(k): tuple(v) for k, v in sup.items()}
U.keep("d1_1", "supported", sup)
U.check(all(len(str(r).split()) >= 6 for _, r in sup.values()), "a reason of six words or more for every claim")

# %% [markdown]
# **Look at.** Claim 1 is the one this course returns to. A coefficient for the social tariff in a model of consumption compares households that differ in many ways. Written as "the social tariff makes families save water", it becomes a claim about poorer households that the data cannot carry. Every report in this course keeps the two apart.

# %% [markdown]
# ## 4 · Write the estimand of claims 1 and 3 (5')
#
# An **estimand** is the quantity a claim is about, stated before any model: the population, the outcome with its unit, and the comparison. A model is only a way to estimate it.
#
# ✏️ **Exercise** · For claims 1 and 3, fill `population`, `outcome` and `comparison` (each a phrase of at least four words). For claim 1, write the estimand of what the evidence **can** support.

# %%
def estimands():
    # BEGIN SOLUTION
    return {
        1: {"population": "the 40,000 households billed that month",
            "outcome": "consumption in cubic metres in one month",
            "comparison": "mean on the social tariff minus mean on the other tariffs"},
        3: {"population": "all districts of the network in 2026",
            "outcome": "leaks reported per kilometre of main",
            "comparison": "rate in programme districts divided by rate in the others"},
    }
    # END SOLUTION


# %%
try:
    est = estimands()
except NotImplementedError:
    est = U.reference("d1_1", "estimands")
est = {int(k): v for k, v in est.items()}
U.keep("d1_1", "estimands", est)
for i in (1, 3):
    for part in ("population", "outcome", "comparison"):
        print(f"claim {i} · {part}: {est[i][part]}")
U.check(all(len(est[i][p].split()) >= 4 for i in (1, 3) for p in ("population", "outcome", "comparison")),
        "population, outcome and comparison written for both claims")

# %% [markdown]
# ## 5 · Mark the sheet against the key (3')

# %%
sheet = {i: (uses[i], sup[i][0], sup[i][1]) for i in uses}
score = U.mark_claims(sheet)
U.keep("d1_1", "score", score)
U.check(score >= 4, "at least four of five claims labelled and judged as the key does")

# %% [markdown]
# ## ✱ Stretch · Rewrite claim 1
#
# Rewrite claim 1 in one or two sentences that say only what the evidence supports, and name one thing that would be needed for the causal version.

# %%
def rewrite_claim_1():
    # BEGIN SOLUTION
    return ("In one month of bills, households on the social tariff used 12% less water than households on other tariffs. "
            "This compares different households; whether the tariff itself changes use would need, for example, the same households observed before and after they joined it.")
    # END SOLUTION


try:
    print(rewrite_claim_1())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked: your labels and judgements against the key of data/claims_key.json.",
       "Not checked: the estimands are free text; compare them with a neighbour's and with the trainer's.",
       "The five claims are written for this course; none is quoted from a real publication.")

# %% [markdown]
# ## Checkpoint
#
# 1. A model of late payment is fitted on last year's bills and scores well on this year's. Which use does that evidence support?
#    <details><summary>Answer</summary>Predictive: the model was checked on cases it did not see. It says nothing about what a reminder would change.</details>
# 2. Why write the estimand before choosing a model?
#    <details><summary>Answer</summary>Because the estimand decides what must be in the model, which rows count and what the output must be turned into. A model chosen first answers whatever question its coefficients happen to answer.</details>
# 3. Billing data were collected to bill. What is a planning model built on them, in the words of the national rules?
#    <details><summary>Answer</summary>A secondary use of data: a use for a purpose other than the one of collection. Its purpose is stated, and only the data it needs are used (Day 4, lab 4.3).</details>
#
# ## Carry forward
#
# Every lab of the course starts with one line that states the use and the estimand. The capstone README does too.
