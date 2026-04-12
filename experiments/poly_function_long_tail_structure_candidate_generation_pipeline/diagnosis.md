# Experiment-Craft Diagnosis: Structure-Aware Candidate Generation

## 1. Problem Definition

The previous cycle showed that structural signatures fail as a post-hoc rerank bonus. This cycle tested the more targeted hypothesis that the same structural signal might still help if it enters earlier, at candidate generation time.

## 2. What Was Tried

### Attempt 1: Conservative Structure Candidate Generation

- base window `20`
- candidate limit `5`
- activation `0.5`

### Attempt 2: Stronger Structure Candidate Generation

- base window `30`
- candidate limit `10`
- activation `3.0`

## 3. Evidence

- Clean baseline filtered `Hits@3`: `0.724`
- Clean structure-candidate v1/v2 filtered `Hits@3`: `0.724 / 0.715`
- Disease-aware upper-bound baseline filtered `Hits@3`: `0.912`
- Disease-aware structure-candidate v1/v2 filtered `Hits@3`: `0.911 / 0.892`
- Disease-aware tail micro filtered `Hits@3`: unchanged at `0.1667`
- Disease-aware mid micro filtered `Hits@3`: `0.450 -> 0.450 -> 0.275`
- Disease-aware head micro filtered `Hits@3`: `0.9361 -> 0.9350 -> 0.9224`

## 4. Diagnosis

This cycle rules out a simple pipeline-location explanation. The structural signal was moved earlier, and the result still followed the same two-regime pattern:

- weak activation: no practical change
- strong activation: worse overall ranking, unchanged tail

So the dominant bottleneck is not merely that the signal arrived too late. The bottleneck is that the current structural signatures are not selective enough to propose genuinely useful rare-label candidates. When activated strongly, they still prefer structurally plausible but label-misaligned functions, which harms mid/head retrieval before any tail gain appears.

## 5. Next Action

- Mark this candidate-generation formulation as failed.
- If structural long-tail work continues, change the evidence source itself:
  - motif rarity conditioned on source taxonomy
  - label-specific subgraph motifs instead of flat feature overlap
  - external structural evidence beyond the current meta-path feature blocks
