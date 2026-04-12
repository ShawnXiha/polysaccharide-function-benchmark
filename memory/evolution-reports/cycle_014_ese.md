# Evolution Report: Cycle 014 - ESE

**Date**: 2026-03-28
**Trigger**: Integrated support-aware expansion improved the disease-aware retrieval baseline
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_with_integrated_support_knn_v1.json`
- `experiments/poly_function_link_prediction_with_integrated_support_knn_v2.json`
- `experiments/poly_function_long_tail_integrated_support_knn_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_integrated_support_knn_pipeline/diagnosis.md`

## Changes Made

### Added

- `Integrated Support Expansion Can Improve Mid-Support Retrieval`
- `Integrated Expansion Can Move Mid Labels Before It Moves Tail`

### Updated

- The preferred disease-aware retrieval variant now uses conservative integrated support-aware kNN before frequency-adjusted disease-prior calibration

### Removed

- None

## Reasoning

This cycle succeeded because it fixed the structural issue from the previous round. Candidate support was no longer attached as a detached pre-rerank bonus. Instead, it became part of the base kNN voting process, which allowed it to change shortlist formation directly.

The resulting gain is modest but real. It improves filtered `Hits@3` and specifically lifts the mid-support stratum. At the same time, the stronger setting showed that broader support expansion mainly buys MRR, not top-3 accuracy. So the conservative setting is the defensible operating point.

## Impact on Future Cycles

- **For experiment-pipeline**: use the conservative integrated support-aware kNN plus frequency-adjusted disease prior as the default disease-aware retrieval variant.
- **For experiment-craft**: when candidate expansion is intended to alter retrieval, integrate it into shortlist formation or inspect shortlist membership explicitly.
- **Confidence level**: Moderate. The gain is small but consistent, and the stronger setting produced the expected precision-vs-smoothness tradeoff.

## Raw Evidence Summary

- Filtered `Hits@3`: `0.880 -> 0.881`
- Filtered `MRR`: `0.8191 -> 0.8193`
- Mid micro filtered `Hits@3`: `0.400 -> 0.425`
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Stronger setting: filtered `MRR -> 0.8228`, but filtered `Hits@3 -> 0.879`
