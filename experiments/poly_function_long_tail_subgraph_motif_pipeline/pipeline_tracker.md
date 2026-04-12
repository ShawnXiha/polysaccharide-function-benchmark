# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can label-specific pairwise subgraph motifs provide a more selective tail evidence source than flat structural signatures?
- **Start Date**: 2026-03-29
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_subgraph_motifs_v1.json`

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
- **Method**: label-specific subgraph motifs for candidate generation
- **Config**: motif limit `20`, min local rate `0.2`, base window `20`, candidate limit `5`, activation `0.75`
- **Outcome**:
  - clean filtered `Hits@3`: `0.724 -> 0.724`
  - disease-aware upper-bound filtered `Hits@3`: `0.912 -> 0.911`
- **Status Notes**: executable, but effectively a no-op

### Stage 2: Hyperparameter Tuning
- **Attempt**: stronger motif candidate generation
- **Config**: motif limit `30`, min local rate `0.1`, base window `30`, candidate limit `10`, activation `3.0`
- **Outcome**:
  - clean filtered `Hits@3`: `0.724 -> 0.715`
  - disease-aware upper-bound filtered `Hits@3`: `0.912 -> 0.897`
- **Status Notes**: stronger motif activation changed the shortlist, but still failed to recover tail labels

### Stage 3: Proposed Method Validation
- **Validation**: failed
- **Reason**: tail micro filtered `Hits@3` did not move in either setting; stronger activation degraded mid/head retrieval first

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: pairwise motifs are cleaner than flat overlap, but not strong enough to become a useful tail evidence source in the current KG representation.
- **Status Notes**: classify this cycle as a formulation failure for current subgraph-motif evidence

## Results Summary

| Setting | Baseline filtered `Hits@3` | Subgraph Motif filtered `Hits@3` | Baseline filtered `MRR` | Subgraph Motif filtered `MRR` | Tail micro filtered `Hits@3` | Mid micro filtered `Hits@3` | Head micro filtered `Hits@3` |
|--------|-----------------------------|----------------------------------|-------------------------|-------------------------------|------------------------------|-----------------------------|------------------------------|
| clean v1 | 0.724 | 0.724 | 0.6020 | 0.6019 | 0.000 -> 0.000 | 0.050 -> 0.050 | 0.7568 -> 0.7568 |
| clean v2 | 0.724 | 0.715 | 0.6020 | 0.5943 | 0.000 -> 0.000 | 0.050 -> 0.050 | 0.7568 -> 0.7474 |
| disease-aware v1 | 0.912 | 0.911 | 0.8491 | 0.8484 | 0.1667 -> 0.1667 | 0.450 -> 0.450 | 0.9361 -> 0.9350 |
| disease-aware v2 | 0.912 | 0.897 | 0.8491 | 0.8409 | 0.1667 -> 0.1667 | 0.450 -> 0.275 | 0.9361 -> 0.9277 |

## Decision

- Do not continue tuning the current pairwise motif family.
- Structural-tail evidence based only on the current KG local blocks remains too weak.
- The next tail-evidence direction should bring in a different evidence source, not another variation of the same local structural overlap family.
