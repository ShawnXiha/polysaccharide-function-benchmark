# Experiment Log: Stage 2 Tuning

## Goal of This Week
Stabilize a publishable baseline on `dataset_publishable_supervised_v1.jsonl` and identify one justified hyperparameter change that improves over the untuned configuration.

## Experiment 1: Logistic Seed Stability

### Purpose
Check whether the current logistic baseline is stable enough across seeds to be a valid Stage 2 starting point.

### Setting
- Data: `data_processed/dataset_publishable_supervised_v1.jsonl`
- Split: `data_processed/splits_publishable_supervised_v1/random_split.json`
- Algorithm changes: none; baseline logistic configuration
- Hyperparameters: `C=1.0`, `min_df=1`, `max_features=0`, `binary=false`, seeds `11/22/33`

### Results
- Quantitative:
  - `baseline_c1_min1` across seeds `11/22/33`
  - `macro_f1_mean = 0.1580`
  - `macro_f1_rel_std = 0.0`
  - `exact_match_mean = 0.2848`
  - `exact_match_rel_std = 0.0`
- Qualitative:
  - seed changes do not alter outputs, so current logistic pipeline is effectively deterministic on the fixed split
  - vocabulary size remains `6255`
- Good cases:
  - the baseline is already stable enough for Stage 2 comparisons
- Failure cases:
  - none on stability; no variance-driven debugging needed at this stage

### Analysis
- Do results match expectations? yes
- Stability gate status:
  - stronger than expected; relative variance is `0%`, well below the Stage 2 threshold
- Confirmed cause from diagnosis:
  - current limitation is model bias / representation quality, not stochastic instability

### Next Steps
- [x] Compute seed variance and decide whether stability gate is close enough to continue
- [x] If stable enough, test one vectorizer-side change only
- [ ] Tune one scalar model-side parameter next (`C` or class weighting)

## Experiment 2: Logistic Single-Variable Tuning

### Purpose
Test one feature-space intervention after the baseline stability check, without changing multiple variables at once.

### Setting
- Data: `data_processed/dataset_publishable_supervised_v1.jsonl`
- Split: `data_processed/splits_publishable_supervised_v1/random_split.json`
- Algorithm changes:
  - Run `binary=true` while keeping all other settings fixed
  - Run `min_df=2` while keeping all other settings fixed
- Hyperparameters:
  - baseline: `C=1.0`, `min_df=1`, `binary=false`
  - variant A: `C=1.0`, `min_df=1`, `binary=true`
  - variant B: `C=1.0`, `min_df=2`, `binary=false`
  - seeds: `11/22/33`

### Results
- Quantitative:
  - baseline:
    - `macro_f1_mean = 0.1580`
    - `exact_match_mean = 0.2848`
    - `vocab_size = 6255`
  - `binary=true`:
    - `macro_f1_mean = 0.1515`
    - `exact_match_mean = 0.3091`
    - `vocab_size = 6255`
  - `min_df=2`:
    - `macro_f1_mean = 0.1573`
    - `exact_match_mean = 0.2727`
    - `vocab_size = 2275`
- Qualitative:
  - `binary=true` makes predictions slightly more conservative; exact-match rises, macro-F1 falls
  - `min_df=2` removes a large amount of vocabulary but gives no real macro-F1 gain
- Good cases:
  - both variants remained perfectly stable across seeds, so comparisons are clean
- Failure cases:
  - neither one-variable change improved both macro-F1 and exact match simultaneously

### Analysis
- Do results match expectations? mostly yes
- Ranked hypotheses:
  1. logistic performance is now limited more by label imbalance than by rare-token noise
  2. reducing feature granularity alone is insufficient because the current feature text is already information-limited
  3. a model-side regularization move is more promising than additional vectorizer pruning
- Confirmed cause:
  - no evidence that token binarization or mild vocabulary pruning is the main bottleneck
- Decision:
  - keep `baseline_c1_min1` as current Stage 2 reference

### Next Steps
- [x] Pick next variable based on Experiment 1 and 2 outcomes
- [x] Test `C` as the next single variable
- [ ] If `C` does not improve macro-F1, add class weighting rather than more vectorizer tweaks

## Experiment 3: Logistic Regularization Sweep

### Purpose
Test whether the current logistic baseline is under-regularized or over-regularized by changing only `C`.

### Setting
- Data: `data_processed/dataset_publishable_supervised_v1.jsonl`
- Split: `data_processed/splits_publishable_supervised_v1/random_split.json`
- Algorithm changes: none
- Hyperparameters:
  - baseline reference: `C=1.0`, `min_df=1`, `binary=false`
  - tested variant: `C=4.0`, `min_df=1`, `binary=false`
  - seeds: `11/22/33`

### Results
- Quantitative:
  - baseline:
    - `macro_f1_mean = 0.1580`
    - `exact_match_mean = 0.2848`
  - `C=4.0`:
    - `macro_f1_mean = 0.1938`
    - `exact_match_mean = 0.2824`
    - `macro_f1_rel_std = 0.0`
- Qualitative:
  - stronger `C` improves the main metric substantially without destabilizing the run
  - exact match is essentially unchanged, so the gain is not a metric-trade illusion
- Good cases:
  - this is the first Stage 2 change that clearly beats the untuned logistic baseline on macro-F1
- Failure cases:
  - none yet; the remaining question is whether gains plateau or reverse at higher `C`

### Analysis
- Do results match expectations? yes
- Confirmed cause:
  - the untuned logistic baseline was too conservative under default regularization for this benchmark
- Implication:
  - Stage 2 should now search around `C` and then test class weighting, rather than continue with vectorizer pruning

### Next Steps
- [ ] Test a neighboring `C` value to see whether `4.0` is near the local optimum
- [ ] Add class weighting only after the `C` neighborhood is mapped

## Experiment 4: Logistic C Neighborhood

### Purpose
Determine whether `C=4.0` is already near the local optimum or whether the gain continues when moving to nearby values.

### Setting
- Data: `data_processed/dataset_publishable_supervised_v1.jsonl`
- Split: `data_processed/splits_publishable_supervised_v1/random_split.json`
- Algorithm changes: none
- Hyperparameters:
  - variant A: `C=2.0`, `min_df=1`, `binary=false`
  - variant B: `C=8.0`, `min_df=1`, `binary=false`
  - seeds: `11/22/33`

### Results
- Quantitative:
  - `C=2.0`:
    - `macro_f1_mean = 0.1745`
    - `exact_match_mean = 0.2812`
  - `C=8.0`:
    - `macro_f1_mean = 0.2077`
    - `exact_match_mean = 0.2861`
- Qualitative:
  - performance improved monotonically from `C=1.0 -> 2.0 -> 4.0 -> 8.0`
  - the improvement is on the primary metric, not only the auxiliary metric
- Good cases:
  - no instability appeared while moving `C`
- Failure cases:
  - local optimum has not yet been observed inside the current neighborhood

### Analysis
- Do results match expectations? yes
- Confirmed cause:
  - the current logistic baseline remains too conservative at lower `C`
- Implication:
  - the regularization neighborhood is still promising, but a more important next test is class weighting because class imbalance is likely interacting with the same failure mode

### Next Steps
- [x] Test a neighboring `C` value to see whether `4.0` is near the local optimum
- [ ] Compare the best unweighted config against a class-weighted counterpart

## Experiment 5: Logistic Class Weighting

### Purpose
Test the highest-likelihood hypothesis from Experiment 2 directly: label imbalance is the main remaining bottleneck.

### Setting
- Data: `data_processed/dataset_publishable_supervised_v1.jsonl`
- Split: `data_processed/splits_publishable_supervised_v1/random_split.json`
- Algorithm changes: add `class_weight=balanced`
- Hyperparameters:
  - reference: `C=4.0`, `class_weight=none`
  - tested variant: `C=4.0`, `class_weight=balanced`
  - seeds: `11/22/33`

### Results
- Quantitative:
  - reference (`C=4.0`, unweighted):
    - `macro_f1_mean = 0.1938`
    - `exact_match_mean = 0.2824`
  - tested (`C=4.0`, balanced):
    - `macro_f1_mean = 0.2552`
    - `exact_match_mean = 0.2461`
    - `macro_f1_rel_std = 0.0`
- Qualitative:
  - balanced weighting gives a large macro-F1 gain while sacrificing exact match
  - this is consistent with improved recall on minority labels rather than better conservative set prediction
- Good cases:
  - strongest Stage 2 result so far on the paper's primary metric
- Failure cases:
  - exact match drops, so the balanced setting should be framed as a macro-F1 optimization choice, not a universally dominant setting

### Analysis
- Do results match expectations? yes
- Confirmed cause:
  - class imbalance is a first-order bottleneck for the current logistic baseline
- Decision:
  - keep `C=4.0, class_weight=balanced` as the current best tuned logistic config for macro-F1 oriented reporting

### Next Steps
- [ ] Test whether `C=8.0, class_weight=balanced` improves further or overcorrects
- [ ] If macro-F1 plateaus, move Stage 2 tuning to `graph_gcn`

## Experiment 6: Logistic High-C Balanced

### Purpose
Check whether the tuned logistic baseline is still improving when both useful knobs are combined: higher `C` and balanced class weights.

### Setting
- Data: `data_processed/dataset_publishable_supervised_v1.jsonl`
- Split: `data_processed/splits_publishable_supervised_v1/random_split.json`
- Algorithm changes: none
- Hyperparameters:
  - reference: `C=4.0`, `class_weight=balanced`
  - tested variant: `C=8.0`, `class_weight=balanced`
  - `min_df=1`, `binary=false`
  - seeds: `11/22/33`

### Results
- Quantitative:
  - reference:
    - `macro_f1_mean = 0.2552`
    - `exact_match_mean = 0.2461`
  - tested:
    - `macro_f1_mean = 0.2605`
    - `exact_match_mean = 0.2594`
    - `macro_f1_rel_std = 0.0`
- Qualitative:
  - the combined configuration improves both macro-F1 and exact match over the previous best tuned logistic
- Good cases:
  - this is the strongest logistic result so far
- Failure cases:
  - no instability; the question is only whether higher `C` keeps helping

### Analysis
- Do results match expectations? yes
- Confirmed cause:
  - the model still benefits from weaker regularization after imbalance correction
- Decision:
  - promote `C=8.0, class_weight=balanced` to the current best logistic config

### Next Steps
- [ ] Test one more nearby `C` value only if logistic remains the lead Stage 2 candidate
- [ ] Move tuning focus to graph and decide whether its variance is acceptable

## Experiment 7: Graph GCN First Tuning Pass

### Purpose
Assess whether the graph baseline is worth further Stage 2 budget by testing one larger-capacity setting against the current graph baseline.

### Setting
- Data: `data_processed/dataset_publishable_supervised_v1.jsonl`
- Split: `data_processed/splits_publishable_supervised_v1/random_split.json`
- Algorithm changes: none
- Hyperparameters:
  - baseline: `hidden_dim=16`, `epochs=50`, `lr=0.01`, `batch_size=4`
  - tested variant: `hidden_dim=32`, `epochs=80`, `lr=0.01`, `batch_size=4`
  - seeds: `11/22/33`

### Results
- Quantitative:
  - baseline graph:
    - `macro_f1_mean = 0.1995`
    - `macro_f1_rel_std = 0.0316`
    - `exact_match_mean = 0.1762`
  - tuned graph:
    - `macro_f1_mean = 0.2229`
    - `macro_f1_rel_std = 0.0732`
    - `exact_match_mean = 0.2287`
- Qualitative:
  - the stronger graph setting improves mean performance
  - variance becomes materially higher and exceeds the Stage 2 stability target on macro-F1
- Good cases:
  - graph responds positively to capacity and training-budget changes
- Failure cases:
  - the tuned graph configuration is not yet stable enough to be treated like the logistic anchor

### Analysis
- Do results match expectations? yes
- Confirmed cause:
  - graph performance is sensitivity-limited rather than feature-limited; capacity helps, but optimization variance rises with it
- Decision:
  - keep the tuned graph result as a promising direction, but do not spend broad search budget until variance is addressed

### Next Steps
- [ ] If graph remains important, next single-variable test should be optimization-side (`lr` or batch size), not another capacity jump
- [ ] Keep logistic as the primary tuned baseline for paper-facing comparisons

## Experiment 8: Graph Optimization Tuning

### Purpose
Reduce graph variance without abandoning the stronger `hidden_dim=32, epochs=80` setting.

### Setting
- Data: `data_processed/dataset_publishable_supervised_v1.jsonl`
- Split: `data_processed/splits_publishable_supervised_v1/random_split.json`
- Algorithm changes: none
- Hyperparameters:
  - reference strong graph: `hidden_dim=32`, `epochs=80`, `lr=0.01`, `batch_size=4`
  - variant A: `lr=0.005`
  - variant B: `batch_size=8`
  - seeds: `11/22/33`

### Results
- Quantitative:
  - reference strong graph:
    - `macro_f1_mean = 0.2229`
    - `macro_f1_rel_std = 0.0732`
    - `exact_match_mean = 0.2287`
  - `lr=0.005`:
    - `macro_f1_mean = 0.2007`
    - `macro_f1_rel_std = 0.0960`
    - `exact_match_mean = 0.2020`
  - `batch_size=8`:
    - `macro_f1_mean = 0.2148`
    - `macro_f1_rel_std = 0.0463`
    - `exact_match_mean = 0.2162`
- Qualitative:
  - lowering `lr` hurts both mean performance and stability
  - increasing `batch_size` lowers the mean slightly but restores variance to within the Stage 2 threshold
- Good cases:
  - `batch_size=8` is the first graph setting that is both reasonably strong and variance-controlled
- Failure cases:
  - the highest-mean graph setting (`h32_e80`) remains too unstable to be the default

### Analysis
- Do results match expectations? yes
- Confirmed cause:
  - graph instability is optimization-driven, and larger batch size helps more than lower learning rate in this setup
- Decision:
  - keep `hidden_dim=32, epochs=80, lr=0.01, batch_size=8` as the current stable graph candidate

### Next Steps
- [ ] If more graph budget remains, test one adjacent learning rate around the stable `batch_size=8` setting
- [ ] Otherwise freeze graph here and close Stage 2 with logistic as the primary tuned anchor

## Experiment 9: Logistic High-C Saturation Check

### Purpose
Check whether the tuned logistic baseline is still gaining materially or has entered a near-plateau regime.

### Setting
- Data: `data_processed/dataset_publishable_supervised_v1.jsonl`
- Split: `data_processed/splits_publishable_supervised_v1/random_split.json`
- Algorithm changes: none
- Hyperparameters:
  - reference: `C=8.0`, `class_weight=balanced`
  - tested variant: `C=16.0`, `class_weight=balanced`
  - `min_df=1`, `binary=false`
  - seeds: `11/22/33`

### Results
- Quantitative:
  - reference:
    - `macro_f1_mean = 0.2605`
    - `exact_match_mean = 0.2594`
  - tested:
    - `macro_f1_mean = 0.2610`
    - `exact_match_mean = 0.2606`
    - `macro_f1_rel_std = 0.0`
- Qualitative:
  - the gain from `C=8` to `C=16` is real but very small
- Good cases:
  - performance still did not regress
- Failure cases:
  - marginal improvement suggests diminishing returns

### Analysis
- Do results match expectations? yes
- Confirmed cause:
  - logistic is approaching a local plateau under the current feature set
- Decision:
  - `C=16.0, class_weight=balanced` is the current best logistic config, but the improvement over `C=8.0` is small enough that Stage 2 is close to saturation for this model family

### Next Steps
- [ ] Decide whether to stop logistic tuning here and promote this config as the Stage 2 final tuned logistic
- [ ] Use remaining budget only if another model family has a higher upside than further logistic micro-search

## Experiment 10: Graph Stable-Candidate Epoch Extension

### Purpose
Test whether the stable graph candidate can recover more macro-F1 by training longer, without reopening the variance problem.

### Setting
- Data: `data_processed/dataset_publishable_supervised_v1.jsonl`
- Split: `data_processed/splits_publishable_supervised_v1/random_split.json`
- Algorithm changes: none
- Hyperparameters:
  - reference stable graph: `hidden_dim=32`, `epochs=80`, `lr=0.01`, `batch_size=8`
  - tested variant: `hidden_dim=32`, `epochs=100`, `lr=0.01`, `batch_size=8`
  - seeds: `11/22/33`

### Results
- Quantitative:
  - reference stable graph:
    - `macro_f1_mean = 0.2148`
    - `macro_f1_rel_std = 0.0463`
    - `exact_match_mean = 0.2162`
  - tested:
    - `macro_f1_mean = 0.2244`
    - `macro_f1_rel_std = 0.0887`
    - `exact_match_mean = 0.2356`
- Qualitative:
  - the extra training budget improves the average score
  - the seed spread widens again, so the gain is not stable enough for the Stage 2 acceptance rule
- Good cases:
  - graph mean performance is still sensitive to training budget, so the architecture is not capacity-capped yet
- Failure cases:
  - variance rises back above the 5 percent threshold, which makes the longer-training setting unsuitable as the promoted tuned baseline

### Analysis
- Do results match expectations? yes
- Confirmed cause:
  - graph is still optimization-sensitive; once training is extended, batch-size stabilization alone is no longer sufficient to keep seed variance controlled
- Decision:
  - freeze `hidden_dim=32, epochs=80, lr=0.01, batch_size=8` as the Stage 2 graph candidate
  - freeze `C=16.0, class_weight=balanced` as the Stage 2 logistic anchor
  - stop Stage 2 here because further budget is likely lower value than starting Stage 3

### Next Steps
- [x] Decide whether to stop logistic tuning here and promote this config as the Stage 2 final tuned logistic
- [x] Freeze the strongest stable graph candidate for the comparison table
- [x] Close Stage 2 and move to Stage 3 proposed-method work
