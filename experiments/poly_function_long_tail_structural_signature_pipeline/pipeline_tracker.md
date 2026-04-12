# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can rare-label structural signatures from non-disease KG motifs provide a new tail evidence channel without relying on disease semantics?
- **Start Date**: 2026-03-29
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_conditioned_vote_v2.json`

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
- **Method**: tail structural signature rerank using `organism`, `monosaccharide`, and `bond` motif enrichment
- **Config**: threshold `<=10`, top `20`, feature limit `12`, weight `0.5`, min local rate `0.25`, max boost `2.0`
- **Outcome**:
  - clean filtered `Hits@3`: `0.724 -> 0.721`
  - disease-aware upper-bound filtered `Hits@3`: `0.912 -> 0.911`
- **Status Notes**: executable, but effectively a no-op

### Stage 2: Hyperparameter Tuning
- **Attempt**: stronger structural bonus
- **Config**: top `40`, feature limit `20`, weight `5.0`, min local rate `0.15`, max boost `5.0`
- **Outcome**:
  - clean filtered `Hits@3`: `0.724 -> 0.623`
  - disease-aware upper-bound filtered `Hits@3`: `0.912 -> 0.864`
- **Status Notes**: stronger bonuses changed the shortlist, but in the wrong direction

### Stage 3: Proposed Method Validation
- **Validation**: failed
- **Reason**: neither clean nor disease-aware evaluation improved tail recovery; aggressive settings degraded mid/head retrieval substantially

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: structural signatures are not useless in principle, but this specific post-hoc bonus formulation is mismatched to the ranking pipeline. Weak settings do not alter candidates, while strong settings overwhelm local kNN evidence.
- **Status Notes**: classify this cycle as a direction failure for post-hoc structural-signature reranking

## Results Summary

| Setting | Baseline filtered `Hits@3` | Structural Signature filtered `Hits@3` | Baseline filtered `MRR` | Structural Signature filtered `MRR` | Tail micro filtered `Hits@3` | Mid micro filtered `Hits@3` | Head micro filtered `Hits@3` |
|--------|-----------------------------|----------------------------------------|-------------------------|-------------------------------------|------------------------------|-----------------------------|------------------------------|
| clean v1 | 0.724 | 0.721 | 0.6020 | 0.6016 | 0.000 -> 0.000 | 0.050 -> 0.050 | 0.7568 -> 0.7537 |
| clean v2 | 0.724 | 0.623 | 0.6020 | 0.5224 | 0.000 -> 0.000 | 0.050 -> 0.025 | 0.7568 -> 0.6520 |
| disease-aware v1 | 0.912 | 0.911 | 0.8491 | 0.8483 | 0.1667 -> 0.1667 | 0.450 -> 0.450 | 0.9361 -> 0.9350 |
| disease-aware v2 | 0.912 | 0.864 | 0.8491 | 0.8172 | 0.1667 -> 0.1667 | 0.450 -> 0.150 | 0.9361 -> 0.8983 |

## Decision

- Do not continue tuning post-hoc structural-signature bonuses.
- Keep `disease-conditioned base vote + frequency-adjusted disease prior` as the best disease-aware upper bound.
- If structural tail cues are revisited, move them into candidate generation or base-vote construction instead of reranking.
