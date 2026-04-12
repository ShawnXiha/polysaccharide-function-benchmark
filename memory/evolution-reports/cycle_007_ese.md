# Evolution Report: Cycle 007 - ESE

**Date**: 2026-03-28
**Trigger**: Label-specific backoff produced the first stable clean long-tail improvement
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_clean_label_backoff_w05.json`
- `experiments/poly_function_link_prediction_clean_label_backoff_w10.json`
- `experiments/poly_function_long_tail_label_specific_backoff_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_label_specific_backoff_pipeline/diagnosis.md`

## Changes Made

### Added

- `Label-Specific Backoff Preserves Head Performance While Helping Tail Labels`

### Updated

- The preferred clean long-tail variant now uses label-specific backoff instead of post-hoc tail candidate injection

### Removed

- None

## Reasoning

This cycle succeeded because it addressed the main design mistake from the previous two rounds. Global source backoff was too broad and mainly sharpened head labels. Tail candidate generation could move rare labels but distorted the ranking scale. Label-specific backoff changed the unit of intervention from the whole ranking to the individual low-support label.

That shift was enough to find a workable operating point. The method delivered a real tail improvement while keeping the base clean retrieval quality intact. The overall gain is small, so it is not a new headline result, but it is the first long-tail method in this line that is both useful and stable.

## Impact on Future Cycles

- **For experiment-pipeline**: use label-specific backoff as the default long-tail clean variant.
- **For experiment-craft**: when global reranking is too blunt, move the control logic to the label level rather than widening the candidate set.
- **Confidence level**: Moderate. The effect is small but consistent across two nearby backoff weights.

## Raw Evidence Summary

- Clean filtered `Hits@3`: `0.743 -> 0.744`
- Tail micro filtered `Hits@3`: `0.167 -> 0.333`
- Mid micro filtered `Hits@3`: unchanged at `0.375`
- Head micro filtered `Hits@3`: unchanged at `0.762`
