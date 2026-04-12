# polysaccharidesgraph

DoLPHiN-derived polysaccharide knowledge graph, benchmark experiments, and manuscript/submission assets.

This repository turns semi-structured DoLPHiN polysaccharide records into a typed knowledge graph and uses it for interpretable function retrieval, clean diagnostic baselines, disease-aware upper-bound retrieval, and ontology-enhanced tail analysis.

## Repository Layout

- `src/polysaccharidesgraph/kg/`: KG construction, validation, normalization, and PyG export.
- `src/polysaccharidesgraph/models/`: clean baselines, GNN baselines, final retrieval wrappers, and experiment backend.
- `configs/`: KG schema and task-specific function hierarchies.
- `data/processed/`: generated KG CSV and PyG payloads.
- `experiments/`: experiment outputs, pipeline trackers, and stability runs.
- `paper/`: manuscript, figures, supplement, reviews, improvement plans, and Chinese presentation slides.
- `submission_packages/`: BMC Bioinformatics and Database submission-ready package drafts.
- `tests/`: lightweight smoke tests for normalization, ranking helpers, and feature-boundary checks.

## Environment

`nv` is a PowerShell alias on this machine, so use `uv` for environment management:

```powershell
$env:UV_CACHE_DIR='D:\projects\paper_writing\polysaccharidesgraph\uv_cache'
uv venv .venv39 --python 3.9 --system-site-packages
```

Install or synchronize dependencies:

```powershell
$env:UV_CACHE_DIR='D:\projects\paper_writing\polysaccharidesgraph\uv_cache'
uv pip install --python .\.venv39\Scripts\python.exe -e ".[dev]"
```

Current runtime dependencies are declared in `pyproject.toml`. The PyG stack is required for `export_pyg.py` and GNN baselines; shallow feature utilities and normalization tests do not require GPU hardware.

Known local environment note: on this machine `.venv39` inherits an Anaconda `_ssl` DLL problem that can break `torch_geometric` import paths touching `ssl`. The project code itself does not require network access during export; this is a local environment issue to fix before a clean public release.

## KG Build And Export

Build KG v0 CSV exports from the neighboring `polysaccharidesdb` repository:

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesgraph\src'
.venv39\Scripts\python -m polysaccharidesgraph.kg.build_graph
```

Outputs land under `data/processed/neo4j/`.

Validate the export:

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesgraph\src'
.venv39\Scripts\python -m polysaccharidesgraph.kg.validate_graph
```

Neo4j-friendly bulk import CSV files are written under `data/processed/neo4j/bulk_import/`.

Export PyG training input:

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesgraph\src'
.venv39\Scripts\python -m polysaccharidesgraph.kg.export_pyg
```

The default export is the leakage-controlled clean graph. Its feature schema is written next to the payload as:

```text
data/processed/pyg/dolphin_kg_v0.feature_schema.json
```

To export the disease-aware graph and include the disease-derived feature `degree__disease`, use:

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesgraph\src'
.venv39\Scripts\python -m polysaccharidesgraph.kg.export_pyg --include-disease-edges --output data\processed\pyg\dolphin_kg_v0_with_disease.pt
```

Run baselines:

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesgraph\src'
.venv39\Scripts\python -m polysaccharidesgraph.models.meta_path_baseline
.venv39\Scripts\python -m polysaccharidesgraph.models.run_hetero_gnn_baseline
.venv39\Scripts\python -m polysaccharidesgraph.models.run_hybrid_hetero_gnn_baseline
.venv39\Scripts\python -m polysaccharidesgraph.models.run_poly_function_link_prediction
.\.venv39\Scripts\python.exe scripts\summarize_experiments.py
```

Run final paper-facing retrieval methods:

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesgraph\src'
.venv39\Scripts\python -m polysaccharidesgraph.models.run_final_retrieval --method disease_aware_freq_prior --seed 42
.venv39\Scripts\python -m polysaccharidesgraph.models.run_final_retrieval --method ontology_parent_child_best --seed 42
```

The broad `run_poly_function_link_prediction.py` script remains available as the experiment-workbench backend. For the manuscript-facing methods, prefer `run_final_retrieval.py`; see `docs/code_structure_review.md`.

## Paper And Submission Assets

Main files:

- `paper/manuscript_v1.tex`
- `paper/manuscript_v1.pdf`
- `paper/supplementary_v1.tex`
- `paper/supplementary_v1.pdf`

Venue packages:

- `submission_packages/bmc_bioinformatics/`
- `submission_packages/database/`

Chinese general-audience presentation:

- `paper/slides/polysaccharide_kg_general_audience_cn.pptx`
- `paper/slides/polysaccharide_kg_general_audience_cn_talk_script.md`

## Smoke Tests

Run the lightweight tests before regenerating manuscript results:

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesgraph\src'
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest tests
```

These tests cover normalization helpers, ranking utilities, and the disease-free clean feature schema boundary.

## Current Submission-Readiness Notes

- The clean `poly_x` leakage issue has been fixed. Default clean PyG export now has `num_disease_derived_poly_features = 0`.
- The strongest leakage-controlled clean baseline is `meta_path + logreg` with macro-F1 `0.3465`.
- The final public retrieval wrapper is `polysaccharidesgraph.models.run_final_retrieval`.
- Remaining manual items before journal upload: author metadata, public repository URL, Database URL, ORCID, funding, and final declarations.
