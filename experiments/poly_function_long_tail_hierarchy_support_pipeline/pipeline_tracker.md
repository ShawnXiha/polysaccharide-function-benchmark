# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can external ontology/hierarchy support provide a new rare-label evidence channel beyond local structure motifs?
- **Start Date**: 2026-03-29
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_conditioned_vote_v2.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | No |
| 2. Hyperparameter Tuning | Complete | 1 / 8 | <=8 | No |
| 3. Proposed Method Validation | Complete | 1 / 6 | <=6 | No |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 4 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: hierarchy-guided candidate support from external coarse function families
- **Config**: base window `20`, threshold `10`, candidate limit `5`, activation `0.75`
- **Outcome**:
  - clean filtered `Hits@3`: `0.724 -> 0.724`
  - disease-aware upper-bound filtered `Hits@3`: `0.912 -> 0.911`
- **Status Notes**: conservative hierarchy support is effectively a stable no-op

### Stage 2: Hyperparameter Tuning
- **Attempt**: stronger hierarchy activation
- **Config**: base window `30`, threshold `10`, candidate limit `10`, activation `3.0`
- **Outcome**:
  - clean filtered `Hits@3`: `0.724 -> 0.713`
  - disease-aware upper-bound filtered `Hits@3`: `0.912 -> 0.889`
- **Status Notes**: stronger hierarchy support harms overall retrieval and collapses tail hits

### Stage 3: Proposed Method Validation
- **Validation**: failed
- **Reason**: the hierarchy does not add discriminative evidence beyond the existing scorer; stronger activation only over-smooths label ranking

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: the current external hierarchy behaves as a coarse smoothing prior, not as a genuine new evidence source. It can leave the shortlist unchanged in weak mode, or distort it in strong mode, but it does not improve rare-label recovery.
- **Status Notes**: classify this cycle as a fundamental failure for the current coarse ontology/hierarchy formulation

## Results Summary

| Setting | Baseline filtered `Hits@3` | Hierarchy filtered `Hits@3` | Baseline filtered `MRR` | Hierarchy filtered `MRR` | Tail micro filtered `Hits@3` | Mid micro filtered `Hits@3` | Head micro filtered `Hits@3` |
|--------|-----------------------------|-----------------------------|-------------------------|--------------------------|------------------------------|-----------------------------|------------------------------|
| clean v1 | 0.724 | 0.724 | 0.6020 | 0.6018 | 0.000 -> 0.000 | 0.050 -> 0.050 | 0.7568 -> 0.7568 |
| clean v2 | 0.724 | 0.713 | 0.6020 | 0.5873 | 0.000 -> 0.000 | 0.050 -> 0.025 | 0.7568 -> 0.7463 |
| disease-aware v1 | 0.912 | 0.911 | 0.8491 | 0.8483 | 0.1667 -> 0.1667 | 0.450 -> 0.450 | 0.9361 -> 0.9350 |
| disease-aware v2 | 0.912 | 0.889 | 0.8491 | 0.8390 | 0.1667 -> 0.000 | 0.450 -> 0.275 | 0.9361 -> 0.9203 |

## Decision

- Do not continue tuning the current coarse hierarchy support formulation.
- Treat `configs/function_hierarchy_v1.json` as a useful ontology wiring test, not as a validated improvement method.
- If ontology/hierarchy is revisited, it needs either:
  - finer-grained curated relations than the current family map
  - true external ontological edges injected into base evidence construction
  - hierarchy-aware retrieval that preserves sibling discrimination instead of family-level smoothing
