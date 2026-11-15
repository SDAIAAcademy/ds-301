# %% [markdown]
# # Lab 4.4 · A one-page model report
#
# Day 4 · Session 4 (Reporting a model) · 25 min.
#
# Ghaliya takes the consumption model to the planning committee next week. She does not want coefficients on a log scale; she wants a page that says what was asked, what was fitted, how it was checked, what the numbers are in cubic metres and percentages, and what they do not mean. You draft that page from the stored results of this course, check it for numbers, intervals and limits, and then choose your capstone brief and write its use and estimand.
#
# **Use and estimand.** Descriptive: monthly household consumption at Sahil by household size, band and temperature, and the difference between programme and other districts, at equal household size, band and temperature.
#
# **AI policy.** AI-off for the report text and the capstone choice: the wording is the skill. The hint-only tutor may comment on a draft you wrote, and help with the stretch item.
#
# **Reference state.** The stored results of labs 1.3, 1.4, 3.4 and 4.2 in `data/reference/`, the same on every computer; nothing has to be refitted. The capstone briefs are in `capstone/briefs.json`.
#
# **Tasks**
# - [ ] 1 · The question, the use and the estimand (5')
# - [ ] 2 · Model, family and diagnostics (5')
# - [ ] 3 · Effects with intervals in the reader's units (6')
# - [ ] 4 · Limits, and what the coefficients are not (4')
# - [ ] 5 · Choose a capstone brief and write its estimand (5')
# - [ ] ✱ Stretch · Ask a neighbour to find one causal word in your report

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

import json
import numpy as np
import pandas as pd
import sahil as U
print("mode:", U.MODE)

ame = U.stored("d1_4", "ame_table", "full")        # m³ a month per extra household member, by band
temp = U.stored("d1_3", "band_at", "full")         # mean m³ a month at 20, 30 and 40 °C
three = U.stored("d4_2", "three_way", "full")      # the programme: naive, clustered, mixed
funnel = U.stored("d3_4", "funnel", "full")        # residual spread, top decile over bottom
print(ame.round(2).to_string(), "\n")
print(temp.to_string(), "\n")
print(three.round(4).to_string())

# %% [markdown]
# ## 1 · The question, the use and the estimand (5')
#
# ✏️ **Exercise** · Complete `write_head()` so that it returns a dict of three short entries: `question` (Ghaliya's question in her words), `use` (one of `"descriptive"`, `"predictive"`, `"causal"`) and `estimand` (the quantity, the population and the comparison).

# %%
def write_head():
    # BEGIN SOLUTION
    return {"question": "How does a household's monthly consumption differ with its size, band and the month's temperature, and do programme districts use less?",
            "use": "descriptive",
            "estimand": "mean m³ a month per extra household member in each band, mean m³ at 20, 30 and 40 °C, and the percentage difference between "
                        "programme and other districts at equal size, band and temperature, for Sahil's billed households in 2026"}
    # END SOLUTION

# %%
try:
    HEAD = write_head()
except NotImplementedError:
    HEAD = U.reference("d4_4", "head")
U.keep("d4_4", "head", HEAD)
U.check(HEAD["use"] == "descriptive", "the use is descriptive: districts chose the programme and households their size, so nothing here is an effect of an action")

# %% [markdown]
# ## 2 · Model, family and diagnostics (5')
#
# ✏️ **Exercise** · Complete `write_model()` to return at most 70 words: the outcome and its scale, the terms, how districts are handled, and the diagnostics that were run. Use the words "log", "spline", "district" and "residual".

# %%
def write_model():
    # BEGIN SOLUTION
    return ("Linear model of log monthly consumption with band, household size and their interaction, a spline in temperature; "
             "the programme flag added with a random intercept per district. Checked by residual plots against each predictor (the straight temperature term failed, the spline passed), "
             "a funnel on the m³ scale that the log removes, and fake data with known effects that the model recovered.")
    # END SOLUTION

# %%
try:
    MODEL = write_model()
except NotImplementedError:
    MODEL = U.reference("d4_4", "model")
U.keep("d4_4", "model", MODEL)
print(MODEL)
U.text_check(MODEL, {}, ["log", "spline", "district", "residual"], max_words=70)

# %% [markdown]
# ## 3 · Effects with intervals in the reader's units (6')
#
# ✏️ **Exercise** · Complete `write_effects()` to return at most 100 words: the m³ per extra household member for each band, the consumption at 30 and 40 °C, and the programme difference as a percentage with the mixed model's interval. Every estimate gets its interval, with one decimal as printed below.

# %%
mix = three.loc["mixed"]
print({band: f"{r.estimate:.1f} m³ ({r.low:.1f} to {r.high:.1f})" for band, r in ame.iterrows()})
print({t: f"{r.estimate:.1f} m³ ({r.low:.1f} to {r.high:.1f})" for t, r in temp.iterrows()})
print(f"programme: {100 * (np.exp(mix.estimate) - 1):.1f}% ({mix.low_pct:.1f}% to {mix.high_pct:.1f}%)")

# %%
def write_effects():
    # BEGIN SOLUTION
    return (f"Each extra household member goes with {ame.loc['social', 'estimate']:.1f} m³ a month more on the social tariff "
               f"({ame.loc['social', 'low']:.1f} to {ame.loc['social', 'high']:.1f}), {ame.loc['standard', 'estimate']:.1f} on the standard "
               f"({ame.loc['standard', 'low']:.1f} to {ame.loc['standard', 'high']:.1f}) and {ame.loc['villa', 'estimate']:.1f} for villas "
               f"({ame.loc['villa', 'low']:.1f} to {ame.loc['villa', 'high']:.1f}). A typical household uses {temp.loc[30, 'estimate']:.1f} m³ "
               f"in a 30 °C month and {temp.loc[40, 'estimate']:.1f} m³ ({temp.loc[40, 'low']:.1f} to {temp.loc[40, 'high']:.1f}) in a 40 °C month. "
               f"Households in programme districts used {abs(100 * (np.exp(mix.estimate) - 1)):.1f}% less "
               f"({abs(mix.high_pct):.1f}% to {abs(mix.low_pct):.1f}% less).")
    # END SOLUTION

# %%
try:
    EFFECTS = write_effects()
except NotImplementedError:
    EFFECTS = U.reference("d4_4", "effects")
U.keep("d4_4", "effects", EFFECTS)
print(EFFECTS)
U.text_check(EFFECTS, {"villa effect": f"{ame.loc['villa', 'estimate']:.1f}",
                       "villa interval": f"{ame.loc['villa', 'low']:.1f} to {ame.loc['villa', 'high']:.1f}",
                       "40 °C": f"{temp.loc[40, 'estimate']:.1f}",
                       "programme upper": f"{abs(mix.low_pct):.1f}%"},
             ["m³"], max_words=100)

# %% [markdown]
# ## 4 · Limits, and what the coefficients are not (4')
#
# ✏️ **Exercise** · Complete `write_limits()` to return at most 70 words: what the programme comparison is not, what the uncertainty does not cover, and where the model should not be used. Use the words "comparison" and "district".

# %%
def write_limits():
    # BEGIN SOLUTION
    return ("The programme figure is a comparison of districts that chose to join, not the saving from joining. "
              "Intervals cover sampling and district variation in 2026, not a change in tariffs or habits. "
              "Temperatures above 43 °C are outside the data, and a new district, like D30, has no history of its own.")
    # END SOLUTION

# %%
try:
    LIMITS = write_limits()
except NotImplementedError:
    LIMITS = U.reference("d4_4", "limits")
U.keep("d4_4", "limits", LIMITS)
print(LIMITS)
U.text_check(LIMITS, {}, ["comparison", "district"], max_words=70)

# %% [markdown]
# **The page.** Your four parts make a report of well under a page. Read it as Ghaliya would.

# %%
page = (f"## Household consumption at Sahil Water, 2026\n\n**Question.** {HEAD['question']}\n\n**Use.** {HEAD['use'].capitalize()}. "
        f"**Estimand.** {HEAD['estimand']}.\n\n**Model and checks.** {MODEL}\n\n**Effects.** {EFFECTS}\n\n**Limits.** {LIMITS}\n")
print(page)
print(f"{len(page.split())} words")
U.check(len(page.split()) <= 450, "the report fits on one page")

# %% [markdown]
# ## 5 · Choose a capstone brief and write its estimand (5')
#
# The three briefs are below. Each has a planted problem your diagnostics should find.
#
# ✏️ **Exercise** · Complete `write_choice()` to return a dict with `brief` (`"C1"`, `"C2"` or `"C3"`), `use` and `estimand` (at least ten words). A causal use is defensible only where the data come from a randomised comparison.

# %%
briefs = json.loads((U.LABS / "capstone" / "briefs.json").read_text(encoding="utf-8"))
for br in briefs:
    print(f"{br['id']} · {br['title']}: {br['brief']}\n   data: capstone/data/{br['file']}; {br['family_hint']}; {br['grouping']}\n")

# %%
def write_choice():
    # BEGIN SOLUTION
    return {"brief": "C2", "use": "causal",
              "estimand": "the difference in the share of households taking the kit between a text message and a letter, overall and within each tariff band, for the 6,000 households offered it"}
    # END SOLUTION

# %%
try:
    CHOICE = write_choice()
except NotImplementedError:
    CHOICE = U.reference("d4_4", "choice")
U.keep("d4_4", "choice", CHOICE)
U.ARTIFACTS.mkdir(exist_ok=True)
(U.ARTIFACTS / "capstone_choice.json").write_text(json.dumps(CHOICE, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(CHOICE)
ok = CHOICE["brief"] in {br["id"] for br in briefs} and CHOICE["use"] in {"descriptive", "predictive", "causal"} and len(CHOICE["estimand"].split()) >= 10
U.check(ok, "a brief, a use and an estimand of at least ten words")
U.check(CHOICE["use"] != "causal" or CHOICE["brief"] == "C2", "a causal use is chosen only for the brief with a randomised channel")

# %% [markdown]
# ## ✱ Stretch · One causal word
#
# Ask a neighbour to read your page and mark any word that claims an effect the data cannot support: "reduces", "drives", "because of", "the effect of", "leads to". The function below finds the common ones; a neighbour finds the rest.

# %%
def stretch():
    # BEGIN SOLUTION
    words = ["reduces", "reduce", "drives", "because of", "effect of", "leads to", "causes", "impact", "saves", "saving from"]
    low = page.lower()
    found = [w for w in words if w in low]
    print("causal words found:", found or "none")
    print("Each must be either removed or stated as what it is not, as in 'not the saving from joining'.")
    # END SOLUTION


try:
    stretch()
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked: every number in the report comes from a stored, verified result of an earlier lab; the checks above confirm each is quoted as printed.",
       "Checked against the truth: the programme's true difference (−5.8%) lies inside the reported interval.",
       "Not checked: whether a reader understands the page. Read it aloud to someone who has not seen the model.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why does the report give the programme as a percentage and not as a coefficient of −0.109?
#    <details><summary>Answer</summary>The committee reads percentages of consumption; a coefficient on the log scale needs a translation the reader should not have to make.</details>
# 2. Which brief allows a causal use, and why?
#    <details><summary>Answer</summary>C2: the channel was chosen at random, so a difference between channels estimates the effect of the channel.</details>
# 3. Where in the report does the diagnostics section of the capstone rubric show?
#    <details><summary>Answer</summary>In "Model and checks": what was run, what failed, and what was changed.</details>
#
# ## Carry forward
#
# Your choice is saved in `artifacts/capstone_choice.json`. The capstone report has the same five parts as this page.
