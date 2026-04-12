# Experiment-Craft Diagnosis: Integrated Support-Aware kNN

## 1. Problem Definition

The previous support-aware candidate generation cycle failed because it never changed the downstream shortlist. This cycle tested a stronger structural hypothesis: if support-aware expansion is merged directly into the base kNN scorer, it may finally alter initial retrieval rather than behaving as a detached bonus.

## 2. What Was Tried

### Attempt 1: Conservative Integrated Expansion

- base top `25`
- extended top `100`
- support threshold `50`
- decay `0.35`
- exact/genus/kingdom weights `1.0/0.6/0.3`

### Attempt 2: Stronger Integrated Expansion

- base top `20`
- extended top `150`
- support threshold `50`
- decay `0.75`
- exact/genus/kingdom weights `1.0/0.8/0.5`

## 3. Evidence

- Baseline filtered `Hits@3`: `0.880`
- Conservative integrated filtered `Hits@3`: `0.881`
- Conservative integrated filtered `MRR`: `0.8193`
- Mid micro filtered `Hits@3`: `0.400 -> 0.425`
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Stronger integrated filtered `Hits@3`: `0.879`
- Stronger integrated filtered `MRR`: `0.8228`

## 4. Diagnosis

This cycle succeeded where the previous candidate-generation design failed because the added support signal was no longer structurally detached. By contributing inside the base kNN score itself, the extra low-support evidence could actually change initial shortlist formation.

The gain pattern is also informative. The first improvement appeared in mid-support labels, not the hardest tail. That suggests the method is recovering labels that already have some latent support but were previously just below the shortlist boundary. The rarest labels still do not have enough support density for this expansion alone to rescue them.

The stronger setting confirms the tradeoff boundary. More aggressive expansion improves MRR, meaning it smooths the broader ranking, but it starts to sacrifice top-3 precision. So the useful regime here is conservative integration, not large-radius expansion.

## 5. Next Action

- Keep the conservative integrated support-aware kNN as the preferred variant.
- If the next target is still the hardest tail, test:
  - tail-specific support integration inside the base scorer
  - disease-conditioned support smoothing inside the neighbor vote
  - adaptive expansion that triggers only for labels below the shortlist boundary
