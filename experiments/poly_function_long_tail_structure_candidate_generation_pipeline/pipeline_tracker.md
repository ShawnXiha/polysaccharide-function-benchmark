# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can structure-aware candidate generation recover rare labels by promoting tail candidates before reranking?
- **Start Date**: 2026-03-29
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_structure_candidates_v1.json`

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
- **Method**: structure-aware candidate generation using label-specific structural signatures
- **Config**: base window `20`, candidate limit `5`, activation `0.5`
- **Outcome**:
  - clean filtered `Hits@3`: `0.724 -> 0.724`
  - disease-aware upper-bound filtered `Hits@3`: `0.912 -> 0.911`
- **Status Notes**: executable, but effectively a no-op

### Stage 2: Hyperparameter Tuning
- **Attempt**: stronger candidate generation
- **Config**: base window `30`, candidate limit `10`, activation `3.0`
- **Outcome**:
  - clean filtered `Hits@3`: `0.724 -> 0.715`
  - disease-aware upper-bound filtered `Hits@3`: `0.912 -> 0.892`
- **Status Notes**: stronger activation changed the shortlist, but still failed to improve tail retrieval

### Stage 3: Proposed Method Validation
- **Validation**: failed
- **Reason**: tail micro filtered `Hits@3` did not move in either setting; stronger activation degraded mid/head retrieval first

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: moving structural cues from reranking into candidate generation is not enough. The structure signal itself is not discriminative enough for true tail recovery in the current representation.
- **Status Notes**: classify this cycle as another formulation failure for structural-tail evidence

## Results Summary

| Setting | Baseline filtered `Hits@3` | Structure Candidate filtered `Hits@3` | Baseline filtered `MRR` | Structure Candidate filtered `MRR` | Tail micro filtered `Hits@3` | Mid micro filtered `Hits@3` | Head micro filtered `Hits@3` |
|--------|-----------------------------|---------------------------------------|-------------------------|------------------------------------|------------------------------|-----------------------------|------------------------------|
| clean v1 | 0.724 | 0.724 | 0.6020 | 0.6019 | 0.000 -> 0.000 | 0.050 -> 0.050 | 0.7568 -> 0.7568 |
| clean v2 | 0.724 | 0.715 | 0.6020 | 0.5923 | 0.000 -> 0.000 | 0.050 -> 0.050 | 0.7568 -> 0.7474 |
| disease-aware v1 | 0.912 | 0.911 | 0.8491 | 0.8483 | 0.1667 -> 0.1667 | 0.450 -> 0.450 | 0.9361 -> 0.9350 |
| disease-aware v2 | 0.912 | 0.892 | 0.8491 | 0.8399 | 0.1667 -> 0.1667 | 0.450 -> 0.275 | 0.9361 -> 0.9224 |

## Decision

- Do not continue tuning this structure-aware candidate-generation formulation.
- Structural evidence remains too weak for tail recovery in the current feature space.
- If structural tail work continues, the next move should change the evidence source itself, not only the injection stage.
