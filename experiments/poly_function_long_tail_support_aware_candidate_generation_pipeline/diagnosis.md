# Experiment-Craft Diagnosis: Support-Aware Candidate Generation Before Reranking

## 1. Problem Definition

The previous cycles established that rerank-only calibration helps overall retrieval but does not move the long tail. This cycle tested whether the missing piece was candidate support: perhaps rare or mid-support labels need to be introduced into the candidate set before the disease-aware rerank can help them.

## 2. What Was Tried

### Attempt 1: Conservative Candidate Expansion

- candidate top `75`
- base window `20`
- support threshold `50`
- candidate limit `6`
- activation `0.3`

### Attempt 2: Wider Candidate Expansion

- candidate top `100`
- base window `25`
- candidate limit `10`
- activation `0.5`

### Attempt 3: Aggressive Candidate Expansion

- candidate top `150`
- base window `10`
- candidate limit `15`
- activation `2.0`
- rerank top `25`

## 3. Evidence

- In all three attempts, candidate-generation metrics were numerically identical to the paired frequency-adjusted disease-prior baseline
- Filtered `Hits@3`: unchanged
- Filtered `MRR`: unchanged
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Mid micro filtered `Hits@3`: unchanged at `0.400`
- Head micro filtered `Hits@3`: unchanged

## 4. Diagnosis

This cycle failed because the generator never became operational in a retrieval sense. It produced extra support-aware bonuses, but those bonuses did not change which labels actually entered the downstream rerank shortlist strongly enough to alter the final ranking metrics.

That makes the failure mode different from earlier tail-candidate generation. Earlier, candidate injection was too strong and harmed head labels. Here, the design is too detached from the actual shortlist formation, so the method becomes a stable no-op.

The important lesson is structural: in a two-stage retrieval pipeline, candidate generation must be evaluated at the shortlist boundary, not only through its local scoring rule. If it never changes the labels passed forward, then it is not truly part of the retrieval process.

## 5. Next Action

- Stop tuning this exact pre-rerank bonus design.
- Next candidate-generation directions:
  - inspect shortlist entry explicitly and enforce candidate replacement
  - integrate support-aware expansion into the base kNN scorer instead of attaching it afterward
  - use disease-conditioned support smoothing that changes initial retrieval rather than reranking
