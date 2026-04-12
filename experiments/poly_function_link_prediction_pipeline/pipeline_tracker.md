# Experiment Pipeline Tracker

## Project Info

- **Project**: DoLPHiN KG poly-function masked link prediction
- **Research Question**: Can KG-derived clean meta-path features recover masked polysaccharide-function edges better than naive popularity ranking, and what side-information actually helps?
- **Start Date**: 2026-03-27
- **Source**: `docs/dolphin_kg_research_ideation.md`

## Pipeline Status

| Stage | Status | Attempts Used | Budget | Gate Met? |
|-------|--------|---------------|--------|-----------|
| 1. Initial Implementation | Complete | 3 / 20 | <=20 | Yes |
| 2. Hyperparameter Tuning | Complete | 4 / 12 | <=12 | Yes |
| 3. Proposed Method | Complete | 2 / 12 | <=12 | Yes |
| 4. Ablation Study | Complete | 3 / 18 | <=18 | Yes |

**Total Attempts**: 12 / 62

## Stage Details

### Stage 1: Initial Implementation
- **Baseline**: popularity ranking, centroid scoring, and kNN scoring over clean meta-path features
- **Target Metric**: executable masked-edge evaluation with sensible ranking metrics; clean method should exceed centroid
- **Best Result**: clean `meta_path_knn` with default `top_k=50`, `Hits@3=0.639`
- **Status Notes**: executable evaluation established; centroid diagnosed as a poor scoring choice

### Stage 2: Hyperparameter Tuning
- **Key Parameters**: `top_k` in kNN voting
- **Best Config**: clean `meta_path_knn`, `top_k=10`
- **Stability**: consistent superiority over centroid; `Hits@3` remained `0.618-0.655`
- **Status Notes**: chose `Hits@3` as primary metric for retrieval quality; `top_k=10` best on primary metric

### Stage 3: Proposed Method
- **Method**: disease-aware meta-path kNN link prediction
- **vs Baseline**: `Hits@3` improved from `0.655` to `0.814`
- **Integration Status**: disease features added to graph-derived similarity space; no model architecture change
- **Status Notes**: strong gain, but should be framed as side-information-enhanced link recovery rather than clean structure-only prediction

### Stage 4: Ablation Study
- **Components Tested**: disease features, `idf` label weighting, centroid vs kNN scoring, raw vs filtered ranking, label-support stratification
- **Key Finding**: disease features help substantially; `idf` weighting hurts; centroid scoring is not viable; filtered ranking is required; remaining weakness is long-tail label recovery
- **Status Notes**: clean kNN is the strongest defensible clean method; disease-aware kNN is the strongest upper-bound setting; head-label gains dominate the aggregate metrics

## Backtracking Log

| Date | From Stage | To Stage | Reason | Resolution |
|------|-----------|----------|--------|------------|
| 2026-03-27 | 1 | 1 | Centroid scorer collapsed to frequent labels and nonsensical nearest functions | Switched to local kNN label propagation using the same meta-path features |

## Cross-Stage Insights

- Local neighborhood voting preserves KG signal better than global function centroids.
- Disease features are powerful but should be treated as auxiliary semantics, not clean primary evidence.
- Label-frequency corrections (`idf` weighting) can hurt more than help when high-frequency functions are genuinely common in local neighborhoods.
- Multi-label link prediction should be reported with filtered ranking as the primary metric.
- Per-label stratification is necessary because aggregate gains mostly come from head functions while tail labels remain poorly recovered.

## Results Summary

| Method | Primary Metric | Secondary Metric 1 | Secondary Metric 2 |
|--------|---------------|--------------------|--------------------|
| Popularity (filtered) | Hits@3 = 0.693 | MRR = 0.5893 | Hits@5 = 0.782 |
| Clean centroid (filtered) | Hits@3 = 0.014 | MRR = 0.0553 | Mean rank = 25.275 |
| Tuned clean kNN (`top_k=10`, filtered) | Hits@3 = 0.743 | MRR = 0.6168 | Hits@5 = 0.809 |
| Proposed method: disease-aware kNN (`top_k=25`, filtered) | Hits@3 = 0.875 | MRR = 0.8119 | Hits@5 = 0.924 |

## Stratified Summary

| Setting | Tail `Hits@3` | Mid `Hits@3` | Head `Hits@3` |
|--------|---------------|--------------|---------------|
| Clean kNN (filtered micro) | 0.167 | 0.375 | 0.762 |
| Disease-aware kNN (filtered micro) | 0.167 | 0.400 | 0.899 |

## Evolution Memory Triggers

- [x] Pipeline succeeded -> Trigger ESE (Experiment Strategy Evolution)
- [ ] No executable code within budget, or method underperforms baseline -> Trigger IVE (Idea Validation Evolution)
- [x] Evolution report written to `/memory/evolution-reports/`

## Handoff Checklist

- [x] All stage logs complete
- [x] Trajectory logs saved
- [x] Results tables ready for paper-writing
- [x] Ablation table ready
- [x] Key implementation details documented
- [x] evo-memory updated
