# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can tail-aware disease priors improve disease-aware tail-label recovery without sacrificing the calibration benefit of the original disease-label prior?
- **Start Date**: 2026-03-28
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_prior_w10.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | No |
| 2. Hyperparameter Tuning | Complete | 1 / 8 | <=8 | No |
| 3. Proposed Method Validation | Complete | 1 / 6 | <=6 | No |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 3 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: tail-aware disease prior rerank
- **Config**: disease-aware `top_k=25`, rerank top `30`, tail threshold `10`, prior weight `1.0`, tail boost `2.0`, max multiplier `4.0`
- **Outcome**: filtered `Hits@3` stayed at `0.875`; filtered `MRR` slightly decreased
- **Status Notes**: the tail-aware restriction removed the small gain seen from the ordinary disease prior

### Stage 2: Hyperparameter Tuning
- **Attempt**: more aggressive tail emphasis
- **Config**: rerank top `40`, prior weight `2.0`, tail boost `3.0`, max multiplier `6.0`
- **Outcome**: filtered `Hits@3` still `0.875`; no tail stratum improvement
- **Status Notes**: stronger tail amplification did not cross the top-3 threshold for rare labels

### Stage 3: Proposed Method Validation
- **Validation**: failed
- **Reason**: the method did not improve overall retrieval, did not improve tail `Hits@3`, and did not preserve the calibration gain of the ordinary disease prior

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: disease priors help because they calibrate strong candidates broadly. Restricting them to low-support labels removes the calibration benefit before it becomes strong enough to rescue the rarest labels.
- **Status Notes**: classify this as a method-design failure, not an implementation bug

## Results Summary

| Setting | Baseline filtered `Hits@3` | Tail-aware disease prior | Filtered `MRR` | Tail filtered `Hits@3` | Mid filtered `Hits@3` | Head filtered `Hits@3` |
|--------|-----------------------------|--------------------------|----------------|------------------------|-----------------------|------------------------|
| Conservative | 0.875 | 0.875 | 0.8119 -> 0.8112 | 0.167 -> 0.167 | 0.400 -> 0.400 | 0.899 -> 0.899 |
| Aggressive | 0.875 | 0.875 | 0.8119 -> 0.8111 | 0.167 -> 0.167 | 0.400 -> 0.400 | 0.899 -> 0.899 |

## Decision

- Do not promote tail-aware disease priors.
- Keep the ordinary disease-label compatibility prior as the best disease-aware calibration variant.
- If the goal remains disease-aware tail recovery, the next method should refine tail-label prototypes or change the base disease-function compatibility estimation instead of tail-only reranking.
