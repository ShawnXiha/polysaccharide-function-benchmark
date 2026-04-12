# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can source-constrained reranking improve filtered retrieval quality while shifting more mass toward source-consistent function labels, especially for mid- and low-support functions?
- **Start Date**: 2026-03-27
- **Parent Baseline**: `experiments/poly_function_link_prediction_clean_filtered_stratified.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | Yes |
| 2. Hyperparameter Tuning | Complete | 1 / 8 | <=8 | Yes |
| 3. Proposed Method Validation | Complete | 1 / 6 | <=6 | Yes |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 4 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: two-stage `source-constrained reranking`
- **Config**: rerank top `10` candidates with exact shared-organism bonus, weight `1.0`
- **Outcome**: clean filtered `Hits@3` improved from `0.743` to `0.768`; disease-aware improved from `0.875` to `0.886`
- **Status Notes**: unlike rare-label expansion, this method improved overall retrieval without opening a broad noisy neighborhood

### Stage 2: Hyperparameter Tuning
- **Config**: rerank top `20`, weight `2.0`
- **Outcome**: clean filtered `Hits@3` dropped from `0.768` to `0.762`; disease-aware `Hits@3` stayed `0.886`
- **Status Notes**: stronger source pressure did not help the primary metric; keep the more conservative reranker

### Stage 3: Proposed Method Validation
- **Best Config**: `source_rerank_top_n=10`, `source_rerank_weight=1.0`
- **Clean Result**: filtered `MRR=0.6519`, `Hits@1=0.525`, `Hits@3=0.768`
- **Disease-Aware Result**: filtered `MRR=0.8197`, `Hits@1=0.739`, `Hits@3=0.886`
- **Status Notes**: method is promoted as the new best reranking variant

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: source-constrained reranking improves head and mid-support labels, but does not move the hardest tail labels
- **Status Notes**: this is a selective precision improvement, not a full long-tail solution

## Results Summary

| Setting | Baseline filtered `Hits@3` | Best source-rerank filtered `Hits@3` | Tail filtered `Hits@3` | Mid filtered `Hits@3` | Head filtered `Hits@3` |
|--------|-----------------------------|--------------------------------------|------------------------|-----------------------|------------------------|
| Clean baseline | 0.743 | 0.768 | 0.167 -> 0.167 | 0.375 -> 0.400 | 0.762 -> 0.787 |
| Disease-aware baseline | 0.875 | 0.886 | 0.167 -> 0.167 | 0.400 -> 0.425 | 0.899 -> 0.910 |

## Decision

- `source-constrained reranking` is **promoted** over plain kNN as the best current reranking variant.
- The method is useful because it raises overall filtered quality and improves mid-support labels.
- The hardest unresolved problem remains true tail-label recovery.
