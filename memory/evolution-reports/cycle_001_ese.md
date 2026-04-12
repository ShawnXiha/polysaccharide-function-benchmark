# Evolution Report: Cycle 001 - ESE

**Date**: 2026-03-27
**Trigger**: Successful completion of the `poly-function` link prediction experiment pipeline through Stage 4 ablation
**Source Artifacts**: 
- `experiments/poly_function_link_prediction_pipeline/pipeline_tracker.md`
- `experiments/poly_function_link_prediction_pipeline/stage1_initial_implementation/trajectory.md`
- `experiments/poly_function_link_prediction_pipeline/stage2_tuning/trajectory.md`
- `experiments/poly_function_link_prediction_pipeline/stage3_proposed_method/trajectory.md`
- `experiments/poly_function_link_prediction_pipeline/stage4_ablation/trajectory.md`
- `experiments/poly_function_link_prediction_pipeline/diagnosis_centroid_failure.md`
- `experiments/poly_function_link_prediction_clean.json`
- `experiments/poly_function_link_prediction_clean_k10.json`
- `experiments/poly_function_link_prediction_with_disease_k25.json`
- `experiments/poly_function_link_prediction_with_disease_k25_idf.json`

## Changes Made

### Added

- `KG Meta-Path Feature Blocks For DoLPHiN`: added to Experimentation Memory / Data Processing Strategies
- `Local kNN Voting Beats Global Centroids`: added to Experimentation Memory / Model Training Strategies
- `Re-Tune Neighborhood Size After Adding New Relation Families`: added to Experimentation Memory / Model Training Strategies
- `Auxiliary Disease Features As Upper-Bound Semantics`: added to Experimentation Memory / Architecture Strategies
- `Diagnose Prototype Collapse By Holding Features Fixed`: added to Experimentation Memory / Debugging Strategies
- `Frequency Reweighting Can Remove Useful Local Signal`: added to Experimentation Memory / Debugging Strategies

### Updated

- None

### Removed/Archived

- None

## Reasoning

This cycle produced a clean sequence of evidence that was useful beyond a single run. The most important pattern was that the representation itself was not the main bottleneck early on; the scorer was. Global centroid scoring failed catastrophically, but local kNN voting over the same graph-derived features recovered masked edges well. That makes the resulting strategy reusable in any sparse multi-label KG retrieval setting where class prototypes are likely to be multimodal.

The second strong pattern was the role of disease information. Disease-aware features produced a substantial improvement, but the semantics are too tightly coupled to target labels to serve as the main clean claim. This is a strategic lesson about experimental framing as much as model design: separate clean structure-driven settings from auxiliary-semantic upper-bound settings. That distinction is likely to matter in future cycles beyond this repository.

Finally, the failed `idf` weighting attempts were worth recording because they overturned a plausible default assumption. In many retrieval systems inverse-frequency weighting is beneficial, but here it consistently harmed results, indicating that local frequency carries useful evidence. That is exactly the kind of negative but reusable result evo-memory should preserve.

## Impact on Future Cycles

- **For idea-tournament**: No direct M_I change in this cycle, but future ideas involving KG link prediction should prioritize local neighborhood methods over prototype scorers.
- **For experiment-pipeline**: Future KG retrieval experiments should start from local kNN voting, tune `top_k` early, and treat disease-style auxiliary nodes as an explicit upper-bound ablation.
- **Confidence level**: Moderate. Several strategies were confirmed by controlled ablations within one cycle, but cross-cycle confirmation is still pending.

## Raw Evidence Summary

- Clean centroid baseline: `MRR=0.0538`, `Hits@3=0.014`
- Clean tuned kNN baseline: `Hits@3=0.655` at `top_k=10`
- Disease-aware kNN: `Hits@3=0.814` at `top_k=25`
- Disease-aware + idf weighting: `Hits@3=0.780`
- Controlled comparison shows disease features help and `idf` hurts under the same scorer family
