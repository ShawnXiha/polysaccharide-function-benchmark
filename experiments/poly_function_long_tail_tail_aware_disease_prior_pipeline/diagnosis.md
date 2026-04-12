# Experiment-Craft Diagnosis: Tail-Aware Disease Priors

## 1. Problem Definition

The ordinary disease-label prior improved disease-aware retrieval slightly, but only through calibration on stronger labels. This cycle tested whether making that prior explicitly tail-aware could preserve the calibration signal while finally moving the rarest labels.

## 2. What Was Tried

### Attempt 1: Conservative Tail-Aware Prior

- disease-aware `top_k=25`
- rerank top `30`
- tail threshold `10`
- prior weight `1.0`
- tail boost `2.0`
- max multiplier `4.0`

### Attempt 2: Aggressive Tail-Aware Prior

- disease-aware `top_k=25`
- rerank top `40`
- tail threshold `10`
- prior weight `2.0`
- tail boost `3.0`
- max multiplier `6.0`

## 3. Evidence

- Disease-aware baseline filtered `Hits@3`: `0.875`
- Tail-aware disease prior filtered `Hits@3`: `0.875` in both attempts
- Disease-aware baseline filtered `MRR`: `0.8119`
- Tail-aware disease prior filtered `MRR`: approximately `0.8112` and `0.8111`
- Disease-aware tail micro filtered `Hits@3`: unchanged at `0.167`
- Disease-aware mid micro filtered `Hits@3`: unchanged at `0.400`
- Disease-aware head micro filtered `Hits@3`: unchanged at `0.899`

## 4. Diagnosis

This method failed for a structural reason. The ordinary disease prior works because it adds broad compatibility calibration to candidates that are already plausible under the disease-aware representation. Once that prior is restricted to low-support labels, the method gives up the part that was actually useful.

The remaining tail-only signal is too weak to change the ranking in a meaningful way. Rare labels still have sparse disease-conditioned support, so even after boosting them, they usually do not cross the top-3 cutoff. In other words, the prior was not failing because it was insufficiently tail-aware. It was helping somewhere else.

That makes this a method-design failure rather than an implementation issue. The code did what it was intended to do, but the design assumption was wrong: narrowing a calibration prior to tail labels does not automatically turn it into a tail-recovery mechanism.

## 5. Next Action

- Keep the ordinary disease-label prior as the preferred disease-aware variant.
- Do not continue tuning tail-aware prior weights or thresholds.
- Next disease-aware long-tail directions:
  - label prototype refinement
  - frequency-adjusted disease-function calibration
  - tail-aware candidate generation integrated before reranking rather than after it
