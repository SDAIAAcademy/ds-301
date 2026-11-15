---
course: "Regression and Generalised Linear Modelling"
code: "DS-301"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-301/slides/day3.html"
---

# Regression and Generalised Linear Modelling

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
