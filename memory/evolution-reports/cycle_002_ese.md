# Evolution Report: Cycle 002 - ESE

**Date**: 2026-03-27
**Trigger**: Successful upgrade of the `poly-function` link prediction evaluation protocol with filtered ranking and per-label stratified analysis
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_clean_filtered_stratified.json`
- `experiments/poly_function_link_prediction_with_disease_filtered_stratified.json`
- `experiments/poly_function_link_prediction_pipeline/pipeline_tracker.md`
- `experiments/poly_function_link_prediction_pipeline/stage4_ablation/trajectory.md`

## Changes Made

### Added

- `Use Filtered Ranking For Multi-Label KG Edge Recovery`: added to Experimentation Memory / Model Training Strategies
- `Aggregate Metrics Can Hide Head-Tail Failure Gaps`: added to Experimentation Memory / Debugging Strategies

### Updated

- Pipeline Stage 4 records now include filtered ranking and support-stratified evaluation results

### Removed/Archived

- None

## Reasoning

This cycle did not change the scorer family. It changed the validity of the evaluation. The previous protocol ranked a held-out true function against other functions that were also true for the same polysaccharide, which is not a fair interpretation of retrieval error in a multi-label setting. Adding filtered ranking corrected that mismatch and materially changed the measured quality of both clean and disease-aware kNN retrieval.

The second useful lesson was that stronger global metrics still did not mean the task was solved. Once results were broken down by label support, the performance gap between head and tail labels became obvious. Most of the apparent success comes from high-support functions, while low-support functions remain poorly recovered even after adding disease information. That makes long-tail recovery the next real bottleneck, not incremental tuning of already strong head-label behavior.

These are reusable evaluation lessons, not just dataset-specific numbers. Future KG retrieval cycles should adopt filtered ranking by default and should avoid relying on only one aggregate metric when the target-label distribution is highly skewed.

## Impact on Future Cycles

- **For experiment-pipeline**: Future multi-label link prediction stages should use filtered ranking as the default gate metric.
- **For experiment-craft**: If aggregate metrics improve but long-tail strata do not, treat the issue as a distributional weakness rather than a global optimization failure.
- **Confidence level**: Moderate. The protocol correction is conceptually strong and empirically verified within this cycle, but broader confirmation across tasks is still pending.

## Raw Evidence Summary

- Clean kNN raw vs filtered: `MRR 0.4806 -> 0.6168`, `Hits@3 0.655 -> 0.743`
- Disease-aware kNN raw vs filtered: `MRR 0.6097 -> 0.8119`, `Hits@3 0.814 -> 0.875`
- Clean filtered micro `Hits@3` by support stratum: tail `0.167`, mid `0.375`, head `0.762`
- Disease-aware filtered micro `Hits@3` by support stratum: tail `0.167`, mid `0.400`, head `0.899`
