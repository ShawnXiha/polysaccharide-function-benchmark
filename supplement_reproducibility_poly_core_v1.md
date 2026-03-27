# Supplementary Reproducibility Note for `poly_core_v1`

## Scope

This note records the exact benchmark artifacts, split layout, tuned baseline configuration, and final representation definition used by the paper draft in:

- [paper_poly_core_v1.tex](/D:/projects/paper_writing/polysaccharidesdb/paper_poly_core_v1.tex)

It is intentionally narrower than a full repository walkthrough. The goal is to make the paper's final claim reproducible without mixing in earlier exploratory scaffolding.

## Main Benchmark Artifacts

- Supervised benchmark dataset:
  - [dataset_publishable_supervised_v1.jsonl](/D:/projects/paper_writing/polysaccharidesdb/data_processed/dataset_publishable_supervised_v1.jsonl)
- Benchmark report:
  - [dataset_publishable_supervised_v1_report.json](/D:/projects/paper_writing/polysaccharidesdb/data_interim/dataset_publishable_supervised_v1_report.json)
- Benchmark summary:
  - [dataset_publishable_supervised_v1_summary.json](/D:/projects/paper_writing/polysaccharidesdb/data_interim/dataset_publishable_supervised_v1_summary.json)
- Fixed split:
  - [random_split.json](/D:/projects/paper_writing/polysaccharidesdb/data_processed/splits_publishable_supervised_v1/random_split.json)

## Benchmark Definition

- Source retained for the main supervised task: `DoLPHiN` only
- Labels removed: `unknown`
- Label retention rule: global frequency `>= 20`
- Final record count: `4121`
- Final label count: `18`

## Fixed Split Layout

The paper uses a precomputed fixed split:

- `train = 2472`
- `valid = 824`
- `test = 825`

The main paper reports metrics on the test partition only. Stage 2 through Stage 4 intentionally reuse the same split so that later comparisons isolate representation or configuration changes.

## Tuned Logistic Anchor

Primary tuned-anchor result:

- [count_c16_balanced_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage2_tuning/results/logistic/count_c16_balanced_summary.json)

Final configuration:

- model: `OneVsRest LogisticRegression`
- solver: `liblinear`
- `C = 16.0`
- `class_weight = balanced`
- `min_df = 1`
- `max_features = 0` meaning uncapped vocabulary
- `binary = false`
- seeds: `11 / 22 / 33`
- observed deterministic behavior on the fixed split:
  - `macro_f1_mean = 0.2610`
  - `macro_f1_std = 0.0`
  - `exact_match_mean = 0.2606`

Implementation entry point:

- [run_logistic_baseline.py](/D:/projects/paper_writing/polysaccharidesdb/src/polysaccharidesdb/models/run_logistic_baseline.py)

## Final Proposed Method

Primary final-method result:

- [poly_core_v1_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage4_ablation/results/poly_core_v1_summary.json)

Final metrics:

- `macro_f1_mean = 0.2678`
- `exact_match_mean = 0.2570`
- `macro_f1_std = 0.0`

Implementation entry point:

- [run_evidence_aware_logistic.py](/D:/projects/paper_writing/polysaccharidesdb/src/polysaccharidesdb/models/run_evidence_aware_logistic.py)

Although the runner file name still reflects its Stage 3 origin, the final published method is the simplified Stage 4 configuration `poly_core_v1`, not the broad `evidence-aware` variant.

## Final `poly_core_v1` Token Families

The final method keeps only three structured token families:

1. Molecular-weight buckets
2. Branching-presence tokens
3. Residue-set tokens

These are derived by:

- parsing `mw_or_range` into coarse bins
- checking whether `branching` is informative
- extracting residue-family indicators from:
  - `canonical_representation`
  - `monomer_composition`
  - `linkage`
  - `branching`

Implementation support:

- [evidence_aware.py](/D:/projects/paper_writing/polysaccharidesdb/src/polysaccharidesdb/models/evidence_aware.py)

## Components Explicitly Removed from the Final Method

The final paper method does **not** use:

- evidence-proxy tokens
- completeness/sample weighting
- source-kingdom tokens
- modification tokens
- coarse composition-count tokens

This simplification is justified by Stage 3 and Stage 4:

- Stage 3 evolution evidence:
  - [evidence_aware_v1_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage3_method/results/evidence_aware_v1_summary.json)
  - [evidence_weight_only_v1_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage3_method/results/evidence_weight_only_v1_summary.json)
  - [evidence_feature_only_v1_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage3_method/results/evidence_feature_only_v1_summary.json)
  - [poly_feature_only_v1_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage3_method/results/poly_feature_only_v1_summary.json)
- Stage 4 ablation evidence:
  - [ablate_no_mw_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage4_ablation/results/ablate_no_mw_summary.json)
  - [ablate_no_branching_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage4_ablation/results/ablate_no_branching_summary.json)
  - [ablate_no_modification_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage4_ablation/results/ablate_no_modification_summary.json)
  - [ablate_no_residue_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage4_ablation/results/ablate_no_residue_summary.json)
  - [ablate_no_source_kingdom_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage4_ablation/results/ablate_no_source_kingdom_summary.json)
  - [ablate_no_composition_terms_summary.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/stage4_ablation/results/ablate_no_composition_terms_summary.json)

## Main-Table Interpretation Rule

The main comparison table in the paper mixes:

- reproduced baseline families
- one explicitly tuned anchor
- proposed method variants

That is intentional, but it must be read correctly:

- the upper block is a breadth-of-family comparison under a shared fixed protocol
- the lower block is a tuned-anchor-plus-method comparison
- the paper does **not** claim that every baseline family received an equally exhaustive tuning budget

## Figures Used in the Draft

- Pipeline figure:
  - [figure1_pipeline.pdf](/D:/projects/paper_writing/polysaccharidesdb/figures/figure1_pipeline.pdf)
- Main-results figure:
  - [figure2_main_results.pdf](/D:/projects/paper_writing/polysaccharidesdb/figures/figure2_main_results.pdf)
- Ablation figure:
  - [figure3_ablation.pdf](/D:/projects/paper_writing/polysaccharidesdb/figures/figure3_ablation.pdf)

Figure generation script:

- [generate_paper_figures.py](/D:/projects/paper_writing/polysaccharidesdb/scripts/generate_paper_figures.py)

## What This Supplement Does Not Claim

- It does not upgrade the current `DoLPHiN + CSDB` pipeline into a publishable cross-source biological benchmark.
- It does not claim a strong `evidence-aware modeling` result.
- It does not claim that `poly_core_v1` is universally optimal beyond the current benchmark and metric choice.
