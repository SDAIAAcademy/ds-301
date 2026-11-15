---
course: "Regression and Generalised Linear Modelling"
code: "DS-301"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-301/index.html"
---

# Regression and Generalised Linear Modelling

الانحدار والنماذج الخطية المُعمَّمة

Data Science Track · 4 teaching days + capstone day · 26 hours · Level 300

Fit linear, logistic and count models that answer a stated question, check them by simulating from the fit, and report effects with intervals people can read

Participants build regression models that answer a stated question and defend what each term means. On synthetic data from Sahil Water, a fictional utility with 30 districts, they fit linear models with splines and interactions, logistic models for late payment and count models for leak reports, diagnose misfit by simulating from the fit, handle grouped data with clustered errors and random intercepts, and penalise many predictors. Results are reported as marginal effects with intervals.

**Who it is for:** Specialists. Analysts and data scientists who have completed the level 200 set or can show equivalent work: an analysis or model they built, validated and can explain.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Sahil Water.** Sahil Water (شركة ساحل للمياه) is a fictional utility serving 40,000 households in 30 districts of very different sizes, and all of its data are synthetic, generated with a fixed seed: one month's bill for every household with tariff band, household size, temperature and a late-payment flag, weekly leak reports on 1,200 pipe segments with their lengths, a district leak summary from a previous analyst, and 126 candidate columns for next summer's demand. Planted problems (a missing log term, two districts with pipe lengths keyed a tenth too small, overdispersed leaks, a notice flag that separates late payers, a variance funnel) are found by named labs; participants work as Arjuwan Al-Sabhan, a junior data scientist answering the planner Ghaliya Al-Muhairi, household keys are pseudonyms and results are reported by band or district only.

## The course

### Day 1: Linear models that answer a question

Slides: https://sdaiaacademy.github.io/ds-301/slides/day1.md

- **Session 1: A regression answers a question**
  - Distinguish descriptive, predictive and causal uses of a regression
  - State the estimand of a question before choosing a model
  - Judge whether the evidence behind a published claim supports the use it states
  - [Lab 1.1: Three uses of a regression (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D1_1_three_uses.ipynb)
- **Session 2: Fake data first**
  - Simulate an outcome from a stated model with a seed
  - Recover known coefficients and check their intervals by coverage
  - Show what leaving out a correlated term does to a coefficient
  - [Lab 1.2: Fake data first (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D1_2_fake_data.ipynb)
- **Session 3: Transformations and splines**
  - Fit a model of log consumption and read its coefficients as percentages
  - Replace a straight temperature term with a spline and compare the fits
  - Plot a fitted curve with its band and back-transform it correctly
  - [Lab 1.3: A temperature spline (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D1_3_temperature_spline.ipynb)
- **Session 4: Interactions and marginal effects**
  - Add an interaction and say what each of its coefficients means
  - Compute an average marginal effect on the outcome scale
  - Report marginal effects by group with intervals from simulation
  - [Lab 1.4: Interaction and marginal effects (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D1_4_interaction_effects.ipynb)

### Day 2: Generalised linear models

Slides: https://sdaiaacademy.github.io/ds-301/slides/day2.md

- **Session 1: Links and families**
  - Name the family and link that fit an outcome
  - Fit a linear probability model and a logistic model to the same outcome
  - Show where the linear model breaks
  - [Lab 2.1: Linear against logistic (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D2_1_linear_vs_logistic.ipynb)
- **Session 2: Reading a logistic model**
  - Convert logistic coefficients to odds ratios
  - Turn a coefficient into probability differences for stated profiles
  - Report a probability difference with an interval
  - [Lab 2.2: Three household profiles (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D2_2_three_profiles.ipynb)
- **Session 3: Counts and exposure**
  - Fit a Poisson model to counts
  - Use the log of the exposure as an offset
  - Read coefficients as rate ratios
  - [Lab 2.3: Leaks with an exposure (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D2_3_poisson_offset.ipynb)
- **Session 4: Overdispersion**
  - Measure dispersion from a fitted Poisson model
  - Fit a negative binomial model with the same exposure
  - Compare effects and intervals on the count scale
  - [Lab 2.4: Dispersion and the negative binomial (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D2_4_negative_binomial.ipynb)

### Day 3: Check and repair

Slides: https://sdaiaacademy.github.io/ds-301/slides/day3.md

- **Session 1: Residuals that tell you something**
  - Explain why raw logistic residuals are uninformative
  - Draw binned residuals against a predictor with their band
  - Find a missing term and show the repaired fit
  - [Lab 3.1: Binned residuals (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D3_1_binned_residuals.ipynb)
- **Session 2: Influential observations**
  - Compute leverage and Cook's distance for a fitted model
  - Find the most influential units and refit without them
  - Trace an influential unit to its cause before deciding
  - [Lab 3.2: Influential districts (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D3_2_influential_districts.ipynb)
- **Session 3: Simulation-based checks**
  - Simulate replicate data sets from a fitted count model
  - Choose a test statistic that matters to the question
  - Judge a model by where the observed statistic falls
  - [Lab 3.3: The share of zeros (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D3_3_share_of_zeros.ipynb)
- **Session 4: Separation and error structure**
  - Recognise separation from its symptoms
  - Repair a separated fit and say why the variable does not belong
  - Use heteroskedasticity-consistent standard errors on a funnel
  - [Lab 3.4: Separation and robust errors (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D3_4_separation_hc.ipynb)

### Day 4: Grouped data and many predictors

Slides: https://sdaiaacademy.github.io/ds-301/slides/day4.md

- **Session 1: Clustered data**
  - Identify the unit at which a predictor varies
  - Compute standard errors clustered by district
  - Explain why clustering widens some intervals and not others
  - [Lab 4.1: Clustered standard errors (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D4_1_clustered_errors.ipynb)
- **Session 2: Partial pooling**
  - Fit a random-intercept model
  - Read the district variance and the share of variance between districts
  - Show how small districts shrink towards the average
  - [Lab 4.2: Partial pooling (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D4_2_partial_pooling.ipynb)
- **Session 3: Penalised regression**
  - Screen candidate predictors for necessity before modelling
  - Tune ridge and lasso penalties by cross-validation
  - Measure how stable the lasso's selection is
  - [Lab 4.3: Ridge and lasso (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D4_3_ridge_lasso.ipynb)
- **Session 4: Reporting a model**
  - Write predictions and effects in the units of the reader
  - Separate descriptive, predictive and causal statements
  - State the limits of a model in a report
  - [Lab 4.4: A one-page model report (25 min)](https://sdaiaacademy.github.io/ds-301/labs/D4_4_model_report.ipynb)

### Capstone: Capstone project presentations

Slides: https://sdaiaacademy.github.io/ds-301/slides/capstone.md

## Capstone

A regression analysis of a planner's brief on a supplied or public dataset, in a public repository whose README reports choices, diagnostics, effects with intervals and limits; eight-minute defence plus questions

**What you submit:** A link to a public GitHub repository with a notebook that reruns from the raw data with a fixed seed, a report, and a README that states the brief, the use (descriptive, predictive or causal), the estimand, the model and its family, the diagnostics run, the effects with intervals and the limits, with the commit history and the run log. Then an eight-minute live defence and four minutes of questions, in which the assessor changes one term or the family and the participant predicts the effect before re-running.

**Rubric:**

- Specification: 20%
- Diagnostics: 30%
- Uncertainty: 20%
- Interpretation: 20%
- Reproducibility: 10%

## Outcomes

- **LO1** Implement linear models with interactions and splines and report average marginal effects with intervals, given household consumption with tariff band, household size and temperature (Applied) Evidence: effect plots and an interval table matching the reference
- **LO2** Apply logistic and count models, choosing between Poisson and negative binomial from a dispersion check, given late-payment flags and weekly leak reports with pipe length as exposure (Applied) Evidence: a notebook stating effects on the probability and count scales
- **LO3** Diagnose misfit with residuals, influence measures and simulation from the fitted model, then correct the model, given a model with five seeded problems such as overdispersion and separation (Performance) Evidence: a diagnosis log naming at least four problems, and the corrected model
- **LO4** Analyse grouped data with clustered standard errors and a random-intercept model and explain how the intervals change, given readings nested in 30 districts of very different sizes (Applied) Evidence: a table of naive, clustered and mixed-effects estimates with a short explanation
- **LO5** Apply ridge and lasso with cross-validated tuning and measure the stability of the selected predictors, given 120 correlated candidate predictors (Applied) Evidence: a coefficient path, the chosen penalty and a bootstrap selection-frequency table
- **LO6** Build and defend a regression model for a planner's question, justifying terms, family, uncertainty and whether the use is descriptive, predictive or causal, given a supplied dataset and a written brief (Performance) Evidence: a report and notebook defended live

## Tools

- **Analysis language and notebooks:** Python with Jupyter or marimo, R with Quarto
- **Regression, mixed-effects and penalised models:** statsmodels, scikit-learn, R with lme4 and glmnet
- **Marginal effects:** marginaleffects for R and Python, course-provided functions

## Prerequisites

- DS-201 Statistical Inference by Simulation
- Fits a simple linear regression and reads its coefficient table
- Pre-work: about two hours on simple regression, labs/P0_prework_simple_regression.ipynb, before the supervised entry quiz
- Setup: a laptop with uv, or Google Colab. Nothing calls or downloads a model. Run 00_setup_check before Day 1; see labs/README.md.

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

---

SDAIA Academy · Data Science Track · Regression and Generalised Linear Modelling

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-15 · commit 5c64064
