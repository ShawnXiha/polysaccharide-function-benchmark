# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can frequency-adjusted disease-function calibration improve disease-aware retrieval by reducing the high-frequency bias of the disease prior without destabilizing the ranking?
- **Start Date**: 2026-03-28
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_prior_w10.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | Yes |
| 2. Hyperparameter Tuning | Complete | 2 / 8 | <=8 | Yes |
| 3. Proposed Method Validation | Complete | 1 / 6 | <=6 | Partial |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 4 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: frequency-adjusted disease prior
- **Config**: `divide` mode, rerank top `20`, prior weight `1.0`, adjustment strength `0.5`
- **Outcome**: filtered `Hits@3` improved from `0.878` to `0.880`; filtered `MRR` improved from `0.8186` to `0.8191`
- **Status Notes**: immediate gain with no aggregate instability

### Stage 2: Hyperparameter Tuning
- **Attempt 1**: aggressive `subtract` mode
- **Config**: rerank top `25`, weight `1.25`, strength `1.0`
- **Outcome**: filtered `Hits@3` fell to `0.877`
- **Status Notes**: aggressive frequency correction over-penalized useful head labels

### Stage 2: Hyperparameter Tuning
- **Attempt 2**: tighter divisive adjustment
- **Config**: rerank top `15`, weight `1.0`, strength `0.75`
- **Outcome**: filtered `Hits@3` returned to `0.878`, below the best conservative setting
- **Status Notes**: the gain is local to a mild adjustment window, not monotonic with strength

### Stage 3: Proposed Method Validation
- **Validation**: partial success
- **Reason**: the method improved the disease-aware baseline overall, but the gain came from calibration rather than long-tail recovery

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: frequency adjustment is useful when mild and divisive. Stronger or subtractive correction removes good head signal before helping the tail.
- **Status Notes**: promote as the new best disease-aware calibration variant, but not as a tail method

## Results Summary

| Setting | Disease prior filtered `Hits@3` | Adjusted filtered `Hits@3` | Disease prior filtered `MRR` | Adjusted filtered `MRR` | Tail micro filtered `Hits@3` |
|--------|----------------------------------|----------------------------|------------------------------|-------------------------|------------------------------|
| Divide v1 | 0.878 | 0.880 | 0.8186 | 0.8191 | 0.167 -> 0.167 |
| Subtract v2 | 0.878 | 0.877 | 0.8186 | 0.8119 | 0.167 -> 0.167 |
| Divide v3 | 0.878 | 0.878 | 0.8186 | 0.8182 | 0.167 -> 0.167 |

## Decision

- Promote mild divisive frequency-adjusted disease prior as the current best disease-aware calibration variant.
- Do not frame it as a long-tail recovery method.
- If the goal remains tail improvement, the next cycle should modify support generation or candidate coverage rather than only rerank calibration.
