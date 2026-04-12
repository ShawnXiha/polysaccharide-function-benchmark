# Evolution Report: Cycle 019 - IVE

**Date**: 2026-03-29
**Trigger**: A structural-tail candidate-generation variant underperformed existing clean and disease-aware baselines
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_clean_structure_candidates_v1.json`
- `experiments/poly_function_link_prediction_clean_structure_candidates_v2.json`
- `experiments/poly_function_link_prediction_with_disease_structure_candidates_v1.json`
- `experiments/poly_function_link_prediction_with_disease_structure_candidates_v2.json`
- `experiments/poly_function_long_tail_structure_candidate_generation_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_structure_candidate_generation_pipeline/diagnosis.md`

## Failure Classification

- **Type**: Fundamental direction failure for the current formulation
- **Direction**: structure-aware candidate generation from current structural signatures

## Reasoning

Cycle 18 already showed that post-hoc structural bonuses fail. Cycle 19 tested the most obvious rescue: move the same signal earlier into candidate generation. That rescue also failed.

The failure pattern remained consistent:

1. Conservative settings were nearly identical to baseline.
2. Stronger settings degraded mid/head retrieval.
3. Tail micro filtered `Hits@3` remained unchanged in both clean and disease-aware evaluation.

That means the bottleneck is not just the injection stage. It is the weakness of the current structural evidence source.

## Changes Made

### Added

- `Structural Candidate Generation Still Needs A Stronger Evidence Source`

### Updated

- Structural-tail evidence should no longer be pursued with the current flat signature overlap representation

### Removed

- None

## Impact on Future Cycles

- Stop revisiting current structural signatures for both reranking and candidate generation.
- If structural tail work continues, redesign the evidence itself rather than its placement.
- Keep disease-conditioned base vote plus frequency-adjusted disease prior as the best disease-aware upper bound.

## Raw Evidence Summary

- clean baseline filtered `Hits@3`: `0.724`
- clean structure-candidate v1/v2 filtered `Hits@3`: `0.724 / 0.715`
- disease-aware upper-bound baseline filtered `Hits@3`: `0.912`
- disease-aware structure-candidate v1/v2 filtered `Hits@3`: `0.911 / 0.892`
- disease-aware tail micro filtered `Hits@3`: `0.1667 -> 0.1667 -> 0.1667`
