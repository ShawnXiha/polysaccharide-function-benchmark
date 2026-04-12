# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function link prediction long-tail improvement
- **Research Question**: Can label-specific backoff improve tail recovery by applying source-aware backoff only to low-support labels instead of using a global rerank?
- **Start Date**: 2026-03-28
- **Parent Baseline**: `experiments/poly_function_link_prediction_clean_filtered_stratified.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 1 / 8 | <=8 | Yes |
| 2. Hyperparameter Tuning | Complete | 1 / 8 | <=8 | Yes |
| 3. Proposed Method Validation | Complete | 1 / 6 | <=6 | Partial |
| 4. Ablation / Failure Analysis | Complete | 1 / 8 | <=8 | Yes |

**Total Attempts**: 3 / 30

## Stage Details

### Stage 1: Initial Implementation
- **Method**: label-specific backoff rerank
- **Config**: threshold `10`, rerank top `15`, exact / genus / kingdom `1.0 / 0.6 / 0.3`, weight `0.5`
- **Outcome**: clean filtered `Hits@3` improved from `0.743` to `0.744`; tail micro filtered `Hits@3` improved from `0.167` to `0.333`
- **Status Notes**: this is the first long-tail method that improves tail without harming head or overall clean performance

### Stage 2: Hyperparameter Tuning
- **Attempt**: increase label backoff weight from `0.5` to `1.0`
- **Outcome**: filtered `Hits@3` remained `0.744`
- **Status Notes**: the effect is stable and does not collapse under slightly stronger backoff

### Stage 3: Proposed Method Validation
- **Validation**: partial success
- **Reason**: the gain is small in overall score, but the long-tail signal is real and the method stays stable

### Stage 4: Ablation / Failure Analysis
- **Key Finding**: conditioning backoff on label support fixes the main failure from earlier methods. It preserves the strong base ranking for head labels while allowing some rare labels with meaningful source support to move up
- **Status Notes**: this is a usable long-tail variant, though not yet a large enough jump to replace the main clean baseline narrative

## Results Summary

| Setting | Baseline filtered `Hits@3` | Label-specific backoff | Tail filtered `Hits@3` | Mid filtered `Hits@3` | Head filtered `Hits@3` |
|--------|-----------------------------|------------------------|------------------------|-----------------------|------------------------|
| Clean | 0.743 | 0.744 | 0.167 -> 0.333 | 0.375 -> 0.375 | 0.762 -> 0.762 |

## Decision

- Promote label-specific backoff as the first credible clean long-tail improvement.
- Keep the gain framed as a targeted tail-recovery result, not a new global best overall method.
- Next step should test whether the same idea remains useful with disease-aware features or richer label priors.
