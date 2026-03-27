# Stage Log: Stage 2 - Hyperparameter Tuning

## Stage Info

- **Pipeline**: Polysaccharide benchmark
- **Stage**: 2
- **Budget**: 12 attempts
- **Gate Condition**: stable baseline configuration with variance below 5 percent across 3 seeds
- **Start Date**: 2026-03-26

## Attempt Log

| # | Hypothesis | Code Changes | Configuration | Result | Analysis | Gate Met? |
|---|-----------|-------------|--------------|--------|----------|-----------|
| 1 | The logistic baseline should first be checked for seed stability before any hyperparameter tuning; otherwise Stage 2 comparisons are not trustworthy. | Added seed control and tunable vectorizer / regularization flags to `run_logistic_baseline.py`, plus a Stage 2 multi-seed tuning runner `run_stage2_logistic_tuning.py`. | Dataset = `dataset_publishable_supervised_v1.jsonl`; split = `random_split`; config = `C=1.0`, `min_df=1`, `binary=false`; seeds = `11/22/33`. | All three runs produced identical results: `macro_f1 = 0.1580`, `exact_match = 0.2848`, `macro_f1_rel_std = 0.0`. | The Stage 2 stability condition is already satisfied for this fast baseline. This means further work should target bias / representation rather than randomness. **[Reusable]** Verify seed stability before searching hyperparameters; otherwise tuning conclusions are noisy by construction. | [x] |
| 2 | A single vectorizer-side change might improve generalization without changing the model class. | Ran two one-variable interventions using the new tuning runner: `binary=true` and `min_df=2`, keeping all other settings fixed. Added structured experiment-craft logging under `experiments/stage2_tuning/experiment_log.md`. | Variant A = `binary=true`; Variant B = `min_df=2`; both with `C=1.0`, seeds = `11/22/33`. | `binary=true` reduced `macro_f1` to `0.1515` but increased exact match to `0.3091`; `min_df=2` yielded `macro_f1 = 0.1573`, exact match `0.2727`, and shrank vocab from `6255` to `2275`. | Neither vectorizer tweak dominates the untuned baseline on the main metric. The current bottleneck appears to be model bias / class imbalance, not stochasticity or obvious token-noise overfitting. **[Reusable]** In multilabel sparse-text baselines, token binarization can improve exact-match while hurting macro-F1; do not treat them as interchangeable wins. | [ ] |
| 3 | If the logistic baseline is under-regularized, increasing `C` should improve macro-F1 without destabilizing seed behavior. | Reused the Stage 2 tuning runner and changed only `C`, keeping vectorizer settings fixed. | Dataset = `dataset_publishable_supervised_v1.jsonl`; split = `random_split`; config = `C=4.0`, `min_df=1`, `binary=false`; seeds = `11/22/33`. | All three runs again matched exactly. `macro_f1 = 0.1938`, `exact_match = 0.2824`, `macro_f1_rel_std = 0.0`. | This is the first Stage 2 tuning move with a clear win on the primary metric, so the next tuning direction should stay on model-side regularization rather than feature pruning. **[Reusable]** Once a one-variable change gives a clean gain on the primary metric, search locally around that variable before branching to new knobs. | [ ] |
| 4 | If the gain at `C=4.0` is real, nearby `C` values should reveal whether the model is still under-regularized or already near a local optimum. | Reused the tuning runner and changed only `C` to `2.0` and `8.0`, keeping the vectorizer and class weighting fixed. | Dataset = `dataset_publishable_supervised_v1.jsonl`; split = `random_split`; configs = `C=2.0` and `C=8.0`; seeds = `11/22/33`. | `C=2.0` gave `macro_f1 = 0.1745`; `C=8.0` gave `macro_f1 = 0.2077`; both remained perfectly stable across seeds. | The monotonic improvement across `C=1,2,4,8` confirms that the current logistic baseline is still benefiting from weaker regularization. **[Reusable]** When a tuning direction keeps improving monotonically, do not stop at the first win; map the local neighborhood before switching axes. | [ ] |
| 5 | If class imbalance is the main remaining bottleneck, adding balanced class weights on top of the improved `C` setting should raise macro-F1 even if exact-match falls. | Extended the logistic baseline and Stage 2 runner to accept `class_weight`, then tested `class_weight=balanced` while keeping `C=4.0` fixed. | Dataset = `dataset_publishable_supervised_v1.jsonl`; split = `random_split`; config = `C=4.0`, `class_weight=balanced`, `min_df=1`, `binary=false`; seeds = `11/22/33`. | All three runs matched exactly. `macro_f1 = 0.2552`, `exact_match = 0.2461`, `macro_f1_rel_std = 0.0`. | This is the strongest tuned logistic configuration so far on the primary metric and confirms the earlier diagnosis: class imbalance is a first-order limitation. **[Reusable]** In multilabel settings, class weighting can produce the clearest macro-F1 gains once basic regularization is set correctly. | [ ] |
| 6 | If both higher `C` and balanced class weights help independently, combining them should further improve the logistic baseline unless the model has already crossed into overfitting. | Reused the tuning runner and changed only `C` from `4.0` to `8.0` while keeping `class_weight=balanced` fixed. | Dataset = `dataset_publishable_supervised_v1.jsonl`; split = `random_split`; config = `C=8.0`, `class_weight=balanced`, `min_df=1`, `binary=false`; seeds = `11/22/33`. | All three runs matched exactly. `macro_f1 = 0.2605`, `exact_match = 0.2594`, `macro_f1_rel_std = 0.0`. | The logistic baseline is still improving, and this configuration is the current best tuned baseline overall. **[Reusable]** Once two single-variable improvements are verified independently, test their combination before declaring a local optimum. | [ ] |
| 7 | A first graph-stage tuning pass should tell us whether graph baselines justify further Stage 2 budget or whether their variance is still too high. | Added seed, hidden-dimension, learning-rate, and batch-size controls to `run_graph_gcn_baseline.py`, then added a Stage 2 graph tuning runner `run_stage2_graph_tuning.py`. Ran the baseline graph config and one stronger single-variable-style capacity/training-budget variant. | Baseline = `hidden_dim=16`, `epochs=50`; Variant = `hidden_dim=32`, `epochs=80`; both with `lr=0.01`, `batch_size=4`, seeds = `11/22/33`. | Baseline graph: `macro_f1_mean = 0.1995`, `macro_f1_rel_std = 0.0316`. Tuned graph: `macro_f1_mean = 0.2229`, `macro_f1_rel_std = 0.0732`. | Graph tuning shows real upside, but the stronger setting violates the Stage 2 stability target. That means graph remains promising but not yet as reliable as the tuned logistic baseline. **[Reusable]** For neural baselines, treat mean improvement and variance as separate acceptance tests; a better mean is not enough if stability degrades too far. | [ ] |
| 8 | If graph instability is optimization-driven, changing optimization knobs should reduce variance without discarding the stronger architecture. | Reused the graph tuning runner and changed one optimization variable at a time from the stronger graph setting: `lr=0.005` and `batch_size=8`. | Reference = `hidden_dim=32`, `epochs=80`, `lr=0.01`, `batch_size=4`; variants = `lr=0.005` and `batch_size=8`; seeds = `11/22/33`. | `lr=0.005` reduced mean macro-F1 to `0.2007` and worsened variance. `batch_size=8` produced `macro_f1_mean = 0.2148` with `macro_f1_rel_std = 0.0463`, bringing stability back under the 5% target. | Batch size is the first graph-side knob that improves the stability profile while keeping most of the mean gain. **[Reusable]** When a neural baseline is too noisy, increase batch size before lowering learning rate if the latter already hurts mean performance. | [ ] |
| 9 | If the tuned logistic baseline is close to saturation, doubling `C` again should yield only marginal gains rather than another large jump. | Reused the logistic tuning runner and changed only `C` from `8.0` to `16.0`, keeping `class_weight=balanced` fixed. | Dataset = `dataset_publishable_supervised_v1.jsonl`; split = `random_split`; config = `C=16.0`, `class_weight=balanced`, `min_df=1`, `binary=false`; seeds = `11/22/33`. | All three runs matched exactly. `macro_f1 = 0.2610`, `exact_match = 0.2606`, `macro_f1_rel_std = 0.0`. | The gain over `C=8.0` is real but very small, which suggests diminishing returns and a near-plateau. **[Reusable]** Use one extra high-value point to confirm saturation before stopping a monotonic tuning direction. | [ ] |
| 10 | If the stable graph candidate is still undertrained, increasing epochs from `80` to `100` should improve mean macro-F1 without breaking the stability constraint. | Reused the graph tuning runner and changed only `epochs`, keeping the current stable graph candidate fixed. | Reference = `hidden_dim=32`, `epochs=80`, `lr=0.01`, `batch_size=8`; tested = `epochs=100`; seeds = `11/22/33`. | `epochs=100` increased `macro_f1_mean` to `0.2244` and `exact_match_mean` to `0.2356`, but `macro_f1_rel_std` rose to `0.0887`. | Longer training improves the average graph score, but it reopens the same variance failure mode, so the stable graph choice should remain `h32_e80_bs8`. **[Reusable]** When a neural model regains mean performance only by exceeding the variance budget, keep the lower-variance candidate and stop Stage 2 rather than chasing unstable wins. | [x] |

## Gate Assessment

- **Gate condition**: stable baseline configuration with variance below 5 percent across 3 seeds
- **Current best result**: logistic baseline is perfectly stable across 3 seeds on `publishable_supervised_v1`
- **Met?**: [x] Yes / [ ] No
- **If not met**: [ ] Continue / [ ] Load experiment-craft / [ ] Escalate to evo-memory

## Key Observations

- Logistic is deterministic enough to serve as the fast Stage 2 anchor baseline.
- Feature-space tweaks alone did not improve the primary metric.
- Increasing `C` from `1.0` to `4.0` materially improved macro-F1 while preserving stability.
- Class weighting produced the largest macro-F1 gain so far, confirming that imbalance matters more than token pruning.
- Graph capacity increases improve mean performance, but graph stability is currently weaker than logistic stability.
- For the graph baseline, `batch_size=8` is the first setting that restores macro-F1 variance below the Stage 2 threshold.
- Extending the stable graph candidate from `80` to `100` epochs improves mean performance but breaks the variance constraint again.

## Lessons Learned

- [Reusable] Establish a seed-stable fast baseline first, then tune one variable at a time.
- [Reusable] Prefer the metric tied to the paper claim when tuning; here that is macro-F1, not exact-match alone.
- [Reusable] Separate feature-space tuning from model-space tuning; if one feature tweak family stalls, switch axes instead of searching it deeper.
- [Reusable] Once regularization is in a reasonable range, class weighting is often a higher-value knob than further bag-of-words cleanup for multilabel long-tail tasks.
- [Reusable] For neural baselines in Stage 2, track variance explicitly before promoting a higher-capacity setting as the new default.
- [Reusable] Once a monotonic scalar search shows diminishing returns, stop expanding it and redirect budget to the next highest-uncertainty knob.
- [Reusable] Do not accept a higher-mean neural setting as the Stage 2 default if it crosses the predeclared variance budget; stability is part of the result, not an afterthought.

## Next Stage Preparation

- [x] Gate condition verified for the logistic anchor
- [x] Results documented and saved to `/experiments/stage2_tuning/`
- [x] Trajectory log completed
- [x] Key artifacts ready for next stage
