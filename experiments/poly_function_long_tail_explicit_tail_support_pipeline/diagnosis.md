# Experiment-Craft Diagnosis: Explicit Tail-Support Integration

## 1. Problem Definition

The integrated support-aware kNN cycle improved the mid-support stratum but still left the rarest labels unchanged. This cycle tested the sharper hypothesis that the support signal must be explicitly targeted to the tail inside the base scorer itself.

## 2. What Was Tried

### Attempt 1: Conservative Tail-Only Integration

- base top `25`
- extended top `150`
- tail threshold `10`
- decay `0.75`
- tail boost `2.0`

### Attempt 2: Stronger Tail-Only Integration

- base top `20`
- extended top `200`
- tail threshold `10`
- decay `1.25`
- tail boost `3.0`
- stronger genus/kingdom weights

## 3. Evidence

- Baseline filtered `Hits@3`: `0.880`
- Conservative tail-support filtered `Hits@3`: `0.880`
- Stronger tail-support filtered `Hits@3`: `0.878`
- Stronger tail-support filtered `MRR`: `0.8223`
- Tail micro filtered `Hits@3`: unchanged at `0.167` in both attempts
- Mid micro filtered `Hits@3`: `0.400 -> 0.375` in the stronger attempt

## 4. Diagnosis

This cycle clarifies an important negative result. Making the expansion tail-specific does not automatically create useful tail evidence. In the conservative setting, the signal stayed too weak to change the final retrieval. In the stronger setting, the added pressure changed the broader ranking but still did not help the rarest labels.

That means the main bottleneck is not simply insufficient targeting. The issue is that the true tail labels do not have enough recoverable support structure in the current feature-neighbor space, even when the scorer is told to focus on them.

So this is not the same as the earlier no-op candidate-generation failure. Here the method can influence ranking when pushed hard enough, but it still fails on the actual target metric. That makes it a task-level failure rather than a pure integration failure.

## 5. Next Action

- Stop tuning explicit tail-support expansion in this form.
- Next tail-focused directions:
  - disease-conditioned support smoothing inside the base vote
  - adaptive expansion triggered only when the positive label is near the shortlist boundary
  - richer evidence channels for tail labels rather than stronger weighting alone
