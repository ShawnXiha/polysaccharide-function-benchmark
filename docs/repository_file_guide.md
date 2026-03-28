# Repository File Guide

## Purpose

This document explains which files matter, which files are historical scaffolding, and which files are intended as final paper-facing artifacts.

## Top-Level Draft Files

- `paper_poly_core_v1.tex`
  - master scientific draft
  - keeps the full benchmark story in one place
  - should be treated as the source manuscript, not the final venue-formatted submission file
- `paper_poly_core_v1.pdf`
  - compiled output of the master draft
- `references_poly_core_v1.bib`
  - shared bibliography source for the manuscript and venue packages

## Review and Planning Files

- `paper_review_selfcheck.md`
  - early self-review notes
- `paper_review_selfcheck_round3.md`
  - intermediate review notes
- `paper_review_selfcheck_round4.md`
  - latest pre-submission self-review; use this as the current review reference
- `多糖论文结果整理与主表.md`
  - working summary of numerical results and table logic
- `论文图表与caption草案.md`
  - working figure and caption notes

## Submission Packages

Use `submission_packages/` when the task is journal submission rather than scientific drafting.

- `submission_packages/journal_of_cheminformatics/`
  - Journal of Cheminformatics `Methodology` package
- `submission_packages/bmc_bioinformatics/`
  - BMC Bioinformatics `Research article` package

Each venue folder contains:

- one journal-specific main manuscript `.tex/.pdf`
- one supplementary-information `.tex/.pdf`
- one venue README
- one checklist
- one cover-letter template
- one title-page template
- one declarations template
- one submission manifest
- one conversion-note file

Current submission metadata status:

- repository remote:
  - `git@github.com:ShawnXiha/polysaccharide-function-benchmark.git`
- public repository URL used in submission documents:
  - `https://github.com/ShawnXiha/polysaccharide-function-benchmark`
- current filled author metadata:
  - `Qiang Xia`
  - `Zhejiang Tea Group`
- still pending:
  - corresponding-author designation
  - contact email

## Data and Experiment Files

- `data_raw/`
  - original source exports and manually curated source templates
- `data_interim/`
  - ETL validation reports and summary outputs
- `data_processed/`
  - benchmark-ready datasets and split files
- `experiments/`
  - all stage-wise experiment outputs, including revision-specific robustness analyses

## Important Notes

1. The repository contains both exploratory and finalized artifacts.
2. If the task is paper writing, start from the master draft or a venue package.
3. If the task is reproducing numbers, follow the split and artifact pointers recorded in the supplementary notes and `experiments/`.
