# Evolution Report: Cycle 010 - IVE

**Date**: 2026-03-28
**Trigger**: Tail-aware disease priors failed to improve disease-aware long-tail retrieval
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_with_tail_disease_prior_conservative.json`
- `experiments/poly_function_link_prediction_with_tail_disease_prior_aggressive.json`
- `experiments/poly_function_long_tail_tail_aware_disease_prior_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_tail_aware_disease_prior_pipeline/diagnosis.md`

## Failure Type

**Method-design failure**

## What Failed

The cycle modified the successful disease-label compatibility prior so that it only boosted low-support labels within the rerank window. Two settings were tested, one conservative and one aggressive.

Neither setting improved filtered `Hits@3`, neither improved tail micro filtered `Hits@3`, and both slightly reduced filtered `MRR` relative to the ordinary disease prior baseline.

## Why It Failed

The original disease prior helped because it provided broad compatibility calibration across already plausible candidates. Tail-only gating removed that calibration benefit, but the remaining tail-specific evidence was still too weak to move rare labels across the top-k boundary.

This means the core assumption behind the cycle was wrong. A calibration prior cannot be converted into a tail-recovery method simply by applying it only to rare labels.

## Changes To Memory

### Added

- `Over-Targeting Tail Priors Can Remove Calibration Gains Without Unlocking Tail`

### Updated

- The preferred disease-aware variant remains the ordinary disease-label compatibility prior rather than its tail-aware extension

### Removed

- None

## Impact on Future Cycles

- **For experiment-pipeline**: stop spending tuning budget on tail-aware disease prior weights or thresholds.
- **For experiment-craft**: when a prior helps overall through calibration, test whether a tail-specific variant removes the original utility before assuming it will help rare labels.
- **Confidence level**: Moderate. The two attempts were directionally consistent and failed for the same reason.

## Raw Evidence Summary

- Disease-aware filtered `Hits@3`: stayed `0.875`
- Disease-aware filtered `MRR`: `0.8119 -> 0.8112` and `0.8111`
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Mid micro filtered `Hits@3`: unchanged at `0.400`
- Head micro filtered `Hits@3`: unchanged at `0.899`
