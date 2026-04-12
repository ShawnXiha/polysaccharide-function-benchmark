# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can rare-label neighbor expansion improve tail or mid-support function recovery without materially degrading the filtered retrieval quality of the existing kNN baseline?
- **Start Date**: 2026-03-27
- **Parent Baseline**: `experiments/poly_function_link_prediction_clean_filtered_stratified.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | Yes |
| 2. Hyperparameter Tuning | Complete | 1 / 8 | <=8 | No |
| 3. Proposed Method Validation | Complete | 0 / 6 | <=6 | No |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 3 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: rare-label neighbor expansion on top of filtered meta-path kNN
- **Config**: clean `top_k=10`, `rare_threshold=10`, `rare_top_k=50`, `decay=0.5`
- **Outcome**: tail filtered micro `Hits@3` improved from `0.167` to `0.333`, but overall filtered `Hits@3` dropped from `0.743` to `0.740`
- **Status Notes**: method is executable and does affect the intended region, but gain is narrow and fragile

### Stage 2: Hyperparameter Tuning
- **Config**: clean `rare_threshold=50`, `rare_top_k=75`, `decay=1.0`; disease-aware `rare_threshold=50`, `rare_top_k=100`, `decay=1.0`
- **Outcome**: clean overall filtered `Hits@3` fell further to `0.703`; disease-aware overall filtered `Hits@3` fell from `0.875` to `0.867`
- **Status Notes**: more aggressive expansion improved some mid-support labels but degraded head-heavy aggregate quality

### Stage 3: Proposed Method Validation
- **Gate Condition**: must improve at least one long-tail stratum while keeping overall filtered `Hits@3` within 0.5 points of the baseline, or produce a clearly superior tail metric with acceptable tradeoff
- **Outcome**: not met
- **Status Notes**: no tuned configuration satisfied the tradeoff condition

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: expansion helps isolated rare labels but introduces noisy co-occurrence evidence broadly enough to hurt stable head-label retrieval
- **Status Notes**: this direction is currently a weak partial fix, not a new mainline method

## Results Summary

| Setting | Baseline filtered `Hits@3` | Best rare-expand filtered `Hits@3` | Tail filtered `Hits@3` | Mid filtered `Hits@3` | Head filtered `Hits@3` |
|--------|-----------------------------|------------------------------------|------------------------|-----------------------|------------------------|
| Clean baseline | 0.743 | 0.740 (`t=10,k=50,d=0.5`) | 0.167 -> 0.333 | 0.375 -> 0.375 | 0.762 -> 0.758 |
| Disease-aware baseline | 0.875 | 0.874 (`t=10,k=75,d=0.5`) | 0.167 -> 0.167 | 0.400 -> 0.400 | 0.899 -> 0.898 |
| Disease-aware aggressive | 0.875 | 0.867 (`t=50,k=100,d=1.0`) | 0.167 -> 0.167 | 0.400 -> 0.475 | 0.899 -> 0.888 |

## Decision

- `rare-label neighbor expansion` is **not promoted** to the main pipeline.
- The direction remains interesting as a targeted reranker, but not as a global scoring replacement.
- Next long-tail iteration should prefer mechanisms that improve label specificity without opening large noisy neighborhoods.
