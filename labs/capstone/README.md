# Capstone: build and defend a regression model

You answer one planner's brief with a regression model, in a public GitHub repository of your own, and defend it live: eight minutes, then four minutes of questions in which the assessor changes one term or the family of your model and you predict the effect before re-running.

## The briefs

Choose one in lab 4.4. The datasets are synthetic, generated with a fixed seed by `prepare_data.py`, and describe the fictional Sahil Water.

| Brief | Question from Ghaliya | Data | Outcome |
|---|---|---|---|
| C1 · Low-pressure complaints | How do complaints per 1,000 customers move with temperature, and do districts in the pressure management programme report more of them? Which districts should the committee watch next summer? | `data/c1_pressure_complaints.csv`: 30 districts × 12 months, customers, mean temperature, programme flag, complaints | a count with an exposure |
| C2 · The water-saving kit offer | Which channel should the next offer use, a letter or a text message, and does the answer differ by tariff band? The channel was chosen at random. | `data/c2_kit_offer.csv`: 6,000 households, district, band, size, consumption, channel, whether the kit was taken | a binary outcome |
| C3 · Villa peak demand | How much does a villa's peak-month consumption rise with garden size and temperature, and does an irrigation timer change the garden effect? | `data/c3_villa_peak.csv`: 3,000 villas, district, garden area, pool, timer, peak temperature, peak-month m³ | a positive continuous outcome |

**Your own dataset.** You may instead use a public dataset, for example from the Saudi Open Data Platform (open.data.gov.sa), with a planner's question you write yourself. Agree it with your trainer by the end of Day 4. It must hold no personal data beyond what the publisher released.

Each brief contains at least one problem that your diagnostics should find. Finding it, and showing how, is part of the diagnostics criterion.

## What the repository contains

- A notebook (or script) that reruns from the raw data to every number in the README, with a fixed seed.
- The environment: `pyproject.toml` with `uv.lock`, or `requirements.txt` with pinned versions.
- A README with these parts, in this order:
  1. **Brief.** The question in the planner's words.
  2. **Use and estimand.** Descriptive, predictive or causal, and why; the quantity, the population and the comparison.
  3. **Model.** The outcome and its scale, the family and link, the terms and why each is there, and how grouping is handled.
  4. **Diagnostics.** At least three checks, each as problem, evidence with its number, and fix; what failed and what you changed.
  5. **Effects.** In the planner's units (m³, percentage points, complaints per 1,000 customers), each with a 95% interval.
  6. **Limits.** What the numbers are not, what the intervals leave out, and where the model should not be used.
- The commit history and the run log (the notebook's output, or a log file from the last full run).

## How it is scored

| Criterion | Weight | Full marks |
|---|---|---|
| Specification | 20 | Use and estimand stated; family and terms justified from the data and the question |
| Diagnostics | 30 | At least three checks with numbers; the brief's planted problem found and repaired, or a check that would have found it |
| Uncertainty | 20 | Every effect with an interval, at the right level of grouping |
| Interpretation | 20 | Effects in the planner's units; no claim the design cannot carry; limits stated |
| Reproducibility | 10 | A fresh clone reruns from the raw data to the same numbers |

The capstone rubric counts for 60% of the course result. Passing needs 70% overall and at least 60% on both the capstone rubric and the supervised check.

## Assistants

You may use any assistant in the capstone. The question round is where the work is shown to be yours: you predict what changes when the assessor changes the model, and explain why.

## Before the defence

Clone your repository into a fresh folder and rerun it. Check that the README's numbers match the run.
