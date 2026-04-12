# Evolution Report: Cycle 003 - IVE

**Date**: 2026-03-27
**Trigger**: Rare-label neighbor expansion failed to clear the long-tail improvement gate as a new default method
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_long_tail_rare_label_expansion_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_rare_label_expansion_pipeline/diagnosis.md`
- `experiments/poly_function_link_prediction_clean_rare_expand.json`
- `experiments/poly_function_link_prediction_clean_rare_expand_t50_k75_d1.json`
- `experiments/poly_function_link_prediction_with_disease_rare_expand.json`
- `experiments/poly_function_link_prediction_with_disease_rare_expand_t50_k100_d1.json`

## Failure Classification

- **Type**: Fundamental weakness under current formulation
- **Reason**: The implementation worked as intended, but the scoring idea itself introduced too much non-specific neighborhood evidence to serve as a robust default retriever

## What Failed

Rare-label neighbor expansion improved a few long-tail cases, but did not produce a clean gain profile. Conservative expansion slightly improved clean tail recovery while still reducing overall filtered `Hits@3`. Aggressive expansion improved some mid-support labels but degraded head-label retrieval enough to lower the total score in both clean and disease-aware settings.

## Why It Failed

The method assumes that farther neighbors are useful primarily for rare labels. In this KG that assumption is too weak. Once the neighborhood is expanded, the scorer absorbs broad co-occurrence patterns that are not label-specific enough. The resulting signal is sometimes helpful for sparse labels, but it is not selective enough to preserve the quality of already strong rankings.

This is a formulation problem, not a coding bug. The current expansion rule is based only on label support and distance rank, without any mechanism to filter noisy semantic spillover.

## Memory Updates

### Added

- `Rare-Label Neighbor Expansion Is A Tradeoff, Not A Free Gain`
- `Long-Tail Expansion Can Amplify Structural Noise`

### Updated

- None

### Removed

- None

## Raw Evidence Summary

- Clean baseline filtered `Hits@3`: `0.743`
- Clean conservative rare expansion filtered `Hits@3`: `0.740`
- Clean aggressive rare expansion filtered `Hits@3`: `0.703`
- Disease-aware baseline filtered `Hits@3`: `0.875`
- Disease-aware conservative rare expansion filtered `Hits@3`: `0.874`
- Disease-aware aggressive rare expansion filtered `Hits@3`: `0.867`
- Clean tail filtered `Hits@3`: `0.167 -> 0.333`
- Disease-aware mid filtered `Hits@3`: `0.400 -> 0.475`

## Recommendation For Next Cycle

- Keep the original filtered kNN as the default baseline.
- If continuing long-tail work, move from broad neighborhood expansion to more selective second-stage reranking.
