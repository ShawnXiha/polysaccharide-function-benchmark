# Evolution Report: Cycle 020 - IVE

**Date**: 2026-03-29
**Trigger**: A label-specific subgraph-motif variant underperformed existing clean and disease-aware baselines
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_clean_subgraph_motifs_v1.json`
- `experiments/poly_function_link_prediction_clean_subgraph_motifs_v2.json`
- `experiments/poly_function_link_prediction_with_disease_subgraph_motifs_v1.json`
- `experiments/poly_function_link_prediction_with_disease_subgraph_motifs_v2.json`
- `experiments/poly_function_long_tail_subgraph_motif_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_subgraph_motif_pipeline/diagnosis.md`

## Failure Classification

- **Type**: Fundamental direction failure for the current formulation
- **Direction**: pairwise local subgraph motifs from current KG structural blocks

## Reasoning

This cycle tested a stronger and cleaner evidence source than flat structural signatures. The result improved formulation quality, but not task outcome. The same failure pattern remained:

1. Conservative settings were effectively unchanged from baseline.
2. Stronger settings degraded overall and stratified mid/head performance.
3. Tail micro filtered `Hits@3` remained unchanged.

This indicates that the problem is not merely poor scoring design inside this motif family. The current KG local blocks do not carry enough tail-discriminative structural evidence for this approach.

## Changes Made

### Added

- `Pairwise Subgraph Motifs Are Cleaner Than Flat Signatures But Still Not Sufficient`

### Updated

- Structural-tail work should stop iterating on local structural overlap families built only from current graph blocks

### Removed

- None

## Impact on Future Cycles

- Stop trying flat and pairwise local structural overlap variants.
- Next tail-evidence work should use a different evidence source entirely.
- Keep disease-conditioned base vote plus frequency-adjusted disease prior as the best disease-aware upper bound.

## Raw Evidence Summary

- clean baseline filtered `Hits@3`: `0.724`
- clean subgraph-motif v1/v2 filtered `Hits@3`: `0.724 / 0.715`
- disease-aware upper-bound baseline filtered `Hits@3`: `0.912`
- disease-aware subgraph-motif v1/v2 filtered `Hits@3`: `0.911 / 0.897`
- disease-aware tail micro filtered `Hits@3`: `0.1667 -> 0.1667 -> 0.1667`
