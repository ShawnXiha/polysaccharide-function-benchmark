# Experiment-Craft Diagnosis: Tail Evidence Channels

## 1. Problem Definition

The previous tail-focused cycles showed that reweighting or support expansion alone did not move the rarest labels. This cycle asked whether a new evidence channel could help by changing how support is accumulated at the base vote stage rather than only adjusting scores after retrieval.

## 2. What Was Tried

### Attempt 1: Conservative Disease-Conditioned Base Vote

- vote top `25`
- disease vote weight `0.5`
- max boost `3.0`

### Attempt 2: Stronger Disease-Conditioned Base Vote

- vote top `30`
- disease vote weight `1.0`
- max boost `5.0`

## 3. Evidence

- Baseline filtered `Hits@3`: `0.880`
- Conservative new channel filtered `Hits@3`: `0.902`
- Conservative new channel filtered `MRR`: `0.8433`
- Stronger new channel filtered `Hits@3`: `0.912`
- Stronger new channel filtered `MRR`: `0.8496`
- Tail micro filtered `Hits@3`: unchanged at `0.167`
- Mid micro filtered `Hits@3`: `0.400 -> 0.425` and `0.450`
- Head micro filtered `Hits@3`: `0.905 -> 0.927` and `0.936`

## 4. Diagnosis

This cycle succeeded because it introduced the side-information signal at the point where evidence is actually accumulated. Earlier disease priors only reshaped the shortlist after the fact. Base-vote conditioning changed the vote itself, and that made the system much stronger overall.

At the same time, this cycle also sharpened the long-tail diagnosis. The strongest gains appeared in head and mid labels, while the rarest labels remained flat. That means the current channel is powerful, but it is not new tail evidence. It is more effective use of already dominant disease semantics.

So the correct interpretation is not that the tail problem is solved. The correct interpretation is that the disease-aware upper bound is now much stronger, and the remaining tail gap is more clearly isolated.

## 5. Next Action

- Use disease-conditioned base vote as the default disease-aware upper bound.
- For true tail recovery, next channels should add information not already captured by disease:
  - source-taxonomy compatibility priors
  - monosaccharide or bond motif rarity cues
  - label-specific structural signatures for rare functions
