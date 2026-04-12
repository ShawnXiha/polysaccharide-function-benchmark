# Evolution Report: Cycle 022 - IVE

**Date**: 2026-03-29
**Trigger**: An external ontology/hierarchy support variant failed to improve rare-label retrieval
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `configs/function_hierarchy_v1.json`
- `experiments/poly_function_link_prediction_clean_hierarchy_support_v1.json`
- `experiments/poly_function_link_prediction_clean_hierarchy_support_v2.json`
- `experiments/poly_function_link_prediction_with_disease_hierarchy_support_v1.json`
- `experiments/poly_function_link_prediction_with_disease_hierarchy_support_v2.json`
- `experiments/poly_function_long_tail_hierarchy_support_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_hierarchy_support_pipeline/diagnosis.md`

## Failure Classification

- **Type**: Fundamental direction failure for the current formulation
- **Direction**: coarse external ontology/hierarchy support through family-level label smoothing

## Reasoning

This cycle changed the evidence family, not just the scoring surface. The new method introduced an explicit external hierarchy over function labels.

The result is diagnostic:

- weak hierarchy support is a no-op
- stronger hierarchy support degrades overall retrieval
- tail retrieval does not improve and can collapse

So the issue is not missing optimization. It is that the current hierarchy is too coarse to supply discriminative rare-label evidence. It behaves as smoothing, not as a useful support channel.

## Changes Made

### Added

- `Coarse Function Hierarchies Can Behave Like Smoothing, Not New Evidence`

### Updated

- The next ontology attempt should require finer-grained or graph-native hierarchical evidence

### Removed

- None

## Impact on Future Cycles

- Stop tuning the current family-level hierarchy support.
- Do not count coarse ontology support as a new tail evidence channel by default.
- If external ontology work continues, require finer resolution or direct graph integration.

## Raw Evidence Summary

- clean hierarchy support filtered `Hits@3`: `0.724 / 0.713`
- disease-aware hierarchy support filtered `Hits@3`: `0.911 / 0.889`
- disease-aware tail micro filtered `Hits@3`: `0.1667 -> 0.1667 -> 0.000`
