# Experiment-Craft Diagnosis: Label-Specific Subgraph Motifs

## 1. Problem Definition

The previous cycle showed that flat structural signatures are too weak even when moved into candidate generation. This cycle tested a more selective evidence source: pairwise subgraph motifs built from local structure blocks.

## 2. What Was Tried

### Attempt 1: Conservative Motif Candidate Generation

- motif feature limit `20`
- min local rate `0.2`
- base window `20`
- candidate limit `5`
- activation `0.75`

### Attempt 2: Stronger Motif Candidate Generation

- motif feature limit `30`
- min local rate `0.1`
- base window `30`
- candidate limit `10`
- activation `3.0`

## 3. Evidence

- Clean baseline filtered `Hits@3`: `0.724`
- Clean subgraph-motif v1/v2 filtered `Hits@3`: `0.724 / 0.715`
- Disease-aware upper-bound baseline filtered `Hits@3`: `0.912`
- Disease-aware subgraph-motif v1/v2 filtered `Hits@3`: `0.911 / 0.897`
- Disease-aware tail micro filtered `Hits@3`: unchanged at `0.1667`
- Disease-aware mid micro filtered `Hits@3`: `0.450 -> 0.450 -> 0.275`

## 4. Diagnosis

This cycle improves the formulation slightly in principle: pairwise motifs are more selective than flat overlap. But the experimental outcome still follows the same pattern:

- conservative activation: almost no change
- stronger activation: shortlist distortion before any tail gain

That means the dominant issue is no longer about whether the evidence is flat or pairwise. The issue is that the current graph blocks do not contain enough rare-label-discriminative structure for these motif families to recover the tail.

## 5. Next Action

- Stop iterating on local structural-overlap motif variants.
- If tail work continues, switch to a genuinely different source:
  - taxonomy-conditioned motif rarity
  - publication/provenance-guided rare-label support
  - external graph augmentation or ontology support for rare functions
