# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can tail candidate generation recover rare functions by injecting a small set of source-aware tail labels from an expanded neighborhood without damaging the strong base kNN ranking?
- **Start Date**: 2026-03-27
- **Parent Baseline**: `experiments/poly_function_link_prediction_clean_filtered_stratified.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | No |
| 2. Hyperparameter Tuning | Complete | 2 / 8 | <=8 | No |
| 3. Proposed Method Validation | Complete | 0 / 6 | <=6 | No |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 3 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: source-aware tail candidate generation from expanded neighbors
- **Config**: `top_k=10`, tail threshold `10`, candidate top-k `75`, candidate limit `5`, activation `1.0`
- **Outcome**: filtered `Hits@3` dropped from `0.743` to `0.653`, while tail micro filtered `Hits@3` improved from `0.167` to `0.333`
- **Status Notes**: candidate generation was active, but activation was too aggressive and displaced strong head labels

### Stage 2: Hyperparameter Tuning
- **Attempt A**: candidate limit `3`, activation `0.5`
- **Attempt B**: candidate limit `3`, activation `1.0`
- **Outcome**: both settings collapsed back to the baseline, with filtered `Hits@3 = 0.743` and tail micro filtered `Hits@3 = 0.167`
- **Status Notes**: stricter source gating removed the harmful over-activation, but also removed almost all useful long-tail gains

### Stage 3: Proposed Method Validation
- **Validation**: failed
- **Reason**: no tuned setting improved the clean baseline or the previous source-aware variants

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: the current method has a calibration failure. Strong activation injects noisy rare labels and harms head precision; strict source-gated activation becomes nearly a no-op
- **Status Notes**: tail candidate generation in its current rerank-only form should not be promoted

## Results Summary

| Setting | Baseline filtered `Hits@3` | Tail candidate generation | Tail filtered `Hits@3` | Head filtered `Hits@3` |
|--------|-----------------------------|---------------------------|------------------------|------------------------|
| Initial candidate activation | 0.743 | 0.653 | 0.333 | 0.667 |
| Tuned activation `0.5`, limit `3` | 0.743 | 0.743 | 0.167 | 0.762 |
| Tuned activation `1.0`, limit `3` | 0.743 | 0.743 | 0.167 | 0.762 |

## Decision

- Do not promote tail candidate generation in its current form.
- Treat this cycle as a method-design failure, not a simple hyperparameter miss.
- The next long-tail step should change where candidate support is introduced, for example:
  - label-specific backoff
  - pre-retrieval tail priors
  - source-cluster features inside the base similarity space rather than post-hoc activation
