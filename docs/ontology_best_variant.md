# Ontology Best Variant

## Current Best Variant

- **Name**: confidence-gated parent/child ontology propagation
- **Config**:
  - `--hierarchy-parent-child-native`
  - `--hierarchy-config configs/function_hierarchy_v3_parent_child.json`
  - `--hierarchy-base-window 20`
  - `--hierarchy-threshold 10`
  - `--hierarchy-min-seed-count 2`
  - `--hierarchy-specificity-power 2.0`
  - `--hierarchy-graph-weight 0.1`
  - `--hierarchy-confidence-threshold 0.25`
  - `--hierarchy-adaptive-power 1.5`

## Best Result

- **File**: `experiments/poly_function_link_prediction_with_disease_hierarchy_parent_child_tune_c025.json`
- **Primary baseline**: `meta_path_knn_disease_conditioned_vote_freq_prior`
- **Ontology variant**: `meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native`

| Metric | Baseline | Ontology Best Variant |
|--------|----------|-----------------------|
| filtered MRR | 0.8491 | 0.8490 |
| filtered Hits@3 | 0.912 | 0.912 |
| filtered Hits@5 | 0.938 | 0.939 |

## Stratified Comparison

| Stratum | Baseline micro filtered Hits@3 | Ontology Best Variant |
|---------|--------------------------------|-----------------------|
| tail | 0.1667 | 0.3333 |
| mid | 0.4500 | 0.4500 |
| head | 0.9361 | 0.9350 |

## Interpretation

This is the current best ontology-aware variant because it preserves the earlier tail gain from parent/child propagation while recovering almost all of the global metric loss.

It should not be described as a new overall best model. It is better framed as:

- the current best ontology-enhanced tail-sensitive variant
- a controlled tradeoff that doubles tail micro filtered `Hits@3`
- an ontology mechanism that now matches the main baseline on filtered `Hits@3`

## Recommended Positioning

- Use `meta_path_knn_disease_conditioned_vote_freq_prior` as the main disease-aware upper-bound baseline.
- Use this ontology best variant as the ontology-enhanced tail-recovery result.
- Emphasize that ontology edges help the tail only after converting family bonuses into parent/child propagation with confidence gating.

## Stability Validation

- **Protocol**: paired baseline-vs-ontology evaluation with identical splits across `16` seeds and per-edge records
- **Summary File**: `experiments/ontology_stability_runs/ontology_stability_summary.json`
- **Report**: `experiments/ontology_stability_pipeline/stability_significance.md`

| Metric | Baseline Mean | Ontology Mean | Delta | Statistical Note |
|--------|---------------|---------------|-------|------------------|
| filtered Hits@3 | 0.9088 | 0.9085 | -0.0003 | effectively unchanged |
| tail micro filtered Hits@3 | 0.0552 | 0.1021 | +0.0469 | one-sided McNemar `p=0.03125` |
| tail filtered MRR | - | - | +0.0395 | permutation `p=0.0002499` |

This validates the current ontology best variant as a stable tail-sensitive improvement rather than a single-seed artifact. The ontology version does not become a new overall best model, but it consistently improves tail retrieval without introducing any observed tail regression across the `16` paired seeds.
