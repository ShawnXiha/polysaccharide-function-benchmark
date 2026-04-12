# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can disease-conditioned support smoothing inside the base vote outperform post-hoc disease reranking by injecting disease semantics directly into initial neighbor voting?
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
- **Method**: disease-conditioned base vote
- **Config**: vote top `25`, disease vote weight `0.5`, max boost `3.0`
- **Outcome**: filtered `Hits@3` improved from `0.880` to `0.902`; filtered `MRR` improved from `0.8191` to `0.8433`
- **Status Notes**: immediate large gain over post-hoc disease reranking

### Stage 2: Hyperparameter Tuning
- **Attempt**: stronger disease-conditioned smoothing
- **Config**: vote top `30`, disease vote weight `1.0`, max boost `5.0`
- **Outcome**: filtered `Hits@3` improved further to `0.912`; filtered `MRR` improved to `0.8496`
- **Status Notes**: stronger base-vote conditioning remained beneficial in this regime

### Stage 3: Proposed Method Validation
- **Validation**: partial success
- **Reason**: the method is clearly the strongest disease-aware variant overall, but the tail stratum still does not move

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: if disease semantics are truly informative, injecting them into the base vote is much stronger than applying them only at rerank time. The gain appears in head and mid strata, not the rarest tail.
- **Status Notes**: promote this as the new best disease-aware upper-bound variant, not as a clean tail-recovery method

## Results Summary

| Setting | Baseline filtered `Hits@3` | Disease-conditioned filtered `Hits@3` | Baseline filtered `MRR` | Disease-conditioned filtered `MRR` | Tail micro filtered `Hits@3` | Mid micro filtered `Hits@3` | Head micro filtered `Hits@3` |
|--------|-----------------------------|---------------------------------------|-------------------------|------------------------------------|------------------------------|-----------------------------|------------------------------|
| v1 | 0.880 | 0.902 | 0.8191 | 0.8433 | 0.167 -> 0.167 | 0.400 -> 0.425 | 0.905 -> 0.927 |
| v2 | 0.880 | 0.912 | 0.8194 | 0.8496 | 0.167 -> 0.167 | 0.400 -> 0.450 | 0.904 -> 0.936 |

## Decision

- Promote disease-conditioned base vote plus frequency-adjusted disease prior as the current best disease-aware upper-bound variant.
- Do not present it as evidence that the tail problem is solved.
- If the next goal remains tail recovery, focus on new evidence channels rather than stronger disease exploitation.
