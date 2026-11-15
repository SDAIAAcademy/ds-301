---
course: "Regression and Generalised Linear Modelling"
code: "DS-301"
version: "2027.1.0"
deck: "day2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-301/slides/day2.html"
---

# Regression and Generalised Linear Modelling

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
