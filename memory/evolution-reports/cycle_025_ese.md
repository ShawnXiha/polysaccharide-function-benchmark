# Evolution Report: Cycle 025 - ESE

**Date**: 2026-03-29
**Trigger**: Standard shallow baselines and GNN failure ablations completed on the unified clean `train/valid/test` split
**Source Artifacts**:
- `src/polysaccharidesgraph/models/run_shallow_feature_baselines.py`
- `src/polysaccharidesgraph/models/run_hetero_gnn_baseline.py`
- `src/polysaccharidesgraph/models/run_hybrid_hetero_gnn_baseline.py`
- `experiments/shallow_baseline_gnn_ablation_pipeline/pipeline_tracker.md`
- `experiments/shallow_baseline_gnn_ablation_pipeline/diagnosis.md`

## Success Classification

- **Type**: Reusable strategy extraction
- **Direction**: standard shallow benchmarks and representation-focused GNN diagnosis

## Reasoning

This cycle answered two revision-critical questions for the paper.

First, it established a stronger clean shallow benchmark under the same `train/valid/test` protocol used by the neural baselines. The best setting was not a neural shallow model but a regularized linear one-vs-rest classifier on concatenated local graph features:

- `meta_path + logreg`: macro-F1 `0.3465`
- `poly_x + meta_path + logreg`: macro-F1 `0.3603`
- `meta_path + mlp`: macro-F1 `0.3065`

Second, it converted the qualitative "GNN seems weak" claim into a controlled failure diagnosis. Across multiple seeds, the full hetero model and the no-message ablation were nearly identical:

- base `hetero_sage`: mean macro-F1 `0.0443`
- base `hetero_no_message`: mean macro-F1 `0.0423`

The same pattern persisted on the hybrid graph, where no-message stayed competitive with or better than the full hetero model. This means the current bottleneck is not just a missing tuning trick; the present graph evidence and node semantics are not giving message passing enough useful incremental signal.

## Changes Made

### Added

- `Standard Linear One-Vs-Rest Baselines Are Mandatory On Sparse Typed KGs`
- `Full Hetero GNN Matching No-Message Ablations Signals A Representation Bottleneck`
- `Diagnose Message Passing Value With Full Vs No-Message Paired Ablations`

### Updated

- The paper-side interpretation of the clean benchmark now has stronger support: explicit shallow feature models are stronger than the current hetero / hybrid GNN formulations on DoLPHiN KG v0.

### Removed

- None

## Impact on Future Cycles

- Always run a strong linear OVR baseline on explicit graph feature blocks before judging a new GNN formulation.
- If `full ≈ no-message`, stop optimizer-centric tuning and revisit graph evidence, node semantics, and feature design.
- In writing, frame the clean result as a representation mismatch diagnosis rather than a generic anti-GNN claim.

## Raw Evidence Summary

- best shallow clean baseline: `poly_x + meta_path + logreg`, macro-F1 `0.3603`, exact match `0.5364`
- strongest meta-path-only shallow baseline: `meta_path + logreg`, macro-F1 `0.3465`
- `meta_path + mlp`: macro-F1 `0.3065`
- base `hetero_sage` mean over seeds `42 / 7 / 123`: `0.0443`
- base `hetero_no_message` mean over seeds `42 / 7 / 123`: `0.0423`
- hybrid `hetero_sage`: `0.0347`
- hybrid `hetero_no_message`: `0.0386`
