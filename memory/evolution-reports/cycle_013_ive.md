# Evolution Report: Cycle 013 - IVE

**Date**: 2026-03-28
**Trigger**: Support-aware candidate generation before reranking failed to change retrieval outcomes
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_with_support_aware_candidates_v1.json`
- `experiments/poly_function_link_prediction_with_support_aware_candidates_v2.json`
- `experiments/poly_function_link_prediction_with_support_aware_candidates_v3.json`
- `experiments/poly_function_long_tail_support_aware_candidate_generation_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_support_aware_candidate_generation_pipeline/diagnosis.md`

## Failure Type

**Pipeline-integration failure**

## What Failed

The cycle added support-aware candidate bonuses before reranking and tested conservative, moderate, and aggressive settings. None of them changed the final retrieval metrics relative to the paired frequency-adjusted disease-prior baseline.

## Why It Failed

The candidate generation stage did not meaningfully alter the shortlist entering the downstream rerank step. As a result, the added scores existed locally but did not become operative in the end-to-end retrieval pipeline.

This is not a case of harmful overcorrection. It is a case of structural detachment. The generator was too weakly coupled to shortlist formation, so even aggressive settings behaved as a no-op.

## Changes To Memory

### Added

- `Candidate Expansion Must Change The Downstream Shortlist To Matter`

### Updated

- Candidate-generation work should focus on shortlist entry and base scorer integration rather than pre-rerank additive bonuses

### Removed

- None

## Impact on Future Cycles

- **For experiment-pipeline**: do not spend more tuning budget on this specific pre-rerank candidate-bonus design.
- **For experiment-craft**: inspect whether a candidate-generation method changes shortlist membership before trusting end metrics alone.
- **Confidence level**: High. Three settings spanning conservative to aggressive produced the same outcome.

## Raw Evidence Summary

- Filtered `Hits@3`: unchanged in all attempts
- Filtered `MRR`: unchanged in all attempts
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Mid micro filtered `Hits@3`: unchanged at `0.400`
- Head micro filtered `Hits@3`: unchanged
