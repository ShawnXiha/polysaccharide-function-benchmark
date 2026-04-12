# Figure Captions v1

## Figure 1

**DoLPHiN KG construction and evaluation pipeline.** Raw DoLPHiN records are normalized into typed entities and relations spanning polysaccharides, organisms, monosaccharides, glycosidic bonds, functions, diseases, and publications. The resulting graph supports masked `poly-function` link prediction under filtered ranking. The paper studies three settings on top of the same graph substrate: clean meta-path retrieval, disease-aware upper-bound retrieval, and ontology-enhanced tail-sensitive retrieval.

## Figure 2

**Clean benchmarks, upper-bound retrieval, and GNN failure ablations.** Panel A compares clean function-prediction baselines under the unified split, showing that the strongest model is a shallow linear classifier on explicit graph features rather than a neural message-passing model. Panel B compares the tuned disease-aware retrieval baseline against the ontology-enhanced variant on filtered MRR, Hits@3, and Hits@5. Panel C summarizes the GNN failure ablation, showing that no-message variants remain close to the full hetero models.

## Figure 3

**Stability validation for ontology-enhanced tail retrieval.** Panel A shows paired seed-wise tail micro filtered Hits@3 for the disease-aware baseline and the ontology-enhanced variant. Panel B shows the per-seed ontology-minus-baseline delta. Panel C summarizes the paired statistical tests, indicating that ontology-enhanced propagation yields a stable tail-sensitive gain with no observed tail regression across seeds.

# Table Captions v1

## Table 1

**Summary statistics of the DoLPHiN-derived knowledge graph.** The graph contains typed structural, biological, functional, disease, and publication evidence derived from normalized DoLPHiN records.

## Table 2

**Main predictive results on the representative unified split.** Clean rows assess structure-only graph signal under a common train/valid/test protocol. Disease-aware retrieval is treated as an upper-bound semantic setting. The ontology row should be interpreted as a tail-sensitive supplement rather than as a new overall best model.

## Table 3

**GNN failure ablation under the clean unified split.** Base rows use the original exported graph, while hybrid rows append sparse meta-path features to the polysaccharide input. Message-passing variants remain close to no-message controls, indicating that the current bottleneck is graph representation rather than a missing training trick.

## Table 4

**Paired stability and significance analysis for the ontology-enhanced variant.** Reported values summarize `16` paired seeds and `16,000` masked edges. The ontology variant remains practically unchanged in aggregate ranking while providing a statistically supported tail-sensitive gain.
