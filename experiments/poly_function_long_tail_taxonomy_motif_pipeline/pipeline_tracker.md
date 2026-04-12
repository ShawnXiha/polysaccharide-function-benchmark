# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can taxonomy-conditioned motif rarity provide a cleaner rare-label evidence source than unconditioned structural motifs?
- **Start Date**: 2026-03-29
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_taxonomy_motifs_v1.json`

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
- **Method**: taxonomy-conditioned motif candidate generation
- **Config**: feature limit `20`, min local rate `0.2`, base window `20`, candidate limit `5`, activation `1.0`
- **Outcome**:
  - clean filtered `Hits@3`: `0.724 -> 0.724`
  - disease-aware upper-bound filtered `Hits@3`: `0.912 -> 0.912`
- **Status Notes**: fully stable, but effectively a no-op

### Stage 2: Hyperparameter Tuning
- **Attempt**: stronger taxonomy-conditioned motif generation
- **Config**: feature limit `30`, min local rate `0.1`, base window `30`, candidate limit `10`, activation `3.0`
- **Outcome**:
  - clean filtered `Hits@3`: `0.724 -> 0.724`
  - disease-aware upper-bound filtered `Hits@3`: `0.912 -> 0.912`
- **Status Notes**: still no practical tail gain; only tiny secondary metric drift

### Stage 3: Proposed Method Validation
- **Validation**: failed
- **Reason**: no tail improvement in either clean or disease-aware evaluation, even after strengthening the method

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: taxonomy conditioning successfully suppresses structural noise, but that only turns the method into a clean no-op. The conditioned signal still lacks enough rare-label evidence density to help retrieval.
- **Status Notes**: classify this cycle as a denoising-only formulation, not a tail-recovery method

## Results Summary

| Setting | Baseline filtered `Hits@3` | Taxonomy Motif filtered `Hits@3` | Baseline filtered `MRR` | Taxonomy Motif filtered `MRR` | Tail micro filtered `Hits@3` | Mid micro filtered `Hits@3` | Head micro filtered `Hits@3` |
|--------|-----------------------------|----------------------------------|-------------------------|-------------------------------|------------------------------|-----------------------------|------------------------------|
| clean v1 | 0.724 | 0.724 | 0.6020 | 0.6019 | 0.000 -> 0.000 | 0.050 -> 0.050 | 0.7568 -> 0.7568 |
| clean v2 | 0.724 | 0.724 | 0.6020 | 0.6017 | 0.000 -> 0.000 | 0.050 -> 0.050 | 0.7568 -> 0.7568 |
| disease-aware v1 | 0.912 | 0.912 | 0.8491 | 0.8491 | 0.1667 -> 0.1667 | 0.450 -> 0.450 | 0.9361 -> 0.9361 |
| disease-aware v2 | 0.912 | 0.912 | 0.8491 | 0.8489 | 0.1667 -> 0.1667 | 0.450 -> 0.450 | 0.9361 -> 0.9361 |

## Decision

- Do not continue tuning taxonomy-conditioned motifs from the current local structural blocks.
- Taxonomy conditioning improves formulation cleanliness, but not retrieval power.
- The next evidence-source change should move outside the current structure-only family.
