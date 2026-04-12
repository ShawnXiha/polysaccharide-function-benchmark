# Experiment Pipeline Tracker

## Project Info

- **Project**: Ontology tail-gain stability and significance validation
- **Research Question**: Is the confidence-gated parent/child ontology best variant statistically significant and stably tail-improving relative to the disease-aware main baseline?
- **Start Date**: 2026-03-29
- **Parent Baseline**: `experiments/poly_function_link_prediction_with_disease_hierarchy_parent_child_tune_c025.json`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Protocol Design | Completed | 2 / 4 | <=4 | Yes |
| 2. Paired Execution | Completed | 2 / 8 | <=8 | Yes |
| 3. Significance Analysis | Completed | 2 / 4 | <=4 | Yes |
| 4. Stability Summary | Completed | 1 / 4 | <=4 | Yes |

## Planned Protocol

- paired runs with identical seeds for baseline and ontology variant
- `save-edge-records` enabled for per-edge paired testing
- statistical tests:
  - paired permutation test on per-edge delta
  - bootstrap confidence interval on mean delta
- targets:
  - overall filtered `Hits@3`
  - overall filtered `MRR`
  - tail micro filtered `Hits@3`

## Execution Notes

- Attempt 1 used `8` paired seeds and showed positive but underpowered tail `Hits@3` improvement: two-sided McNemar `p=0.125`.
- The bottleneck was statistical power, not method reversal: all observed discordant tail cases favored the ontology variant and tail filtered `MRR` was already clearly positive.
- Attempt 2 expanded the paired set to `16` seeds and kept the method fixed.
- To support large paired outputs, `run_poly_function_link_prediction.py` was patched to avoid printing the full JSON when `--save-edge-records` is enabled.
- PowerShell redirection created mixed encodings in the earliest files, so the summary script now reads JSON robustly across `utf-8` and `utf-16` variants.

## Final Outcome

- Final report: `experiments/ontology_stability_pipeline/stability_significance.md`
- Final summary JSON: `experiments/ontology_stability_runs/ontology_stability_summary.json`
- Main conclusion:
  - overall filtered `Hits@3` remains effectively unchanged
  - tail micro filtered `Hits@3` improves from `0.0552` to `0.1021`
  - tail `Hits@3` is significant under the directional one-sided paired test: `p=0.03125`
  - tail filtered `MRR` gain is strongly significant: permutation `p=0.0002499`
  - no seed shows a tail regression (`16/16` ontology `>=` baseline)
