# Evolution Report: Cycle 015 - IVE

**Date**: 2026-03-28
**Trigger**: Explicit tail-support integration failed to improve tail retrieval
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_with_explicit_tail_support_v1.json`
- `experiments/poly_function_link_prediction_with_explicit_tail_support_v2.json`
- `experiments/poly_function_long_tail_explicit_tail_support_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_explicit_tail_support_pipeline/diagnosis.md`

## Failure Type

**Task-level method failure**

## What Failed

The cycle restricted integrated support expansion to only the rarest labels in the base scorer. A conservative setting produced no change, and a stronger setting changed overall ranking but still failed to improve the tail stratum.

## Why It Failed

Tail-specific weighting does not solve the problem when the missing ingredient is evidence density rather than objective focus. The rarest labels still lack enough recoverable local structure in the current neighborhood space. As a result, stronger tail emphasis only shifts broader ranking behavior instead of lifting true tail labels into the top-3.

## Changes To Memory

### Added

- `Tail-Only Expansion Can Still Miss The True Tail Bottleneck`

### Updated

- Tail-focused work should move toward richer support construction rather than stronger tail weighting alone

### Removed

- None

## Impact on Future Cycles

- **For experiment-pipeline**: do not spend more tuning budget on explicit tail-only expansion with the current feature space.
- **For experiment-craft**: distinguish between insufficient target focus and insufficient evidence density before sharpening a method toward the tail.
- **Confidence level**: Moderate. The conservative and stronger settings failed in different ways but led to the same task-level conclusion.

## Raw Evidence Summary

- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Conservative setting: no metric change
- Stronger setting: filtered `MRR -> 0.8223`, but filtered `Hits@3 -> 0.878`
- Mid micro filtered `Hits@3`: `0.400 -> 0.375`
