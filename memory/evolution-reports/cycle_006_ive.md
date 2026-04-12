# Evolution Report: Cycle 006 - IVE

**Date**: 2026-03-27
**Trigger**: Tail candidate generation failed to produce a usable long-tail improvement
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_clean_tail_candidates.json`
- `experiments/poly_function_link_prediction_clean_tail_candidates_tuned_a05_l3.json`
- `experiments/poly_function_link_prediction_clean_tail_candidates_tuned_a10_l3.json`
- `experiments/poly_function_long_tail_tail_candidate_generation_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_tail_candidate_generation_pipeline/diagnosis.md`

## Failure Classification

- **Type**: Method-design failure
- **Why not implementation failure**: the method produced the expected qualitative behavior in both directions. Aggressive activation moved tail labels upward but damaged head precision. Conservative activation preserved head precision but removed the tail gain. The code path is behaving consistently; the problem is the design tradeoff itself.

## Changes Made

### Added

- `Tail Candidate Generation Needs Calibration And Support`

### Updated

- None

### Removed

- The current rerank-only tail candidate generation method from the list of promising long-tail directions

## Reasoning

This cycle clarified an important boundary. The earlier long-tail methods failed because they either widened neighborhoods too broadly or only reranked the existing short list. Tail candidate generation looked promising because it explicitly tried to add new rare-label candidates. But in practice it ran into the same structural problem in a different form: weak rare evidence is hard to calibrate against strong head-label evidence.

The first implementation proved that candidate injection can raise tail ranks, but the resulting score distortion was too large. Tightening activation and source support fixed the distortion but removed the long-tail gain. That means the current mechanism does not offer a workable operating point.

## Impact on Future Cycles

- **For experiment-pipeline**: do not continue tuning rerank-only tail candidate injection.
- **For experiment-craft**: when a method alternates between over-activation and no-op under small calibration changes, classify it as a design failure.
- **Confidence level**: Moderate to high. The failure mode is consistent across initial and tuned attempts.

## Raw Evidence Summary

- Baseline clean filtered `Hits@3`: `0.743`
- Initial tail candidate generation filtered `Hits@3`: `0.653`
- Initial tail micro filtered `Hits@3`: `0.167 -> 0.333`
- Initial head micro filtered `Hits@3`: `0.762 -> 0.667`
- Tuned candidate generation filtered `Hits@3`: `0.743`
- Tuned tail micro filtered `Hits@3`: unchanged at `0.167`
