# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can disease-label compatibility priors improve disease-aware retrieval by calibrating function labels using training-set disease-function associations?
- **Start Date**: 2026-03-28
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_filtered_stratified.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | Yes |
| 2. Hyperparameter Tuning | Complete | 1 / 8 | <=8 | Yes |
| 3. Proposed Method Validation | Complete | 1 / 6 | <=6 | Partial |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 3 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: disease-label compatibility prior rerank
- **Config**: disease-aware `top_k=25`, rerank top `15`, prior weight `0.5`, Laplace smoothing `alpha=1.0`
- **Outcome**: filtered `Hits@3` improved from `0.875` to `0.878`
- **Status Notes**: immediate gain without destabilizing the strong disease-aware baseline

### Stage 2: Hyperparameter Tuning
- **Attempt**: increase prior weight to `1.0`
- **Outcome**: metrics remained effectively identical to `w=0.5`
- **Status Notes**: the method is stable in this local range

### Stage 3: Proposed Method Validation
- **Validation**: partial success
- **Reason**: the method improves the disease-aware baseline, but the gain comes from head-label calibration rather than long-tail recovery

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: disease-label priors add useful compatibility calibration on top of disease-aware kNN, but they do not change the hard tail labels
- **Status Notes**: this is a disease-aware calibration method, not a tail-specific fix

## Results Summary

| Setting | Baseline filtered `Hits@3` | Disease prior | Tail filtered `Hits@3` | Mid filtered `Hits@3` | Head filtered `Hits@3` |
|--------|-----------------------------|---------------|------------------------|-----------------------|------------------------|
| Disease-aware | 0.875 | 0.878 | 0.167 -> 0.167 | 0.400 -> 0.400 | 0.899 -> 0.903 |

## Decision

- Promote disease-label compatibility prior as the preferred disease-aware calibration variant.
- Do not claim it as a long-tail solution.
- If the goal remains disease-aware tail recovery, the next method should target tail labels explicitly rather than relying on global disease-function priors.
