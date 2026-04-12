# Evolution Report: Cycle 021 - IVE

**Date**: 2026-03-29
**Trigger**: A taxonomy-conditioned structural motif variant failed to improve rare-label retrieval
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `experiments/poly_function_link_prediction_clean_taxonomy_motifs_v1.json`
- `experiments/poly_function_link_prediction_clean_taxonomy_motifs_v2.json`
- `experiments/poly_function_link_prediction_with_disease_taxonomy_motifs_v1.json`
- `experiments/poly_function_link_prediction_with_disease_taxonomy_motifs_v2.json`
- `experiments/poly_function_long_tail_taxonomy_motif_pipeline/pipeline_tracker.md`
- `experiments/poly_function_long_tail_taxonomy_motif_pipeline/diagnosis.md`

## Failure Classification

- **Type**: Fundamental direction failure for the current formulation
- **Direction**: taxonomy-conditioned motif rarity from current local structural blocks

## Reasoning

This cycle serves as a strong diagnostic control. Earlier structural variants failed partly because they were noisy. Taxonomy conditioning removed most of that instability, but the method still did not help tail retrieval.

So the failure is not just “too much noise.” It is that the remaining evidence source is intrinsically too weak for tail recovery in this task.

## Changes Made

### Added

- `Taxonomy Conditioning Can Stabilize Structural Motifs Without Unlocking Tail`

### Updated

- Current local structure families should be treated as exhausted for tail-evidence mining

### Removed

- None

## Impact on Future Cycles

- Stop iterating on structure-only motif families from current graph blocks.
- The next evidence-source change should leave the current structural family entirely.
- Keep disease-conditioned base vote plus frequency-adjusted disease prior as the best disease-aware upper bound.

## Raw Evidence Summary

- clean taxonomy-conditioned motifs filtered `Hits@3`: `0.724 / 0.724`
- disease-aware taxonomy-conditioned motifs filtered `Hits@3`: `0.912 / 0.912`
- disease-aware tail micro filtered `Hits@3`: `0.1667 -> 0.1667 -> 0.1667`
