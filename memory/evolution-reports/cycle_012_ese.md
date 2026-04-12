# Evolution Report: Cycle 012 - ESE

**Date**: 2026-03-28
**Trigger**: Frequency-adjusted disease prior improved the disease-aware retrieval baseline
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_with_freq_adjusted_disease_prior_v1.json`
- `experiments/poly_function_link_prediction_with_freq_adjusted_disease_prior_v2.json`
- `experiments/poly_function_link_prediction_with_freq_adjusted_disease_prior_v3.json`
- `experiments/poly_function_long_tail_frequency_adjusted_disease_prior_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_frequency_adjusted_disease_prior_pipeline/diagnosis.md`

## Changes Made

### Added

- `Mild Frequency Adjustment Can Improve Disease-Prior Calibration`
- `Frequency Adjustment Helps Calibration Before It Helps Tail`

### Updated

- The preferred disease-aware variant now uses mild divisive frequency adjustment on top of the disease prior

### Removed

- None

## Reasoning

This cycle succeeded because it corrected only part of the disease prior's bias instead of trying to replace the prior itself. The disease prior contains real semantic signal, but it is somewhat tilted toward frequent labels. Mild divisive normalization preserved the useful part and reduced the over-reward on common labels just enough to improve ranking.

The failed tuning runs clarified the boundary. Aggressive subtraction and stronger penalization removed useful signal before they created any benefit for rare labels. So the lesson is not that stronger frequency correction helps more. The lesson is that mild correction improves calibration.

## Impact on Future Cycles

- **For experiment-pipeline**: use mild divisive frequency adjustment as the default disease-aware calibration variant.
- **For experiment-craft**: separate calibration wins from tail wins; even successful frequency correction may leave tail retrieval unchanged.
- **Confidence level**: Moderate. One setting improved both filtered `Hits@3` and `MRR`, while nearby stronger settings regressed as expected.

## Raw Evidence Summary

- Disease prior filtered `Hits@3`: `0.878 -> 0.880`
- Disease prior filtered `MRR`: `0.8186 -> 0.8191`
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Mid micro filtered `Hits@3`: unchanged at `0.400`
- Head micro filtered `Hits@3`: `0.903 -> 0.905`
