# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can explicit tail-support integration inside the base scorer finally improve the hardest tail labels without losing overall disease-aware retrieval quality?
- **Start Date**: 2026-03-28
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_integrated_support_knn_v1.json`

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
- **Method**: explicit tail-support integration inside base kNN
- **Config**: base top `25`, extended top `150`, tail threshold `10`, decay `0.75`, tail boost `2.0`
- **Outcome**: metrics were identical to the paired frequency-adjusted disease-prior baseline
- **Status Notes**: the tail-only expansion did not become operative at conservative strength

### Stage 2: Hyperparameter Tuning
- **Attempt**: stronger tail forcing
- **Config**: base top `20`, extended top `200`, decay `1.25`, tail boost `3.0`, stronger genus/kingdom weights
- **Outcome**: filtered `MRR` improved to `0.8223`, but filtered `Hits@3` fell from `0.880` to `0.878`
- **Status Notes**: stronger tail emphasis distorted broader ranking without helping the tail

### Stage 3: Proposed Method Validation
- **Validation**: failed
- **Reason**: tail micro filtered `Hits@3` stayed `0.167` in all tested settings, so the method did not solve the target problem

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: narrowing support expansion to tail labels is not enough when the real bottleneck is missing evidence density. The method either does nothing or degrades overall top-3 precision.
- **Status Notes**: classify as a task-level failure, not a promising next main method

## Results Summary

| Setting | Baseline filtered `Hits@3` | Tail-support filtered `Hits@3` | Baseline filtered `MRR` | Tail-support filtered `MRR` | Tail micro filtered `Hits@3` | Mid micro filtered `Hits@3` |
|--------|-----------------------------|--------------------------------|-------------------------|-----------------------------|------------------------------|-----------------------------|
| v1 | 0.880 | 0.880 | 0.8191 | 0.8191 | 0.167 -> 0.167 | 0.400 -> 0.400 |
| v2 | 0.880 | 0.878 | 0.8194 | 0.8223 | 0.167 -> 0.167 | 0.400 -> 0.375 |

## Decision

- Do not promote explicit tail-support integration as the next default method.
- The next tail-focused cycle should change evidence construction itself, for example disease-conditioned support smoothing or adaptive expansion around shortlist boundaries.
