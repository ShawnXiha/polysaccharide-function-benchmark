# Evolution Report: Cycle 011 - IVE

**Date**: 2026-03-28
**Trigger**: Label prototype refinement failed to improve the disease-aware long-tail objective
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_with_disease_label_prototype_refine_v1.json`
- `experiments/poly_function_link_prediction_with_disease_label_prototype_refine_v2.json`
- `experiments/poly_function_link_prediction_with_disease_label_prototype_refine_v3.json`
- `experiments/poly_function_link_prediction_with_disease_label_prototype_refine_v4.json`
- `experiments/poly_function_long_tail_label_prototype_refinement_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_label_prototype_refinement_pipeline/diagnosis.md`

## Failure Type

**Task-level method failure with a reusable implementation lesson**

## What Failed

The cycle tested whether label prototype refinement could improve disease-aware long-tail retrieval by reranking the top candidate labels. Absolute prototype bonuses failed immediately, and a contrastive revision recovered stability but still did not improve the primary retrieval objective or the tail stratum.

## Why It Failed

Absolute prototype similarity was the wrong signal. It mostly re-rewarded labels that were already strong under the base scorer. That caused ranking distortion without supplying new evidence for rare labels.

The contrastive revision fixed the scoring bug in the method design by rewarding only local-over-global prototype gain. That produced a small filtered MRR improvement, but the improvement stayed in head-label calibration and did not translate into better tail `Hits@3`. The rare labels still lack enough candidate support for prototype reranking alone to matter.

## Changes To Memory

### Added

- `Contrastive Prototype Refinement Is Safer Than Absolute Prototype Bonuses`
- `Prototype Refinement Can Improve MRR Without Improving Tail Retrieval`

### Updated

- Prototype refinement is not promoted as the next main method for disease-aware long-tail retrieval

### Removed

- None

## Impact on Future Cycles

- **For experiment-pipeline**: stop allocating major tuning budget to label prototype refinement on this task.
- **For experiment-craft**: when adding label-level rerank signals, compare them against the existing centroid or base score so the new term measures added structure instead of duplicating confidence.
- **Confidence level**: Moderate. Four attempts showed a consistent pattern and clarified both the unstable and stabilized variants.

## Raw Evidence Summary

- Disease prior filtered `Hits@3`: `0.878`
- Best prototype refine filtered `Hits@3`: `0.877`
- Best prototype refine filtered `MRR`: `0.8191`
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Mid micro filtered `Hits@3`: `0.400 -> 0.350`
- Head micro filtered `Hits@3`: `0.903 -> 0.904`
