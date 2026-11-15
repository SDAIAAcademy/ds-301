---
course: "Regression and Generalised Linear Modelling"
code: "DS-301"
version: "2027.1.0"
deck: "day4"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-301/slides/day4.html"
---

# Regression and Generalised Linear Modelling

## Day 4: Grouped data and many predictors

Districts of very different sizes, 120 candidate predictors, and a report people can read

#### [day4#title] Grouped data and many predictors

*SDAIA Academy · Regression and Generalised Linear Modelling*

Day 4: Districts of very different sizes, 120 candidate predictors, and a report people can read

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-301

#### [day4#agenda] Grouped data and many predictors

*Today*

- **Session 1 · Clustered data**: Households in one district share more than the model knows, so a district-level effect has far fewer independent pieces of evidence than rows
- **Session 2 · Partial pooling**: A random intercept for each district pools what districts share, so small districts borrow strength and shrink
- **Session 3 · Penalised regression**: With many correlated predictors, a penalty trades a little bias for stability; which predictors it keeps is itself uncertain
- **Session 4 · Reporting a model**: A model report says what was asked, what was fitted, how it was checked and what the numbers do not mean

#### [day4#review-day3] Which line belongs in a diagnosis log?

*Review of Day 3*

**Question:** A colleague's logistic model of meter faults is ready for review. Which entry would an assessor accept?

- A. The residuals looked a bit off, so I added a log term
- B. No problems: the model converged without warnings
- C. Missing curve: 6 of 20 binned residuals against meter age outside the 2-SE band; with a spline in age, 1 of 20
- D. AIC fell by 40, so the model is right

### Session 1: Clustered data

#### [day4#s1] Clustered data

*Session 1*

- Identify the unit at which a predictor varies
- Compute standard errors clustered by district
- Explain why clustering widens some intervals and not others

#### [day4#programme-question] Do the 13 programme districts use less water? The naive answer is suspiciously sure

*The case*

- **−7.8%** programme against other districts, at equal size, band and temperature
- **±0.6** points: the naive 95% interval from 40,000 bills

Pressure management is decided per district. How many pieces of evidence are there: 40,000 or 30?

#### [day4#unit-of-variation] Ask first where each predictor varies: within districts or only between them

*Lab 4.1, step 1*

| Predictor | Varies | Evidence comes from |
| --- | --- | --- |
| household size | within every district | thousands of household comparisons |
| tariff band | within every district | thousands of household comparisons |
| temperature | by month | months in every district |
| pressure programme | only between districts | 13 districts against 17 |

#### [day4#shared-district] Households in one district share pressure, network and neighbourhood

*Why the rows are not independent*

- Each district has its own level of consumption the model does not know.
- Every household in it carries the same deviation.
- 9,423 bills from D17 repeat one district's deviation 9,423 times.

- **Design effect.** With m bills per district and a share ρ of variance between districts, the variance grows by about 1 + (m − 1)ρ. With m ≈ 1,300 and ρ = 0.06, about 80.

#### [day4#clustered-se] Clustered errors let residuals within a district be correlated in any way

*Lab 4.1, step 3*

```python
fit = smf.ols(FORMULA, data=b).fit(
    cov_type="cluster",
    cov_kwds={"groups": pd.factorize(b["district"])[0]})
```

- The estimates do not change; only their standard errors.
- They assume districts independent of each other, nothing within them.
- In R: `sandwich::vcovCL(fit, cluster = ~district)`.

#### [day4#ratios] The programme's standard error grows 13.7 times; household size's does not grow at all

*Lab 4.1, step 4*

Figure: Clustered over naive standard errors. Lab 4.1.

#### [day4#interval-changes] From "certainly about 8% less" to "somewhere between 15% less and no difference"

*Lab 4.1, step 3*

- **Naive.** −8.3% to −7.2%. A planner would budget on it.
- **Clustered by district.** −15.3% to +0.5%. A planner would ask for more districts or a trial.

> **What goes wrong.** Reporting the naive interval for a district-level policy is the most common error in utility analyses: the precision of 40,000 rows for a question that 30 districts answer.

#### [day4#check-cluster] Which interval widens most?

*Checkpoint*

**Question:** A model of 50,000 students' scores in 80 schools has two predictors: hours of homework (per student) and a new curriculum (per school). You switch to errors clustered by school. What happens?

- A. Both coefficients change, and both intervals widen
- B. The curriculum's interval widens far more than homework's, and neither estimate changes
- C. Homework's interval widens most, because it has more variation
- D. Nothing much: with 50,000 students clustering does not matter

#### [day4#lab-4-1] Clustered standard errors

Lab 4.1 · 25 min

Estimate the consumption difference of pressure-managed districts with naive and district-clustered standard errors side by side, and explain why the interval widens many times for the district-level term and little for household size.

[D4_1_clustered_errors.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D4_1_clustered_errors.ipynb)

- [ ] Which predictors vary by household and which by district (4 min)
- [ ] The naive fit (4 min)
- [ ] Errors clustered by district (6 min)
- [ ] The ratio of standard errors, term by term (6 min)
- [ ] Two sentences that explain the change (5 min)
- [ ] ✱ Stretch: Resample whole districts and compare the bootstrap interval

### Session 2: Partial pooling

#### [day4#s2] Partial pooling

*Session 2*

- Fit a random-intercept model
- Read the district variance and the share of variance between districts
- Show how small districts shrink towards the average

#### [day4#three-choices] Ignore districts, give each its own mean, or let them share: partial pooling

*The idea*

- **Complete pooling.** One mean for all. Districts differ, so it is wrong for most of them.
- **No pooling.** Each district its own mean. D13's rests on 40 bills: noisy.
- **Partial pooling.** Each district its own level, drawn from a distribution of district levels whose spread is estimated.

#### [day4#random-intercept] A random intercept gives each district its own level, drawn from a normal distribution

*Lab 4.2, step 1*

```python
mix = smf.mixedlm(FORMULA, data=b, groups=b["district"]).fit()
# R:  lmer(log_m3 ~ tariff_band * household_size + bs(temperature_c, 5)
#                  + pressure_managed + (1 | district), data = b)
```

- Two variances: between districts (τ²) and between bills within one (σ²).
- The programme's standard error now counts districts, as clustering did.

#### [day4#variances] Only 6% of the variance is between districts, and it still changes everything for the programme

*Lab 4.2, step 2*

- **0.079** SD between districts, log scale (about ±8%)
- **0.301** SD between bills within a district
- **6.4%** share of variance between districts

#### [day4#shrinkage] Small districts move towards the average; large ones stay where their data put them

*Lab 4.2, step 3*

Figure: Raw district means and random-intercept estimates against bills per district. Lab 4.2.

#### [day4#three-way] Naive, clustered, mixed: both honest intervals are many times wider than the naive one

*Lab 4.2, step 4*

Figure: Programme districts against others, % difference with 95% intervals. Labs 4.1 and 4.2.

#### [day4#which-to-use] Clustered errors fix the uncertainty; a mixed model also estimates the districts

*Choosing*

|  | Clustered errors | Random intercept |
| --- | --- | --- |
| Assumes | districts independent; nothing within | district levels normal, residuals independent within |
| Gives | honest standard errors for the same estimates | estimates, standard errors and each district's level |
| Needs | enough clusters (30 is about the minimum) | enough clusters to estimate τ |

#### [day4#check-pooling] Which district moves most?

*Checkpoint*

**Question:** In a random-intercept model, district A has 50 bills and a raw mean 0.12 above average; district B has 5,000 bills and the same raw mean. What do their estimated levels look like?

- A. Both shrink by the same share, as their raw means are equal
- B. B shrinks more, because it has more bills to average
- C. Neither moves: each district keeps its own mean
- D. A moves noticeably towards the average; B stays almost at 0.12

#### [day4#lab-4-2] Partial pooling

Lab 4.2 · 25 min

Fit a random-intercept model by district, plot each district's raw and shrunken effect against its size, and complete the table of naive, clustered and mixed-effects estimates.

[D4_2_partial_pooling.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D4_2_partial_pooling.ipynb)

- [ ] Fit the random-intercept model (5 min)
- [ ] District and household variance (4 min)
- [ ] Raw against shrunken district effects (7 min)
- [ ] The three-way table (5 min)
- [ ] A short explanation of the table (4 min)
- [ ] ✱ Stretch: Add a random slope for household size and compare

### Session 3: Penalised regression

#### [day4#s3] Penalised regression

*Session 3*

- Screen candidate predictors for necessity before modelling
- Tune ridge and lasso penalties by cross-validation
- Measure how stable the lasso's selection is

#### [day4#candidates] Billing exported 126 candidate columns to predict August consumption

*The case*

- **Useful-looking.** 12 months of past consumption, property details, appliance answers, area climate.
- **Noise.** 38 survey questions, app logins, bill queries.
- **Nobody asked for.** A member's chronic condition, nationality, income band, employer, phone brand, marital status.

#### [day4#minimisation] Remove what the purpose cannot justify, before you check whether it predicts

*Lab 4.3, step 1*

- The PDPL limits personal data to the minimum needed for the purpose (Article 11).
- Health data is sensitive data under the Law.
- A supply forecast needs none of the six columns.

> **What goes wrong.** "Let the lasso decide." A penalty chooses by prediction; minimisation is decided by the purpose. A column that predicts can still be one you may not use.

#### [day4#ridge] Ridge shrinks every coefficient a little and keeps them all

*Lab 4.3, step 2*

- Least squares plus a penalty on the sum of squared coefficients.
- Correlated predictors share the weight between them.
- Standardise first, so one penalty treats all alike.

**120** nonzero coefficients at the cross-validated penalty, 34.6

#### [day4#lasso] The lasso sets coefficients to zero: one fit selects 27 of 120 predictors

*Lab 4.3, step 3*

- A penalty on the sum of absolute coefficients.
- Cross-validation picks the penalty that predicts best.
- That penalty is chosen for prediction, not to find the true predictors.

- **Correlated groups.** The twelve lag months are correlated at about 0.9. The lasso picks some of a group and drops the rest, almost at random.

#### [day4#selection] Over 100 bootstrap samples, eight predictors are selected every time; the rest come and go

*Lab 4.3, step 4*

Figure: Share of 100 bootstrap samples in which the lasso selects each predictor, 40 most frequent. Lab 4.3.

#### [day4#report-stable] Report the stable set for prediction; report no selected predictor as a "driver"

*Lab 4.3, step 5*

- **Defensible.** "Eight predictors were selected in every bootstrap sample; the forecast uses the lasso's predictions."
- **Not defensible.** "The lasso shows that October consumption and dishwashers drive August demand."

> **Estimating after selecting.** Least squares on the data that chose the predictors overstates them; select on one half and estimate on the other (the stretch item).

#### [day4#check-lasso] What do you tell the planner?

*Checkpoint*

**Question:** A lasso with a cross-validated penalty selected 25 of 90 predictors. Over 100 bootstrap samples, 6 are selected every time and 40 are selected between 20% and 80% of the time. What can you say?

- A. The 25 selected predictors are the drivers of demand
- B. The 6 are a stable core; the others' selection depends on the sample and should not be reported as findings
- C. The model is useless and should be dropped
- D. Lower the penalty until all 40 are always selected

#### [day4#lab-4-3] Ridge and lasso

Lab 4.3 · 25 min

Remove the candidate columns a utility could not justify for supply planning, tune ridge and lasso on the remaining 120 predictors, plot the coefficient paths and count how often each predictor is selected over bootstrap samples.

[D4_3_ridge_lasso.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D4_3_ridge_lasso.ipynb)

- [ ] Remove the columns that fail data minimisation (4 min)
- [ ] Ridge path and cross-validated penalty (5 min)
- [ ] Lasso path and cross-validated penalty (5 min)
- [ ] Selection frequency over bootstrap samples (7 min)
- [ ] Which selections to trust (4 min)
- [ ] ✱ Stretch: Fit ordinary least squares on half the data after selecting on the other half

### Session 4: Reporting a model

#### [day4#s4] Reporting a model

*Session 4*

- Write predictions and effects in the units of the reader
- Separate descriptive, predictive and causal statements
- State the limits of a model in a report

#### [day4#report-parts] A model report has five parts, and the capstone README has the same five

*The report*

1. **Question** in the reader's words
2. **Use and estimand** descriptive, predictive or causal
3. **Model and checks** what failed, what changed
4. **Effects** in the reader's units, with intervals
5. **Limits** what it does not mean

#### [day4#readers-units] Write m³ and percentages, never coefficients on a log scale

*Lab 4.4, step 3*

| Not for Ghaliya | For Ghaliya |
| --- | --- |
| household_size:villa 0.020 (SE 0.004) | Each extra member: 5.0 m³ a month for villas (4.8 to 5.2), 2.3 on the standard tariff |
| five spline coefficients for temperature | A typical household: 20.7 m³ in a 30 °C month, 37.9 m³ (37.3 to 38.4) at 40 °C |
| pressure_managed −0.109 | Programme districts used 10.3% less (5.0% to 15.4% less) |

#### [day4#three-uses-again] The use decides which words you may write

*Lab 4.4, steps 1 and 4*

- **Descriptive.** "used", "differed", "at equal size and band": the consumption report.
- **Predictive.** "forecast", "expected", "with this error": the August forecast.
- **Causal.** "reduces", "the effect of": only with a randomised or well-argued comparison, as in brief C2.

#### [day4#limits] Limits say what the numbers are not, what the intervals leave out, and where not to use the model

*Lab 4.4, step 4*

- The programme figure compares districts that chose to join; it is not the saving from joining.
- Intervals cover sampling and district variation in 2026, not a change of tariff.
- Temperatures above 43 °C and a new district without history are outside the data.

#### [day4#briefs] Three briefs from Ghaliya; each hides a problem your diagnostics should find

*Lab 4.4, step 5*

- **C1 · Pressure complaints.** Complaints per 1,000 customers, 30 districts × 12 months. Counts with an exposure.
- **C2 · Kit offer.** 6,000 households, letter or text chosen at random. A binary outcome.
- **C3 · Villa peak.** Peak-month m³ against garden, pool, timer and heat. A positive outcome.

Or a public dataset of your own, such as one from open.data.gov.sa, with the same five parts.

#### [day4#check-report] Which sentence can go in the report?

*Checkpoint*

**Question:** Households with a smart meter display used less water than comparable households without one. They asked for the displays themselves. Which sentence fits the report?

- A. Installing displays will cut demand across Sahil
- B. The display coefficient is −0.07 on the log scale
- C. Households with a display used about 7% less than comparable ones (with its interval); they chose it, so this is not the effect of installing one
- D. Displays save water

#### [day4#lab-4-4] A one-page model report

Lab 4.4 · 25 min

Draft a one-page report of the consumption model from the supplied results, check it for numbers, intervals and limits, then choose a capstone brief and write its estimand and use.

[D4_4_model_report.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D4_4_model_report.ipynb)

- [ ] The question, the use and the estimand (5 min)
- [ ] Model, family and diagnostics (5 min)
- [ ] Effects with intervals in the reader's units (6 min)
- [ ] Limits, and what the coefficients are not (4 min)
- [ ] Choose a capstone brief and write its estimand (5 min)
- [ ] ✱ Stretch: Ask a neighbour to find one causal word in your report

#### [day4#wrap-up] Three things to keep

*Day 4 · wrap-up*

- **Count the evidence.** A district-level predictor has 30 districts behind it, not 40,000 bills.
- **Purpose before penalty.** Minimise first; then trust only the selections that survive resampling.
- **Five parts.** Question, use and estimand, model and checks, effects, limits.

#### [day4#next] Capstone day: build and defend your model

*Next*

A repository that reruns from the raw data, a README with the five parts, an eight-minute defence and four minutes of questions in which the assessor changes one term or the family.
