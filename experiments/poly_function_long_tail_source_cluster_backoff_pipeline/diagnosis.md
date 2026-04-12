# Experiment-Craft Diagnosis: Source-Cluster Backoff

## 1. Problem Definition

Exact source-constrained reranking improved filtered retrieval quality, but it left the rarest function labels unchanged. The hypothesis in this cycle was that exact organism matches are sometimes too sparse, so reranking should back off from exact organism to broader source clusters such as genus and kingdom.

## 2. What Was Tried

### Attempt 1: Conservative Source-Cluster Backoff

- clean `top_k=10`
- disease-aware `top_k=25`
- rerank top `10`
- exact / genus / kingdom weights `1.0 / 0.6 / 0.3`

## 3. Evidence

- Clean baseline filtered `Hits@3`: `0.743`
- Clean exact source rerank filtered `Hits@3`: `0.768`
- Clean source-cluster backoff filtered `Hits@3`: `0.773`
- Disease-aware baseline filtered `Hits@3`: `0.875`
- Disease-aware exact source rerank filtered `Hits@3`: `0.886`
- Disease-aware source-cluster backoff filtered `Hits@3`: `0.883`

Stratified effects under the tested configuration:

- Clean tail filtered `Hits@3`: unchanged at `0.167`
- Clean mid filtered `Hits@3`: unchanged at `0.375`
- Clean head filtered `Hits@3`: `0.762 -> 0.794`
- Disease-aware tail filtered `Hits@3`: unchanged at `0.167`
- Disease-aware mid filtered `Hits@3`: unchanged at `0.400`
- Disease-aware head filtered `Hits@3`: `0.899 -> 0.908`

## 4. Diagnosis

This method partially works because genus and kingdom backoff can recover source-adjacent evidence when exact organism overlap is missing. In the clean setting, that extra support is useful enough to slightly beat exact source reranking.

But the gain is narrow. The method mostly sharpens head-label ranking and does not change the real long-tail bottleneck. The hardest tail labels still lack enough reliable source support even after backoff, so broadening the source scope does not create genuinely new evidence for them.

The disease-aware setting makes this boundary clearer. Once stronger side-information is already present, soft genus/kingdom bonuses become less useful than precise exact-source evidence. That is why source-cluster backoff improves over plain kNN but still underperforms exact source reranking in the disease-aware regime.

## 5. Next Action

- Keep source-cluster backoff as the best clean source-aware variant.
- Keep exact source reranking as the best disease-aware source-aware variant.
- If the goal remains true tail recovery, move to methods that change candidate support rather than only reranking:
  - tail candidate generation
  - label-specific backoff
  - source-cluster features injected before retrieval instead of after retrieval
