# polysaccharidesdb

Polysaccharide structure-function benchmark, traceable experiment pipeline, and journal submission workspace.

Repository URL:

- `https://github.com/ShawnXiha/polysaccharide-function-benchmark`

## What This Repository Contains

This repository now has three parallel responsibilities:

1. raw-data ingestion and benchmark construction
2. staged experiment execution and revision tracking
3. paper drafting and journal-specific submission packaging

The code and experiment pipeline live under `src/` and `experiments/`. The paper and submission artifacts live at the repository root and under `submission_packages/`.

## Installation

Create an environment with Python 3.10 or newer, then install the package in editable mode.

For ETL-only work:

```powershell
python -m pip install -e .
```

For the main sparse baselines, bootstrap analysis, and figure generation:

```powershell
python -m pip install -e ".[ml,figures]"
```

For graph or lightweight neural baselines:

```powershell
python -m pip install -e ".[ml,graph]"
```

For development checks:

```powershell
python -m pip install -e ".[ml,figures,dev]"
```

The `graph` extra installs PyTorch and PyTorch Geometric. If those packages need a platform-specific wheel source on your machine, install them according to the official PyTorch/PyG instructions first, then rerun the editable install.

If editable installation is not available in the local environment, run commands from the repository root with:

```powershell
$env:PYTHONPATH = "src"
```

## Directory Guide

- `configs/`: data manifests and experiment configuration files
- `data_raw/`: raw source exports and source templates
- `data_interim/`: validation reports and intermediate ETL artifacts
- `data_processed/`: benchmark datasets and split files
- `docs/`: schema notes, protocol notes, and repository guidance
- `experiments/`: stage-wise experiment logs, summaries, and revision outputs
- `figures/`: manuscript figures in PDF/PNG form
- `scripts/`: utility scripts such as figure generation
- `src/polysaccharidesdb/`: ETL, modeling, and analysis code
- `submission_packages/`: venue-specific submission bundles

## Paper and Submission Entry Points

- master draft:
  - `paper_poly_core_v1.tex`
  - `paper_poly_core_v1.pdf`
- root bibliography:
  - `references_poly_core_v1.bib`
- review notes:
  - `paper_review_selfcheck_round4.md`
- venue packages:
  - `submission_packages/journal_of_cheminformatics/`
  - `submission_packages/bmc_bioinformatics/`
- general-audience Chinese presentation:
  - `presentations/polysaccharide_function_benchmark_general_audience_zh.pptx`
  - `presentations/polysaccharide_function_benchmark_general_audience_zh_script.md`

## Recommended Reading Order

If the goal is to understand the repository quickly, use this order:

1. `docs/repository_file_guide.md`
2. `docs/paper_and_submission_map.md`
3. `paper_review_selfcheck_round4.md`
4. the relevant venue folder under `submission_packages/`

## Data and Experiment Entry Points

For real exported source files and benchmark construction:

- `data_raw/README_real_data.md`
- `configs/data/source_manifest_v0.yaml`
- `docs/real_data_ingestion.md`
- `docs/publishable_evaluation_protocol_v1.md`
- `docs/split_protocol.md`

For staged experimentation:

- `experiments/pipeline_tracker.md`
- `experiments/stage1_baseline/trajectory.md`
- `experiments/stage2_tuning/trajectory.md`
- `experiments/stage3_method/trajectory.md`
- `experiments/stage4_ablation/trajectory.md`

For presentation materials:

- `presentations/polysaccharide_function_benchmark_general_audience_zh.pptx`
- `presentations/polysaccharide_function_benchmark_general_audience_zh_script.md`
- `scripts/generate_general_audience_deck.py`

## Quick Reproduction Path

The repository does not commit raw or processed data artifacts by default. The tracked `data_raw/`, `data_interim/`, and `data_processed/` directories contain `.gitkeep` placeholders; datasets are regenerated from the public-source ingestion pipeline or provided local exports.

### 1. Fetch public DoLPHiN records

```powershell
python -m polysaccharidesdb.etl.fetch_dolphin --sleep-seconds 0.15 --timeout 30
```

Expected generated files:

- `data_raw/dolphin_export.csv`
- `data_interim/dolphin_raw_records.jsonl`
- `data_interim/dolphin_fetch_state.json`

### 2. Build the real and publishable benchmark datasets

```powershell
python -m polysaccharidesdb.etl.build_real_dataset `
  --manifest configs/data/source_manifest_dolphin_only.yaml

python -m polysaccharidesdb.etl.build_publishable_dataset `
  --input data_processed/dataset_dolphin_only.jsonl `
  --output-dataset data_processed/dataset_publishable_supervised_v1.jsonl `
  --output-report data_interim/dataset_publishable_supervised_v1_report.json
```

### 3. Build random and DOI-grouped splits

```powershell
python -m polysaccharidesdb.etl.build_splits `
  --input data_processed/dataset_publishable_supervised_v1.jsonl `
  --output-dir data_processed/splits_publishable_supervised_v2 `
  --seed 42
```

Expected split files:

- `data_processed/splits_publishable_supervised_v2/random_split.json`
- `data_processed/splits_publishable_supervised_v2/doi_grouped_split.json`

### 4. Run validation-phase checks

Development and tuning commands default to the validation split. This prevents accidental test-driven method selection.

Tuned sparse logistic anchor on validation:

```powershell
python -m polysaccharidesdb.models.run_logistic_baseline `
  --dataset data_processed/dataset_publishable_supervised_v1.jsonl `
  --split data_processed/splits_publishable_supervised_v2/random_split.json `
  --seed 11 `
  --c 16 `
  --class-weight balanced `
  --output experiments/reproduction/tuned_logistic_random_valid.json
```

Final `poly-core v1` configuration on validation:

```powershell
python -m polysaccharidesdb.models.run_evidence_aware_logistic `
  --dataset data_processed/dataset_publishable_supervised_v1.jsonl `
  --split data_processed/splits_publishable_supervised_v2/random_split.json `
  --seed 11 `
  --c 16 `
  --class-weight balanced `
  --disable-evidence-features `
  --disable-sample-weight `
  --disable-modification-feature `
  --disable-source-kingdom-feature `
  --disable-composition-feature `
  --output experiments/reproduction/poly_core_random_valid.json
```

### 5. Run the frozen final-test suite

Only run this step after the configuration is frozen.

```powershell
python -m polysaccharidesdb.models.run_final_test_suite `
  --dataset data_processed/dataset_publishable_supervised_v1.jsonl `
  --split data_processed/splits_publishable_supervised_v2/random_split.json `
  --output-dir experiments/reproduction/final_test_random `
  --seed 11
```

Expected final-test outputs:

- `experiments/reproduction/final_test_random/tuned_logistic_test.json`
- `experiments/reproduction/final_test_random/poly_core_v1_test.json`
- `experiments/reproduction/final_test_random/final_test_manifest.json`

### 6. Reproduce the paired bootstrap comparison

```powershell
python -m polysaccharidesdb.analysis.bootstrap_compare `
  --result-a experiments/reproduction/final_test_random/tuned_logistic_test.json `
  --result-b experiments/reproduction/final_test_random/poly_core_v1_test.json `
  --split-name default `
  --metric macro_f1 `
  --num-bootstrap 2000 `
  --seed 42 `
  --output experiments/reproduction/bootstrap_random_test_macro_f1.json
```

### 7. Regenerate manuscript figures

```powershell
python scripts/generate_paper_figures.py
```

Expected generated figure files:

- `figures/figure1_pipeline.pdf`
- `figures/figure2_main_results.pdf`
- `figures/figure3_ablation.pdf`

## Reproducibility Caveats

- The public DoLPHiN website can change over time, so regenerated crawls may not be byte-identical to the manuscript snapshot.
- The current supervised benchmark treats missing labels as unreported rather than confirmed negative; the paper therefore frames metrics as comparative benchmark metrics, not absolute biological truth.
- The graph and transformer baselines are retained as broad baseline-family references. The main manuscript claim is anchored on tuned sparse logistic regression and the `poly-core v1` feature audit.
