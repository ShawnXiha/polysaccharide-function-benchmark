# Evolution Report: Cycle 004 - ESE

**Date**: 2026-03-27
**Trigger**: Source-constrained reranking successfully improved the filtered link prediction pipeline
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_clean_source_rerank.json`
- `experiments/poly_function_link_prediction_with_disease_source_rerank.json`
- `experiments/poly_function_link_prediction_clean_source_rerank_tuned.json`
- `experiments/poly_function_link_prediction_with_disease_source_rerank_tuned.json`
- `experiments/poly_function_long_tail_source_rerank_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_source_rerank_pipeline/diagnosis.md`

## Changes Made

### Added

- `Source-Constrained Reranking Improves Precision Without Broadening Search`
- `Missing Source Support Limits Tail Gains`

### Updated

- The preferred link prediction variant now includes a selective source-aware rerank stage

### Removed

- None

## Reasoning

This cycle succeeded because it corrected the weakness exposed in the previous one. Rare-label neighbor expansion changed the search space itself and introduced broad noise. Source-constrained reranking instead preserved the strong base scorer and only adjusted the top candidate list using exact shared-source evidence. That made the change much more selective and easier to trust.

The result was a real improvement in both clean and disease-aware settings. At the same time, the cycle also clarified the remaining bottleneck: exact source evidence is not enough for the hardest tail labels, likely because those labels do not have enough source-consistent support in the training graph. That means the next long-tail step should focus on backoff or candidate-generation, not stronger rerank weights.

## Impact on Future Cycles

- **For experiment-pipeline**: Use source-constrained reranking as the default improvement over plain kNN when source metadata is available.
- **For experiment-craft**: Distinguish between selective reranking improvements and true tail-recovery improvements; they are not the same problem.
- **Confidence level**: Moderate. The improvement is controlled and consistent in this cycle, but cross-task confirmation is still pending.

## Raw Evidence Summary

- Clean filtered `Hits@3`: `0.743 -> 0.768`
- Disease-aware filtered `Hits@3`: `0.875 -> 0.886`
- Clean mid filtered `Hits@3`: `0.375 -> 0.400`
- Disease-aware mid filtered `Hits@3`: `0.400 -> 0.425`
- Tail filtered `Hits@3`: unchanged at `0.167` in both settings
