# Experiment-Craft Diagnosis: Disease-Aware Label-Specific Backoff

## 1. Problem Definition

Label-specific backoff worked in the clean setting by giving a small source-aware boost only to low-support labels. This cycle tested whether the same mechanism remains helpful once disease features are already included in the base retrieval representation.

## 2. What Was Tried

### Attempt 1: Conservative Disease-Aware Backoff

- disease-aware `top_k=25`
- label threshold `10`
- rerank top `15`
- label backoff weight `0.5`

### Attempt 2: Stronger Disease-Aware Backoff

- same setup
- label backoff weight `1.0`

## 3. Evidence

- Disease-aware baseline filtered `Hits@3`: `0.875`
- Attempt 1 filtered `Hits@3`: `0.875`
- Attempt 2 filtered `Hits@3`: `0.873`
- Disease-aware tail micro filtered `Hits@3`: unchanged at `0.167` in both attempts
- Disease-aware mid micro filtered `Hits@3`: unchanged at `0.400`
- Disease-aware head micro filtered `Hits@3`: `0.899 -> 0.897` under stronger backoff

## 4. Diagnosis

This is not a useful extension of the clean result. In the disease-aware setting, the base scorer already carries strong semantic information. The additional source-aware label-specific backoff does not expose new tail evidence; at best it is redundant, and at worst it perturbs an already well-calibrated ranking.

The contrast with the clean setting is important. There, label-specific backoff supplied missing structure. Here, disease features already dominate the ranking, so the same backoff channel has little marginal value. This should be interpreted as signal saturation, not as a tuning miss.

## 5. Next Action

- Keep label-specific backoff only for clean experiments.
- For disease-aware long-tail work, try mechanisms that add label priors orthogonal to source evidence:
  - disease-label compatibility priors
  - label prototype refinement
  - calibration-aware reranking instead of extra source backoff
