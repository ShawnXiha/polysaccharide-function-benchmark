# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can source-cluster backoff recover signal when exact source matches are sparse by backing off from organism to genus and kingdom?
- **Start Date**: 2026-03-27
- **Parent Baseline**: `experiments/poly_function_link_prediction_clean_filtered_stratified.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | Yes |
| 2. Hyperparameter Tuning | Complete | 0 / 8 | <=8 | No |
| 3. Proposed Method Validation | Complete | 1 / 6 | <=6 | Partial |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 2 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: source-cluster backoff reranking with `organism -> genus -> kingdom`
- **Config**: rerank top `10`, weights `1.0 / 0.6 / 0.3`
- **Outcome**: clean filtered `Hits@3` improved from `0.743` to `0.773`; disease-aware changed from `0.875` to `0.883`
- **Status Notes**: clean setting benefits from soft source backoff, but disease-aware setting does not surpass exact source rerank

### Stage 2: Hyperparameter Tuning
- **Decision**: skipped
- **Reason**: first run already showed a clear pattern: cluster backoff helps clean overall score slightly, but does not improve tail and is weaker than exact source rerank in the disease-aware setting

### Stage 3: Proposed Method Validation
- **Validation**: partial success
- **Clean Result**: promotes from plain kNN to `0.773`, and exceeds exact source rerank `0.768`
- **Disease-Aware Result**: underperforms exact source rerank `0.886`, reaching `0.883`
- **Status Notes**: this is a conditional improvement, not a universal replacement

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: genus/kingdom backoff restores some source signal when exact matches are sparse, but mainly benefits head-label precision; it still does not unlock true tail recovery
- **Status Notes**: cluster backoff should be treated as a clean-setting variant, not the new global best method

## Results Summary

| Setting | Baseline filtered `Hits@3` | Exact source rerank | Source-cluster backoff | Tail filtered `Hits@3` | Mid filtered `Hits@3` | Head filtered `Hits@3` |
|--------|-----------------------------|---------------------|------------------------|------------------------|-----------------------|------------------------|
| Clean | 0.743 | 0.768 | 0.773 | 0.167 | 0.375 | 0.794 |
| Disease-aware | 0.875 | 0.886 | 0.883 | 0.167 | 0.400 | 0.908 |

## Decision

- Promote `source-cluster backoff` only as the best **clean** source-aware variant.
- Keep exact `source-constrained rerank` as the best **disease-aware** source-aware variant.
- Tail recovery remains unresolved.
