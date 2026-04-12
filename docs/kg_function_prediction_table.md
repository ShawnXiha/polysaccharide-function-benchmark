# KG Function Prediction Table Draft

## Main Table

| Model | Setting | Labels | Valid Macro-F1 | Test Macro-F1 | Test Exact Match |
| --- | --- | ---: | ---: | ---: | ---: |
| Meta-Path | Clean | 66 | - | 0.3046 | 0.4144 |
| Hetero GNN | Clean | 66 | 0.0739 | 0.0443 | 0.0256 |
| Hybrid Hetero GNN | Clean | 66 | 0.0631 | 0.0347 | 0.0364 |
| Meta-Path | With Disease Features | 66 | - | 0.4560 | 0.6781 |
| Hetero GNN | With Disease Edges | 66 | 0.1184 | 0.0613 | 0.1831 |
| Hybrid Hetero GNN | Disease Edges + Disease Features | 66 | 0.3304 | 0.2250 | 0.4951 |

## Caption Draft

Comparison of knowledge-graph-based function prediction baselines on the DoLPHiN-derived polysaccharide benchmark. Clean settings exclude disease edges and disease-derived meta-path features to better isolate structure- and source-driven signals. Disease-enhanced settings are reported as auxiliary upper-bound results because disease information is strongly coupled to function labels. Under the clean setting, the meta-path baseline is the strongest model, indicating that explicit relation-derived features are currently more effective than end-to-end heterogeneous message passing on the KG v0 graph.

## Notes

- `Clean` = no disease edges and no disease meta-path features.
- `With Disease Features` and `With Disease Edges` should be treated as side-information experiments.
- The clean meta-path baseline is the most defensible primary result.
