<!-- academy:title -->
# Regression and Generalised Linear Modelling

الانحدار والنماذج الخطية المُعمَّمة

Data Science Track · SDAIA Academy · DS-301 · Level 300

Fit linear, logistic and count models that answer a stated question, check them by simulating from the fit, and report effects with intervals people can read

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

**Sahil Water (شركة ساحل للمياه)** is a fictional utility serving 40,000 households in 30 districts of very different sizes. Every file is synthetic and generated with a fixed seed by `labs/prepare_data.py`: one month's bill for each household (tariff band, household size, temperature, consumption, bill, autopay, past late payments, a late-payment flag), weekly leak reports on 1,200 pipe segments with their length, material, age and pressure, a district leak summary from a previous analyst, and 126 candidate columns for a forecast of next summer's demand. Participants work as Arjuwan Al-Sabhan, a junior data scientist answering Ghaliya Al-Muhairi, head of network and demand planning. Five problems are planted in the previous analyst's models and found on Day 3; what is planted and where is in `labs/solutions/answer_key.md`, for trainers.

Billing data describe households. Household keys are pseudonyms, results are reported by band or district only, one lab removes the columns that supply planning cannot justify under the data minimisation principle of the Personal Data Protection Law, and every report separates descriptive from causal claims: no coefficient is presented as a tariff's effect on poorer households.

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Three uses of a regression | [`D1_1_three_uses.ipynb`](labs/D1_1_three_uses.ipynb) |
| 1.2 | Day 1 · Session 2 | Fake data first | [`D1_2_fake_data.ipynb`](labs/D1_2_fake_data.ipynb) |
| 1.3 | Day 1 · Session 3 | A temperature spline | [`D1_3_temperature_spline.ipynb`](labs/D1_3_temperature_spline.ipynb) |
| 1.4 | Day 1 · Session 4 | Interaction and marginal effects | [`D1_4_interaction_effects.ipynb`](labs/D1_4_interaction_effects.ipynb) |
| 2.1 | Day 2 · Session 1 | Linear against logistic | [`D2_1_linear_vs_logistic.ipynb`](labs/D2_1_linear_vs_logistic.ipynb) |
| 2.2 | Day 2 · Session 2 | Three household profiles | [`D2_2_three_profiles.ipynb`](labs/D2_2_three_profiles.ipynb) |
| 2.3 | Day 2 · Session 3 | Leaks with an exposure | [`D2_3_poisson_offset.ipynb`](labs/D2_3_poisson_offset.ipynb) |
| 2.4 | Day 2 · Session 4 | Dispersion and the negative binomial | [`D2_4_negative_binomial.ipynb`](labs/D2_4_negative_binomial.ipynb) |
| 3.1 | Day 3 · Session 1 | Binned residuals | [`D3_1_binned_residuals.ipynb`](labs/D3_1_binned_residuals.ipynb) |
| 3.2 | Day 3 · Session 2 | Influential districts | [`D3_2_influential_districts.ipynb`](labs/D3_2_influential_districts.ipynb) |
| 3.3 | Day 3 · Session 3 | The share of zeros | [`D3_3_share_of_zeros.ipynb`](labs/D3_3_share_of_zeros.ipynb) |
| 3.4 | Day 3 · Session 4 | Separation and robust errors | [`D3_4_separation_hc.ipynb`](labs/D3_4_separation_hc.ipynb) |
| 4.1 | Day 4 · Session 1 | Clustered standard errors | [`D4_1_clustered_errors.ipynb`](labs/D4_1_clustered_errors.ipynb) |
| 4.2 | Day 4 · Session 2 | Partial pooling | [`D4_2_partial_pooling.ipynb`](labs/D4_2_partial_pooling.ipynb) |
| 4.3 | Day 4 · Session 3 | Ridge and lasso | [`D4_3_ridge_lasso.ipynb`](labs/D4_3_ridge_lasso.ipynb) |
| 4.4 | Day 4 · Session 4 | A one-page model report | [`D4_4_model_report.ipynb`](labs/D4_4_model_report.ipynb) |
<!-- /academy:labs -->

## Capstone

A regression analysis of a planner's brief on a supplied or public dataset, in a public repository whose README reports choices, diagnostics, effects with intervals and limits; eight-minute defence plus questions

**Submission:** a link to a public GitHub repository with a notebook that reruns from the raw data with a fixed seed, a report, and a README that states the brief, the use (descriptive, predictive or causal), the estimand, the model and its family, the diagnostics, the effects with intervals and the limits, with the commit history and the run log. Then an eight-minute live defence and four minutes of questions, in which the assessor changes one term or the family and the participant predicts the effect before re-running. The three briefs and their datasets are in `labs/capstone/`; a table from the national Open Data Platform approved by the trainer is also accepted.

**Rubric:** specification 20, diagnostics 30, uncertainty 20, interpretation 20, reproducibility 10.

## How the course is assessed

- AI-off entry and exit checks on reading and specifying models (20%). They are supervised and are not in this repository; the practice questions on the course page are of the same kind.
- The capstone, scored with the rubric above (60%), and its live defence (20%).
- Passing: 70% overall and at least 60% on both the capstone rubric and the supervised check. Authenticity rests on the commit history, the run logs and the change the assessor makes in the defence.
- AI policy: no assistant in the supervised checks and in each lab's first fit and interpretation; a hint-only tutor in the lab extensions (`labs/tutor_instruction.md`); any assistant in the capstone, which is defended live.

## How the course is organised

Four teaching days of four sessions, each about 25 minutes of ideas and a 25-minute lab, then a capstone day. Each day has a deck in `slides/` with speaker notes and a checkpoint per session; each lab is a notebook with exercises, safety nets that let later cells run, and a solution in `labs/solutions/`. Pre-work: about two hours on simple regression in `labs/P0_prework_simple_regression.ipynb`. Follow-up: a critique of a published regression from the participant's own field, `labs/followup/README.md`.

## Prerequisites

- DS-201 Statistical Inference by Simulation
- Fits a simple linear regression and reads its coefficient table
- Pre-work: about two hours on simple regression, `labs/P0_prework_simple_regression.ipynb`, before the supervised entry quiz
- Setup: a laptop with uv, or Google Colab. Nothing calls or downloads a model. Run `labs/00_setup_check.ipynb` before Day 1; see `labs/README.md`

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Analysis language and notebooks:** Python with Jupyter or marimo, R with Quarto
- **Regression, mixed-effects and penalised models:** statsmodels, scikit-learn, R with lme4 and glmnet
- **Marginal effects:** marginaleffects for R and Python, course-provided functions
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

### National references

- [Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [General Rules for Secondary Use of Data (SDAIA)](https://sdaia.gov.sa/Documents/GeneralRulesForSecondaryUseOfData_EN.pdf)
- [AI Ethics Principles (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf)

### Methods

- [Gelman, Hill and Vehtari, Regression and Other Stories: examples and code](https://avehtari.github.io/ROS-Examples/)

### Library documentation

- [statsmodels: generalized linear models](https://www.statsmodels.org/stable/glm.html)
- [statsmodels: NegativeBinomial](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.NegativeBinomial.html)
- [statsmodels: linear mixed effects models](https://www.statsmodels.org/stable/mixed_linear.html)
- [statsmodels: robust and cluster-robust covariance (get_robustcov_results)](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.get_robustcov_results.html)
- [statsmodels: OLSInfluence (leverage, Cook's distance, DFBETA)](https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.OLSInfluence.html)
- [patsy: spline regression](https://patsy.readthedocs.io/en/latest/spline-regression.html)
- [scikit-learn: linear models (ridge, lasso)](https://scikit-learn.org/stable/modules/linear_model.html)
- [scikit-learn: LassoCV](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoCV.html)
- [scikit-learn: lasso_path](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.lasso_path.html)
- [marginaleffects (R and Python)](https://marginaleffects.com/)
- [marginaleffects on PyPI](https://pypi.org/project/marginaleffects/)
- [lme4 on CRAN](https://cran.r-project.org/package=lme4)
- [glmnet on CRAN](https://cran.r-project.org/package=glmnet)

### Tools

- [Project Jupyter](https://jupyter.org/)
- [marimo](https://marimo.io/)
- [Quarto](https://quarto.org/)
- [Google Colab](https://colab.research.google.com/)
- [Saudi Open Data Platform](https://open.data.gov.sa/)
<!-- /academy:sources -->
