# Revision P0 Findings

## Purpose

This note records the first round of experiments triggered by the major-review criticism on evaluation protocol, grouped split robustness, and uncertainty analysis.

## What Changed

1. Evaluation runners now distinguish between `valid` and `test` partitions explicitly.
2. A deterministic `doi_grouped_split.json` was added for stricter generalization testing.
3. Tuned logistic and `poly_core_v1` were rerun on:
   - random split / validation
   - random split / test
   - DOI-grouped split / validation
   - DOI-grouped split / test
4. Paired bootstrap comparison was added for final random-test and DOI-grouped-test comparisons.

## New Artifacts

### Split files

- [random_split.json](/D:/projects/paper_writing/polysaccharidesdb/data_processed/splits_publishable_supervised_v2/random_split.json)
- [doi_grouped_split.json](/D:/projects/paper_writing/polysaccharidesdb/data_processed/splits_publishable_supervised_v2/doi_grouped_split.json)

### Corrected protocol results

- [tuned_logistic_random_valid_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/logistic_random_valid/tuned_logistic_random_valid_summary.json)
- [poly_core_random_valid_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/poly_core_random_valid/poly_core_random_valid_summary.json)
- [tuned_logistic_random_test_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/logistic_random_test/tuned_logistic_random_test_summary.json)
- [poly_core_random_test_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/poly_core_random_test/poly_core_random_test_summary.json)
- [tuned_logistic_doi_valid_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/logistic_doi_valid/tuned_logistic_doi_valid_summary.json)
- [poly_core_doi_valid_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/poly_core_doi_valid/poly_core_doi_valid_summary.json)
- [tuned_logistic_doi_test_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/logistic_doi_test/tuned_logistic_doi_test_summary.json)
- [poly_core_doi_test_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/poly_core_doi_test/poly_core_doi_test_summary.json)

### Bootstrap comparisons

- [bootstrap_random_test_macro_f1.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/bootstrap_random_test_macro_f1.json)
- [bootstrap_random_test_exact.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/bootstrap_random_test_exact.json)
- [bootstrap_doi_test_macro_f1.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/bootstrap_doi_test_macro_f1.json)
- [bootstrap_doi_test_exact.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/bootstrap_doi_test_exact.json)

## Key Numerical Results

### Random split

- validation:
  - tuned logistic: `macro_f1 = 0.3143`
  - `poly_core_v1`: `macro_f1 = 0.3152`
- test:
  - tuned logistic: `macro_f1 = 0.2610`
  - `poly_core_v1`: `macro_f1 = 0.2678`

### DOI-grouped split

- validation:
  - tuned logistic: `macro_f1 = 0.1189`
  - `poly_core_v1`: `macro_f1 = 0.1218`
- test:
  - tuned logistic: `macro_f1 = 0.1250`
  - `poly_core_v1`: `macro_f1 = 0.1140`

## Bootstrap Interpretation

### Random test, macro-F1

- observed delta (`poly_core_v1 - tuned logistic`): `+0.0068`
- 95% CI: `[-0.0115, 0.0260]`
- two-sided bootstrap p-value: `0.448`

Interpretation:

- The random-split gain is directionally positive, but not statistically convincing under paired bootstrap.

### DOI-grouped test, macro-F1

- observed delta (`poly_core_v1 - tuned logistic`): `-0.0110`
- 95% CI: `[-0.0254, 0.0020]`
- two-sided bootstrap p-value: `0.108`

Interpretation:

- Under stricter DOI-grouped generalization, the current final method does not retain its random-split advantage and is directionally worse than the tuned logistic anchor.

## Scientific Consequence

This revision materially changes the paper risk profile.

What remains supported:

1. The benchmark problem is real and technically nontrivial.
2. A tuned sparse logistic baseline is very strong.
3. The feature ablation still provides useful structural insight about MW, residue-set, and branching under the current benchmark.

What is no longer strong enough as written:

1. A generic claim that `poly_core_v1` robustly improves over the tuned anchor.
2. Any wording that suggests the gain persists under stricter grouped generalization.
3. Any claim that the random-split result alone is sufficient evidence.

## Recommended Story Update

The paper should now be reframed more conservatively:

- keep the benchmark contribution
- keep the strong tuned sparse anchor contribution
- keep the ablation-derived feature insight
- downgrade the method claim from `robust improvement` to `promising but split-sensitive structured augmentation`

## Immediate Next Steps

1. Rewrite the paper's main claim around benchmark difficulty and feature insight, not around a stable model win.
2. Add the grouped-split table and bootstrap CI to the paper.
3. Add a direct discussion of split sensitivity in the limitation or main results section.
4. Continue with weak-supervision framing and dataset-statistics supplementation.
