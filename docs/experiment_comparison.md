# Experiment Comparison

| Model | Setting | Labels | Valid Macro-F1 | Test Macro-F1 | Test Exact Match |
| --- | --- | ---: | ---: | ---: | ---: |
| Meta-Path | Clean | 66 | - | 0.3046 | 0.4144 |
| Meta-Path | With Disease | 66 | - | 0.4560 | 0.6781 |
| Hetero GNN | Clean | 66 | 0.0739 | 0.0443 | 0.0256 |
| Hetero GNN | With Disease Edges | 66 | 0.1184 | 0.0613 | 0.1831 |
| Hybrid Hetero GNN | Clean | 66 | 0.0631 | 0.0347 | 0.0364 |
| Hybrid Hetero GNN | Meta-Path + Disease Features | 66 | 0.1148 | 0.0775 | 0.2864 |
| Hybrid Hetero GNN | Disease Edges + Disease Features | 66 | 0.3304 | 0.2250 | 0.4951 |

## Readout

- `Clean` means no disease edges and no disease meta-path features.
- `With Disease` variants are stronger but less clean for causal interpretation because disease information is tightly coupled to labels.
- Current strongest clean baseline is `Meta-Path`.
- Current strongest overall baseline is `Meta-Path` with disease features.
- Current strongest graph-neural setting is `Hybrid Hetero GNN` with disease edges and disease features.
