# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG standard shallow baselines and GNN failure ablation
- **Research Question**: On the unified `train/valid/test` split, do standard shallow feature baselines outperform the current hetero/hybrid GNNs, and do failure ablations show that message passing is not the main source of signal?
- **Start Date**: 2026-03-29
- **Parent Baselines**:
  - `experiments/meta_path_baseline_random.json`
  - `experiments/hetero_gnn_baseline_random_tuned.json`
  - `experiments/hybrid_hetero_gnn_baseline_random.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | Yes |
| 2. Hyperparameter Tuning | Complete | 2 / 8 | <=8 | Yes |
| 3. Proposed Method Validation | Complete | 1 / 6 | <=6 | Yes |
| 4. Ablation / Failure Analysis | Complete | 2 / 8 | <=8 | Yes |

**Total Attempts**: 6 / 30

## Stage Notes

### 2026-04-12 P0 Clean Feature Leakage Remediation

The original `poly_x` export included `degree__disease` even in the nominal clean payload. This has now been fixed in `export_pyg.py`: the default clean export has `poly_feature_dim=354` and `num_disease_derived_poly_features=0`, while the explicit disease-aware export has `poly_feature_dim=355` and includes `degree__disease` as the only disease-derived polysaccharide feature.

The clean shallow baselines were rerun on the corrected payload:

- `meta_path + logreg`: test macro-F1 `0.3465`, exact match `0.5118`
- `poly_x + logreg`: test macro-F1 `0.0612`, exact match `0.0079`
- `poly_x + meta_path + logreg`: test macro-F1 `0.3317`, exact match `0.5059`
- `meta_path + mlp`: test macro-F1 `0.3065`, exact match `0.5295`

The clean GNN failure ablations were also rerun on the corrected payload:

- `hetero_sage`: test macro-F1 `0.0464`, exact match `0.0138`
- `hetero_no_message`: test macro-F1 `0.0426`, exact match `0.0315`
- `poly_mlp`: test macro-F1 `0.0466`, exact match `0.0197`

Decision update: promote `meta_path + logreg` as the strongest leakage-controlled clean baseline. Keep `poly_x + meta_path + logreg` as a secondary diagnostic showing that the corrected `poly_x` block does not add value over meta-path features alone.

### Stage 1: Initial Implementation
- **Goal**: reproduce the current clean meta-path / hetero baselines under the unified `train/valid/test` protocol and verify the new runner scripts work.
- **Outcome**:
  - `meta_path + logreg`: test macro-F1 `0.3465`
  - `poly_x + logreg`: test macro-F1 `0.0972`
  - `poly_x + meta_path + logreg`: test macro-F1 `0.3603`
  - `hetero_sage`: test macro-F1 `0.0443`
- **Superseded note**: these values were computed before the 2026-04-12 clean `poly_x` feature-boundary fix. Use the P0 remediation values above for paper claims.
- **Interpretation**: the new unified protocol is working, and the old qualitative conclusion survives protocol tightening: explicit shallow feature models dominate the current hetero GNN.

### Stage 2: Hyperparameter Tuning
- **Goal**: find stable shallow baseline settings among `logreg`, `sgd_logloss`, and `mlp` on `meta_path`, `poly_x`, and `poly_x_meta`.
- **Outcome**:
  - `meta_path + sgd_logloss`: test macro-F1 `0.1649`
  - `meta_path + mlp`: test macro-F1 `0.3065`
  - best setting remains `poly_x + meta_path + logreg`: test macro-F1 `0.3603`
  - seed re-runs (`42 / 7 / 123`) for `poly_x + meta_path + logreg` were identical, confirming a stable deterministic shallow baseline
- **Interpretation**: on this KG, a regularized linear one-vs-rest classifier is stronger than both a shallow neural classifier and a weaker linear SGD surrogate.

### Stage 3: Proposed Method Validation
- **Goal**: lock the strongest shallow baseline for paper comparison and confirm that the result is not a metric artifact.
- **Decision**: promote `poly_x + meta_path + logreg` as the primary shallow benchmark for the revised paper.
- **Reason**:
  - it improves over `meta_path + logreg` (`0.3465 -> 0.3603`)
  - it is stable across seeds
  - it uses the same clean split and validation-threshold protocol as the GNN baselines

### Stage 4: Ablation / Failure Analysis
- **Goal**: compare `hetero_sage` against `hetero_no_message`, `poly_mlp`, and hybrid variants to isolate whether message passing adds value beyond node-local features.
- **Outcome**:
  - base graph:
    - `hetero_sage`: macro-F1 mean over seeds `0.0443`
    - `hetero_no_message`: macro-F1 mean over seeds `0.0423`
    - `poly_mlp`: macro-F1 `0.0474`
  - hybrid graph:
    - `hybrid hetero_sage`: macro-F1 `0.0347`
    - `hybrid no-message`: macro-F1 `0.0386`
    - `hybrid poly_mlp`: macro-F1 `0.0440`
- **Interpretation**: message passing does not supply meaningful gain under the current KG representation. Across both base and hybrid inputs, removing message passing leaves performance essentially unchanged, while all neural variants remain far below the best shallow linear baseline.

## Results Summary

| Family | Variant | Test macro-F1 | Test exact match |
|--------|---------|---------------|------------------|
| Shallow | `meta_path + logreg` | `0.3465` | `0.5118` |
| Shallow | `poly_x + logreg` | `0.0972` | `0.0364` |
| Shallow | `poly_x + meta_path + logreg` | `0.3603` | `0.5364` |
| Shallow | `meta_path + mlp` | `0.3065` | `0.5295` |
| Shallow | `meta_path + sgd_logloss` | `0.1649` | `0.2372` |
| GNN | `hetero_sage` | `0.0443` | `0.0256` |
| GNN Ablation | `hetero_no_message` | `0.0430` | `0.0236` |
| GNN Ablation | `poly_mlp` | `0.0474` | `0.0187` |
| Hybrid GNN | `hetero_sage` | `0.0347` | `0.0364` |
| Hybrid Ablation | `hetero_no_message` | `0.0386` | `0.1132` |
| Hybrid Ablation | `poly_mlp` | `0.0440` | `0.0089` |

## Decision

- Keep `meta_path + logreg` as the strongest leakage-controlled clean shallow baseline under the unified split.
- Treat `poly_x + meta_path + logreg` as a secondary diagnostic after the disease-derived `poly_x` feature was removed.
- Use the GNN ablations as evidence that current failures are not mainly an optimizer problem: message passing itself is not adding useful signal on top of the present graph and feature design.
- In the paper, phrase the conclusion as `explicit retrieval / explicit feature classification > current hetero message passing on DoLPHiN KG v0`, not as a blanket anti-GNN claim.
