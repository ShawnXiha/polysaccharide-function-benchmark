# Experiment-Craft Diagnosis: Rare-Label Neighbor Expansion

## 1. Problem Definition

The baseline filtered kNN retriever performs well on head labels but poorly on tail labels. The proposed fix was to expand the neighborhood only for rare labels so that sparse functions could collect evidence from a larger local region.

## 2. What Was Tried

### Attempt 1: Conservative Rare Expansion

- clean `top_k=10`
- `rare_threshold=10`
- `rare_top_k=50`
- `rare_decay=0.5`

### Attempt 2: Aggressive Rare + Mid Expansion

- clean `top_k=10`, `rare_threshold=50`, `rare_top_k=75`, `rare_decay=1.0`
- disease-aware `top_k=25`, `rare_threshold=50`, `rare_top_k=100`, `rare_decay=1.0`

## 3. Evidence

- Clean baseline filtered `Hits@3`: `0.743`
- Clean conservative rare expansion filtered `Hits@3`: `0.740`
- Clean aggressive rare expansion filtered `Hits@3`: `0.703`
- Disease-aware baseline filtered `Hits@3`: `0.875`
- Disease-aware conservative rare expansion filtered `Hits@3`: `0.874`
- Disease-aware aggressive rare expansion filtered `Hits@3`: `0.867`

Stratified effects:

- Clean tail filtered `Hits@3`: `0.167 -> 0.333` under conservative expansion
- Disease-aware tail filtered `Hits@3`: stayed `0.167`
- Disease-aware mid filtered `Hits@3`: `0.400 -> 0.475` under aggressive expansion
- Head metrics consistently decreased when expansion became more aggressive

## 4. Diagnosis

This is not a pure implementation bug. The method does what it was designed to do: it exposes rare labels to more neighbors. The issue is that the added neighbors are not label-specific enough. In this graph, larger neighborhoods quickly reintroduce broad co-occurrence patterns dominated by common biological functions. That extra evidence occasionally rescues a rare label, but more often it dilutes the ranking signal for already stable labels.

The failure mode is therefore **structural noise amplification**, not code failure. Expanding the neighborhood by label frequency alone is too blunt because rarity does not imply that farther neighbors are more semantically precise.

## 5. Next Action

- Do not promote rare-label neighbor expansion as the new default scorer.
- If this direction is revisited, constrain it more sharply:
  - source-aware reranking
  - label-specific prototype neighborhoods
  - two-stage reranking only on a short candidate list
