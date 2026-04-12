# Evolution Report: Cycle 008 - IVE

**Date**: 2026-03-28
**Trigger**: Disease-aware label-specific backoff failed to provide additional long-tail value
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_with_disease_label_backoff_w05.json`
- `experiments/poly_function_link_prediction_with_disease_label_backoff_w10.json`
- `experiments/poly_function_long_tail_label_specific_backoff_disease_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_label_specific_backoff_disease_pipeline/diagnosis.md`

## Failure Classification

- **Type**: Method-transfer failure
- **Why not implementation failure**: the same implementation produced a stable clean improvement in Cycle 7. In the disease-aware setting it consistently showed no gain, which indicates the issue is the transfer assumption, not the code path.

## Changes Made

### Added

- `Side-Information Saturation Can Nullify Source-Aware Tail Fixes`

### Updated

- The scope of label-specific backoff is now explicitly limited to clean experiments

### Removed

- The assumption that clean long-tail fixes should automatically be extended to disease-aware settings

## Reasoning

This cycle sharpened the boundary of the previous success. Label-specific backoff worked because it injected source-aware structure into a clean retrieval problem that still lacked useful long-tail support. But once disease features were already present, that missing structure was no longer the bottleneck. The extra backoff channel had no room to help.

The important lesson is not that label-specific backoff is weak. It is that auxiliary semantic channels can saturate the ranking and erase the marginal value of source-based corrections. That means clean and disease-aware long-tail analyses should be treated as different methodological regimes.

## Impact on Future Cycles

- **For experiment-pipeline**: do not automatically port clean long-tail methods into disease-aware settings.
- **For experiment-craft**: when a transferred method yields no gain at low weight and harms performance at high weight, classify it as a regime-transfer failure rather than continuing to tune.
- **Confidence level**: Moderate. The failure pattern is stable across two nearby backoff weights.

## Raw Evidence Summary

- Disease-aware baseline filtered `Hits@3`: `0.875`
- Disease-aware label-specific backoff `w=0.5`: `0.875`
- Disease-aware label-specific backoff `w=1.0`: `0.873`
- Disease-aware tail micro filtered `Hits@3`: unchanged at `0.167`
