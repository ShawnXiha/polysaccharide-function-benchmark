# Evolution Report: Cycle 016 - ESE

**Date**: 2026-03-28
**Trigger**: Disease-conditioned base voting substantially improved the disease-aware retrieval baseline
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_with_disease_conditioned_vote_v1.json`
- `experiments/poly_function_link_prediction_with_disease_conditioned_vote_v2.json`
- `experiments/poly_function_long_tail_disease_conditioned_base_vote_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_disease_conditioned_base_vote_pipeline/diagnosis.md`

## Changes Made

### Added

- `Disease-Conditioned Base Voting Is Stronger Than Post-Hoc Disease Reranking`
- `Strong Disease Smoothing Improves Overall Retrieval Before It Improves Tail`

### Updated

- The preferred disease-aware upper-bound variant now uses disease-conditioned base voting before frequency-adjusted disease-prior calibration

### Removed

- None

## Reasoning

This cycle succeeded because it stopped treating disease information as a late correction signal. In this dataset, disease semantics are strong enough to shape base evidence accumulation. Once that signal entered the neighbor vote, the system improved far more than with rerank-only methods.

The resulting gain is large and stable across two settings. That makes the design defensible as the best disease-aware upper bound so far. At the same time, the unchanged tail stratum shows that this is not a hidden tail solution. It is stronger exploitation of side-information.

## Impact on Future Cycles

- **For experiment-pipeline**: use disease-conditioned base vote plus frequency-adjusted disease prior as the default disease-aware upper-bound variant.
- **For experiment-craft**: when side-information is highly predictive, test moving it earlier into evidence accumulation rather than only refining scores later.
- **Confidence level**: High. Two settings produced strong gains with the same qualitative pattern.

## Raw Evidence Summary

- Filtered `Hits@3`: `0.880 -> 0.902` and `0.912`
- Filtered `MRR`: `0.8191 -> 0.8433` and `0.8496`
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Mid micro filtered `Hits@3`: `0.400 -> 0.425` and `0.450`
- Head micro filtered `Hits@3`: `0.905 -> 0.927` and `0.936`
