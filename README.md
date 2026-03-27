# polysaccharidesdb

Polysaccharide structure-function benchmark, traceable experiment pipeline, and journal submission workspace.

## What This Repository Contains

This repository now has three parallel responsibilities:

1. raw-data ingestion and benchmark construction
2. staged experiment execution and revision tracking
3. paper drafting and journal-specific submission packaging

The code and experiment pipeline live under `src/` and `experiments/`. The paper and submission artifacts live at the repository root and under `submission_packages/`.

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
