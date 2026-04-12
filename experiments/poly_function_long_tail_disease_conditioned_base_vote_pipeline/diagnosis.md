# Experiment-Craft Diagnosis: Disease-Conditioned Base Vote

## 1. Problem Definition

Previous cycles showed that rerank-only disease priors helped overall but did not fully exploit disease semantics. This cycle tested whether disease-conditioned support should be moved into the base vote itself, so that the initial kNN evidence already reflects disease-function compatibility.

## 2. What Was Tried

### Attempt 1: Conservative Disease-Conditioned Vote

- vote top `25`
- disease vote weight `0.5`
- max boost `3.0`

### Attempt 2: Stronger Disease-Conditioned Vote

- vote top `30`
- disease vote weight `1.0`
- max boost `5.0`

## 3. Evidence

- Baseline filtered `Hits@3`: `0.880`
- Conservative disease-conditioned filtered `Hits@3`: `0.902`
- Conservative disease-conditioned filtered `MRR`: `0.8433`
- Stronger disease-conditioned filtered `Hits@3`: `0.912`
- Stronger disease-conditioned filtered `MRR`: `0.8496`
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Mid micro filtered `Hits@3`: `0.400 -> 0.425` and `0.450`
- Head micro filtered `Hits@3`: `0.905 -> 0.927` and `0.936`

## 4. Diagnosis

This cycle succeeded because it moved the right signal to the right place. Disease information is not merely a final-stage calibration hint in this dataset. It is strong enough to shape which labels should receive neighbor support in the first place. Once disease compatibility entered the base vote, the ranking improved sharply.

The size of the gain also clarifies why earlier methods underperformed. Post-hoc disease priors were only correcting the shortlist. Disease-conditioned base voting changes the evidence accumulation process itself, so it can reinforce compatible labels earlier and more consistently.

But the long-tail limitation remains. The rarest labels still do not move, which means the tail problem is not just about when disease information is injected. It is about missing tail-support evidence altogether. So this method is best understood as a stronger disease-aware upper bound, not a tail-recovery solution.

## 5. Next Action

- Use disease-conditioned base vote as the default disease-aware upper-bound variant.
- If long-tail remains the core target, next test:
  - new tail-specific evidence channels
  - disease-conditioned support smoothing combined with explicit shortlist-boundary triggers
  - structure enrichment for rare labels rather than stronger disease weighting
