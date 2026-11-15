---
course: "Regression and Generalised Linear Modelling"
code: "DS-301"
version: "2027.1.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-301/slides/day1.html"
---

# Regression and Generalised Linear Modelling

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
