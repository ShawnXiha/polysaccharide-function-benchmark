# Experiment-Craft Diagnosis: Tail Candidate Generation

## 1. Problem Definition

Previous cycles showed that reranking can improve precision, but it does not recover the rarest function labels because those labels often never become serious candidates. This cycle tested whether a separate tail candidate generator could inject a small number of rare labels from an expanded neighborhood and rescue tail retrieval.

## 2. What Was Tried

### Attempt 1: Active Tail Candidate Injection

- clean `top_k=10`
- tail threshold `10`
- candidate top-k `75`
- candidate limit `5`
- activation `1.0`

### Attempt 2: Calibrated Tail Injection

- candidate limit `3`
- activation `0.5`
- require source-cluster support for activation

### Attempt 3: Slightly Stronger Calibrated Injection

- candidate limit `3`
- activation `1.0`
- same source-cluster gating

## 3. Evidence

- Baseline clean filtered `Hits@3`: `0.743`
- Attempt 1 filtered `Hits@3`: `0.653`
- Attempt 1 tail micro filtered `Hits@3`: `0.167 -> 0.333`
- Attempt 1 head micro filtered `Hits@3`: `0.762 -> 0.667`
- Attempt 2 filtered `Hits@3`: `0.743`
- Attempt 3 filtered `Hits@3`: `0.743`
- Attempt 2 and 3 tail micro filtered `Hits@3`: unchanged at `0.167`

## 4. Diagnosis

The failure is not just bad tuning. It comes from an internal contradiction in the method.

If the tail candidates are activated strongly enough to move rare labels upward, they also disturb the stable head-label ordering and damage overall retrieval. That happened in Attempt 1. The generated candidates were real, but the activation rule was too blunt and treated weak rare evidence as if it were comparable to the core kNN score.

When the activation was tightened and source support was required, the opposite happened. The generator became too conservative and essentially stopped changing the ranking. That means the current post-hoc candidate injection design cannot simultaneously satisfy both requirements:

- enough force to rescue true tail labels
- enough selectivity to avoid damaging head precision

## 5. Next Action

- Do not continue tuning this rerank-only candidate generator.
- Move candidate support earlier in the pipeline, not after scoring:
  - label-specific backoff before final scoring
  - source-cluster or tail priors embedded into the base similarity representation
  - candidate generation conditioned on function prototypes rather than raw neighbor presence
