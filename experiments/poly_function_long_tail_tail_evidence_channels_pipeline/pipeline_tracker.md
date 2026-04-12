# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can new tail evidence channels improve disease-aware retrieval beyond rerank-only methods by changing the base evidence accumulation process?
- **Start Date**: 2026-03-28
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_integrated_support_knn_v1.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | Yes |
| 2. Hyperparameter Tuning | Complete | 1 / 8 | <=8 | Yes |
| 3. Proposed Method Validation | Complete | 1 / 6 | <=6 | Partial |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 4 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: disease-conditioned support smoothing inside the base vote
- **Config**: vote top `25`, disease vote weight `0.5`, max boost `3.0`
- **Outcome**: filtered `Hits@3` improved from `0.880` to `0.902`; filtered `MRR` improved from `0.8191` to `0.8433`
- **Status Notes**: immediate gain showed that disease-conditioned smoothing is stronger when injected into evidence accumulation rather than reranking

### Stage 2: Hyperparameter Tuning
- **Attempt**: stronger disease-conditioned smoothing
- **Config**: vote top `30`, disease vote weight `1.0`, max boost `5.0`
- **Outcome**: filtered `Hits@3` improved further to `0.912`; filtered `MRR` improved to `0.8496`
- **Status Notes**: stronger conditioning stayed beneficial for overall retrieval

### Stage 3: Proposed Method Validation
- **Validation**: partial success
- **Reason**: the new base-vote evidence channel is clearly the strongest disease-aware upper-bound variant, but it still does not improve the hardest tail stratum

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: moving strong side-information into the base vote is far more effective than rerank-only use, but it remains an upper-bound improvement rather than a true tail-evidence solution
- **Status Notes**: promote as the best disease-aware variant; do not over-claim tail recovery

## Results Summary

| Setting | Baseline filtered `Hits@3` | New channel filtered `Hits@3` | Baseline filtered `MRR` | New channel filtered `MRR` | Tail micro filtered `Hits@3` | Mid micro filtered `Hits@3` | Head micro filtered `Hits@3` |
|--------|-----------------------------|-------------------------------|-------------------------|----------------------------|------------------------------|-----------------------------|------------------------------|
| v1 | 0.880 | 0.902 | 0.8191 | 0.8433 | 0.167 -> 0.167 | 0.400 -> 0.425 | 0.905 -> 0.927 |
| v2 | 0.880 | 0.912 | 0.8194 | 0.8496 | 0.167 -> 0.167 | 0.400 -> 0.450 | 0.904 -> 0.936 |

## Decision

- Promote disease-conditioned base vote plus frequency-adjusted disease prior as the current best disease-aware upper-bound variant.
- Do not frame this cycle as solving the tail problem.
- If the next goal remains tail recovery, the next evidence channel must add new information rather than stronger disease exploitation.
