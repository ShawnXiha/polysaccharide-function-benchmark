# Evolution Report: Cycle 017 - ESE

**Date**: 2026-03-28
**Trigger**: A new base-vote evidence channel substantially improved disease-aware retrieval
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_with_disease_conditioned_vote_v1.json`
- `experiments/poly_function_link_prediction_with_disease_conditioned_vote_v2.json`
- `experiments/poly_function_long_tail_tail_evidence_channels_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_tail_evidence_channels_pipeline/diagnosis.md`

## Changes Made

### Added

- `Tail Evidence Channels Need New Information, Not Just Stronger Disease Use`
- `Large Upper-Bound Gains Can Mask Unchanged Tail Failure`

### Updated

- The current best disease-aware upper-bound variant remains disease-conditioned base voting plus frequency-adjusted disease-prior calibration

### Removed

- None

## Reasoning

This cycle confirmed that base-stage evidence channels can produce much larger gains than rerank-only methods. However, it also made the remaining limitation easier to see: strong side-information gains do not automatically translate into tail recovery.

That means future tail work should not keep intensifying disease semantics. The next useful direction must add information channels that are complementary to disease, especially channels that are available for rare labels.

## Impact on Future Cycles

- **For experiment-pipeline**: keep disease-conditioned base voting as the upper-bound reference.
- **For experiment-craft**: separate “better use of dominant side-information” from “new tail evidence”.
- **Confidence level**: High. Two settings produced large and consistent gains, with the same unchanged tail profile.

## Raw Evidence Summary

- Filtered `Hits@3`: `0.880 -> 0.902` and `0.912`
- Filtered `MRR`: `0.8191 -> 0.8433` and `0.8496`
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Mid micro filtered `Hits@3`: `0.400 -> 0.425` and `0.450`
- Head micro filtered `Hits@3`: `0.905 -> 0.927` and `0.936`
