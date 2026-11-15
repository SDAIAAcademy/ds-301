# Regression and Generalised Linear Modelling: labs

Hands-on notebooks for the SDAIA Academy course **DS-301 Regression and Generalised Linear Modelling (الانحدار والنماذج الخطية المُعمَّمة)**. Every lab works on **Sahil Water (شركة ساحل للمياه)**, a fictional utility with 40,000 households in 30 districts. Each lab starts from supplied files, so none depends on an earlier one, and each ends with a short verification note: what was checked against the generator's truth and what was not.

**Nothing calls or downloads a model.** A laptop processor or a Colab CPU runtime is enough. The optional hint-only tutor, Sadeed, is an instruction file, `tutor_instruction.md`, that you paste into an assistant your Academy has approved.

## Quick start

**Google Colab.** Open a notebook from the [course page](https://sdaiaacademy.github.io/ds-301/), or directly: `https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/<notebook>.ipynb`. Run the first cell: it clones this repository and installs `requirements-colab.txt`.

**Local**
```bash
git clone https://github.com/SDAIAAcademy/ds-301
cd ds-301/labs
uv sync                          # creates the environment from pyproject.toml (uv.lock pins every version)
uv run jupyter lab
```
Run `00_setup_check.ipynb` once before Day 1. It imports the libraries, reads every data file and fits one model.

| Setting | Default | Meaning |
|---|---|---|
| `DS301_QUICK` | `0` | `1` runs fewer simulations, repeats and bootstrap samples, for a fast pass |

**Windows and long folder paths.** If an import fails with "The filename or extension is too long", keep the environment in a short folder: set `UV_PROJECT_ENVIRONMENT` to a short path (for example a folder at the root of your drive) before `uv sync`.

## Notebooks

| Day | Session | Notebook |
|---|---|---|
| 0 | Setup | [`00_setup_check.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/00_setup_check.ipynb) |
| 0 | Pre-work: simple regression | [`P0_prework_simple_regression.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/P0_prework_simple_regression.ipynb) |
| 1 | Three uses of a regression | [`D1_1_three_uses.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D1_1_three_uses.ipynb) |
| 1 | Fake data first | [`D1_2_fake_data.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D1_2_fake_data.ipynb) |
| 1 | A temperature spline | [`D1_3_temperature_spline.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D1_3_temperature_spline.ipynb) |
| 1 | Interaction and marginal effects | [`D1_4_interaction_effects.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D1_4_interaction_effects.ipynb) |
| 2 | Linear against logistic | [`D2_1_linear_vs_logistic.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D2_1_linear_vs_logistic.ipynb) |
| 2 | Three household profiles | [`D2_2_three_profiles.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D2_2_three_profiles.ipynb) |
| 2 | Leaks with an exposure | [`D2_3_poisson_offset.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D2_3_poisson_offset.ipynb) |
| 2 | Dispersion and the negative binomial | [`D2_4_negative_binomial.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D2_4_negative_binomial.ipynb) |
| 3 | Binned residuals | [`D3_1_binned_residuals.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D3_1_binned_residuals.ipynb) |
| 3 | Influential districts | [`D3_2_influential_districts.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D3_2_influential_districts.ipynb) |
| 3 | The share of zeros | [`D3_3_share_of_zeros.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D3_3_share_of_zeros.ipynb) |
| 3 | Separation and robust errors | [`D3_4_separation_hc.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D3_4_separation_hc.ipynb) |
| 4 | Clustered standard errors | [`D4_1_clustered_errors.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D4_1_clustered_errors.ipynb) |
| 4 | Partial pooling | [`D4_2_partial_pooling.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D4_2_partial_pooling.ipynb) |
| 4 | Ridge and lasso | [`D4_3_ridge_lasso.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D4_3_ridge_lasso.ipynb) |
| 4 | A one-page model report | [`D4_4_model_report.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-301/blob/main/labs/D4_4_model_report.ipynb) |

Exercises are marked **✏️ Exercise** and raise `NotImplementedError` until you fill them in; the cell after each one then uses a stored reference result, so the rest of the notebook still runs. Complete reference versions are in `solutions/`. Cells marked **✱ Stretch** are optional. Self-checks print ✅ or ❌.

**Assistant policy.** The supervised checks and each lab's first fit and interpretation are done without an assistant. In the other steps and the stretch items the tutor instruction may hint one step at a time; it never writes model code. The capstone is open to an assistant and is defended live.

## The case study: Sahil Water

Synthetic and deterministic (seed 301), written by `prepare_data.py`. No real utility, household, district or person is described.

| Data | File | Contents |
|---|---|---|
| Districts | `data/districts.csv` | 30 districts, from 40 to 9,423 households: coastal or inland, temperature offset, pressure management |
| Bills | `data/bills.csv` | 40,000 households, one month each: pseudonymised key, district, tariff band, household size, month, temperature, consumption in m³, bill in SAR, autopay, late payments in the past 12 months, a late-payment flag, a notice flag |
| Pipe segments | `data/segments.csv` | 1,200 segments: district, length in km, material, age, pressure, weeks in service |
| Weekly leak reports | `data/leaks.csv` | one row per segment and week in service, with the week's count of leaks |
| The previous analyst's summary | `data/qusai/district_leaks.csv` | leaks per 100 km by district, as he sent it (Day 3) |
| Candidate predictors | `data/candidates.csv`, `data/candidates_key.json` | 2,000 households with 126 candidate columns and next August's log consumption (lab 4.3) |
| Claims | `data/claims.json`, `data/claims_key.json` | the five claims of lab 1.1 and their key, written for this course |
| Reference results | `data/reference/` | what each exercise returns in the solution run, for the safety nets (full and quick mode) |

**Handled as personal data.** The bills are synthetic, and the labs still treat them as personal data under the Personal Data Protection Law: households appear only as pseudonymised keys, results are reported by band or district and never by household, and lab 4.3 removes the columns that a planning purpose cannot justify.

What is planted and which lab finds it is in `solutions/answer_key.md`, for the trainer; the generator's true parameters are in `solutions/truth.json`.

## Capstone and follow-up

- `capstone/README.md`: the three briefs, their datasets and what the repository must contain.
- `followup/README.md`: the follow-up task, a critique of a published regression from your own field.

## For authors

The notebooks are generated from the percent-format sources in `_src/` by `_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions to `solutions/`. Edit the sources, not the notebooks. A solution run with `DS301_STRICT=1` stops at the first failed check; with `DS301_WRITE_REF=1` it rewrites `data/reference/`.
