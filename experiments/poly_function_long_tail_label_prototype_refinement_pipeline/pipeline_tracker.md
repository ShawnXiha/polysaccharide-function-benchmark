# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can label prototype refinement improve disease-aware retrieval for rare function labels by adding a local label-shape rerank on top of the disease prior baseline?
- **Start Date**: 2026-03-28
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_prior_w10.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | No |
| 2. Hyperparameter Tuning | Complete | 1 / 8 | <=8 | No |
| 3. Proposed Method Validation | Complete | 2 / 6 | <=6 | Partial |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 5 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: absolute label prototype refinement
- **Config**: disease-aware prior base, rerank top `15`, prototype neighbors `5`, prototype weight `0.5`, tail boost `1.0`
- **Outcome**: filtered `Hits@3` dropped from `0.878` to `0.876`, and tail micro filtered `Hits@3` collapsed from `0.167` to `0.000`
- **Status Notes**: absolute prototype bonuses over-rewarded already strong labels and distorted tail ranking

### Stage 2: Hyperparameter Tuning
- **Attempt**: stronger prototype emphasis
- **Config**: rerank top `20`, prototype neighbors `8`, prototype weight `0.75`, tail boost `2.0`
- **Outcome**: filtered `Hits@3` fell further to `0.858`
- **Status Notes**: stronger prototype weights amplified the failure mode instead of fixing it

### Stage 3: Proposed Method Validation
- **Method Revision**: switch from absolute prototype similarity to contrastive prototype gain against the global centroid
- **Attempt 1**: `top_n=15`, neighbors `5`, weight `0.5`, tail boost `1.0`
- **Outcome**: filtered `Hits@3=0.877`, filtered `MRR=0.8185`, tail micro filtered `Hits@3=0.167`
- **Attempt 2**: `top_n=20`, neighbors `8`, weight `0.35`, tail boost `1.5`
- **Outcome**: filtered `Hits@3=0.877`, filtered `MRR=0.8191`, tail micro filtered `Hits@3=0.167`
- **Validation Result**: partial
- **Reason**: contrastive refinement stabilized the method and slightly improved MRR, but it still did not beat the disease prior baseline on filtered `Hits@3` and did not improve tail retrieval

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: prototype refinement can act as a mild head-calibration tool when written as contrastive gain, but it does not unlock disease-aware tail labels under the current KG signal
- **Status Notes**: keep the contrastive scoring lesson, but do not promote prototype refinement as the new main method

## Results Summary

| Setting | Disease prior filtered `Hits@3` | Prototype refine filtered `Hits@3` | Disease prior filtered `MRR` | Prototype refine filtered `MRR` | Tail micro filtered `Hits@3` |
|--------|----------------------------------|------------------------------------|------------------------------|---------------------------------|------------------------------|
| Absolute v1 | 0.878 | 0.876 | 0.8186 | 0.8178 | 0.167 -> 0.000 |
| Absolute v2 | 0.878 | 0.858 | 0.8186 | 0.8090 | 0.167 -> 0.000 |
| Contrastive v3 | 0.878 | 0.877 | 0.8186 | 0.8185 | 0.167 -> 0.167 |
| Contrastive v4 | 0.878 | 0.877 | 0.8186 | 0.8191 | 0.167 -> 0.167 |

## Decision

- Do not replace the ordinary disease-label prior baseline.
- Keep the contrastive-prototype formulation as a reusable idea, but not as the promoted method for this task.
- If the goal remains long-tail improvement, the next cycle should target frequency-aware calibration or candidate generation before reranking.
