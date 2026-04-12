# Evolution Report: Cycle 023 - ESE

**Date**: 2026-03-29
**Trigger**: Parent/child ontology propagation with confidence gating produced the current best ontology-aware variant
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`
- `configs/function_hierarchy_v3_parent_child.json`
- `experiments/poly_function_link_prediction_with_disease_hierarchy_parent_child_v2_confidence.json`
- `experiments/poly_function_link_prediction_with_disease_hierarchy_parent_child_tune_w008.json`
- `experiments/poly_function_link_prediction_with_disease_hierarchy_parent_child_tune_c025.json`
- `experiments/poly_function_link_prediction_with_disease_hierarchy_parent_child_tune_p20.json`
- `docs/ontology_best_variant.md`

## Success Classification

- **Type**: Reusable strategy extraction
- **Direction**: ontology-aware tail-sensitive propagation through confidence-gated parent/child edges

## Reasoning

Earlier ontology variants either acted as no-ops or degraded the ranking by over-smoothing labels inside a family. This cycle converted ontology support into a graph-native parent/child propagation mechanism and then stabilized it with a confidence gate and adaptive weighting.

That changed the result qualitatively:

- overall filtered `Hits@3` recovered to the baseline level
- filtered `Hits@5` slightly improved
- tail micro filtered `Hits@3` stayed at `0.3333`, doubling the disease-aware baseline

So the reusable lesson is not merely "ontology helps." It is that ontology becomes useful only when:

- the hierarchy is encoded as parent/child relations
- propagation is confidence-gated
- family-level over-smoothing is controlled

## Changes Made

### Added

- `Confidence-Gated Parent Child Ontology Propagation Preserves Tail Gains`

### Updated

- Current ontology best variant is now the confidence-gated parent/child version

### Removed

- None

## Impact on Future Cycles

- Keep family-bonus ontology variants archived as inferior formulations.
- Start from confidence-gated parent/child propagation for any future ontology work.
- If further improvements are needed, tune gating and evidence confidence before expanding the ontology size.

## Raw Evidence Summary

- baseline filtered `MRR/Hits@3/Hits@5`: `0.8491 / 0.912 / 0.938`
- ontology best variant filtered `MRR/Hits@3/Hits@5`: `0.8490 / 0.912 / 0.939`
- tail micro filtered `Hits@3`: `0.1667 -> 0.3333`
