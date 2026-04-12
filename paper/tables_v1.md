# Table 1. Knowledge Graph Summary

| Entity or relation type | Count |
| --- | ---: |
| Polysaccharide nodes | 5,078 |
| Organism nodes | 1,487 |
| Monosaccharide nodes | 23 |
| Glycosidic bond nodes | 323 |
| Function nodes | 66 |
| Disease nodes | 14 |
| Publication nodes | 2,386 |
| Polysaccharide-organism edges | 5,075 |
| Polysaccharide-monosaccharide edges | 17,448 |
| Polysaccharide-bond edges | 2,313 |
| Polysaccharide-function edges | 7,408 |
| Polysaccharide-disease edges | 3,633 |
| Polysaccharide-publication edges | 5,071 |

# Table 2. Main Predictive Results On The Unified Split

| Task | Model | Setting | Protocol | Metric 1 | Metric 2 | Metric 3 |
| --- | --- | --- | --- | ---: | ---: | --- |
| Function prediction | Meta-path + LogReg | Clean | Unified split | Macro-F1 0.3465 | Exact match 0.5118 | - |
| Function prediction | Poly-X + Meta-path + LogReg | Clean | Unified split | Macro-F1 0.3603 | Exact match 0.5364 | strongest clean baseline |
| Function prediction | Meta-path + MLP | Clean | Unified split | Macro-F1 0.3065 | Exact match 0.5295 | neural shallow baseline |
| Function prediction | Hetero GNN | Clean | Unified split | Macro-F1 0.0443 | Exact match 0.0256 | - |
| Function prediction | Hybrid Hetero GNN | Clean | Unified split | Macro-F1 0.0347 | Exact match 0.0364 | - |
| Link prediction | Disease-aware baseline | Main upper bound | Tuned split | Filtered MRR 0.8491 | Hits@3 0.912 | Hits@5 0.938 |
| Link prediction | Ontology best variant | Tail-sensitive | Tuned split | Filtered MRR 0.8490 | Hits@3 0.912 | Hits@5 0.939 |

# Table 3. GNN Failure Ablation

| Input graph | Model | Protocol | Metric 1 | Metric 2 | Note |
| --- | --- | --- | ---: | ---: | --- |
| Base | Hetero GNN | Seed 42 | Macro-F1 0.0443 | Exact match 0.0256 | full message passing |
| Base | No-message ablation | Mean over 3 seeds | Macro-F1 0.0423 | Exact match 0.0276 | within ~0.002 of full GNN |
| Base | Poly-MLP | Seed 42 | Macro-F1 0.0474 | Exact match 0.0187 | node-local neural baseline |
| Hybrid | Hetero GNN | Seed 42 | Macro-F1 0.0347 | Exact match 0.0364 | full message passing |
| Hybrid | No-message ablation | Seed 42 | Macro-F1 0.0386 | Exact match 0.1132 | no gain from propagation |
| Hybrid | Poly-MLP | Seed 42 | Macro-F1 0.0440 | Exact match 0.0089 | node-local neural baseline |

# Table 4. Ontology Stability And Significance

| Metric | Baseline mean | Ontology mean | Mean delta | Statistical test | Result |
| --- | ---: | ---: | ---: | --- | --- |
| Filtered MRR | 0.8430 | 0.8427 | -0.0003 | Paired permutation | p = 0.0015 |
| Filtered Hits@3 | 0.9088 | 0.9085 | -0.0003 | Paired McNemar, two-sided | p = 0.3018 |
| Filtered Hits@5 | 0.9366 | 0.9366 | 0.0000 | Paired permutation | p = 1.0000 |
| Tail micro filtered Hits@3 | 0.0552 | 0.1021 | 0.0469 | Paired McNemar, one-sided | p = 0.03125 |
| Tail filtered MRR delta | - | - | 0.0395 | Paired permutation | p = 0.0002499 |
