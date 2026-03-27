# Stage Log: Stage 3 - Proposed Method

## Stage Info

- **Pipeline**: Polysaccharide benchmark
- **Stage**: 3
- **Budget**: 12 attempts
- **Gate Condition**: consistent improvement over the tuned baseline on the primary metric across 3 runs
- **Start Date**: 2026-03-26

## Attempt Log

| # | Hypothesis | Code Changes | Configuration | Result | Analysis | Gate Met? |
|---|-----------|-------------|--------------|--------|----------|-----------|
| 1 | A minimal evidence-aware logistic method should outperform the tuned Stage 2 logistic anchor if traceability weighting and polysaccharide-specific token augmentation both add useful signal. | Added `evidence_aware.py` for completeness weighting and derived polysaccharide feature tokens, implemented `run_evidence_aware_logistic.py`, and added the Stage 3 multi-seed runner `run_stage3_evidence_aware.py`. | Dataset = `dataset_publishable_supervised_v1.jsonl`; split = `random_split`; config = `C=16.0`, `class_weight=balanced`, `poly features = on`, `evidence features = on`, `sample weight = on`; seeds = `11/22/33`. | Stable but weaker than tuned logistic: `macro_f1_mean = 0.2579`, `exact_match_mean = 0.2606`, `macro_f1_rel_std = 0.0`. Stage 2 tuned logistic reference remains `macro_f1_mean = 0.2610`. | The first evidence-aware version is executable and deterministic, but it does not beat the tuned anchor. The likely issue is that the current dataset has no explicit evidence-level annotations (`evidence_type = unknown` for all records), so the constructed completeness/traceability signal is weak and the added tokens may be mostly noise. **[Reusable]** If Stage 3 underperforms with a compound method, immediately split the method into components before changing families. | [ ] |
| 2 | If traceability-based sample weighting is the useful part and token augmentation is noise, a weight-only variant should recover most of the logistic baseline while staying simpler. | Reused `run_stage3_evidence_aware.py` and disabled both evidence and polysaccharide feature tokens, leaving only sample weighting active. | Dataset = `dataset_publishable_supervised_v1.jsonl`; split = `random_split`; config = `C=16.0`, `class_weight=balanced`, `poly features = off`, `evidence features = off`, `sample weight = on`; seeds = `11/22/33`. | `macro_f1_mean = 0.2595`, `exact_match_mean = 0.2594`, `macro_f1_rel_std = 0.0`. This is closer to the tuned logistic anchor than the full Stage 3 method, but still does not exceed it. | The weighting component is less harmful than the token-augmentation component, but it still does not create a real gain over the tuned baseline. **[Reusable]** When a weighted variant nearly matches baseline but does not improve it, treat the weighting signal as weakly aligned rather than clearly useful. | [ ] |
| 3 | If derived polysaccharide/evidence tokens are useful on their own, a feature-only variant should beat or at least match the tuned logistic anchor without sample weighting. | Reused the Stage 3 runner and disabled sample weighting while keeping the feature augmentation active. | Dataset = `dataset_publishable_supervised_v1.jsonl`; split = `random_split`; config = `C=16.0`, `class_weight=balanced`, `poly features = on`, `evidence features = on`, `sample weight = off`; seeds = `11/22/33`. | `macro_f1_mean = 0.2582`, `exact_match_mean = 0.2618`, `macro_f1_rel_std = 0.0`. It improves exact match slightly but remains below the tuned logistic anchor on macro-F1. | The current token augmentation does not help the paper's primary metric. On this dataset, the extra tokens are not sufficiently discriminative to justify the added representation complexity. **[Reusable]** If feature augmentation raises an auxiliary metric but lowers the primary one, do not promote it without a stronger task-specific rationale. | [ ] |
| 4 | If the useful signal comes from polysaccharide-specific structure tokens rather than weak evidence proxies, removing evidence tokens should convert the Stage 3 method from a near-miss into a real gain over tuned logistic. | Reused the Stage 3 runner and disabled evidence features while keeping polysaccharide-specific feature tokens active. Ran both unweighted and weighted variants to isolate the effect of sample weighting. | Dataset = `dataset_publishable_supervised_v1.jsonl`; split = `random_split`; Variant A = `poly features = on`, `evidence features = off`, `sample weight = off`; Variant B = `poly features = on`, `evidence features = off`, `sample weight = on`; both with `C=16.0`, `class_weight=balanced`, seeds = `11/22/33`. | Variant A (`poly_feature_only_v1`) beat the tuned logistic anchor with `macro_f1_mean = 0.2654`, `exact_match_mean = 0.2582`, `macro_f1_rel_std = 0.0`. Variant B (`poly_feature_weighted_v1`) also beat the anchor, but by less: `macro_f1_mean = 0.2628`, `exact_match_mean = 0.2594`, `macro_f1_rel_std = 0.0`. | This identifies the real Stage 3 win condition: polysaccharide-specific representation is useful, while the current evidence-proxy machinery is not. The simplest strong method is now `poly_feature_only_v1`, and Stage 3 gate is satisfied on the paper's primary metric. **[Reusable]** When a compound method fails, isolate components aggressively; the winning signal may be one structural submodule rather than the originally emphasized mechanism. | [x] |

## Gate Assessment

- **Gate condition**: consistent improvement over the tuned baseline on the primary metric across 3 runs
- **Current best result**: `poly_feature_only_v1` with `macro_f1_mean = 0.2654`, above tuned logistic `0.2610`
- **Met?**: [x] Yes / [ ] No
- **If not met**: [ ] Continue / [ ] Load experiment-craft / [ ] Escalate to evo-memory

## Key Observations

- The minimal evidence-aware method is fully executable and stable across seeds.
- The current dataset offers no explicit evidence-level variation because `evidence_type = unknown` for all supervised records.
- Traceability/completeness weighting is less harmful than token augmentation, but neither variant beats the tuned logistic anchor.
- The current augmented token set is better interpreted as a debugging probe than as a publishable Stage 3 win.
- Removing weak evidence tokens reveals that polysaccharide-specific structure tokens are the component that actually improves macro-F1.
- Adding sample weighting on top of the winning poly-specific representation slightly reduces the gain, so weighting should not be part of the default Stage 3 method.

## Lessons Learned

- [Reusable] Stage 3 should not overclaim "evidence-aware" gains when the supervised dataset lacks true evidence-level annotations.
- [Reusable] On this dataset, sample weighting based on structural completeness is a softer intervention than adding many derived tokens.
- [Reusable] Keep Stage 3 diagnostics tightly coupled to the paper's primary metric; exact-match bumps alone are not enough.
- [Reusable] If explicit evidence metadata is absent, shift the Stage 3 claim toward stronger structure-aware representation rather than forcing an evidence-aware narrative.

## Next Stage Preparation

- [x] Gate condition verified
- [x] Results documented and saved to `/experiments/stage3_method/`
- [x] Trajectory log completed
- [x] Key artifacts ready for next stage
