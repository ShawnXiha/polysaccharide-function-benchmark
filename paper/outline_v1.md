# Paper Outline v1

## Working Title

Ontology-Aware Tail-Sensitive Function Retrieval on a DoLPHiN-Derived Polysaccharide Knowledge Graph

## Story

This paper starts from a practical gap in polysaccharide informatics. Existing polysaccharide resources contain rich but weakly structured evidence linking polymer composition, source organisms, biological functions, diseases, and publications, yet they are not organized as graph-native resources that support retrieval-style learning or ontology-aware reasoning. We convert DoLPHiN into a heterogeneous knowledge graph and ask a focused question: what kind of graph signal is already useful for function inference, and when does ontology support matter?

The first contribution is a graph construction pipeline that normalizes DoLPHiN into a reusable knowledge graph with explicit `polysaccharide`, `organism`, `monosaccharide`, `glycosidic_bond`, `function`, `disease`, and `publication` entities. The second contribution is an empirical benchmark showing that explicit meta-path retrieval is a stronger clean baseline than the current hetero GNN variants on this graph. The third contribution is an ontology-aware tail-sensitive retrieval mechanism based on confidence-gated parent/child propagation, which does not improve the overall upper-bound metric but provides a stable gain on tail labels.

## Core Claims

1. A DoLPHiN-derived KG provides usable supervision for function retrieval without requiring disease information.
2. On the current KG version, explicit relation-derived retrieval features outperform current hetero GNN baselines under clean evaluation.
3. Disease-aware signals act primarily as upper-bound side information rather than the main causal mechanism.
4. Ontology helps only after it is encoded as confidence-gated parent/child propagation, and its main benefit is stable tail-sensitive improvement.

## Proposed Figure Set

1. Figure 1: KG construction and task pipeline schematic.
2. Figure 2: Main benchmark comparison for clean, disease-aware, and ontology-enhanced settings.
3. Figure 3: Stability validation figure for ontology-enhanced tail retrieval across paired seeds.

## Proposed Table Set

1. Table 1: KG summary statistics.
2. Table 2: Function prediction and link prediction baseline comparison.
3. Table 3: Ontology stability and significance summary.

## Section Plan

### Abstract

State the resource gap, summarize KG construction, highlight the clean-vs-disease retrieval comparison, and report the ontology tail improvement with significance-aware validation.

### Introduction

Motivate polysaccharide structure-function discovery, discuss the lack of graph-native resources, frame the challenge of sparse and long-tailed function evidence, and position the paper around interpretable KG retrieval rather than end-to-end deep graph models.

### Methods

Describe graph construction, node and edge normalization, masked `poly-function` link prediction, filtered ranking, support-stratified evaluation, and the confidence-gated parent/child ontology propagation method.

### Experiments

Present KG statistics, function prediction baselines, clean and disease-aware link prediction baselines, long-tail iterations, the final ontology variant, and the paired stability/significance analysis.

### Discussion

Interpret why meta-path retrieval is strong on the current KG, why disease should be treated as side information, and why ontology provides targeted tail gains rather than broad global gains.

### Conclusion

Emphasize that the current value of the DoLPHiN KG lies in structured retrieval and interpretable graph signals, with ontology-enhanced tail retrieval as a stable supplementary gain.
