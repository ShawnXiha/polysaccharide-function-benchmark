# Experiment-Craft Diagnosis: Disease-Label Compatibility Prior

## 1. Problem Definition

The previous disease-aware experiments showed that source-based long-tail fixes do not transfer well once disease features are already present. This cycle tested a different hypothesis: instead of adding more source structure, use training-set disease-function compatibility as a lightweight prior to calibrate the disease-aware ranking.

## 2. What Was Tried

### Attempt 1: Conservative Disease Prior

- disease-aware `top_k=25`
- rerank top `15`
- prior weight `0.5`
- Laplace smoothing `alpha=1.0`

### Attempt 2: Stronger Disease Prior

- same setup
- prior weight `1.0`

## 3. Evidence

- Disease-aware baseline filtered `Hits@3`: `0.875`
- Disease prior filtered `Hits@3`: `0.878`
- Disease-aware tail micro filtered `Hits@3`: unchanged at `0.167`
- Disease-aware mid micro filtered `Hits@3`: unchanged at `0.400`
- Disease-aware head micro filtered `Hits@3`: `0.899 -> 0.903`

Representative compatible-label gains:

- `antimicrobial`: filtered mean rank improved from `4.00` to `3.84`
- `cholesterol_lowering`: filtered `Hits@3` improved from `0.500` to `0.556`

## 4. Diagnosis

This method works because it aligns the ranking with the semantics that already dominate the disease-aware setting. Unlike label-specific source backoff, it is not trying to supply missing structure from another channel. It simply says: given the diseases attached to this polysaccharide, which function labels have historically been compatible in the training graph?

That makes the effect clean but limited. The prior sharpens already plausible head and upper-mid predictions, which is why overall filtered `Hits@3` improves. But the hard tail does not move, because the tail labels do not have enough disease-linked training support for the prior to become informative.

## 5. Next Action

- Keep disease-label priors as the best disease-aware calibration method.
- Separate this result from true long-tail recovery in the write-up.
- If disease-aware tail recovery is still the goal, next test:
  - tail-aware disease priors
  - label prototype refinement
  - frequency-adjusted disease-function calibration
