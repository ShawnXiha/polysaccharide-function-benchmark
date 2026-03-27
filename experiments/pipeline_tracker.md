# Experiment Pipeline Tracker

## Project Info

- **Project**: Polysaccharide Structure-Function Benchmark and Evidence-Aware Modeling
- **Research Question**: Can evidence-aware modeling and polysaccharide-specific representations improve reliable cross-source generalization over glycan-centric baselines?
- **Start Date**: 2026-03-26
- **Source**: `多糖机器学习研究可执行计划.md`, `多糖论文规划_story_experiments_checklists.md`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Completed (engineering) | 20 / 20 | <= 20 | [x] |
| 2. Hyperparameter Tuning | Completed | 10 / 12 | <= 12 | [x] |
| 3. Proposed Method | Completed | 4 / 12 | <= 12 | [x] |
| 4. Ablation Study | Completed | 7 / 18 | <= 18 | [x] |

**Total Attempts**: 41 / 62

## Stage Details

### Stage 1: Initial Implementation
- **Baseline**: majority, logistic regression, xgboost, transformer-IUPAC, GCN/GIN, SweetNet-style
- **Target Metric**: internally reproducible baselines on fixed splits
- **Best Result**: full public-site DoLPHiN ingestion (`5078` records) and lightweight CSDB ingestion (`453` records) are both executable; the full Stage 1 suite now runs reproducibly on fixed random and leave-one-source-out splits
- **Status Notes**: Stage 1 engineering is complete. For paper-facing evaluation, use `dataset_publishable_supervised_v1.jsonl` (`4121` DoLPHiN records, `18` kept labels, `min_label_count >= 20`) as the supervised benchmark. Treat merged `DoLPHiN + CSDB` source-shift runs as engineering stress tests, not the main scientific evidence, until a label-aligned second source is available

### Stage 2: Hyperparameter Tuning
- **Key Parameters**: learning rate, batch size, class weighting, regularization
- **Best Config**: logistic `C=16.0`, `min_df=1`, `binary=false`, `class_weight=balanced`
- **Stability**: logistic seed variance `0%` across seeds `11/22/33`
- **Status Notes**: Stage 2 was executed under `experiment-craft` logging and is now closed. Logistic saturated near `macro_f1 = 0.2610` at `C=16.0, class_weight=balanced`. Graph tuning found a stable candidate at `hidden_dim=32, epochs=80, lr=0.01, batch_size=8` with `macro_f1 = 0.2148` and acceptable variance. Extending that graph candidate to `epochs=100` raised mean macro-F1 to `0.2244` but broke the variance budget (`macro_f1_rel_std = 0.0887`), so it was not promoted

### Stage 3: Proposed Method
- **Method**: evidence-aware polysaccharide predictor
- **vs Baseline**: tuned logistic `0.2610` -> initial Stage 3 winner `poly_feature_only_v1` `0.2654`
- **Integration Status**: completed; refined by Stage 4 ablation
- **Status Notes**: Stage 3 established that the useful signal comes from polysaccharide-specific representation, not the weak evidence proxy machinery. Stage 4 later refined the winning Stage 3 variant into the final `poly_core_v1` method

### Stage 4: Ablation Study
- **Components Tested**: evidence weighting, source encoding, MW, modification, repeating-unit encoding
- **Key Finding**: MW and residue tokens are the dominant positive components; branching helps; composition-count tokens hurt and were removed
- **Status Notes**: Stage 4 is complete. Controlled ablations show that the final supported method should be `poly_core_v1`, which keeps MW, branching, and residue tokens while removing weak evidence features, sample weighting, source-kingdom tokens, modification tokens, and composition-count tokens. Final result: `macro_f1 = 0.2678`

## Backtracking Log

| Date | From Stage | To Stage | Reason | Resolution |
|------|-----------|----------|--------|------------|

## Cross-Stage Insights

- Use leave-one-source-out as the primary reliability split.
- Keep traceability outputs from the first executable baseline onward.
- Early Stage 1 metrics on toy data are for pipeline validation, not model judgment.

## Revision P0 Status

- **Protocol correction**: completed. Core runners now support explicit `valid` vs `test` evaluation.
- **Stricter grouped split**: completed. A deterministic DOI-grouped split was added and verified to have `0` group leakage.
- **Corrected comparison result**:
  - random test: tuned logistic `0.2610` vs `poly_core_v1` `0.2678`
  - DOI-grouped test: tuned logistic `0.1250` vs `poly_core_v1` `0.1140`
- **Bootstrap result**:
  - random-test macro-F1 delta CI: `[-0.0115, 0.0260]`
  - DOI-grouped-test macro-F1 delta CI: `[-0.0254, 0.0020]`
- **Implication**: the benchmark and ablation claims remain useful, but the paper can no longer claim that `poly_core_v1` robustly improves over the tuned logistic anchor under stricter grouped generalization. Revision details are recorded in `experiments/revision_p0/revision_p0_findings.md`.

## Results Summary

| Method | Primary Metric | Secondary Metric 1 | Secondary Metric 2 |
|--------|---------------|--------------------|--------------------|
| Published baseline | pending | pending | pending |
| Reproduced baseline | `publishable_supervised_v1` and merged stress-test suites both executable | publishable logistic random macro-F1: 0.1580 | publishable graph random macro-F1: 0.1941 |
| Tuned baseline | logistic tuned on `publishable_supervised_v1` | macro-F1: 0.2610 (`C=16.0`, `class_weight=balanced`) | exact match: 0.2606 |
| Proposed method | `poly_core_v1` on `publishable_supervised_v1` | macro-F1: 0.2678 | exact match: 0.2570 |

## Evolution Memory Triggers

- [ ] Pipeline succeeded -> Trigger ESE
- [ ] No executable code within budget, or method underperforms baseline -> Trigger IVE
- [ ] Evolution report written to `/memory/evolution-reports/`

## Handoff Checklist

- [x] All stage logs complete
- [x] Trajectory logs saved
- [x] Results tables ready for paper-writing
- [x] Ablation table ready
- [ ] Key implementation details documented
- [ ] evo-memory updated
