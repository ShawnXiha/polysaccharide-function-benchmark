# Evolution Report: Cycle 027 - ESE

**Date**: 2026-03-29
**Trigger**: Biology-facing case-study local subgraph figure finalized for the manuscript
**Source Artifacts**:
- `scripts/make_case_study_figure.py`
- `paper/figures/figure4_case_subgraphs.png`
- `paper/figures/figure4_case_subgraphs.pdf`
- `experiments/case_study_pipeline/pipeline_tracker.md`

## Success Classification

- **Type**: Reusable strategy extraction
- **Direction**: manuscript figure construction for evidence-grounded case studies

## Reasoning

The main lesson from this cycle is that manuscript-facing case-study figures should be assembled from category-aware evaluation records rather than from a single raw row keyed only by sample ID. In this project, the persistent-failure case appeared in both `clean_failure` and `ontology_failure` categories, and the first plotting pass silently dropped some ranks because the script overwrote one record with another. The fix was simple but important: use `(category, poly_id)` as the retrieval key and explicitly merge the fields needed for the final panel.

The second lesson is visual rather than algorithmic. For biology-facing cases, a local subgraph figure is more useful than a ranking-only chart because it keeps the actual evidence channels visible: source organism, monosaccharides, bond signatures, disease cue, ontology path, and DOI provenance can all be shown in one compact panel. This makes the paper's claim easier to trust because the reader can inspect the evidence chain instead of only reading a metric delta.

## Changes Made

### Added

- `Merge Category-Specific Evaluation Rows Before Drawing Manuscript Case Figures`

### Updated

- The case-study pipeline is now complete through figure design.
- `scripts/make_case_study_figure.py` now uses category-aware case selection and merged metric fields for the persistent-failure panel.

### Removed

- None

## Impact on Future Cycles

- When one sample appears in multiple evaluation categories, treat manuscript figure assembly as a data-integration step, not a direct plotting step.
- Prefer local evidence subgraphs over ranking-only visuals when the paper needs biology-facing interpretability.
- Shorten ontology node labels and move ranking callouts early in the design loop; readability problems usually come from text placement, not graph structure.

## Raw Evidence Summary

- final figure PNG: `paper/figures/figure4_case_subgraphs.png`
- final figure PDF: `paper/figures/figure4_case_subgraphs.pdf`
- finalized pipeline status: `experiments/case_study_pipeline/pipeline_tracker.md`
