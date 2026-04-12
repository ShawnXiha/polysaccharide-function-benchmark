# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can integrating support-aware expansion directly into the base kNN scorer improve disease-aware retrieval by changing shortlist formation rather than adding a detached candidate bonus?
- **Start Date**: 2026-03-28
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_freq_adjusted_disease_prior_v1.json`

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
- **Method**: integrated support-aware kNN scorer
- **Config**: base top `25`, extended top `100`, support threshold `50`, decay `0.35`, exact/genus/kingdom weights `1.0/0.6/0.3`
- **Outcome**: filtered `Hits@3` improved from `0.880` to `0.881`; filtered `MRR` improved from `0.8191` to `0.8193`
- **Status Notes**: the integrated scorer finally changed shortlist behavior and improved mid-support retrieval

### Stage 2: Hyperparameter Tuning
- **Attempt**: stronger expansion
- **Config**: base top `20`, extended top `150`, decay `0.75`, exact/genus/kingdom weights `1.0/0.8/0.5`
- **Outcome**: filtered `MRR` improved further to `0.8228`, but filtered `Hits@3` dropped to `0.879`
- **Status Notes**: stronger expansion helps ranking smoothness more than top-3 recovery

### Stage 3: Proposed Method Validation
- **Validation**: partial success
- **Reason**: the method improved the current best disease-aware baseline overall and improved mid-support labels, but it still did not move the hardest tail

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: integrating expansion into the base scorer matters. Unlike pre-rerank candidate bonuses, it genuinely changes initial retrieval. The first benefit appears in the mid stratum, not the tail.
- **Status Notes**: promote the conservative integrated version as the current best disease-aware retrieval variant

## Results Summary

| Setting | Baseline filtered `Hits@3` | Integrated filtered `Hits@3` | Baseline filtered `MRR` | Integrated filtered `MRR` | Tail micro filtered `Hits@3` | Mid micro filtered `Hits@3` |
|--------|-----------------------------|------------------------------|-------------------------|---------------------------|------------------------------|-----------------------------|
| v1 | 0.880 | 0.881 | 0.8191 | 0.8193 | 0.167 -> 0.167 | 0.400 -> 0.425 |
| v2 | 0.880 | 0.879 | 0.8194 | 0.8228 | 0.167 -> 0.167 | 0.400 -> 0.400 |

## Decision

- Promote the conservative integrated support-aware kNN plus frequency-adjusted disease prior as the current best disease-aware variant.
- Do not claim tail recovery yet.
- If long-tail remains the goal, the next cycle should target explicit tail-support integration rather than only broader support expansion.
