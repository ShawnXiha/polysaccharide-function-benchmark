# Experiment-Craft Diagnosis: Tail Structural Signatures

## 1. Problem Definition

The previous cycle established that the remaining tail gap is not solved by stronger disease use. This cycle tested whether non-disease structural evidence from `organism`, `monosaccharide`, and `bond` motifs could help rare labels through a label-specific structural signature.

## 2. What Was Tried

### Attempt 1: Conservative Structural Signature Bonus

- tail support threshold `<=10`
- rerank top `20`
- feature limit `12`
- signature weight `0.5`
- minimum local rate `0.25`
- max boost `2.0`

### Attempt 2: Strong Structural Signature Bonus

- rerank top `40`
- feature limit `20`
- signature weight `5.0`
- minimum local rate `0.15`
- max boost `5.0`

## 3. Evidence

- Clean baseline filtered `Hits@3`: `0.724`
- Clean structural signature v1 filtered `Hits@3`: `0.721`
- Clean structural signature v2 filtered `Hits@3`: `0.623`
- Disease-aware upper-bound baseline filtered `Hits@3`: `0.912`
- Disease-aware structural signature v1 filtered `Hits@3`: `0.911`
- Disease-aware structural signature v2 filtered `Hits@3`: `0.864`
- Disease-aware tail micro filtered `Hits@3`: unchanged at `0.1667`
- Disease-aware mid micro filtered `Hits@3`: `0.450 -> 0.450 -> 0.150`
- Disease-aware head micro filtered `Hits@3`: `0.9361 -> 0.9350 -> 0.8983`

## 4. Diagnosis

This method failed in a very specific way. The conservative setting did not materially change the ranking, so the new evidence channel did not become active at the scale needed to alter candidate order. The stronger setting did become active, but it overrode useful local neighbor evidence and injected structurally plausible yet label-misaligned candidates into the shortlist.

That means the problem is not simply that the signatures were too weak. The failure pattern is bimodal:

- weak structural bonus: almost no effect
- strong structural bonus: broad ranking distortion without tail gain

This is not the same failure as prototype collapse, because the issue is not a dense representation mismatch. It is a pipeline-stage mismatch. The enriched motif overlap is too coarse to serve as a late rerank bonus, especially once the shortlist is already strong.

## 5. Next Action

- Mark post-hoc structural-signature reranking as a failed direction for this task.
- If structural tail evidence is revisited, inject it earlier:
  - candidate generation conditioned on structural support
  - base-vote modulation using motif-specific support
  - hybrid retrieval where structural candidates are generated separately and then merged before final ranking
