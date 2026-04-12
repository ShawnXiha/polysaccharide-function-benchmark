# GNN Failure Diagnosis

## Question

Why do the current hetero / hybrid GNN baselines underperform the explicit shallow feature baselines on the clean DoLPHiN KG split?

## Observation

The strongest shallow baseline under the unified `train/valid/test` protocol is `poly_x + meta_path + logreg`, with test macro-F1 `0.3603`. This is far above all neural variants:

- `hetero_sage`: mean test macro-F1 `0.0443` over seeds `42 / 7 / 123`
- `hetero_no_message`: mean test macro-F1 `0.0423`
- `poly_mlp`: test macro-F1 `0.0474`
- `hybrid hetero_sage`: test macro-F1 `0.0347`
- `hybrid no-message`: test macro-F1 `0.0386`
- `hybrid poly_mlp`: test macro-F1 `0.0440`

## Main Diagnosis

The dominant failure mode is not "the GNN was slightly under-tuned." The dominant failure mode is that message passing is not creating useful additional evidence under the current graph design.

Three patterns support this:

1. `hetero_sage` and `hetero_no_message` are nearly identical on the base graph.
2. `hybrid hetero_sage` does not outperform `hybrid no-message`; if anything, the no-message variant is slightly better.
3. Even a local `poly_mlp` on the same exported node features stays in the same low-performance band, meaning the exported node feature block itself is weak for direct supervised learning.

## Interpretation

The current KG appears to favor explicit incidence-style features and retrieval-like matching over learned message aggregation.

Likely reasons:

- the graph is sparse and relation-specific support is narrow
- non-polysaccharide node features are weak or absent
- message passing mixes low-information neighbors without adding enough disambiguating context
- explicit feature counts preserve high-signal local structure that linear models can exploit directly

## What This Means For The Paper

The paper should not frame this as "GNNs do not work for polysaccharide KGs" in general. The supported claim is narrower and stronger:

> On the current DoLPHiN KG v0, explicit shallow feature models and interpretable retrieval baselines outperform the present hetero / hybrid GNN formulations; message passing contributes little beyond local node features.

## Practical Next Step

If future work revisits GNNs, the priority should be changing the graph evidence and node semantics first, not stacking deeper message-passing layers:

- richer non-polysaccharide node features
- motif-level or subgraph-level encoders
- edge typing with stronger biological semantics
- retrieval-guided or feature-guided graph models rather than plain hetero GraphSAGE
