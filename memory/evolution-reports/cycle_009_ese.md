# Evolution Report: Cycle 009 - ESE

**Date**: 2026-03-28
**Trigger**: Disease-label compatibility priors improved the disease-aware retrieval baseline
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_with_disease_prior_w05.json`
- `experiments/poly_function_link_prediction_with_disease_prior_w10.json`
- `experiments/poly_function_long_tail_disease_label_prior_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_disease_label_prior_pipeline/diagnosis.md`

## Changes Made

### Added

- `Disease-Label Compatibility Priors Improve Disease-Aware Calibration`
- `Compatibility Priors Can Improve Calibration Without Fixing Tail Labels`

### Updated

- The preferred disease-aware variant now includes a compatibility-prior rerank stage

### Removed

- None

## Reasoning

This cycle succeeded because it matched the disease-aware regime instead of fighting it. The previous transferred source-based method failed because disease features had already saturated the useful semantic signal. Disease-label priors move in the same direction as the existing representation: they sharpen compatibility between observed diseases and plausible function labels.

That is why the method improves overall disease-aware retrieval while staying stable across two nearby prior weights. At the same time, the cycle also clarified that this is not a true long-tail recovery method. The rarest labels still lack enough disease-conditioned support, so the prior mostly improves calibration for stronger labels.

## Impact on Future Cycles

- **For experiment-pipeline**: use disease-label compatibility priors as the default disease-aware calibration variant.
- **For experiment-craft**: separate calibration gains from tail gains when evaluating disease-aware methods.
- **Confidence level**: Moderate. The gain is small but stable and directionally consistent.

## Raw Evidence Summary

- Disease-aware filtered `Hits@3`: `0.875 -> 0.878`
- Disease-aware filtered `MRR`: `0.8119 -> 0.8186`
- Head micro filtered `Hits@3`: `0.899 -> 0.903`
- Tail micro filtered `Hits@3`: unchanged at `0.167`
