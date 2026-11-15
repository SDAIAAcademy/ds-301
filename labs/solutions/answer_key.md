# Answer key for trainers

What each lab plants, what a correct run shows, and the numbers to expect in full mode (`DS301_QUICK=0`). Quick mode uses fewer simulations, so its numbers differ slightly. The complete solutions are the notebooks in this folder; the generator's true parameters are in `truth.json`. Participants can read this folder: it is public with the rest of the repository.

## Pre-work

| Notebook | What a correct run shows |
|---|---|
| P0 Simple regression | On the standard tariff, 2.34 m³ a month per extra person (2.27 to 2.41); residual spread grows with household size; for a five-person household the mean is 25.1 m³ (25.0 to 25.2) while one new household lies between 6.5 and 43.7 m³ |

## Day 1 · Linear models that answer a question

| Lab | Planted | What a correct run shows |
|---|---|---|
| 1.1 Three uses | Five fictional claims, each with a stated use (`data/claims.json`) | Claims 2, 3 and 4 are supported (prediction checked afterwards; a one-year description; a randomised letter). Claims 1 and 5 are not: a comparison of different households, and a prediction read as an effect |
| 1.2 Fake data first | Known coefficients, including social −0.45 | The fit recovers every coefficient; 95% intervals cover about 94% of the time; omitting tariff band biases the household-size slope from 0.095 to 0.076 |
| 1.3 A temperature spline | A curved temperature effect, steeper above 28 °C | A straight term leaves a U-shaped residual pattern; a spline with 5 degrees of freedom removes it (AIC 23,573 to 21,067); 20.7 m³ at 30 °C and 37.9 m³ at 40 °C |
| 1.4 Interaction and marginal effects | Household-size slopes that differ by band | Average marginal effect per extra person: social 1.6 m³ (1.5 to 1.7), standard 2.3 (2.3 to 2.4), villa 5.0 (4.8 to 5.2) |

## Day 2 · Generalised linear models

| Lab | Planted | What a correct run shows |
|---|---|---|
| 2.1 Linear against logistic | A binary late-payment outcome | The linear probability model predicts below zero for 4,369 bills; by decile the logistic predictions lie on the diagonal |
| 2.2 Three household profiles | Autopay, chosen by households | Differences in percentage points depend on the profile: about −48, −17 and −41 points for profiles A, B and C; odds ratio 0.10 for autopay throughout. All statements stay descriptive |
| 2.3 Leaks with an exposure | Leaks per kilometre-week; asbestos cement and pressure raise the rate | With log(km-years) as an offset: asbestos cement 1.62 (1.38 to 1.91) against PVC, 1.32 per bar of pressure; without the offset long segments dominate |
| 2.4 Dispersion and the negative binomial | A gamma frailty per segment (α = 0.67) | Pearson dispersion 2.3; negative binomial α 0.60 (0.50 to 0.71); intervals 1.6 to 1.8 times as wide; AIC 4,968 to 4,240 |

## Day 3 · Diagnosis and repair: the five planted problems

All five are in Qusai's files, `data/qusai/`. The log of lab 3.4 must name at least four, each with evidence and a fix.

| Lab | Problem | Evidence | Fix |
|---|---|---|---|
| 3.1 | Missing non-linear term in `late_v1` | 7 of 20 binned residuals against the bill outside the band | log of the bill: 0 outside; AIC 35,947 to 35,798; coefficient 0.85 against 0.90 planted |
| 3.2 | Influential districts in `district_leaks` | Cook's distance: D21 0.50, D30 0.39, D08 0.18; age −4.5 with all, +2.8 without the three | D08 and D21 had kilometres keyed a tenth too small: recompute from `segments.csv` (age +5.3, 0.3 to 10.4). D30 is real: report with and without it (+2.7 without) |
| 3.3 | Overdispersion in `leaks` | 36.4% of segments without a leak; Poisson replicates 23.3% to 31.0% | Negative binomial: replicates 32.6% to 42.3%, tail share 0.48 |
| 3.4 | Separation in `late_v2` | `notice_sent` 27.2 with SE 6,675; all 2,622 bills with a notice were late | Remove it: the notice is sent after a bill is 30 days late |
| 3.4 | Non-constant variance in `consumption` | Residual SD 4.9 m³ in the lowest decile of fitted values, 19.3 in the highest | HC3 errors (household size ratio 1.31, villa 1.40, social 0.85) or the log model |

## Day 4 · Grouped data and many predictors

| Lab | Planted | What a correct run shows |
|---|---|---|
| 4.1 Clustered standard errors | District levels with SD 0.10; programme set per district | Programme −7.8%: naive SE 0.0032, clustered 0.0435 (ratio 13.7); household size ratio 0.94; district bootstrap SE 0.0430 |
| 4.2 Partial pooling | Districts from 40 to 9,423 bills | District SD 0.079, residual 0.301, share between districts 6.4%; D13 keeps 73% of its raw effect, D30 80%; programme −10.3% (−15.4% to −5.0%) in the mixed model |
| 4.3 Ridge and lasso | Six personal columns; 8 true predictors among 120 correlated ones | The six are removed before modelling; ridge keeps 120; one lasso fit selects 27; 8 are selected in all 100 bootstrap samples, and they are the true ones |
| 4.4 Model report | Stored results of labs 1.3, 1.4, 3.4 and 4.2 | A page of about 250 words with the five parts; a capstone brief with its use and estimand. A causal use is defensible only for C2 |

## Capstone briefs

The planted problems of the three briefs are listed under `capstone` in `truth.json`. In the defence, credit the participant who finds the planted problem with a diagnostic and repairs it, and also the one who misses it but reports diagnostics that would have found it with a different statistic.
