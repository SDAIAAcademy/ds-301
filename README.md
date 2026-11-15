<!-- academy:title -->
# Regression and Generalised Linear Modelling

الانحدار والنماذج الخطية المُعمَّمة

Data Science Track · SDAIA Academy · DS-301 · Level 300

REPLACE: one line under the title: what participants can do after the course

Participants build regression models that answer a stated question and defend what each term means. On synthetic data from Sahil Water, a fictional utility with 30 districts, they fit linear models with splines and interactions, logistic models for late payment and count models for leak reports, diagnose misfit by simulating from the fit, handle grouped data with clustered errors and random intercepts, and penalise many predictors. Results are reported as marginal effects with intervals.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/ds-301/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Implement linear models with interactions and splines and report average marginal effects with intervals, given household consumption with tariff band, household size and temperature | Applied | effect plots and an interval table matching the reference |
| LO2 | Apply logistic and count models, choosing between Poisson and negative binomial from a dispersion check, given late-payment flags and weekly leak reports with pipe length as exposure | Applied | a notebook stating effects on the probability and count scales |
| LO3 | Diagnose misfit with residuals, influence measures and simulation from the fitted model, then correct the model, given a model with five seeded problems such as overdispersion and separation | Performance | a diagnosis log naming at least four problems, and the corrected model |
| LO4 | Analyse grouped data with clustered standard errors and a random-intercept model and explain how the intervals change, given readings nested in 30 districts of very different sizes | Applied | a table of naive, clustered and mixed-effects estimates with a short explanation |
| LO5 | Apply ridge and lasso with cross-validated tuning and measure the stability of the selected predictors, given 120 correlated candidate predictors | Applied | a coefficient path, the chosen penalty and a bootstrap selection-frequency table |
| LO6 | Build and defend a regression model for a planner's question, justifying terms, family, uncertainty and whether the use is descriptive, predictive or causal, given a supplied dataset and a written brief | Performance | a report and notebook defended live |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | Linear models that answer a question | A regression answers a question; Fake data first; Transformations and splines; Interactions and marginal effects | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Generalised linear models | Links and families; Reading a logistic model; Counts and exposure; Overdispersion | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Check and repair | Residuals that tell you something; Influential observations; Simulation-based checks; Separation and error structure | [`slides/day3.html`](slides/day3.html) |
| Day 4 | Grouped data and many predictors | Clustered data; Partial pooling; Penalised regression; Reporting a model | [`slides/day4.html`](slides/day4.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Label five published regression claims descriptive, predictive or causal | [`D1_1_label_five_published.ipynb`](labs/D1_1_label_five_published.ipynb) |
| 1.2 | Day 1 · Session 2 | Simulate consumption from a known model and recover its coefficients | [`D1_2_simulate_consumption_from.ipynb`](labs/D1_2_simulate_consumption_from.ipynb) |
| 1.3 | Day 1 · Session 3 | Fit log consumption with a temperature spline and plot its band | [`D1_3_fit_log_consumption.ipynb`](labs/D1_3_fit_log_consumption.ipynb) |
| 1.4 | Day 1 · Session 4 | Add a tariff-by-household-size interaction and report marginal effects | [`D1_4_add_tariff_household.ipynb`](labs/D1_4_add_tariff_household.ipynb) |
| 2.1 | Day 2 · Session 1 | Fit late payment with linear and logistic models and show where the first breaks | [`D2_1_fit_late_payment.ipynb`](labs/D2_1_fit_late_payment.ipynb) |
| 2.2 | Day 2 · Session 2 | Turn coefficients into probability differences for three household profiles | [`D2_2_turn_coefficients_into.ipynb`](labs/D2_2_turn_coefficients_into.ipynb) |
| 2.3 | Day 2 · Session 3 | Model leak reports with a Poisson model and a pipe-length offset | [`D2_3_model_leak_reports.ipynb`](labs/D2_3_model_leak_reports.ipynb) |
| 2.4 | Day 2 · Session 4 | Test dispersion and refit with a negative binomial model | [`D2_4_test_dispersion_refit.ipynb`](labs/D2_4_test_dispersion_refit.ipynb) |
| 3.1 | Day 3 · Session 1 | Find a missing non-linear term from binned-residual plots | [`D3_1_find_missing_non.ipynb`](labs/D3_1_find_missing_non.ipynb) |
| 3.2 | Day 3 · Session 2 | Find the three most influential districts and refit without them | [`D3_2_find_three_most.ipynb`](labs/D3_2_find_three_most.ipynb) |
| 3.3 | Day 3 · Session 3 | Test whether the count model reproduces the observed share of zeros | [`D3_3_test_whether_count.ipynb`](labs/D3_3_test_whether_count.ipynb) |
| 3.4 | Day 3 · Session 4 | Repair a separated logistic fit and add heteroskedasticity-consistent errors | [`D3_4_repair_separated_logistic.ipynb`](labs/D3_4_repair_separated_logistic.ipynb) |
| 4.1 | Day 4 · Session 1 | Set naive and district-clustered standard errors side by side and explain the change | [`D4_1_set_naive_district.ipynb`](labs/D4_1_set_naive_district.ipynb) |
| 4.2 | Day 4 · Session 2 | Fit a random-intercept model and plot how small districts shrink | [`D4_2_fit_random_intercept.ipynb`](labs/D4_2_fit_random_intercept.ipynb) |
| 4.3 | Day 4 · Session 3 | Tune ridge and lasso on 120 predictors and plot coefficient paths | [`D4_3_tune_ridge_lasso.ipynb`](labs/D4_3_tune_ridge_lasso.ipynb) |
| 4.4 | Day 4 · Session 4 | Draft a one-page model report and choose the capstone brief | [`D4_4_draft_one_page.ipynb`](labs/D4_4_draft_one_page.ipynb) |
<!-- /academy:labs -->

## Capstone

A regression analysis of a planner's brief on a supplied or public dataset, in a public repository whose README reports choices, diagnostics, effects with intervals and limits; eight-minute defence plus questions

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- DS-201 Statistical Inference by Simulation
- Fits a simple linear regression and reads its coefficient table

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Analysis language and notebooks:** Python with Jupyter or marimo, R with Quarto
- **Regression, mixed-effects and penalised models:** statsmodels, scikit-learn, R with lme4 and glmnet
- **Marginal effects:** marginaleffects for R and Python, course-provided functions
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- Personal Data Protection Law and its implementing regulations: REPLACE: the address of the official text
- General Rules for Secondary Use of Data: REPLACE: the address of the official text
- SDAIA AI Ethics Principles: REPLACE: the address of the official text
