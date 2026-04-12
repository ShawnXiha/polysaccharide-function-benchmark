# Experiment-Craft Diagnosis: Taxonomy-Conditioned Motifs

## 1. Problem Definition

The previous cycles showed that structural motifs from current graph blocks are noisy and not tail-discriminative enough. This cycle tested whether taxonomy conditioning could suppress irrelevant support and reveal a hidden useful signal.

## 2. What Was Tried

### Attempt 1: Conservative Taxonomy-Conditioned Motifs

- feature limit `20`
- min local rate `0.2`
- base window `20`
- candidate limit `5`
- activation `1.0`

### Attempt 2: Stronger Taxonomy-Conditioned Motifs

- feature limit `30`
- min local rate `0.1`
- base window `30`
- candidate limit `10`
- activation `3.0`

## 3. Evidence

- Clean baseline filtered `Hits@3`: `0.724`
- Clean taxonomy-motif v1/v2 filtered `Hits@3`: `0.724 / 0.724`
- Disease-aware upper-bound baseline filtered `Hits@3`: `0.912`
- Disease-aware taxonomy-motif v1/v2 filtered `Hits@3`: `0.912 / 0.912`
- Disease-aware tail micro filtered `Hits@3`: unchanged at `0.1667`

## 4. Diagnosis

This cycle differs from the last two in one useful way: taxonomy conditioning does remove enough noise that the method no longer degrades overall retrieval. But the remaining signal is so weak that the method becomes effectively inert.

That makes the interpretation sharper. The problem is no longer “motifs are too noisy.” The problem is “even after denoising, the current motif family still does not encode enough tail-specific evidence.” Taxonomy conditioning therefore acts as a diagnostic lens, not as a new solution.

## 5. Next Action

- Mark taxonomy-conditioned motifs as a stable no-op.
- Move to a genuinely different evidence source:
  - publication/provenance-guided rare-label support
  - external ontology or hierarchy support for rare functions
  - disease-independent metadata channels not already encoded in local structure
