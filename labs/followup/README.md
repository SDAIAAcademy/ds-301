# Follow-up task: critique a published regression

A tracked task after the course. You choose one published regression analysis from your own field and critique it in writing with the checks of this course. It takes about two hours.

## What to choose

A report, paper or public dashboard that fits a regression or a generalised linear model and draws a conclusion from it: a ministry report, an annual report of a utility or a hospital, a journal article, a consultancy study. It must state at least one coefficient, effect or prediction with enough detail to check. Use a published source only; never a colleague's unpublished work or anything that contains personal data.

## The checklist

Answer each question in one to three sentences, quoting the source where you can.

1. **The question and the use.** What question does the analysis answer? Is its use descriptive, predictive or causal, and is that what its conclusion claims?
2. **The estimand.** Which quantity, for which population, compared with what? Is it stated, or do you have to infer it?
3. **The outcome and the family.** Is the family fit for the outcome (a count with an exposure, a yes-or-no outcome, a positive quantity)? Is there an exposure that should be an offset?
4. **The terms.** Are curved relations and interactions considered where the subject suggests them? Is any predictor a consequence of the outcome?
5. **The diagnostics.** Which checks are reported: residuals against predictors, influence, dispersion, simulation from the fit? Which would you have asked for?
6. **The level of the evidence.** Do predictors vary only between groups (schools, districts, hospitals)? Are the standard errors clustered or the groups modelled?
7. **Selection.** Were predictors chosen from many candidates? Is the stability of the choice reported, and were the effects estimated on the same data that chose them?
8. **Effects in the reader's units.** Are the effects translated from log odds or log rates into units a reader can act on, with intervals?
9. **Limits.** Which limits are stated? Which one most needs adding?
10. **Your verdict.** In three sentences: what the analysis supports, what it does not, and the one change that would most improve it.

## What to submit

A Markdown file of at most 800 words with the full reference of the source, the answers to the ten questions, and your verdict. Add it to your capstone repository as `followup.md`, or submit it as your trainer directs.

## How it is read

The trainer reads for the use of the course's checks, not for agreement with the source. A critique that finds nothing wrong is acceptable when every check is answered with evidence from the source.
