# Stage Log: Stage 4 - Ablation Study

## Stage Info

- **Pipeline**: Polysaccharide benchmark
- **Stage**: 4
- **Budget**: 18 attempts
- **Gate Condition**: all contribution claims are supported by controlled experiments
- **Start Date**: 2026-03-26

## Attempt Log

| # | Hypothesis | Code Changes | Configuration | Result | Analysis | Gate Met? |
|---|-----------|-------------|--------------|--------|----------|-----------|
| 1 | If molecular-weight buckets are a real part of the Stage 3 gain, removing them should cause a clear macro-F1 drop from the Stage 3 winning method. | Extended `evidence_aware.py`, `run_evidence_aware_logistic.py`, and `run_stage3_evidence_aware.py` with per-component feature toggles so Stage 4 can remove individual poly-specific token groups without changing anything else. Ran a single-component ablation with `mw` tokens removed from the Stage 3 winner. | Base reference = `poly_feature_only_v1`; ablation = `disable_mw_feature`; fixed settings = `C=16.0`, `class_weight=balanced`, `evidence features = off`, `sample weight = off`; seeds = `11/22/33`. | `ablate_no_mw` dropped to `macro_f1_mean = 0.2461`, `exact_match_mean = 0.2533`, `macro_f1_rel_std = 0.0`. | This is the largest negative ablation in the full Stage 4 set and shows that MW buckets are a first-order contributor to the method gain. **[Reusable]** If removing one structured feature family causes a large deterministic drop, it should move from “nice-to-have metadata” to a core claim component. | [x] |
| 2 | If branching-presence tokens matter, removing them should reduce macro-F1 even when MW and residue tokens remain intact. | Reused the new Stage 4 component toggles and removed only branching-related tokens from the Stage 3 winner. | Ablation = `disable_branching_feature`; all other Stage 3 winner settings fixed; seeds = `11/22/33`. | `ablate_no_branching` gave `macro_f1_mean = 0.2598`, `exact_match_mean = 0.2570`, `macro_f1_rel_std = 0.0`. | Branching contributes positively but not as strongly as MW or residue tokens. It remains a supported component of the representation claim. **[Reusable]** A moderate but consistent ablation drop is enough to support a component-level contribution, even if it is not the largest effect. | [x] |
| 3 | If modification-specific tokens are important on this dataset, removing them should hurt the primary metric; otherwise they should be treated as optional or noisy. | Reused the Stage 4 toggles and removed only modification-related tokens. | Ablation = `disable_modification_feature`; all other Stage 3 winner settings fixed; seeds = `11/22/33`. | `ablate_no_modification` gave `macro_f1_mean = 0.2619`, `exact_match_mean = 0.2582`, `macro_f1_rel_std = 0.0`. | Removing modification tokens slightly improves over the tuned logistic baseline but underperforms the Stage 3 winner. This suggests modification tokens are not the main source of gain and may be near-neutral or mildly noisy. **[Reusable]** If an ablation leaves the model near baseline, avoid elevating that component into the main paper claim. | [x] |
| 4 | If residue-set tokens encode genuinely useful polysaccharide composition information, removing them should materially reduce the Stage 3 gain. | Reused the Stage 4 toggles and removed only residue-set and residue-diversity tokens. | Ablation = `disable_residue_feature`; all other Stage 3 winner settings fixed; seeds = `11/22/33`. | `ablate_no_residue` dropped to `macro_f1_mean = 0.2533`, `exact_match_mean = 0.2545`, `macro_f1_rel_std = 0.0`. | Residue tokens are the second strongest positive component after MW. They clearly belong in the core Stage 3 representation claim. **[Reusable]** Composition-aware residue tokens are worth keeping when their removal causes a multi-point macro-F1 drop on a stable benchmark. | [x] |
| 5 | If coarse source-kingdom tokens are only weak context signals, removing them should have a small effect relative to MW or residue ablations. | Reused the Stage 4 toggles and removed only source-kingdom tokens. | Ablation = `disable_source_kingdom_feature`; all other Stage 3 winner settings fixed; seeds = `11/22/33`. | `ablate_no_source_kingdom` gave `macro_f1_mean = 0.2621`, `exact_match_mean = 0.2594`, `macro_f1_rel_std = 0.0`. | Source-kingdom context is mildly helpful but not central. It should be framed as auxiliary context, not as a primary innovation component. **[Reusable]** Small ablation drops indicate context features can stay optional in the narrative even if they remain cheap to compute. | [x] |
| 6 | If composition-count tokens are too coarse and redundant with the raw composition string, removing them may actually improve performance rather than reduce it. | Reused the Stage 4 toggles and removed only `composition_terms_*` tokens. | Ablation = `disable_composition_feature`; all other Stage 3 winner settings fixed; seeds = `11/22/33`. | `ablate_no_composition_terms` improved to `macro_f1_mean = 0.2669`, `exact_match_mean = 0.2618`, `macro_f1_rel_std = 0.0`. | This is a negative-value component: the token family hurts the primary metric and should be removed from the final method. **[Reusable]** A controlled ablation that improves the model identifies removable noise, not a failed experiment. Use it to simplify the final method definition. | [x] |
| 7 | If the final method keeps only the clearly supported positive components and removes the weak or harmful ones, it should outperform the original Stage 3 winner while remaining fully stable. | Ran a refined method that keeps only the strongest supported poly-specific components: MW, branching, and residue tokens; removed evidence features, sample weighting, modification tokens, source-kingdom tokens, and composition-count tokens. | Tag = `poly_core_v1`; config = `include_mw = true`, `include_branching = true`, `include_residue = true`, `include_modification = false`, `include_source_kingdom = false`, `include_composition_terms = false`, `evidence features = off`, `sample weight = off`; seeds = `11/22/33`. | `poly_core_v1` is the best result so far: `macro_f1_mean = 0.2678`, `exact_match_mean = 0.2570`, `macro_f1_rel_std = 0.0`. | Stage 4 both validates and sharpens the Stage 3 claim. The final paper method should be `poly_core_v1`, not the broader `poly_feature_only_v1`. The supported core representation components are MW, branching, and residue tokens. **[Reusable]** Use ablation not only to defend a method, but to simplify it into the strongest justifiable final form. | [x] |

## Gate Assessment

- **Gate condition**: all contribution claims are supported by controlled experiments
- **Current best result**: `poly_core_v1` with `macro_f1_mean = 0.2678`
- **Met?**: [x] Yes / [ ] No
- **If not met**: [ ] Continue / [ ] Load experiment-craft / [ ] Escalate to evo-memory

## Key Observations

- MW buckets are the single strongest positive component.
- Residue-set tokens are the second strongest positive component.
- Branching tokens contribute positively, but less strongly than MW and residue tokens.
- Modification and source-kingdom tokens are weak components and should not be central to the paper claim.
- `composition_terms_*` tokens are actively harmful and should be removed from the final method.
- The final supported representation is a compact core: MW + branching + residue tokens.

## Lessons Learned

- [Reusable] Controlled ablations can upgrade a provisional Stage 3 win into a cleaner and stronger final method.
- [Reusable] Feature families that are easy to compute can still be harmful; keep them only if the ablation proves they help.
- [Reusable] When one ablation improves performance, treat it as evidence for simplification rather than as a nuisance result.

## Next Stage Preparation

- [x] Gate condition verified
- [x] Results documented and saved to `/experiments/stage4_ablation/`
- [x] Trajectory log completed
- [x] Key artifacts ready for next stage
