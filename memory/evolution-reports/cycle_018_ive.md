# Evolution Report: Cycle 018 - IVE

**Date**: 2026-03-29
**Trigger**: A new tail-evidence direction underperformed the existing baselines in both clean and disease-aware settings
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_clean_tail_structural_signature_v1.json`
- `experiments/poly_function_link_prediction_clean_tail_structural_signature_v2.json`
- `experiments/poly_function_link_prediction_with_disease_tail_structural_signature_v1.json`
- `experiments/poly_function_link_prediction_with_disease_tail_structural_signature_v2.json`
- `experiments/poly_function_long_tail_structural_signature_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_structural_signature_pipeline/diagnosis.md`

## Failure Classification

- **Type**: Fundamental direction failure for the current formulation
- **Direction**: post-hoc rare-label structural-signature reranking

## Reasoning

This cycle produced the characteristic pattern of a pipeline-level direction failure:

1. Conservative settings were executable but nearly unchanged relative to the baseline.
2. Stronger settings clearly affected ranking behavior, but only by degrading mid/head retrieval.
3. Tail micro filtered `Hits@3` did not improve in the disease-aware setting and remained `0.1667`.
4. The same pattern appeared in both clean and disease-aware evaluation.

That combination argues against “more tuning needed.” The method is not blocked by an implementation bug. It is blocked by a mismatch between the evidence channel and the stage where it is injected.

## Changes Made

### Added

- `Tail Structural Signatures Need Candidate-Level Activation, Not Post-Hoc Bonus Injection`
- `Weak Post-Hoc Tail Bonuses And Strong Post-Hoc Tail Bonuses Can Fail Differently`

### Updated

- The current best disease-aware upper bound remains `disease-conditioned base vote + frequency-adjusted disease prior`

### Removed

- None

## Impact on Future Cycles

- Do not revisit post-hoc structural-signature reranking unless the pipeline stage changes.
- Structural tail cues should only be reconsidered if moved into candidate generation or base voting.
- Continue treating new tail channels as distinct from disease-aware upper-bound calibration.

## Raw Evidence Summary

- clean baseline filtered `Hits@3`: `0.724`
- clean structural signature v1/v2 filtered `Hits@3`: `0.721 / 0.623`
- disease-aware upper-bound baseline filtered `Hits@3`: `0.912`
- disease-aware structural signature v1/v2 filtered `Hits@3`: `0.911 / 0.864`
- disease-aware tail micro filtered `Hits@3`: `0.1667 -> 0.1667 -> 0.1667`
- disease-aware mid micro filtered `Hits@3`: `0.450 -> 0.450 -> 0.150`
