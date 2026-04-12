# Evolution Report: Cycle 005 - ESE

**Date**: 2026-03-27
**Trigger**: Source-cluster backoff improved the clean long-tail retrieval pipeline and clarified when source backoff should replace exact reranking
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_clean_source_cluster_backoff.json`
- `experiments/poly_function_link_prediction_with_disease_source_cluster_backoff.json`
- `experiments/poly_function_long_tail_source_cluster_backoff_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_source_cluster_backoff_pipeline/diagnosis.md`

## Changes Made

### Added

- `Source-Cluster Backoff Helps Clean Source-Aware Retrieval`
- `Genus Or Kingdom Backoff Does Not Solve Tail Support`

### Updated

- The preferred clean source-aware link prediction variant now uses source-cluster backoff instead of exact-only reranking

### Removed

- None

## Reasoning

This cycle succeeded in a bounded way. Exact source reranking had already shown that selective source consistency helps, but it left open whether sparse exact matches were the reason tail recovery stalled. Source-cluster backoff tested that hypothesis directly by backing off from organism to genus and kingdom without disturbing the strong base kNN scorer.

The result shows that broader source structure is useful, but only in a narrow regime. In the clean setting, soft backoff gives a small but real gain over exact reranking. In the disease-aware setting, that same softening becomes less useful than precise exact-source evidence. The cycle therefore produced both a practical improvement and a sharper method-selection rule.

## Impact on Future Cycles

- **For experiment-pipeline**: Use source-cluster backoff as the preferred clean source-aware rerank, but keep exact source rerank for disease-aware settings.
- **For experiment-craft**: Treat source-granularity backoff as a precision refinement, not a tail-recovery mechanism.
- **Confidence level**: Moderate. The clean improvement is real, but the boundary is task-specific and does not generalize to the disease-aware regime.

## Raw Evidence Summary

- Clean filtered `Hits@3`: `0.743 -> 0.773`
- Clean exact source rerank comparison: `0.768 -> 0.773`
- Disease-aware filtered `Hits@3`: `0.875 -> 0.883`
- Disease-aware exact source rerank comparison: `0.886` remains better than `0.883`
- Tail filtered `Hits@3`: unchanged at `0.167` in both settings
