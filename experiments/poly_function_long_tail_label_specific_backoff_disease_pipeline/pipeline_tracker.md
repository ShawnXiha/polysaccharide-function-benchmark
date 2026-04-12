# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Does label-specific backoff still provide extra long-tail benefit when disease side-information is already included?
- **Start Date**: 2026-03-28
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_filtered_stratified.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | No |
| 2. Hyperparameter Tuning | Complete | 1 / 8 | <=8 | No |
| 3. Proposed Method Validation | Complete | 0 / 6 | <=6 | No |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 2 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: disease-aware label-specific backoff
- **Config**: `top_k=25`, threshold `10`, rerank top `15`, weight `0.5`
- **Outcome**: identical to the disease-aware baseline
- **Status Notes**: no measurable tail or overall gain

### Stage 2: Hyperparameter Tuning
- **Attempt**: increase label backoff weight to `1.0`
- **Outcome**: filtered `Hits@3` dropped from `0.875` to `0.873`
- **Status Notes**: stronger backoff adds slight noise without producing tail gains

### Stage 3: Proposed Method Validation
- **Validation**: failed
- **Reason**: label-specific backoff does not improve the disease-aware setting

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: disease side-information saturates the useful tail signal that label-specific source backoff was exploiting in the clean setting
- **Status Notes**: keep label-specific backoff only as a clean-setting long-tail method

## Results Summary

| Setting | Baseline filtered `Hits@3` | Label-specific backoff | Tail filtered `Hits@3` | Mid filtered `Hits@3` | Head filtered `Hits@3` |
|--------|-----------------------------|------------------------|------------------------|-----------------------|------------------------|
| Disease-aware, `w=0.5` | 0.875 | 0.875 | 0.167 -> 0.167 | 0.400 -> 0.400 | 0.899 -> 0.899 |
| Disease-aware, `w=1.0` | 0.875 | 0.873 | 0.167 -> 0.167 | 0.400 -> 0.400 | 0.899 -> 0.897 |

## Decision

- Do not promote label-specific backoff in the disease-aware setting.
- Keep it as a clean long-tail method only.
- Treat disease-aware long-tail improvement as a different problem that likely needs label priors beyond source evidence.
