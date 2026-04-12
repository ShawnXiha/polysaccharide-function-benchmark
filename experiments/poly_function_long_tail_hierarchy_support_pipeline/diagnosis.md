# Experiment-Craft Diagnosis: External Ontology / Hierarchy Support

## 1. Problem Definition

After exhausting structure-only motif families, this cycle tested whether an external coarse function hierarchy could supply a genuinely new long-tail evidence channel for masked `poly-function` recovery.

## 2. What Was Tried

### Attempt 1: Conservative Hierarchy Support

- external family map from `configs/function_hierarchy_v1.json`
- base window `20`
- threshold `10`
- candidate limit `5`
- activation `0.75`

### Attempt 2: Stronger Hierarchy Support

- same external family map
- base window `30`
- threshold `10`
- candidate limit `10`
- activation `3.0`

Both attempts were tested in:

- clean retrieval
- disease-aware upper-bound retrieval with disease-conditioned base vote and frequency-adjusted disease prior

## 3. Evidence

- clean baseline filtered `Hits@3`: `0.724`
- clean hierarchy support filtered `Hits@3`: `0.724 / 0.713`
- disease-aware upper-bound baseline filtered `Hits@3`: `0.912`
- disease-aware hierarchy support filtered `Hits@3`: `0.911 / 0.889`
- disease-aware tail micro filtered `Hits@3`: `0.1667 -> 0.1667 -> 0.000`
- disease-aware mid micro filtered `Hits@3`: `0.450 -> 0.450 -> 0.275`
- disease-aware head micro filtered `Hits@3`: `0.9361 -> 0.9350 -> 0.9203`

## 4. Diagnosis

This is not another pipeline-placement failure. The new ingredient here was a genuinely different evidence source: a manually curated external hierarchy over function labels.

The result shows that this hierarchy is too coarse to add useful discrimination. In weak form it behaves like harmless smoothing, leaving the shortlist effectively unchanged. In stronger form it suppresses distinctions between siblings inside the same family and therefore degrades ranking quality.

So the failure is fundamental for the current formulation:

- the hierarchy does not carry enough label-specific resolution
- family-level support is weaker than the current neighbor evidence
- stronger activation turns hierarchy into over-smoothing rather than new support

This means "external ontology/hierarchy support" is not disproven in general. What failed is this specific coarse family-map formulation for this retrieval task.

## 5. Next Action

- Mark the current hierarchy-support method as failed for long-tail recovery.
- Do not spend more tuning budget on the same family map.
- If ontology/hierarchy work continues, switch to a richer evidence form:
  - finer-grained external ontology relations
  - hierarchical edges injected into the base graph rather than post-hoc family smoothing
  - hierarchy-aware scoring that preserves sibling competition within a family
