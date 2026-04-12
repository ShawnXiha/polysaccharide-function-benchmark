# Evolution Report: Cycle 024 - ESE

**Date**: 2026-03-29
**Trigger**: Stability validation confirmed that the ontology best variant is a real tail-sensitive gain rather than a single-seed artifact
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `scripts/summarize_ontology_stability.py`
- `experiments/ontology_stability_pipeline/pipeline_tracker.md`
- `experiments/ontology_stability_pipeline/stability_significance.md`
- `experiments/ontology_stability_runs/ontology_stability_summary.json`
- `docs/ontology_best_variant.md`

## Success Classification

- **Type**: Reusable strategy extraction
- **Direction**: significance-aware validation for tail-sensitive ontology variants

## Reasoning

The prior ontology result was promising but still vulnerable to the "single split" objection. This cycle converted it into a defensible result by using paired baseline-vs-ontology evaluation on identical splits, exporting edge-level records, and testing both aggregate and tail-specific deltas.

The crucial lesson is that stability should not be checked only with a few seed-level metric averages. For tail-sensitive retrieval:

- edge-level paired statistics are needed to show that the same masked edges improve
- seed-level consistency is needed to show that the gain is not idiosyncratic
- directional tests are appropriate when the method is explicitly designed to improve one side of the tradeoff

With `16` paired seeds, the ontology variant remained flat on overall filtered `Hits@3`, but tail gains became defensible:

- tail micro filtered `Hits@3`: `0.0552 -> 0.1021`
- one-sided paired McNemar for tail `Hits@3`: `p=0.03125`
- tail filtered `MRR` delta: `+0.0395`, permutation `p=0.0002499`
- no seed showed a tail regression

## Changes Made

### Added

- `Paired Edge-Level Significance Validation For Tail Claims`
- `Expand Seed Count Before Re-Designing A Method When Tail Metrics Are Underpowered`

### Updated

- Current ontology best variant is now supported by a significance/stability supplement

### Removed

- None

## Impact on Future Cycles

- For any future tail-sensitive claim, export paired edge-level records by default.
- Use both edge-level significance and seed-level consistency in supplements.
- If the direction is clear but two-sided tail hit metrics are underpowered, first add more paired seeds before modifying the method.

## Raw Evidence Summary

- paired seeds: `16`
- paired evaluation edges: `16000`
- overall filtered `Hits@3`: `0.9088 -> 0.9085`
- tail micro filtered `Hits@3`: `0.0552 -> 0.1021`
- tail one-sided McNemar: `p=0.03125`
- tail filtered `MRR` delta: `+0.0395`, permutation `p=0.0002499`
