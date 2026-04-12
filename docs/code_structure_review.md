# Code Structure Review and Final Method Entry Points

## Current State

The project currently contains two kinds of code:

- paper-facing utilities that should remain stable for reviewers
- exploratory experiment code accumulated during long-tail method search

The largest maintainability issue is `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`. It contains many scorers from successful and failed experiment cycles, and its `main()` function is intentionally broad because it was used as an experiment workbench.

## Submission-Facing Entry Points

Use these entry points for paper reproduction:

- KG build: `python -m polysaccharidesgraph.kg.build_graph`
- KG validation: `python -m polysaccharidesgraph.kg.validate_graph`
- clean PyG export: `python -m polysaccharidesgraph.kg.export_pyg`
- disease-aware PyG export: `python -m polysaccharidesgraph.kg.export_pyg --include-disease-edges --output data/processed/pyg/dolphin_kg_v0_with_disease.pt`
- shallow clean baselines: `python -m polysaccharidesgraph.models.run_shallow_feature_baselines`
- final disease-aware baseline / ontology retrieval: `python -m polysaccharidesgraph.models.run_final_retrieval`

## Final Retrieval Methods

The final retrieval configurations are isolated in:

- `src/polysaccharidesgraph/models/final_methods.py`

The stable wrapper is:

- `src/polysaccharidesgraph/models/run_final_retrieval.py`

Supported methods:

- `disease_aware_freq_prior`
- `ontology_parent_child_best`

Example:

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesgraph\src'
.\.venv39\Scripts\python.exe -m polysaccharidesgraph.models.run_final_retrieval --method ontology_parent_child_best --seed 42
```

## Remaining P2 Refactor

The final wrapper reduces reviewer friction but does not fully refactor the exploratory runner. A later cleanup should split the long runner into:

- `data.py`
- `ranking.py`
- `scorers/base_knn.py`
- `scorers/disease.py`
- `scorers/ontology.py`
- `cli/run_link_prediction.py`

Until that refactor is complete, `run_poly_function_link_prediction.py` should be treated as an experiment archive plus backend implementation, not as the primary public interface.

