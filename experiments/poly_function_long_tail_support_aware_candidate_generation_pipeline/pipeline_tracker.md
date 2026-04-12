# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can support-aware candidate generation improve disease-aware long-tail retrieval by expanding the candidate set before frequency-adjusted reranking?
- **Start Date**: 2026-03-28
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_freq_adjusted_disease_prior_v1.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | No |
| 2. Hyperparameter Tuning | Complete | 2 / 8 | <=8 | No |
| 3. Proposed Method Validation | Complete | 1 / 6 | <=6 | No |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 4 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: support-aware candidate generation before reranking
- **Config**: candidate top `75`, base window `20`, support threshold `50`, candidate limit `6`, activation `0.3`
- **Outcome**: filtered `Hits@3` and filtered `MRR` were identical to the paired frequency-adjusted disease-prior baseline
- **Status Notes**: the generator did not produce any observable retrieval change

### Stage 2: Hyperparameter Tuning
- **Attempt 1**: wider search and stronger activation
- **Config**: candidate top `100`, base window `25`, candidate limit `10`, activation `0.5`
- **Outcome**: still identical to baseline
- **Status Notes**: larger search radius did not change the downstream shortlist

### Stage 2: Hyperparameter Tuning
- **Attempt 2**: aggressive shortlist forcing
- **Config**: candidate top `150`, base window `10`, candidate limit `15`, activation `2.0`
- **Outcome**: still identical to baseline, even with larger rerank top `25`
- **Status Notes**: this confirms a structural no-op rather than a mild under-tuned effect

### Stage 3: Proposed Method Validation
- **Validation**: failed
- **Reason**: the method did not alter overall metrics, per-stratum metrics, or practical candidate behavior

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: support-aware candidate generation only matters if it actually changes the labels entering the rerank stage. Under the current design, it does not.
- **Status Notes**: classify as a pipeline-integration failure, not a useful retrieval gain

## Results Summary

| Setting | Baseline filtered `Hits@3` | Candidate generation filtered `Hits@3` | Baseline filtered `MRR` | Candidate generation filtered `MRR` | Tail micro filtered `Hits@3` |
|--------|-----------------------------|----------------------------------------|-------------------------|-------------------------------------|------------------------------|
| v1 | 0.880 | 0.880 | 0.8191 | 0.8191 | 0.167 -> 0.167 |
| v2 | 0.880 | 0.880 | 0.8191 | 0.8191 | 0.167 -> 0.167 |
| v3 | 0.880 | 0.880 | 0.8194 | 0.8194 | 0.167 -> 0.167 |

## Decision

- Do not promote support-aware candidate generation in its current form.
- The next candidate-generation cycle should explicitly inspect whether new labels enter the rerank window, or integrate candidate expansion directly into the base scorer instead of attaching it as a pre-rerank bonus.
