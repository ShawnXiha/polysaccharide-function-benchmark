# Experiment-Craft Diagnosis: Label Prototype Refinement

## 1. Problem Definition

The previous cycle showed that tail-aware disease priors were not enough to move rare labels. This cycle tested a different intuition: perhaps some function labels have a local geometric shape in feature space that is not captured by global kNN vote counts or by disease priors alone. If so, a label prototype could refine the ranking inside the top candidate set.

## 2. What Was Tried

### Attempt 1: Absolute Prototype Bonus

- disease-aware prior base
- rerank top `15`
- prototype neighbors `5`
- prototype weight `0.5`
- tail boost `1.0`

### Attempt 2: Stronger Absolute Prototype Bonus

- rerank top `20`
- prototype neighbors `8`
- prototype weight `0.75`
- tail boost `2.0`

### Attempt 3: Contrastive Prototype Gain

- replace absolute prototype similarity with local-prototype minus global-centroid gain
- rerank top `15`
- prototype neighbors `5`
- prototype weight `0.5`
- tail boost `1.0`

### Attempt 4: Tuned Contrastive Prototype Gain

- rerank top `20`
- prototype neighbors `8`
- prototype weight `0.35`
- tail boost `1.5`

## 3. Evidence

- Disease prior baseline filtered `Hits@3`: `0.878`
- Absolute prototype v1 filtered `Hits@3`: `0.876`
- Absolute prototype v2 filtered `Hits@3`: `0.858`
- Contrastive prototype v3 filtered `Hits@3`: `0.877`
- Contrastive prototype v4 filtered `Hits@3`: `0.877`
- Best contrastive filtered `MRR`: `0.8191` versus baseline `0.8186`
- Tail micro filtered `Hits@3`: baseline `0.167`, best contrastive `0.167`
- Mid micro filtered `Hits@3`: baseline `0.400`, best contrastive `0.350`
- Head micro filtered `Hits@3`: baseline `0.903`, best contrastive `0.904`

## 4. Diagnosis

The first version failed because it used absolute prototype similarity as an additive reward. That duplicated signal already present in the base scorer and disease prior, so strong labels got rewarded again while tail labels still lacked enough support to benefit. The method looked like refinement, but functionally it acted like another broad confidence boost.

Changing the score to a contrastive gain fixed that failure mode. Once the bonus only rewarded labels whose local prototype matched the query better than the global centroid, the method stopped damaging the ranking. That is the useful technical lesson from this cycle.

But the main research question still got a negative answer. Even the stabilized contrastive version improved only overall MRR slightly and did so mostly through head-level reordering. The rarest labels did not move, and mid-support labels even became a bit worse. So prototype refinement is not the missing long-tail mechanism here.

This makes the cycle a partial technical success but a task-level failure. The implementation idea has value, but it should not be promoted as the next main method for disease-aware long-tail retrieval on this KG.

## 5. Next Action

- Keep the contrastive prototype scoring pattern as a reusable rerank design.
- Do not spend more tuning budget on label prototype refinement for this task.
- Next long-tail directions:
  - frequency-adjusted disease-function calibration
  - candidate generation before reranking
  - label-conditional support smoothing that changes the candidate set rather than only reorders it
