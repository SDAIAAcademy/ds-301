---
course: "Regression and Generalised Linear Modelling"
code: "DS-301"
version: "2027.1.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-301/"
---

# Regression and Generalised Linear Modelling

Fit linear, logistic and count models that answer a stated question, check them by simulating from the fit, and report effects with intervals people can read

Participants build regression models that answer a stated question and defend what each term means. On synthetic data from Sahil Water, a fictional utility with 30 districts, they fit linear models with splines and interactions, logistic models for late payment and count models for leak reports, diagnose misfit by simulating from the fit, handle grouped data with clustered errors and random intercepts, and penalise many predictors. Results are reported as marginal effects with intervals.

- **Audience:** Specialists. Analysts and data scientists who have completed the level 200 set or can show equivalent work: an analysis or model they built, validated and can explain.
- **Prerequisites:** DS-201 Statistical Inference by Simulation; Fits a simple linear regression and reads its coefficient table; Pre-work: about two hours on simple regression, labs/P0_prework_simple_regression.ipynb, before the supervised entry quiz; Setup: a laptop with uv, or Google Colab. Nothing calls or downloads a model. Run 00_setup_check before Day 1; see labs/README.md.
- **Case study:** Sahil Water: Sahil Water (شركة ساحل للمياه) is a fictional utility serving 40,000 households in 30 districts of very different sizes, and all of its data are synthetic, generated with a fixed seed: one month's bill for every household with tariff band, household size, temperature and a late-payment flag, weekly leak reports on 1,200 pipe segments with their lengths, a district leak summary from a previous analyst, and 126 candidate columns for next summer's demand. Planted problems (a missing log term, two districts with pipe lengths keyed a tenth too small, overdispersed leaks, a notice flag that separates late payers, a variance funnel) are found by named labs; participants work as Arjuwan Al-Sabhan, a junior data scientist answering the planner Ghaliya Al-Muhairi, household keys are pseudonyms and results are reported by band or district only.

## Outcomes

- LO1 (Applied): Implement linear models with interactions and splines and report average marginal effects with intervals, given household consumption with tariff band, household size and temperature
- LO2 (Applied): Apply logistic and count models, choosing between Poisson and negative binomial from a dispersion check, given late-payment flags and weekly leak reports with pipe length as exposure
- LO3 (Performance): Diagnose misfit with residuals, influence measures and simulation from the fitted model, then correct the model, given a model with five seeded problems such as overdispersion and separation
- LO4 (Applied): Analyse grouped data with clustered standard errors and a random-intercept model and explain how the intervals change, given readings nested in 30 districts of very different sizes
- LO5 (Applied): Apply ridge and lasso with cross-validated tuning and measure the stability of the selected predictors, given 120 correlated candidate predictors
- LO6 (Performance): Build and defend a regression model for a planner's question, justifying terms, family, uncertainty and whether the use is descriptive, predictive or causal, given a supplied dataset and a written brief

## Day 1: Linear models that answer a question

Three uses, fake data, splines and an interaction, ending with marginal effects in cubic metres

#### [day1#title] Linear models that answer a question

*SDAIA Academy · Regression and Generalised Linear Modelling*

Day 1: Three uses, fake data, splines and an interaction, ending with marginal effects in cubic metres

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-301

#### [day1#agenda] Linear models that answer a question

*Today*

- **Session 1 · A regression answers a question**: A regression is chosen for its question: describe, predict or explain a cause, and the estimand comes before the model
- **Session 2 · Fake data first**: Simulate data from a model you choose, then fit it: if the fit cannot recover what you planted, the code or the design is wrong
- **Session 3 · Transformations and splines**: A log outcome makes effects multiplicative, and a spline lets temperature bend without guessing its shape
- **Session 4 · Interactions and marginal effects**: An interaction lets the effect of household size differ by tariff band, and an average marginal effect turns coefficients into cubic metres

### Session 1: A regression answers a question

#### [day1#s1] A regression answers a question

*Session 1*

- Distinguish descriptive, predictive and causal uses of a regression
- State the estimand of a question before choosing a model
- Judge whether the evidence behind a published claim supports the use it states

#### [day1#planner-folder] Every regression Ghaliya receives answers one of three questions

*The case*

- **Describe.** How does consumption differ between tariff bands, among the households we bill?
- **Predict.** How much will each district draw next August?
- **Explain a cause.** Would a usage letter make households use less?

> **Sahil Water.** A fictional utility: 40,000 households in 30 districts, one month's bill each, 1,200 pipe segments with weekly leak reports. All synthetic, seed 301.

#### [day1#one-coefficient-three-readings] A coefficient means what the question and the design let it mean

*Same number, three readings*

| Reading of the social-tariff coefficient | Use | Holds when |
| --- | --- | --- |
| Social-tariff households use less than others billed this month | descriptive | the bills are the population you describe |
| Knowing the band improves next month's forecast | predictive | checked on bills the model did not see |
| The social tariff makes families use less | causal | the compared households are alike apart from the tariff |

> **What goes wrong.** The third row is written from data that support only the first. Social-tariff households differ in income, size and housing.

#### [day1#estimand-first] Write the estimand first: the quantity, in whom, compared with what

*Before any model*

1. **1 · Question** How much more water does one more person mean?
2. **2 · Estimand** Average difference in m³ a month, billed households, by band
3. **3 · Model** Log consumption with size, band, a temperature spline
4. **4 · Estimate** A number with an interval, in the estimand's units

> **Takeaway.** The estimand decides the model and what its output must be turned into. Lab 1.4 answers exactly this one.

#### [day1#what-each-use-needs] Each use asks something different of the data

*The evidence each use needs*

- **Descriptive.** A fair sample of the stated population. Adjusting for a variable changes the comparison, not its meaning.
- **Predictive.** Predictions checked on cases the model did not see. Coefficients need no reading at all.
- **Causal.** A design that makes compared groups alike apart from the action: random assignment, or strong stated assumptions.

A good fit supports none of them on its own.

#### [day1#secondary-use] A planning model built on billing data is a secondary use of that data

*The national rules*

- The General Rules for Secondary Use of Data define it as using data **for purposes other than those of collection**.
- The Personal Data Protection Law asks that personal data be **limited to the minimum necessary** for the purpose.
- So every model of this course states its purpose, and lab 4.3 removes the columns that purpose cannot justify.
- Households appear as pseudonymised keys; results are reported by band or district only.

#### [day1#recap-ds201] You can already fit a line, put an interval on its slope and spot confounding

*What you bring from DS-201*

- Least squares and the slope in the reader's units
- A slope interval, and a robust one when residuals fan out
- Adding a variable moves a slope when the two travel together

- **New here.** Curves and interactions, families other than the normal, checks by simulation, grouped data and many predictors.

#### [day1#check-three-uses] Which use does this evidence support?

*Checkpoint*

**Question:** A vendor's late-payment model, trained on 2025 bills, ranks 2026 bills well: 80% of the late payers are in its top fifth. The vendor says sending reminders to that fifth will cut late payment. What does the evidence support?

- A. That reminders to the top fifth will cut late payment
- B. That the model predicts which 2026 bills will be paid late
- C. That the model's variables explain why bills are paid late
- D. Nothing, since the model was not tested in a trial

#### [day1#lab-1-1] Three uses of a regression

Lab 1.1 · 25 min

Label five published regression claims descriptive, predictive or causal, decide whether the evidence named supports each, and write the estimand of two of them.

[D1_1_three_uses.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D1_1_three_uses.ipynb)

- [ ] Read the five claims and the evidence each names (4 min)
- [ ] Label the use each claim states (6 min)
- [ ] Decide whether the evidence supports it, with a reason (7 min)
- [ ] Write the estimand of claims 1 and 3 (5 min)
- [ ] Mark the sheet against the key (3 min)
- [ ] ✱ Stretch: Rewrite claim 1 so that the evidence supports it

### Session 2: Fake data first

#### [day1#s2] Fake data first

*Session 2*

- Simulate an outcome from a stated model with a seed
- Recover known coefficients and check their intervals by coverage
- Show what leaving out a correlated term does to a coefficient

#### [day1#why-fake-data] On real data you never learn whether the fit got the answer right

*The problem with real data*

- A fit always returns numbers, with intervals, whatever the code does.
- Fake data reverse it: **you choose the coefficients**, generate outcomes, fit, and compare.
- A miss means the code, the model or the design is wrong.

- **In lab 1.2.** The 40,000 real households keep their size, band and temperature; only their consumption is invented from a model you write.

#### [day1#simulator-code] A simulator is the model written forwards

*Lab 1.2, step 1*

```python
# file: D1_2_fake_data.ipynb
TRUE = {"Intercept": 2.00, "household_size": 0.095, "social": -0.45,
        "villa": 0.40, "temperature_c": 0.030, "sigma": 0.30}

def simulate(X, p, gen):
    shift = np.select([X.tariff_band == "social", X.tariff_band == "villa"],
                      [p["social"], p["villa"]], 0.0)
    mean = (p["Intercept"] + p["household_size"] * X.household_size
            + shift + p["temperature_c"] * X.temperature_c)
    return mean + gen.normal(0, p["sigma"], len(X))
```

#### [day1#recovery] One fit gives back what you planted, to within its standard error

*Lab 1.2, step 2*

| Term | Planted | Estimate |
| --- | --- | --- |
| household size | 0.095 | 0.0943 |
| social band | -0.450 | -0.4474 |
| villa band | 0.400 | 0.3918 |
| temperature, per degree | 0.030 | 0.0299 |
| sigma | 0.300 | 0.3023 |

Solution run of lab 1.2, full mode, 40,000 simulated households.

#### [day1#coverage] Over 200 fake data sets, 94% of the intervals hold the planted value

*Lab 1.2, step 3*

Figure: 200 estimates of the size coefficient; the planted value in coral.

- The spread of the 200 estimates, 0.00083, matches one fit's standard error, 0.00079.
- 94% is within simulation noise of 95%.
- Coverage is a claim you can test, not a property you trust.

#### [day1#omitted-band] Leave out the band and the size coefficient drifts, with no warning

*Lab 1.2, step 4*

- **0.095** planted
- **0.0943** with the band
- **0.0761** without the band

> **Why.** Social-tariff households are larger (5.5 people against 4.2 on standard) and, in this fake world, use much less. Without the band, size absorbs part of the band's shift.

#### [day1#fake-data-limits] Fake data test the method, never the world

*The limit*

- **They show.** The code is right; the estimator recovers what it should; intervals cover; a term left out biases what you expect.
- **They cannot show.** That the real bills follow your model. That comes from checking the fit against the data: Day 3.

> **Habit.** Before any new model in the capstone, simulate from it once and fit it.

#### [day1#check-fake-data] What does a perfect recovery prove?

*Checkpoint*

**Question:** You simulate bills from a model with a temperature spline, fit the same model and recover every coefficient within its interval; coverage over 200 repeats is 95%. What have you shown?

- A. That Sahil's real bills follow a temperature spline
- B. That the temperature effect is causal
- C. That the real model's intervals will cover 95%
- D. That the code and the estimator work when the model is right

#### [day1#lab-1-2] Fake data first

Lab 1.2 · 25 min

Simulate monthly consumption for 40,000 households from a known model, recover its coefficients, count the coverage of the intervals over repeated simulations and see the bias of a model that leaves out the tariff band.

[D1_2_fake_data.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D1_2_fake_data.ipynb)

- [ ] Write the simulator with known coefficients (7 min)
- [ ] Fit and compare estimates with the truth (4 min)
- [ ] Coverage of the size interval over repeated simulations (7 min)
- [ ] Leave out the band and watch the size coefficient (5 min)
- [ ] Write the recovery table (2 min)
- [ ] ✱ Stretch: Make the error spread grow with household size and repeat the coverage count

### Session 3: Transformations and splines

#### [day1#s3] Transformations and splines

*Session 3*

- Fit a model of log consumption and read its coefficients as percentages
- Replace a straight temperature term with a spline and compare the fits
- Plot a fitted curve with its band and back-transform it correctly

#### [day1#log-scale] On the log scale, a coefficient is a percentage change

*Transformations*

- Consumption is skewed, and a hot month adds a share, not a fixed amount.
- A coefficient b on log consumption means about **100 × (eb − 1)%** per unit.
- The straight temperature term in lab 1.3: 3.0% more per degree, at every temperature.

- **Rule of thumb.** For b below 0.1, the percentage is close to 100 × b. For 0.40 it is 49%, not 40%.

#### [day1#straight-line-misses] A straight temperature term is too high in mild months and too low in hot ones

*Lab 1.3, step 2*

Figure: Mean residual in each two-degree bin, 40,000 bills. Lab 1.3 solution run.

#### [day1#what-a-spline-is] A spline lets the data choose the curve; you choose only how flexible

*A flexible term*

- Polynomial pieces joined smoothly at knots.
- `bs(temperature_c, df=5)`: five columns; the model weights them.
- More degrees of freedom bend more; cross-validation can pick (the stretch item).
- Its coefficients mean nothing alone: read the curve.

```python
smf.ols("log_m3 ~ household_size + tariff_band"
        " + bs(temperature_c, df=5)", data=b).fit()
```

> **Outside the data.** A spline says nothing beyond 16 to 42 °C. Predictions there need a stated reason.

#### [day1#temp-curve] Consumption is flat until about 28 °C, then doubles by 40 °C

*Lab 1.3, step 4*

Figure: Four people, standard tariff: mean m³ a month. Lab 1.3.

| °C | m³ | 95% band |
| --- | --- | --- |
| 20 | 18.1 | 17.9 to 18.2 |
| 30 | 20.7 | 20.6 to 20.8 |
| 40 | 37.9 | 37.3 to 38.4 |

#### [day1#band-is-for-mean] The band is for the mean, not for one household

*Reading the band*

- **Interval for the mean.** Where the average household of this kind sits: 37.3 to 38.4 m³ at 40 °C. Narrow, because 40,000 bills pin it down.
- **Interval for one household.** Where one such household's bill may fall: many times wider, since σ is about 0.31 on the log scale.

> **Use.** Supply planning adds households up: the mean band. A single customer's complaint about a high bill: the household interval.

#### [day1#median-vs-mean] exp(prediction) is the median; the mean is about 5% higher

*Lab 1.3, step 5*

- **19.7 m³** exp(prediction) at 30 °C
- **20.7 m³** exp(prediction + σ²/2)
- **20.4 m³** observed mean, 435 such bills

> **What goes wrong.** A plan that sums exp(prediction) over households runs about 5% short, every month.

#### [day1#check-spline] What did the planner's total get wrong?

*Checkpoint*

**Question:** A planner fits log consumption with a temperature spline, takes exp of each household's prediction for August and sums them to size the district's supply. The total comes out below the meters' August total. What is the most likely reason?

- A. exp of a log-scale prediction is a median, which sits below the mean
- B. The spline has too few degrees of freedom to fit August
- C. The interval for the mean was too narrow
- D. Log models cannot be used for volumes

#### [day1#lab-1-3] A temperature spline

Lab 1.3 · 25 min

Fit log consumption with a straight temperature term and with a spline, compare them, and plot the spline's curve in cubic metres with its 95% band, using the mean and not the median on the original scale.

[D1_3_temperature_spline.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D1_3_temperature_spline.ipynb)

- [ ] Log consumption against temperature (4 min)
- [ ] The straight-line model and its residual pattern (5 min)
- [ ] The spline model and the comparison (6 min)
- [ ] The curve with its band (6 min)
- [ ] Back to cubic metres: median and mean (4 min)
- [ ] ✱ Stretch: Try three, five and eight degrees of freedom and pick one by cross-validated error

### Session 4: Interactions and marginal effects

#### [day1#s4] Interactions and marginal effects

*Session 4*

- Add an interaction and say what each of its coefficients means
- Compute an average marginal effect on the outcome scale
- Report marginal effects by group with intervals from simulation

#### [day1#interaction-meaning] An interaction gives each band its own slope for household size

*Lab 1.4, steps 1 and 2*

```python
"log_m3 ~ tariff_band * household_size
          + bs(temperature_c, df=5)"
```

| Band | Slope, log scale | Per person |
| --- | --- | --- |
| standard | 0.0956 | 10.0% |
| social | 0.0956 − 0.0219 | 7.6% |
| villa | 0.0956 + 0.0187 | 12.1% |

> **What goes wrong.** Reading −0.0219 as "the effect of size on social households". It is the difference between the social and the standard slopes.

#### [day1#percent-not-answer] A percentage per person is not what Ghaliya asked

*The question was in cubic metres*

- 12.1% of a villa's bill is many more cubic metres than 7.6% of a small flat's.
- The effect in m³ depends on each household's level: its band, size and month.
- So compute it for every household, then average: an **average marginal effect**.

#### [day1#ame-recipe] An average marginal effect: predict, add one, predict again, average

*Lab 1.4, step 3*

1. **1 · Predict** each bill as it is, in m³
2. **2 · Change** the same bill with one more person
3. **3 · Differ** subtract, bill by bill
4. **4 · Average** over the bills of each band

> **On the m³ scale.** Each prediction is exp(prediction + σ²/2), the mean back-transform of session 3.

#### [day1#interval-by-simulation] The interval comes from redoing the average under 1,000 plausible coefficient vectors

*Lab 1.4, step 4*

- Draw coefficient vectors from their estimated sampling distribution.
- Recompute the average marginal effect for each draw.
- The 2.5th and 97.5th percentiles are the 95% interval.

```python
U.contrast(f, b, "household_size",
           low=lambda x: x, high=lambda x: x + 1,
           scale="m3", by="tariff_band")
```

#### [day1#ame-bands] One more person goes with 1.6 m³ more on social and 5.0 m³ more on villa

*Lab 1.4, step 5*

Figure: Average marginal effect of household size by band, m³ a month, with 95% intervals. Lab 1.4, 40,000 bills.

#### [day1#describe-not-cause] Write the effect as a comparison of households, not as what a tariff does

*The sentence*

- **Supported.** "Among billed villa households, one more person goes with about 5.0 m³ more a month (95% interval 4.8 to 5.2)."
- **Not supported.** "The social tariff halves the water each extra person uses."

> **The course rule.** Bands are tied to income and housing. No coefficient is presented as a tariff's effect on poorer households.

#### [day1#check-interaction] What is the villa effect of one more person?

*Checkpoint*

**Question:** In a model of log consumption with a band-by-size interaction, the size coefficient is 0.096 and the villa-by-size term is 0.019. Ghaliya asks how many more cubic metres a month go with one more person in villa households. What do you report?

- A. 0.019 m³, the villa-by-size term
- B. 12.1%, from the summed slope
- C. The average over villa bills of the m³ difference from one more person, with an interval
- D. The standard band's 2.3 m³, since size works the same way

#### [day1#lab-1-4] Interaction and marginal effects

Lab 1.4 · 25 min

Add a tariff-by-household-size interaction to the spline model, compute the average effect of one more person in cubic metres a month in each band with an interval, and plot the effects.

[D1_4_interaction_effects.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D1_4_interaction_effects.ipynb)

- [ ] Fit the interaction model (4 min)
- [ ] Read the slope of each band on the log scale (5 min)
- [ ] One more person, in cubic metres, for each household (6 min)
- [ ] Average marginal effects by band with intervals (6 min)
- [ ] The effect plot and the interval table (4 min)
- [ ] ✱ Stretch: Check the course function against the marginaleffects package

#### [day1#wrap-up] Three things to keep

*Day 1 · wrap-up*

- **Question first.** Name the use and write the estimand before choosing terms.
- **Fake data first.** Recover a planted model before trusting a fit on real data.
- **Answer on the reader's scale.** Turn coefficients into m³ with an interval, averaged over the households asked about.

#### [day1#next] Day 2: Generalised linear models

*Next*

Late payment as a probability, leak reports as counts with pipe length as exposure. Finish any lab of today at home; each starts from the supplied files.

## Day 2: Generalised linear models

Families and links: late payment on the probability scale, leaks on the count scale

#### [day2#title] Generalised linear models

*SDAIA Academy · Regression and Generalised Linear Modelling*

Day 2: Families and links: late payment on the probability scale, leaks on the count scale

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-301

#### [day2#agenda] Generalised linear models

*Today*

- **Session 1 · Links and families**: The outcome decides the family: a straight line for a yes-or-no outcome predicts impossible probabilities
- **Session 2 · Reading a logistic model**: A logistic coefficient is a change in log odds; its effect on the probability depends on who the household is
- **Session 3 · Counts and exposure**: Counts need a count model, and segments of different lengths need an exposure term
- **Session 4 · Overdispersion**: When the counts vary more than the Poisson allows, its intervals are too narrow; a negative binomial model widens them

#### [day2#review-day1] Which number answers Ghaliya?

*Review of Day 1*

**Question:** A model of log monthly consumption has a size slope of 0.096 for standard households. Ghaliya asks how many more cubic metres a month go with one more person in standard households. What do you give her?

- A. 0.096
- B. About 10% more per person
- C. The average over standard bills of the m³ difference from one more person: about 2.3 (2.3 to 2.4)
- D. exp(0.096) times the median bill

### Session 1: Links and families

#### [day2#s1] Links and families

*Session 1*

- Name the family and link that fit an outcome
- Fit a linear probability model and a logistic model to the same outcome
- Show where the linear model breaks

#### [day2#late-payment-question] Which bills are likely to be paid late? The outcome is a flag

*Nidal's question*

| Band | No autopay | Autopay |
| --- | --- | --- |
| standard | 25.7% | 3.8% |
| social | 31.1% | 5.4% |
| villa | 41.2% | 6.5% |

- 21.5% of the 40,000 bills were paid late.
- A probability lives between 0 and 1.
- Near the bounds, differences are squeezed: 3.8% cannot fall by 20 points.

#### [day2#family-from-outcome] The outcome chooses the family; the link connects its mean to a straight line

*Generalised linear models*

| Outcome | Family | Link | A coefficient is |
| --- | --- | --- | --- |
| m³ a month (log) | normal | identity | a difference in log m³ |
| late or not | binomial | logit | a difference in log odds |
| leaks on a segment | Poisson or negative binomial | log | a difference in log rate |

Straight on the link scale; curved, and bounded, on the outcome's scale.

#### [day2#lpm-breaks] The straight line gives 4,369 bills a negative chance of being late

*Lab 2.1, steps 2 and 3*

- **−25 points** autopay, the same for every bill
- **4,369** predictions below 0, all on autopay
- **−0.098** the lowest predicted probability

> **What goes wrong.** A line subtracts the same 25 points from a bill at 30% and from a bill at 4%. The second has nothing left to lose.

#### [day2#decile-plot] By decile, the logistic model sits on the diagonal; the line misses at both ends

*Lab 2.1, step 5*

Figure: Mean prediction and observed rate in ten groups of 4,000 bills.

- Lowest decile: the line predicts −4.1%; 2.8% are late.
- Largest gap: 6.9 points for the line, 2.4 for the logistic model.
- In the middle the two agree.

#### [day2#when-lpm-ok] A linear probability model can describe one average difference, not probabilities

*A fair hearing*

- **Acceptable.** Predictions stay inside 0.1 to 0.9, and the question is one average difference, read as points.
- **Not acceptable.** Predicting a bill's probability, ranking households near the bounds, or any rare outcome.

> **Here.** Its −25 points matches the logistic average, −25.2. It is the bills, not the average, that the line gets wrong.

#### [day2#check-family] Which model fits the outcome?

*Checkpoint*

**Question:** A planner wants the probability that a new connection request is approved within 10 days, from the request's district, type and completeness. About 4% of incomplete requests are approved in time. Which model do you start from?

- A. A logistic model of the approved-in-time flag
- B. A linear model of the approved-in-time flag
- C. A linear model of the number of days to approval
- D. A Poisson model of the approved-in-time flag

#### [day2#lab-2-1] Linear against logistic

Lab 2.1 · 25 min

Fit late payment with a linear model and a logistic model, count the predictions below zero and above one, and compare predicted with observed rates by decile.

[D2_1_linear_vs_logistic.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D2_1_linear_vs_logistic.ipynb)

- [ ] Late-payment rates by band and autopay (4 min)
- [ ] The linear probability model (5 min)
- [ ] Predictions outside zero and one (4 min)
- [ ] The logistic model (5 min)
- [ ] Predicted against observed, by decile (7 min)
- [ ] ✱ Stretch: Compare the two models' average difference for autopay

### Session 2: Reading a logistic model

#### [day2#s2] Reading a logistic model

*Session 2*

- Convert logistic coefficients to odds ratios
- Turn a coefficient into probability differences for stated profiles
- Report a probability difference with an interval

#### [day2#odds-ratios] exp(coefficient) is an odds ratio: exact, and hard to use

*Lab 2.2, step 1*

| Term | Odds ratio | 95% interval |
| --- | --- | --- |
| autopay | 0.100 | 0.092 to 0.110 |
| each past late payment | 1.59 | 1.54 to 1.64 |
| each extra person | 1.06 | 1.05 to 1.08 |
| each extra SAR on the bill | 1.003 | 1.003 to 1.004 |

> **What goes wrong.** "Autopay cuts late payment by 90%." It multiplies the odds by 0.1; the probability falls by much less, and by a different amount for each household.

#### [day2#three-profiles] Three households Nidal recognises

*Lab 2.2, step 2*

- **A.** Social tariff, 7 people, a 180 SAR bill, 3 late payments in the past year.
- **B.** Standard tariff, 4 people, a 120 SAR bill, no late payments.
- **C.** Villa, 3 people, a 400 SAR bill, 1 late payment.

For each: the probability of a late bill without and with autopay, and the difference with an interval.

#### [day2#profiles-curve] One coefficient, three differences: 48, 17 and 41 points

*Lab 2.2, steps 3 and 4*

Figure: Each profile moves 2.3 units left on the log odds scale.

|  | Points | 95% interval |
| --- | --- | --- |
| A | −47.5 | −49.1 to −46.1 |
| B | −17.2 | −17.8 to −16.6 |
| C | −40.6 | −42.2 to −38.9 |

#### [day2#average-over-bills] Averaged over the bills described, autopay goes with 25 points less late payment

*Lab 2.2, stretch*

| Item | Value |
| --- | --- |
| all bills | −25.2 |
| standard | −22.3 |
| social | −26.5 |
| villa | −32.8 |

Average marginal effect of autopay in percentage points, lab 2.2 stretch item.

#### [day2#chose-autopay] Households chose autopay, so the difference describes them, not what promoting it would do

*Lab 2.2, step 5*

- **Write.** "Among households like A, bills on autopay were late about 48 points less often than bills without it (46 to 49)."
- **Do not write.** "Autopay would cut A's late payments by 48 points."

> **To learn the effect.** Offer autopay enrolment to a random half of A-like households and compare.

#### [day2#check-logistic] How big is the difference for this household?

*Checkpoint*

**Question:** The autopay odds ratio is 0.10. Without autopay, a household's predicted probability of a late bill is 5%. About how much lower is it for the same profile with autopay?

- A. 90 percentage points
- B. 25 percentage points
- C. 10 percentage points
- D. About 4.5 percentage points

#### [day2#lab-2-2] Three household profiles

Lab 2.2 · 25 min

Fit the late-payment model, turn the autopay coefficient into probability differences for three household profiles with intervals, and compare them with the single odds ratio.

[D2_2_three_profiles.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D2_2_three_profiles.ipynb)

- [ ] Fit the model and read the odds ratios (5 min)
- [ ] Describe the three profiles (3 min)
- [ ] Predicted probabilities with and without autopay (6 min)
- [ ] Differences with intervals (6 min)
- [ ] One sentence per profile, without causal words (5 min)
- [ ] ✱ Stretch: Compute the average marginal effect of autopay over all bills

### Session 3: Counts and exposure

#### [day2#s3] Counts and exposure

*Session 3*

- Fit a Poisson model to counts
- Use the log of the exposure as an offset
- Read coefficients as rate ratios

#### [day2#leak-question] Which mains leak more often, per kilometre, and by how much?

*Basil's question*

- 1,200 segments, weekly leak reports for 2026: 3,055 leaks.
- Segments run from 0.1 to 8 km; some entered service mid-year.
- The renewal budget goes to the mains with the highest rate.

- **The unit.** One row per segment: its year's count and its exposure, because its predictors do not change week to week.

#### [day2#exposure] A count means nothing without its exposure

*Lab 2.3, step 2*

1. **Length** kilometres of main
2. **Time** weeks in service ÷ 52
3. **Exposure** kilometre-years: 0.1 to 8 here
4. **Rate** leaks per kilometre-year

> **Other exposures.** Customers for complaints, meter-days for faults, kilometres driven for accidents.

#### [day2#offset] The offset puts log exposure in the model with its coefficient fixed at 1

*Lab 2.3, step 3*

```python
po = smf.glm("leaks ~ material + age_years + pressure_bar", data=s,
             family=sm.families.Poisson(),
             offset=np.log(s["km_years"])).fit()
```

log E[leaks] = log(km-years) + β₀ + β·x, so the β describe the rate per kilometre-year.

#### [day2#raw-vs-adjusted] Asbestos cement leaks 4.2 times as often as PVC per km, but only 1.6 times at equal age

*Lab 2.3, steps 2 and 4*

| Material | Leaks per km-year, raw |
| --- | --- |
| PVC | 1.12 |
| ductile iron | 1.71 |
| asbestos cement | 4.70 |

| Rate ratio | Poisson | 95% interval |
| --- | --- | --- |
| ductile iron | 1.09 | 0.98 to 1.22 |
| asbestos cement | 1.62 | 1.38 to 1.91 |
| age, per 10 years | 1.38 | 1.32 to 1.44 |
| pressure, per bar | 1.32 | 1.25 to 1.39 |

#### [day2#expected-counts] On the count scale: 10.4 leaks a year against 1.9 for two 2 km mains

*Lab 2.3, step 5*

- **10.4** asbestos cement, 40 years, 5 bar, 2 km
- **1.85** PVC, 10 years, 4 bar, 2 km

> **Pass the offset.** A prediction for a new main needs its exposure: `po.predict(new, offset=np.log(new["km_years"]))`.

#### [day2#check-offset] What does the offset do?

*Checkpoint*

**Question:** A colleague fits leak counts on material and age with a Poisson model and no offset. Segments of asbestos cement happen to be shorter on average. What happens to the asbestos-cement coefficient?

- A. Nothing: a Poisson model accounts for length
- B. It compares counts, not rates, so short asbestos-cement mains look less leaky than they are
- C. Its standard error grows, but the estimate is fine
- D. Only predictions change; coefficients are unaffected

#### [day2#lab-2-3] Leaks with an exposure

Lab 2.3 · 25 min

Turn weekly leak reports into a year's count per pipe segment, fit a Poisson model with log kilometre-years as an offset, and read material, age and pressure as rate ratios.

[D2_3_poisson_offset.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D2_3_poisson_offset.ipynb)

- [ ] Weekly reports into one count per segment (5 min)
- [ ] Exposure: kilometres times years in service (4 min)
- [ ] The Poisson model with an offset (6 min)
- [ ] Rate ratios with intervals (6 min)
- [ ] Expected leaks for two segments (4 min)
- [ ] ✱ Stretch: Fit length as a predictor in place of the offset and read its coefficient

### Session 4: Overdispersion

#### [day2#s4] Overdispersion

*Session 4*

- Measure dispersion from a fitted Poisson model
- Fit a negative binomial model with the same exposure
- Compare effects and intervals on the count scale

#### [day2#poisson-promise] A Poisson model promises that a count's variance equals its mean

*An assumption you can check*

- Mains of the same material and age still differ: soil, workmanship, traffic.
- That hidden leakiness adds variance the model does not know about.
- The coefficients survive; the **standard errors are too small**.

#### [day2#mean-variance] In every group the variance is above the mean; overall about 2.3 times

*Lab 2.4, steps 1 and 2*

Figure: Ten groups of 120 segments by fitted mean. Lab 2.4.

- Pearson dispersion: **2.32**; about 1 if the Poisson model fitted.
- The top group: mean 10.7, variance 153.
- The curve mean + α·mean² follows the points.

#### [day2#negative-binomial] The negative binomial adds one parameter for the extra variance

*Lab 2.4, step 3*

```python
nb = smf.negativebinomial(
    "leaks ~ material + age_years + pressure_bar",
    data=s, exposure=s["km_years"]).fit(disp=0)
```

|  | Poisson | Neg. binomial |
| --- | --- | --- |
| α | 0 | 0.60 (0.50 to 0.71) |
| AIC | 4,968 | 4,240 |

variance = μ + α·μ². With α = 0 it is the Poisson model.

#### [day2#intervals-widen] The rate ratios barely move; their intervals widen by 1.6 to 1.8 times

*Lab 2.4, step 4*

Figure: Rate ratios with 95% intervals: Poisson in coral, negative binomial in teal. Lab 2.4.

#### [day2#count-scale] Per 10 km a year, asbestos cement has about 11 more leaks than PVC

*Lab 2.4, step 5*

- **10.1** Poisson: 6.6 to 13.3
- **10.8** negative binomial: 4.7 to 16.9

> **The evidence of LO2.** Effects on the count scale with honest intervals, next to lab 2.2's differences on the probability scale.

#### [day2#check-dispersion] What does a dispersion of 2.3 change?

*Checkpoint*

**Question:** A Poisson model of leak counts has a Pearson dispersion of 2.3. Its rate ratio for asbestos cement is 1.62 with a 95% interval of 1.38 to 1.91. What should Basil expect from a negative binomial refit?

- A. A much smaller rate ratio, since the Poisson estimate is inflated
- B. The same interval, with a better AIC
- C. A similar rate ratio with an interval about one and a half times as wide
- D. No answer: counts with overdispersion need a zero-inflated model

#### [day2#lab-2-4] Dispersion and the negative binomial

Lab 2.4 · 25 min

Test the leak model's dispersion, refit it as a negative binomial model, and set rate ratios and expected counts with their intervals side by side for the two models.

[D2_4_negative_binomial.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D2_4_negative_binomial.ipynb)

- [ ] Variance against mean in groups (5 min)
- [ ] The Pearson dispersion statistic (4 min)
- [ ] The negative binomial fit (5 min)
- [ ] Standard errors and intervals side by side (6 min)
- [ ] Effects on the count scale (5 min)
- [ ] ✱ Stretch: Run the auxiliary-regression test of dispersion

#### [day2#wrap-up] Three things to keep

*Day 2 · wrap-up*

- **Family from the outcome.** A flag is binomial, a count is Poisson or negative binomial, before any fit.
- **Read on the reader's scale.** Probability differences at stated profiles; expected counts with their exposure.
- **Check the variance.** A dispersion well above 1 means the Poisson intervals are too narrow.

#### [day2#next] Day 3: Check and repair

*Next*

Qusai, the analyst who left, left five model specifications. Five problems are planted in them. Tomorrow you find them and write the diagnosis log.

## Day 3: Check and repair

Five seeded problems in a previous analyst's models, found and repaired

#### [day3#title] Check and repair

*SDAIA Academy · Regression and Generalised Linear Modelling*

Day 3: Five seeded problems in a previous analyst's models, found and repaired

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-301

#### [day3#agenda] Check and repair

*Today*

- **Session 1 · Residuals that tell you something**: Raw residuals of a yes-or-no model say nothing; binned residuals against each predictor show what the model missed
- **Session 2 · Influential observations**: A few observations can carry a fit: leverage and Cook's distance find them, and the data tell you what to do with them
- **Session 3 · Simulation-based checks**: Simulate new data from the fitted model and ask whether it looks like the data you have
- **Session 4 · Separation and error structure**: A variable that separates the outcome breaks a logistic fit, and a variance funnel breaks the classical standard errors

#### [day3#review-day2] Which statement about the leak model is right?

*Review of Day 2*

**Question:** A Poisson leak model with offset log(km-years) gives asbestos cement a rate ratio of 1.62; its dispersion is 2.3. What can Basil's note say?

- A. Asbestos-cement mains have 1.62 more leaks a year than PVC mains
- B. Asbestos cement leaks at about 1.6 times the rate of PVC at equal age and pressure, with an interval wider than the Poisson one
- C. Replacing asbestos cement with PVC will cut leaks by 38%
- D. Nothing, because the model is overdispersed

### Session 1: Residuals that tell you something

#### [day3#s1] Residuals that tell you something

*Session 1*

- Explain why raw logistic residuals are uninformative
- Draw binned residuals against a predictor with their band
- Find a missing term and show the repaired fit

#### [day3#qusai-files] Five model specifications, four questions, and nobody has checked them

*The case*

| Model | What it is for | Family |
| --- | --- | --- |
| late_v1 | monthly late-payment forecast | logistic |
| late_v2 | the "improved" version, said to fit almost perfectly | logistic |
| district_leaks | district leak rates against age and pressure | least squares |
| leaks | leaks per segment for the renewal plan | Poisson with offset |
| consumption | m³ a month for the supply plan | least squares, classical errors |

#### [day3#check-before-trust] A fit that converged has passed no check at all

*The habit*

- Every one of Qusai's models runs, converges and prints sensible-looking coefficients.
- Checks compare what the model implies with what the data show.
- Each check targets one assumption: form, influence, distribution, structure.

- **The log.** Problem, evidence, fix. One line per problem, with numbers. It is the diagnostics section of the capstone, which carries 30% of its rubric.

#### [day3#raw-residuals] Raw residuals of a yes-or-no model make two bands, whatever the model

*Lab 3.1, step 2*

- A late bill leaves 1 − p; an on-time bill leaves −p.
- Plotted against anything, they form two curved bands.
- Information appears only in **averages** of many residuals.

- **Binned residuals.** Sort by a predictor, cut into 20 bins, plot each bin's mean residual with a ±2 standard-error band. About one bin in 20 falls outside when the form is right.

#### [day3#binned-plot] Against the bill, 7 of 20 bins fall outside the band; with its log, none

*Lab 3.1, steps 3 and 4*

Figure: Mean residual in 20 bins of 2,000 bills. Lab 3.1.

- Small bills: late less often than the model says (−5.3 points).
- Middle bills: more often (+2 to +3 points).
- The largest bills: less often again.
- AIC falls from 35,947 to 35,798 with the log.

#### [day3#per-predictor] Plot against each predictor; the fitted probability alone can hide the problem

*Why per predictor*

- **7** bins outside, against the bill
- **0** against household size
- **1** against past late payments

> **What goes wrong.** A misfit in one predictor is averaged away when residuals are binned by the fitted probability, which mixes all predictors. The stretch item tests it.

#### [day3#log-line-one] A log line names the problem, the evidence with its number, and the fix

*Lab 3.1, step 5*

| Problem | Evidence | Fix |
| --- | --- | --- |
| missing non-linear term | late_v1: 7 of 20 binned residuals against bill_sar outside the 2-SE band, negative for small bills | np.log(bill_sar): 0 bins outside; AIC 35,947 to 35,798 |

> **Not acceptable.** "Residuals looked a bit off, so I added a log." Without the number nobody can check the claim.

#### [day3#check-binned] What does this residual plot tell you?

*Checkpoint*

**Question:** For a logistic model of meter faults, binned residuals against meter age are positive for the youngest and oldest meters and negative in between; 6 of 20 bins sit outside the band. What do you do?

- A. Nothing: some bins always fall outside
- B. Switch to a Poisson model of faults
- C. Use robust standard errors
- D. Give age a curved term, such as a spline, and plot the binned residuals again

#### [day3#lab-3-1] Binned residuals

Lab 3.1 · 25 min

Draw binned residual plots for Qusai's late-payment model, find the bill term that should be on the log scale, refit, and write the first line of the diagnosis log.

[D3_1_binned_residuals.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D3_1_binned_residuals.ipynb)

- [ ] Fit Qusai's model as he wrote it (3 min)
- [ ] Raw residuals, and why they do not help (3 min)
- [ ] Binned residuals against each predictor (8 min)
- [ ] Add the log term and refit (6 min)
- [ ] The first line of the diagnosis log (5 min)
- [ ] ✱ Stretch: Draw binned residuals against the fitted probability

### Session 2: Influential observations

#### [day3#s2] Influential observations

*Session 2*

- Compute leverage and Cook's distance for a fitted model
- Find the most influential units and refit without them
- Trace an influential unit to its cause before deciding

#### [day3#age-backwards] Qusai's district model says older mains leak less

*Lab 3.2, step 1*

**−4.5** leaks per 100 km for each year of mean age, 30 districts

- **Against lab 2.3.** On 1,200 segments, each 10 years of age went with about 38% more leaks per kilometre-year.

A fit on 30 points can be carried by a few of them.

#### [day3#districts-plot] Two districts sit far above the rest; a third sits alone at an age of 2.5 years

*Lab 3.2, step 2*

Figure: Qusai's summary: leaks per 100 km against mean main age, 30 districts.

#### [day3#leverage-cooks] Leverage is how unusual the predictors are; Cook's distance is how much the fit moves

*Lab 3.2, step 2*

| District | Leverage | Cook's distance | Why it stands out |
| --- | --- | --- | --- |
| D21 | 0.08 | 0.50 | a huge residual |
| D30 | 0.70 | 0.39 | predictors far from the rest |
| D08 | 0.07 | 0.18 | a huge residual |
| D24 | 0.25 | 0.04 | next largest |

Mean leverage 3/30 = 0.10; a common flag for Cook's distance is 4/n = 0.13.

#### [day3#dont-just-drop] Without the three, the age slope turns positive; but first ask what each district is

*Lab 3.2, steps 3 and 4*

1. **D08, D21** Kilometres a tenth of the segment table's: keyed in tens of km
2. **Correct** Recompute from segments.csv
3. **D30** Real: a new district of young mains at high pressure
4. **Keep** Report with and without it

> **What goes wrong.** Dropping points until the fit looks right. Errors are corrected; real units stay.

#### [day3#aggregation-loses] A model of 30 district averages throws away what 1,200 segments know

*A better model*

- **District averages.** 30 points; one keying error reverses a slope; age and pressure barely vary between districts.
- **Segment level.** 1,200 rows with their own age and pressure; the count model of Day 2, with exposure and the right family.

#### [day3#check-influence] What do you do with this district?

*Checkpoint*

**Question:** In a model of 30 district rates, one district has leverage 0.7 and Cook's distance 1.5. Its data are correct: a new district with unusually high pressure. What goes in the report?

- A. Keep it, and report the estimates with and without it, saying the pressure result leans on one district
- B. Delete it as an outlier, since its Cook's distance is above 1
- C. Keep it and say nothing, since the data are correct
- D. Take the log of the leak rate so that it is no longer influential

#### [day3#lab-3-2] Influential districts

Lab 3.2 · 25 min

Fit Qusai's district model of leaks per 100 km, find the three most influential districts, refit without them, then trace two to a unit error in the pipe lengths and keep the third.

[D3_2_influential_districts.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D3_2_influential_districts.ipynb)

- [ ] Fit the district model (3 min)
- [ ] Leverage and Cook's distance (6 min)
- [ ] The three districts and the refit without them (6 min)
- [ ] Recompute the kilometres from the segment table (6 min)
- [ ] The second line of the diagnosis log (4 min)
- [ ] ✱ Stretch: Compute DFBETA for the age coefficient

### Session 3: Simulation-based checks

#### [day3#s3] Simulation-based checks

*Session 3*

- Simulate replicate data sets from a fitted count model
- Choose a test statistic that matters to the question
- Judge a model by where the observed statistic falls

#### [day3#simulate-from-fit] If the model is right, data simulated from it look like the data you have

*The idea*

1. **1 · Fit** the model to the data
2. **2 · Simulate** 1,000 replicate data sets from the fit
3. **3 · Compute** a statistic that matters, in each
4. **4 · Compare** with the observed value

> **Day 1 in reverse.** Fake data checked the method; these replicates check the model against the data.

#### [day3#choose-statistic] Choose a statistic the model was not fitted to match

*Lab 3.3, step 1*

- **Total leaks.** Useless: a Poisson model reproduces 3,055 by construction.
- **Share with no leak.** 36.4% of segments. Basil plans inspection crews with it.
- **Largest count.** 75 leaks on one segment. The worst main sets the repair budget.

#### [day3#zeros-plot] No Poisson replicate has as many zero-leak segments as Sahil; the negative binomial does

*Lab 3.3, steps 2 to 4*

Figure: Share of segments with no leak in 1,000 replicate years from each fit. Lab 3.3.

#### [day3#nb-simulation] A negative binomial count is a Poisson count with a gamma-distributed rate

*Lab 3.3, step 3*

```python
def replicate_nb(mu, alpha, R, gen):
    lam = mu * gen.gamma(1 / alpha, alpha, size=(R, len(mu)))   # mean 1, variance alpha
    return gen.poisson(lam)
```

Each replicate gives each segment its own hidden leakiness: exactly what the Poisson model leaves out.

#### [day3#zero-inflation] Reach for a zero-inflated model only when the simpler one fails the check

*The next model*

- Excess zeros against a Poisson model are often just overdispersion.
- Here the negative binomial reproduces both the zeros and the largest count.
- A zero-inflated model would need its own story: mains that cannot leak at all.

#### [day3#check-simulation] Which check would reveal the problem?

*Checkpoint*

**Question:** A Poisson model of complaints per district-month will be used to staff the call centre for the busiest months. You can simulate 1,000 replicate years from it. Which statistic makes the most useful check?

- A. The total number of complaints in the year
- B. The mean temperature of the months
- C. The largest monthly count in any district
- D. The coefficient of temperature

#### [day3#lab-3-3] The share of zeros

Lab 3.3 · 25 min

Simulate replicate leak counts from the Poisson and negative binomial fits, compare the share of segments with no leak and the largest count with the observed values, and log the result.

[D3_3_share_of_zeros.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D3_3_share_of_zeros.ipynb)

- [ ] Observed share of zeros and largest count (3 min)
- [ ] Simulate from the Poisson fit (7 min)
- [ ] Simulate from the negative binomial fit (6 min)
- [ ] Where the observed values fall (5 min)
- [ ] The third line of the diagnosis log (4 min)
- [ ] ✱ Stretch: Add the uncertainty of the coefficients to the simulation

### Session 4: Separation and error structure

#### [day3#s4] Separation and error structure

*Session 4*

- Recognise separation from its symptoms
- Repair a separated fit and say why the variable does not belong
- Use heteroskedasticity-consistent standard errors on a funnel

#### [day3#too-good] A coefficient of 27 with a standard error of 6,675 is a symptom, not a finding

*Lab 3.4, step 1*

| late_v2 term | Coefficient | Std. error |
| --- | --- | --- |
| log bill | 0.88 | 0.05 |
| autopay | −2.30 | 0.05 |
| notice_sent | 27.2 | 6,675 |

- A convergence warning.
- AIC 28,434 against 35,798: "almost perfect".
- One term's standard error in the thousands.

#### [day3#separation-table] Every one of the 2,622 bills with a notice was late: the notice follows the outcome

*Lab 3.4, step 2*

| notice_sent | on time | late |
| --- | --- | --- |
| 0 | 31,406 | 5,972 |
| 1 | 0 | 2,622 |

- **The repair.** Remove it. A disconnection notice is sent after a bill is 30 days late: a consequence of the outcome cannot predict it.

> **When the separating variable is legitimate** (a rare category with no late bills), use a penalised fit, such as Firth's method or a small ridge penalty, and say so.

#### [day3#funnel] In cubic metres, the residual spread grows almost fourfold with the fitted value

*Lab 3.4, step 3*

Figure: Qusai's consumption model on the m³ scale, 40,000 bills. Lab 3.4.

- 4.9 m³ in the lowest decile, 19.3 in the highest.
- Classical standard errors assume one spread for every bill.
- The estimates are fine; their uncertainty is not.

#### [day3#hc3] Heteroskedasticity-consistent errors change the uncertainty, not the estimates

*Lab 3.4, step 4*

| Term | Estimate, m³ | Classical SE | HC3 SE | Ratio |
| --- | --- | --- | --- | --- |
| household size | 2.63 | 0.026 | 0.033 | 1.31 |
| social band | −5.75 | 0.122 | 0.103 | 0.85 |
| villa band | 16.06 | 0.134 | 0.187 | 1.40 |

Not always wider: the social band sits where the spread is small, so its robust error is smaller.

#### [day3#the-log] Five problems, five pieces of evidence, five repairs

*Lab 3.4, step 5*

| Problem | Evidence | Fix |
| --- | --- | --- |
| missing non-linear term | 7 of 20 bins outside, against the bill | log of the bill |
| influential districts | D21, D30, D08 reverse the age slope | correct D08 and D21; report with and without D30 |
| overdispersion | 36.4% zeros; Poisson replicates at most 31.0% | negative binomial |
| separation | notice_sent: 27.2 with SE 6,675 | remove a post-outcome flag |
| non-constant variance | spread 3.9 times larger at the top | HC3, or the log model |

#### [day3#check-separation] What explains this fit?

*Checkpoint*

**Question:** A logistic model of whether a customer cancels includes "closing letter printed". Its coefficient is 31 with a standard error of 9,000, and the model's AIC is far better than without it. What is the likely explanation?

- A. The letter is by far the strongest driver of cancelling
- B. The letter is printed only for customers who cancel, so it separates the outcome and must be removed
- C. The sample is too small; collect more months
- D. Use HC3 standard errors and keep the term

#### [day3#lab-3-4] Separation and robust errors

Lab 3.4 · 25 min

Repair Qusai's logistic fit, which a notice flag separates, then find the funnel in his consumption model, set classical and heteroskedasticity-consistent errors side by side, and close the diagnosis log with the corrected models.

[D3_4_separation_hc.ipynb](https://sdaiaacademy.github.io/ds-301/labs/D3_4_separation_hc.ipynb)

- [ ] The separated fit and its symptoms (5 min)
- [ ] The cross-table that explains it, and the repair (5 min)
- [ ] The funnel in the consumption model (5 min)
- [ ] Classical against robust standard errors (5 min)
- [ ] The full diagnosis log and the corrected models (5 min)
- [ ] ✱ Stretch: Fit the separated model with a small penalty and compare

#### [day3#wrap-up] Three things to keep

*Day 3 · wrap-up*

- **One tool per assumption.** Binned residuals for form, influence for single units, replicates for the distribution.
- **Trace before you delete.** Errors are corrected; real units stay and are reported both ways.
- **Log with numbers.** Problem, evidence, fix: the diagnostics section of your capstone.

#### [day3#next] Day 4: Grouped data and many predictors

*Next*

Households grouped in districts of very different sizes, 120 candidate predictors, and a report Ghaliya can read. Tomorrow you also choose your capstone brief.

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

## Capstone: Capstone project presentations

An eight-minute defence of a regression analysis, then four minutes of questions

#### [capstone#title] Capstone project presentations

*SDAIA Academy · Regression and Generalised Linear Modelling*

Capstone: An eight-minute defence of a regression analysis, then four minutes of questions

Data Science Track · 4 teaching days + capstone day · 8 min talk and demo · 4 min Q&A · DS-301

#### [capstone#agenda] How the day runs

*Capstone*

- **Expectations and final preparation**: the rubric, the defence, a last rerun from the raw data
- **Defences**: each defence, then questions in which the assessor changes the model
- **Review and closing**: peer feedback, the trainer's review, what next

#### [capstone#rubric] The rubric

*How defences are scored*

| Item | Value |
| --- | --- |
| Specification | 20% |
| Diagnostics | 30% |
| Uncertainty | 20% |
| Interpretation | 20% |
| Reproducibility | 10% |

> **Every check with its number.** A diagnostic named without its evidence and its fix scores as not done.

#### [capstone#format] 8 minutes of defence, then 4 minutes of questions

*Format*

- **1 · The brief.** The question, the use and the estimand. One slide or one README section.
- **2 · The model and its checks.** Terms, family, diagnostics: what failed and what you changed.
- **3 · Effects and limits.** In the reader's units with intervals, and what they do not mean.

> **Peer feedback.** After each defence, everyone writes one strength, one question and one suggestion.

#### [capstone#the-question-round] The assessor changes one term or the family; you predict the result before re-running

*The 4 minutes of questions*

- "Drop the interaction: what happens to the villa effect?"
- "Use Poisson instead: which interval narrows?"
- "Remove the district term: what happens to the programme's standard error?"

- **What is scored.** The direction and rough size of the change, and the reason. A wrong prediction with the right reasoning still earns credit.

#### [capstone#running-order] Who defends when

*Running order*

| # | Participant | Brief |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#final-prep] Final preparation · 20 minutes

*Before the first defence*

Clone your repository into a fresh folder and rerun the notebook from the raw data. Then rehearse once.

#### [capstone#now-presenting] Defence

*Now defending*

##### Questions

#### [capstone#review] What the defences showed

*Trainer review*

- **Strongest patterns.** What several analyses got right.
- **Common gaps.** What most analyses would fix next.
- **Planted problems found.** Which briefs' hidden problems were caught, and by which check.

#### [capstone#what-next] Keep going

*After the course*

- **Follow-up task:** critique a published regression from your own field with the checklist in labs/followup/README.md
- **Your repository stays yours:** keep it rerunnable and add the next check you named today
- **Next Academy courses:** DS-303 Causal Inference from Observational Data, DS-305 Uncertainty, Interpretability and Model Validation, DS-401 Bayesian Modelling and Decisions under Uncertainty

#### [capstone#thanks] Thank you

*SDAIA Academy*

Regression and Generalised Linear Modelling
