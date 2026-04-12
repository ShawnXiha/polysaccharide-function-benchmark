# Figure And Table Plan v1

## Figure 1. DoLPHiN KG Construction And Evaluation Pipeline

Purpose: communicate the paper mechanism before metrics. The figure should show raw DoLPHiN records, normalization into graph entities and edges, masked `poly-function` link prediction, clean retrieval, disease-aware upper bound, and ontology-enhanced tail-sensitive propagation.

Data source: conceptual schematic built from the implemented pipeline.

Expected caption focus: the graph contains structural, biological, and bibliographic evidence; evaluation masks one `poly-function` edge and ranks candidate functions under filtered evaluation.

## Figure 2. Main Benchmark Comparison

Purpose: show the clean-vs-disease-vs-ontology story in one decisive figure.

Panels:
- Panel A: function prediction macro-F1 and exact match for Meta-Path, Hetero GNN, and Hybrid GNN.
- Panel B: link prediction filtered MRR / Hits@3 / Hits@5 for the main disease-aware baseline and ontology best variant.
- Panel C: tail micro filtered Hits@3 comparing the same two variants.

Data source:
- `docs/experiment_comparison.md`
- `experiments/poly_function_link_prediction_with_disease_hierarchy_parent_child_tune_c025.json`
- `experiments/ontology_stability_runs/ontology_stability_summary.json`

## Figure 3. Ontology Stability Validation

Purpose: prove the ontology result is not a single-seed artifact.

Panels:
- Panel A: paired seed plot for tail micro filtered Hits@3, baseline vs ontology.
- Panel B: per-seed tail delta distribution.
- Panel C: summary annotation with one-sided McNemar and tail MRR permutation p-values.

Data source:
- `experiments/ontology_stability_runs/ontology_stability_summary.json`

## Table 1. KG Summary Statistics

Rows:
- nodes by type
- edges by type
- number of function labels
- publication coverage

Primary data source:
- `data/processed/neo4j/kg_stats.json`
- `docs/dolphin_kg_design.md`

## Table 2. Function Prediction And Link Prediction Results

Rows:
- clean Meta-Path
- clean Hetero GNN
- clean Hybrid Hetero GNN
- disease-aware Meta-Path
- disease-aware baseline retrieval
- ontology-enhanced retrieval

Purpose: keep the manuscript honest about what improves overall performance and what improves tail performance.

## Table 3. Ontology Stability And Significance

Rows:
- overall filtered MRR
- overall filtered Hits@3
- overall filtered Hits@5
- tail micro filtered Hits@3
- tail filtered MRR delta

Columns:
- baseline mean
- ontology mean
- delta
- confidence interval
- paired significance
- seed consistency
