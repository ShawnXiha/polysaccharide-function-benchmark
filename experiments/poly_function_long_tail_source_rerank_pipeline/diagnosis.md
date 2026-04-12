# Experiment-Craft Diagnosis: Source-Constrained Reranking

## 1. Problem Definition

The base filtered kNN retriever is strong overall, but its ranking is agnostic to whether candidate labels are supported by polysaccharides from the same source organism. The hypothesis was that exact source consistency could improve label specificity without the broad noise introduced by neighborhood expansion.

## 2. What Was Tried

### Attempt 1: Conservative Source Rerank

- clean `top_k=10`
- disease-aware `top_k=25`
- rerank top `10`
- shared-organism bonus weight `1.0`

### Attempt 2: Stronger Source Pressure

- rerank top `20`
- shared-organism bonus weight `2.0`

## 3. Evidence

- Clean baseline filtered `Hits@3`: `0.743`
- Clean source rerank filtered `Hits@3`: `0.768`
- Disease-aware baseline filtered `Hits@3`: `0.875`
- Disease-aware source rerank filtered `Hits@3`: `0.886`

Stratified effects under the best configuration:

- Clean tail filtered `Hits@3`: unchanged at `0.167`
- Clean mid filtered `Hits@3`: `0.375 -> 0.400`
- Clean head filtered `Hits@3`: `0.762 -> 0.787`
- Disease-aware tail filtered `Hits@3`: unchanged at `0.167`
- Disease-aware mid filtered `Hits@3`: `0.400 -> 0.425`
- Disease-aware head filtered `Hits@3`: `0.899 -> 0.910`

## 4. Diagnosis

This method works because source consistency is a selective signal. It only reorders a short candidate list, so it improves precision where same-organism evidence is genuinely informative. That avoids the failure mode of rare-label neighbor expansion, which widened the search space and amplified broad co-occurrence noise.

At the same time, the method does not solve the hardest tail labels. Those cases often lack enough source-consistent training examples to provide a meaningful rerank bonus. So the method improves ranking quality mainly for head and mid-support labels, not for the rarest functions.

## 5. Next Action

- Keep source-constrained reranking as the preferred rerank variant.
- If the goal remains long-tail improvement, combine it with a second mechanism that addresses missing source evidence:
  - source-cluster backoff
  - label-specific reranking
  - candidate-generation for tail labels before source rerank
