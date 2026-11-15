# Regression and Generalised Linear Modelling: labs

## Quick start

- Google Colab: open a notebook from the course page; its first cell clones this repository.
- Locally: clone the repository, then open the notebooks in `labs/` with Jupyter.

| Unit | Session | Notebook |
|---|---|---|
| Day 1 | Session 1 · A regression answers a question | [`D1_1_label_five_published.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D1_1_label_five_published.ipynb) |
| Day 1 | Session 2 · Fake data first | [`D1_2_simulate_consumption_from.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D1_2_simulate_consumption_from.ipynb) |
| Day 1 | Session 3 · Transformations and splines | [`D1_3_fit_log_consumption.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D1_3_fit_log_consumption.ipynb) |
| Day 1 | Session 4 · Interactions and marginal effects | [`D1_4_add_tariff_household.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D1_4_add_tariff_household.ipynb) |
| Day 2 | Session 1 · Links and families | [`D2_1_fit_late_payment.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D2_1_fit_late_payment.ipynb) |
| Day 2 | Session 2 · Reading a logistic model | [`D2_2_turn_coefficients_into.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D2_2_turn_coefficients_into.ipynb) |
| Day 2 | Session 3 · Counts and exposure | [`D2_3_model_leak_reports.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D2_3_model_leak_reports.ipynb) |
| Day 2 | Session 4 · Overdispersion | [`D2_4_test_dispersion_refit.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D2_4_test_dispersion_refit.ipynb) |
| Day 3 | Session 1 · Residuals that tell you something | [`D3_1_find_missing_non.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D3_1_find_missing_non.ipynb) |
| Day 3 | Session 2 · Influential observations | [`D3_2_find_three_most.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D3_2_find_three_most.ipynb) |
| Day 3 | Session 3 · Simulation-based checks | [`D3_3_test_whether_count.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D3_3_test_whether_count.ipynb) |
| Day 3 | Session 4 · Separation and error structure | [`D3_4_repair_separated_logistic.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D3_4_repair_separated_logistic.ipynb) |
| Day 4 | Session 1 · Clustered data | [`D4_1_set_naive_district.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D4_1_set_naive_district.ipynb) |
| Day 4 | Session 2 · Partial pooling | [`D4_2_fit_random_intercept.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D4_2_fit_random_intercept.ipynb) |
| Day 4 | Session 3 · Penalised regression | [`D4_3_tune_ridge_lasso.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D4_3_tune_ridge_lasso.ipynb) |
| Day 4 | Session 4 · Reporting a model | [`D4_4_draft_one_page.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D4_4_draft_one_page.ipynb) |

The notebooks are generated from the percent-format sources in `labs/_src/` by `labs/_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions to `labs/solutions/`. Edit the sources, not the notebooks.
