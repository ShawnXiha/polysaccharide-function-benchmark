# Experimentation Memory

Last Updated: 2026-03-29
Total Cycles: 26

## Data Processing Strategies

### KG Meta-Path Feature Blocks For DoLPHiN

- **Category**: Data Processing
- **Context**: Masked `poly-function` link prediction on the DoLPHiN-derived polysaccharide KG
- **Strategy**: Build explicit relation-derived features from `organism`, `monosaccharide`, `glycosidic_bond`, and `publication` edges first; add `disease` features only as auxiliary side-information.
- **Evidence**: Cycle 1, Stages 1-4, especially `poly_function_link_prediction_clean.json` and `poly_function_link_prediction_with_disease_k25.json`
- **Generality**: Domain-specific
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Local kNN voting over KG meta-path features
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Build Biology-Facing Case Studies From Edge Records Before Writing Narratives

- **Category**: Data Processing
- **Context**: Preparing biology-facing manuscript case studies for KG retrieval and ontology experiments
- **Strategy**: Do not hand-pick examples directly from headline tables. First export or collect edge-level evaluation records, then enrich them with local KG evidence previews (`organism`, `monosaccharide`, `bond`, `disease`, `DOI`) and only then shortlist cases by category (`clean_success`, `ontology_rescue`, `persistent_failure`).
- **Evidence**: Cycle 26; candidate mining over the clean masked-link run and 16-seed ontology stability runs produced a structured pool with `743` clean successes, `1` ontology rescue, `46` ontology failures, and `172` clean failures, enabling a principled shortlist of four manuscript-facing cases
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Validate Tail Claims With Paired Edge-Level Statistics, Not Seed Means Alone
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Merge Category-Specific Evaluation Rows Before Drawing Manuscript Case Figures

- **Category**: Data Processing
- **Context**: Plotting biology-facing case-study figures when one manuscript case needs values from different evaluation categories or protocols
- **Strategy**: Do not key figure inputs only by entity ID if the same sample appears in multiple candidate categories. Build the visualization row explicitly from category-aware records and merge the needed metrics first, then draw the local subgraph and ranking callout from the merged object.
- **Evidence**: Cycle 27; the persistent failure figure initially lost `clean` and `disease-aware` ranks because the plotting script keyed only by `poly_id`. Switching to `(category, poly_id)` lookup and merging `clean_failure` with `ontology_failure` restored the correct values (`clean rank = 12`, `disease-aware rank = 19`, `ontology rank = 19`) in the final figure
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Build Biology-Facing Case Studies From Edge Records Before Writing Narratives
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

## Model Training Strategies

### Standard Linear One-Vs-Rest Baselines Are Mandatory On Sparse Typed KGs

- **Category**: Model Training
- **Context**: Clean multi-label function prediction on the DoLPHiN typed KG under a unified `train/valid/test` split
- **Strategy**: Before claiming anything about graph neural baselines, run strong shallow baselines on explicit KG feature matrices. In this setting, concatenate exported `poly_x` with sparse meta-path incidence features and use a regularized one-vs-rest logistic model with validation threshold tuning.
- **Evidence**: Cycle 25; `poly_x + meta_path + logreg` reached test macro-F1 `0.3603`, outperforming `meta_path + logreg` (`0.3465`), `meta_path + mlp` (`0.3065`), and all current hetero / hybrid GNN variants (`0.0347-0.0476`)
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: KG Meta-Path Feature Blocks For DoLPHiN
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Validate Tail Claims With Paired Edge-Level Statistics, Not Seed Means Alone

- **Category**: Model Training
- **Context**: Tail-sensitive ontology variants on multi-label KG retrieval where aggregate metrics change only weakly
- **Strategy**: Export paired edge-level records for baseline and proposed method on identical splits, then test tail deltas with paired statistics. Combine edge-level significance with seed-level consistency instead of relying only on a few seed averages.
- **Evidence**: Cycle 24; across `16` paired seeds and `16000` masked edges, the ontology variant kept overall filtered `Hits@3` flat (`0.9088 -> 0.9085`) while improving tail micro filtered `Hits@3` from `0.0552` to `0.1021`, with one-sided paired McNemar `p=0.03125` and tail filtered `MRR` permutation `p=0.0002499`
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Use Filtered Ranking For Multi-Label KG Edge Recovery
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Local kNN Voting Beats Global Centroids

- **Category**: Model Training
- **Context**: Sparse multi-label KG retrieval where each function class is heterogeneous
- **Strategy**: Prefer local kNN label propagation over global class-centroid scoring. Tune `top_k` in a small local range instead of expanding to large neighborhoods.
- **Evidence**: Cycle 1, Stage 1 Attempt 3 and Stage 2 Attempts 1-4; clean `meta_path_knn` reached `Hits@3=0.655`, centroid only `0.014`
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Disease-aware kNN side-information boost
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Re-Tune Neighborhood Size After Adding New Relation Families

- **Category**: Model Training
- **Context**: Same scorer, but feature space changes due to new KG relation blocks
- **Strategy**: When adding a new relation family such as disease nodes, re-tune `top_k`; the optimal neighborhood size can shift.
- **Evidence**: Cycle 1, Stage 3 Attempt 2; disease-aware kNN improved from `Hits@3=0.801` at `top_k=50` to `0.814` at `top_k=25`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Local kNN voting beats global centroids
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Use Filtered Ranking For Multi-Label KG Edge Recovery

- **Category**: Model Training
- **Context**: Masked link prediction where one source node can connect to multiple true target labels
- **Strategy**: Report filtered ranking as the primary protocol. Remove the same source node's other true targets from the candidate list before computing rank-based retrieval metrics.
- **Evidence**: Cycle 2; clean kNN improved from raw `MRR=0.4806`, `Hits@3=0.655` to filtered `MRR=0.6168`, `Hits@3=0.743`, and disease-aware kNN improved from raw `MRR=0.6097`, `Hits@3=0.814` to filtered `MRR=0.8119`, `Hits@3=0.875`
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Local kNN Voting Beats Global Centroids
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Rare-Label Neighbor Expansion Is A Tradeoff, Not A Free Gain

- **Category**: Model Training
- **Context**: Long-tail improvement on filtered multi-label KG retrieval
- **Strategy**: Treat rare-label neighbor expansion as a targeted tradeoff mechanism. It can improve a few tail or mid-support labels, but should not replace the default scorer unless the long-tail gain is large enough to offset head-label degradation.
- **Evidence**: Cycle 3; clean tail filtered `Hits@3` improved from `0.167` to `0.333` under conservative expansion, but overall filtered `Hits@3` still fell from `0.743` to `0.740`. More aggressive expansion dropped clean filtered `Hits@3` to `0.703` and disease-aware filtered `Hits@3` to `0.867`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Use Filtered Ranking For Multi-Label KG Edge Recovery
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Source-Constrained Reranking Improves Precision Without Broadening Search

- **Category**: Model Training
- **Context**: Two-stage KG retrieval where a strong base scorer already provides a plausible short candidate list
- **Strategy**: Apply source-constrained reranking only to the top candidate labels. Use exact shared-source evidence as a selective bonus instead of modifying the full neighborhood search.
- **Evidence**: Cycle 4; clean filtered `Hits@3` improved from `0.743` to `0.768`, and disease-aware filtered `Hits@3` improved from `0.875` to `0.886` with `source_rerank_top_n=10`, `source_rerank_weight=1.0`
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Use Filtered Ranking For Multi-Label KG Edge Recovery
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Source-Cluster Backoff Helps Clean Source-Aware Retrieval

- **Category**: Model Training
- **Context**: Source-aware KG reranking when exact organism overlap is informative but sometimes sparse
- **Strategy**: Use `organism -> genus -> kingdom` backoff as a selective rerank bonus only in the clean setting. It can recover soft source signal without changing the base candidate generator.
- **Evidence**: Cycle 5; clean filtered `Hits@3` improved from `0.743` with plain kNN and `0.768` with exact source rerank to `0.773` with source-cluster backoff
- **Generality**: Domain-specific
- **Confidence**: Single observation
- **Related Entries**: Source-Constrained Reranking Improves Precision Without Broadening Search
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Label-Specific Backoff Preserves Head Performance While Helping Tail Labels

- **Category**: Model Training
- **Context**: Long-tail KG retrieval where global source-aware reranking helps precision but fails to recover rare labels
- **Strategy**: Apply source-aware backoff only to low-support labels inside the top candidate set. Normalize the backoff signal by the label's own support mass so the bonus stays label-specific instead of globally distorting the score scale.
- **Evidence**: Cycle 7; clean filtered `Hits@3` improved from `0.743` to `0.744`, while tail micro filtered `Hits@3` improved from `0.167` to `0.333` and head micro filtered `Hits@3` stayed `0.762`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Source-Cluster Backoff Helps Clean Source-Aware Retrieval
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Disease-Label Compatibility Priors Improve Disease-Aware Calibration

- **Category**: Model Training
- **Context**: Disease-aware KG retrieval where query nodes already carry disease semantics
- **Strategy**: Learn a smoothed `P(function | disease)` prior from the training graph and use it to rerank only the top disease-aware candidates. This improves calibration without changing the candidate space.
- **Evidence**: Cycle 9; disease-aware filtered `Hits@3` improved from `0.875` to `0.878`, while head micro filtered `Hits@3` improved from `0.899` to `0.903`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Auxiliary Disease Features As Upper-Bound Semantics
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Contrastive Prototype Refinement Is Safer Than Absolute Prototype Bonuses

- **Category**: Model Training
- **Context**: Label-level reranking on top of a strong disease-aware retrieval baseline
- **Strategy**: If adding a label prototype bonus, compare the local prototype match against the global centroid match and only reward positive gain. Absolute prototype similarity tends to re-reward already strong labels and destabilize the ranking.
- **Evidence**: Cycle 11; absolute prototype scoring degraded filtered `Hits@3` to `0.876` and `0.858`, while the contrastive variant recovered stability to `0.877` with filtered `MRR` up to `0.8191`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Diagnose Prototype Collapse By Holding Features Fixed
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Mild Frequency Adjustment Can Improve Disease-Prior Calibration

- **Category**: Model Training
- **Context**: Disease-aware retrieval where disease-function compatibility priors are helpful but still biased toward frequent labels
- **Strategy**: Apply a mild frequency-normalized penalty to the disease prior bonus inside the rerank window. Use conservative divisive adjustment rather than aggressive subtraction.
- **Evidence**: Cycle 12; `divide` mode with `top_n=20`, `weight=1.0`, `strength=0.5` improved filtered `Hits@3` from `0.878` to `0.880` and filtered `MRR` from `0.8186` to `0.8191`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Disease-Label Compatibility Priors Improve Disease-Aware Calibration
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Integrated Support Expansion Can Improve Mid-Support Retrieval

- **Category**: Model Training
- **Context**: Disease-aware multi-label KG retrieval where rerank-only methods fail to change candidate support
- **Strategy**: Merge support-aware expansion directly into the base kNN scorer instead of attaching it as a later bonus. Use a modest extension radius and low decay so extra support influences shortlist formation without overwhelming the core nearest-neighbor signal.
- **Evidence**: Cycle 14; integrated support-aware kNN plus frequency-adjusted disease prior improved filtered `Hits@3` from `0.880` to `0.881`, filtered `MRR` from `0.8191` to `0.8193`, and mid micro filtered `Hits@3` from `0.400` to `0.425`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Candidate Expansion Must Change The Downstream Shortlist To Matter
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Disease-Conditioned Base Voting Is Stronger Than Post-Hoc Disease Reranking

- **Category**: Model Training
- **Context**: Disease-aware multi-label KG retrieval where disease semantics are highly informative for function prediction
- **Strategy**: Inject disease-conditioned compatibility directly into neighbor voting rather than only adding it during reranking. Reward labels whose `P(function | disease)` is above the uniform prior, and keep a cap on the boost to avoid uncontrolled amplification.
- **Evidence**: Cycle 16; disease-conditioned base vote plus frequency-adjusted disease prior improved filtered `Hits@3` from `0.880` to `0.902` in a conservative setting and to `0.912` in a stronger setting, with filtered `MRR` reaching `0.8496`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Mild Frequency Adjustment Can Improve Disease-Prior Calibration
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Tail Evidence Channels Need New Information, Not Just Stronger Disease Use

- **Category**: Model Training
- **Context**: Disease-aware retrieval after moving disease semantics into the base vote
- **Strategy**: Once disease-conditioned base voting saturates overall performance, treat further gains as upper-bound improvements rather than tail evidence. Tail-oriented work should add new information channels instead of intensifying the same disease signal.
- **Evidence**: Cycle 17; stronger disease-conditioned voting raised filtered `Hits@3` to `0.912` and filtered `MRR` to `0.8496`, but tail micro filtered `Hits@3` remained `0.167`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Disease-Conditioned Base Voting Is Stronger Than Post-Hoc Disease Reranking
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

## Architecture Strategies

### Auxiliary Disease Features As Upper-Bound Semantics

- **Category**: Architecture
- **Context**: DoLPHiN KG tasks where disease nodes are strongly coupled to downstream function labels
- **Strategy**: Separate clean structure-only settings from disease-augmented settings. Use disease features to estimate an upper bound, not as the main claimed mechanism.
- **Evidence**: Cycle 1, Stage 3; `Hits@3` improved from clean tuned `0.655` to disease-aware `0.814`
- **Generality**: Domain-specific
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: KG Meta-Path Feature Blocks For DoLPHiN
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Full Hetero GNN Matching No-Message Ablations Signals A Representation Bottleneck

- **Category**: Architecture
- **Context**: Clean node-label prediction on the DoLPHiN KG where current hetero message passing performs poorly
- **Strategy**: Compare the full hetero GNN against a no-message variant on the same node features and split before redesigning the optimizer. If `full ≈ no-message`, the bottleneck is the graph evidence or node semantics, not the absence of another training trick.
- **Evidence**: Cycle 25; over seeds `42 / 7 / 123`, base `hetero_sage` averaged macro-F1 `0.0443`, while `hetero_no_message` averaged `0.0423`. On the hybrid graph, `hetero_sage` (`0.0347`) also failed to beat `hybrid no-message` (`0.0386`)
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Standard Linear One-Vs-Rest Baselines Are Mandatory On Sparse Typed KGs
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

## Debugging Strategies

### Diagnose Message Passing Value With Full Vs No-Message Paired Ablations

- **Category**: Debugging
- **Context**: Heterogeneous GNNs underperform strong shallow baselines and it is unclear whether the issue is optimization or graph utility
- **Strategy**: Hold the training loop fixed and only remove message passing. If the no-message ablation stays near the full model across multiple seeds, stop tuning depth, learning rate, or dropout and redirect effort toward graph evidence design.
- **Evidence**: Cycle 25; on the base graph, `hetero_sage` and `hetero_no_message` stayed within `~0.002` macro-F1 on average, and both remained far below the shallow linear baseline (`0.3603`)
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Full Hetero GNN Matching No-Message Ablations Signals A Representation Bottleneck
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Increase Paired Seed Count Before Re-Designing An Underpowered Tail Experiment

- **Category**: Debugging
- **Context**: Tail binary hit metrics show a positive direction but two-sided significance remains just above threshold
- **Strategy**: Before changing the method, inspect discordant paired cases. If all discordant cases favor the proposed method and no regression is observed, increase the number of paired seeds to raise statistical power rather than re-designing the scorer prematurely.
- **Evidence**: Cycle 24; the first `8` paired seeds gave tail micro filtered `Hits@3` delta `+0.0781` but two-sided McNemar `p=0.125`. Expanding to `16` paired seeds yielded one-sided McNemar `p=0.03125` and confirmed no tail regression across seeds
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Aggregate Metrics Can Hide Head-Tail Failure Gaps
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Diagnose Prototype Collapse By Holding Features Fixed

- **Category**: Debugging
- **Context**: A scoring layer fails badly and it is unclear whether the issue is the features or the scorer
- **Strategy**: Keep the feature extractor fixed and replace only the scorer. If local voting works while centroids fail, the bottleneck is the scorer, not the representation.
- **Evidence**: Cycle 1, diagnosis file `diagnosis_centroid_failure.md`; same features with kNN sharply outperformed centroid scoring
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Local kNN voting beats global centroids
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Frequency Reweighting Can Remove Useful Local Signal

- **Category**: Debugging
- **Context**: Neighbor-based retrieval on label-skewed KGs
- **Strategy**: Do not assume `idf`-style label reweighting helps. First test whether local label prevalence is genuine signal; if so, inverse-frequency weighting may reduce retrieval quality.
- **Evidence**: Cycle 1, Stage 4 Attempts 1-2; `idf` weighting reduced `Hits@3` from `0.651` to `0.558` in clean mode and from `0.814` to `0.780` with disease features
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Local kNN voting beats global centroids
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Aggregate Metrics Can Hide Head-Tail Failure Gaps

- **Category**: Debugging
- **Context**: Retrieval metrics look strong overall but label frequency is highly skewed
- **Strategy**: Add per-label evaluation and support-stratified summaries before concluding the method works broadly. Inspect head/mid/tail strata separately.
- **Evidence**: Cycle 2 filtered kNN evaluation; clean micro `Hits@3` was `0.762` for head labels, `0.375` for mid labels, and only `0.167` for tail labels. Disease-aware evaluation showed the same pattern: `0.899 / 0.400 / 0.167`
- **Generality**: Broadly applicable
- **Confidence**: Confirmed (1 cycle)
- **Related Entries**: Use Filtered Ranking For Multi-Label KG Edge Recovery
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Long-Tail Expansion Can Amplify Structural Noise

- **Category**: Debugging
- **Context**: Enlarging neighborhoods for low-support labels in a heterogeneous KG retrieval task
- **Strategy**: If farther neighbors help only isolated rare examples while degrading stable head-label ranking, interpret the issue as structural noise amplification rather than insufficient search radius.
- **Evidence**: Cycle 3 diagnosis. Conservative rare expansion improved clean tail filtered `Hits@3`, but aggressive expansion degraded head micro `Hits@3` from `0.762` to `0.719` in clean mode and from `0.899` to `0.888` in disease-aware mode
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Aggregate Metrics Can Hide Head-Tail Failure Gaps
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Missing Source Support Limits Tail Gains

- **Category**: Debugging
- **Context**: Source-aware reranking improves aggregate quality but the rarest labels still do not move
- **Strategy**: When exact source-consistent reranking fails to improve tail labels, interpret the bottleneck as sparse support rather than weak rerank weight. The next method should add a source backoff or candidate-generation step rather than simply strengthening rerank pressure.
- **Evidence**: Cycle 4; source-constrained reranking improved clean and disease-aware overall filtered `Hits@3`, but tail filtered `Hits@3` stayed `0.167` in both settings
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Source-Constrained Reranking Improves Precision Without Broadening Search
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Genus Or Kingdom Backoff Does Not Solve Tail Support

- **Category**: Debugging
- **Context**: Source-cluster backoff improves clean aggregate retrieval but rare labels remain unchanged
- **Strategy**: If source backoff only improves head-label precision while tail filtered `Hits@3` stays fixed, treat the problem as missing candidate support rather than insufficient source granularity. Move to candidate-generation or label-specific mechanisms.
- **Evidence**: Cycle 5; clean source-cluster backoff improved filtered `Hits@3` to `0.773`, but tail filtered `Hits@3` remained `0.167`. Disease-aware source-cluster backoff also left tail filtered `Hits@3` unchanged and underperformed exact source rerank overall
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Missing Source Support Limits Tail Gains
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Tail Candidate Generation Needs Calibration And Support

- **Category**: Debugging
- **Context**: Post-hoc long-tail candidate injection on top of a strong base retrieval model
- **Strategy**: Treat candidate generation as a two-part problem: selection and calibration. If tail candidates are activated too strongly, they displace reliable head labels; if activation is tightly source-gated, the method becomes a no-op. Do not keep tuning a rerank-only generator once both failure modes appear.
- **Evidence**: Cycle 6; the first tail-candidate generator improved tail micro filtered `Hits@3` from `0.167` to `0.333` but dropped overall filtered `Hits@3` from `0.743` to `0.653`. Tuned versions restored overall performance but also removed the tail gain
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Long-Tail Expansion Can Amplify Structural Noise
- **Date Added**: 2026-03-27
- **Last Updated**: 2026-03-27

### Side-Information Saturation Can Nullify Source-Aware Tail Fixes

- **Category**: Debugging
- **Context**: Extending a clean-setting long-tail improvement into a disease-aware retrieval setup
- **Strategy**: Do not assume a method that helps the clean setting will help the side-information setting. When disease or other auxiliary semantics already dominate the ranking, source-aware backoff may have zero marginal value and should be treated as saturated rather than under-tuned.
- **Evidence**: Cycle 8; disease-aware label-specific backoff with weight `0.5` left filtered `Hits@3` unchanged at `0.875`, and weight `1.0` reduced it to `0.873` while tail micro filtered `Hits@3` remained `0.167`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Auxiliary Disease Features As Upper-Bound Semantics
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Compatibility Priors Can Improve Calibration Without Fixing Tail Labels

- **Category**: Debugging
- **Context**: Disease-aware retrieval gains overall performance but the rarest labels remain unchanged
- **Strategy**: Distinguish ranking calibration gains from long-tail recovery. If a disease-function prior improves overall and head metrics but leaves tail unchanged, treat it as a calibration success rather than a tail method.
- **Evidence**: Cycle 9; disease-aware compatibility priors improved filtered `Hits@3` from `0.875` to `0.878`, but tail micro filtered `Hits@3` stayed `0.167`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Disease-Label Compatibility Priors Improve Disease-Aware Calibration
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Over-Targeting Tail Priors Can Remove Calibration Gains Without Unlocking Tail

- **Category**: Debugging
- **Context**: Modifying a successful disease-aware compatibility prior so it only boosts low-support labels
- **Strategy**: Be careful when restricting a useful global prior to tail labels only. If the prior's main utility is calibration on plausible head and upper-mid labels, tail-only gating can remove that benefit while still failing to move true tail labels across the top-k boundary.
- **Evidence**: Cycle 10; tail-aware disease priors left disease-aware filtered `Hits@3` unchanged at `0.875`, slightly reduced filtered `MRR` from `0.8119` to about `0.8111`, and left tail micro filtered `Hits@3` unchanged at `0.167`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Compatibility Priors Can Improve Calibration Without Fixing Tail Labels
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Prototype Refinement Can Improve MRR Without Improving Tail Retrieval

- **Category**: Debugging
- **Context**: Disease-aware long-tail retrieval where label-level prototype reranking is added on top of a calibrated base scorer
- **Strategy**: Evaluate prototype refinement against the task's primary metric and stratified tail metrics, not only overall MRR. A small MRR gain can come entirely from head-label reordering while tail `Hits@3` remains unchanged.
- **Evidence**: Cycle 11; the best contrastive prototype setting reached filtered `MRR=0.8191` versus `0.8186` for the disease prior baseline, but filtered `Hits@3` stayed lower at `0.877` versus `0.878`, tail micro filtered `Hits@3` stayed `0.167`, and mid micro filtered `Hits@3` fell from `0.400` to `0.350`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Compatibility Priors Can Improve Calibration Without Fixing Tail Labels
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Frequency Adjustment Helps Calibration Before It Helps Tail

- **Category**: Debugging
- **Context**: Adding label-frequency correction to disease-aware compatibility priors
- **Strategy**: Treat frequency-adjusted priors first as calibration tools, not as direct tail-recovery methods. If mild adjustment improves overall filtered metrics while tail remains unchanged, the next step should target candidate support rather than stronger penalization.
- **Evidence**: Cycle 12; the best divisive adjustment improved filtered `Hits@3` to `0.880`, but tail micro filtered `Hits@3` stayed `0.167` and mid micro filtered `Hits@3` stayed `0.400`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Mild Frequency Adjustment Can Improve Disease-Prior Calibration
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Candidate Expansion Must Change The Downstream Shortlist To Matter

- **Category**: Debugging
- **Context**: Support-aware candidate generation inserted before a rerank stage in multi-label KG retrieval
- **Strategy**: Verify that candidate generation actually changes the labels entering the rerank window. If downstream metrics are identical across conservative and aggressive settings, the generator is functioning as a no-op and is not materially entering the retrieval pipeline.
- **Evidence**: Cycle 13; three support-aware candidate generation settings produced the same filtered `Hits@3` and stratified results as their paired frequency-adjusted disease-prior baseline, even when candidate activation and search radius were increased substantially
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Tail Candidate Generation Needs Calibration And Support
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Integrated Expansion Can Move Mid Labels Before It Moves Tail

- **Category**: Debugging
- **Context**: Directly integrating low-support expansion into the base scorer after a pre-rerank candidate generator failed as a no-op
- **Strategy**: When integrated expansion begins to help, check whether the first gain lands in mid-support labels rather than the hardest tail. Treat that as a real but limited success, and avoid escalating decay or extension radius too quickly because stronger settings may trade filtered `Hits@3` for only MRR gains.
- **Evidence**: Cycle 14; the conservative integrated scorer improved mid micro filtered `Hits@3` from `0.400` to `0.425`, while the stronger setting raised filtered `MRR` to `0.8228` but reduced filtered `Hits@3` to `0.879`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Integrated Support Expansion Can Improve Mid-Support Retrieval
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Tail-Only Expansion Can Still Miss The True Tail Bottleneck

- **Category**: Debugging
- **Context**: Restricting integrated support expansion to only the rarest labels inside the base kNN scorer
- **Strategy**: Do not assume that narrowing support expansion to tail labels will improve tail retrieval. If conservative settings are a no-op and aggressive settings only trade overall precision for MRR, the bottleneck is likely missing evidence density rather than insufficient targeting.
- **Evidence**: Cycle 15; explicit tail-support integration left tail micro filtered `Hits@3` unchanged at `0.167` in both tested settings. The conservative version matched baseline exactly, while the stronger version reduced filtered `Hits@3` from `0.880` to `0.878` and mid micro filtered `Hits@3` from `0.400` to `0.375`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Integrated Expansion Can Move Mid Labels Before It Moves Tail
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Strong Disease Smoothing Improves Overall Retrieval Before It Improves Tail

- **Category**: Debugging
- **Context**: Moving disease-conditioned semantics from a rerank stage into the base neighbor vote
- **Strategy**: Treat large gains from disease-conditioned base voting as stronger exploitation of side-information, not as long-tail recovery. Check tail strata explicitly before concluding the method addresses rare labels.
- **Evidence**: Cycle 16; the stronger disease-conditioned vote raised filtered `Hits@3` to `0.912` and mid micro filtered `Hits@3` to `0.450`, but tail micro filtered `Hits@3` still stayed `0.167`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Disease-Conditioned Base Voting Is Stronger Than Post-Hoc Disease Reranking
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Large Upper-Bound Gains Can Mask Unchanged Tail Failure

- **Category**: Debugging
- **Context**: A side-information-heavy method produces strong overall improvements in a long-tail setting
- **Strategy**: Always pair strong overall gains with explicit tail checks. If tail strata remain flat, record the method as a stronger upper bound rather than a solution to the long-tail problem.
- **Evidence**: Cycle 17; disease-conditioned base vote lifted filtered `Hits@3` from `0.880` to `0.912`, yet tail micro filtered `Hits@3` still remained `0.167`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Tail Evidence Channels Need New Information, Not Just Stronger Disease Use
- **Date Added**: 2026-03-28
- **Last Updated**: 2026-03-28

### Weak Post-Hoc Tail Bonuses And Strong Post-Hoc Tail Bonuses Can Fail Differently

- **Category**: Debugging
- **Context**: A new tail-specific rerank signal appears promising conceptually but does not improve long-tail metrics
- **Strategy**: Test both a conservative and a strong setting before spending more tuning budget. If the conservative setting is a no-op and the strong setting degrades overall ranking while leaving tail unchanged, classify the issue as a pipeline-stage mismatch rather than insufficient optimization.
- **Evidence**: Cycle 18 structural signatures. Conservative clean run changed filtered `Hits@3` only `0.724 -> 0.721`, and conservative disease-aware upper-bound changed `0.912 -> 0.911`. Stronger settings degraded clean filtered `Hits@3` to `0.623` and disease-aware filtered `Hits@3` to `0.864`, with no tail gain.
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Tail Evidence Channels Need New Information, Not Just Stronger Disease Use
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Tail Structural Signatures Need Candidate-Level Activation, Not Post-Hoc Bonus Injection

- **Category**: Debugging
- **Context**: Tail recovery attempts that use enriched organism/monosaccharide/bond motifs as an extra rerank signal on top of a strong kNN retrieval baseline
- **Strategy**: Do not add structural signatures as a generic post-hoc score bonus. In this task, weak bonuses are effectively no-ops, while strong bonuses distort the shortlist and degrade mid/head retrieval without improving tail hits. If structural tail cues are revisited, they should enter candidate generation or base voting directly.
- **Evidence**: Cycle 18; clean conservative structural signatures changed filtered `Hits@3` only `0.724 -> 0.721`, while the stronger setting dropped it to `0.623`. In disease-aware mode, the current best baseline stayed at filtered `Hits@3=0.912`, but adding structural signatures reduced it to `0.911` conservatively and `0.864` aggressively. Tail micro filtered `Hits@3` stayed `0.1667` throughout disease-aware evaluation.
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Weak Post-Hoc Tail Bonuses And Strong Post-Hoc Tail Bonuses Can Fail Differently
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Structural Candidate Generation Still Needs A Stronger Evidence Source

- **Category**: Debugging
- **Context**: Moving structural-tail cues from post-hoc reranking into candidate generation before final ranking
- **Strategy**: Do not assume that earlier injection alone will fix a weak tail signal. If conservative candidate generation is still a no-op and stronger activation only hurts mid/head strata, the bottleneck is the evidence quality itself rather than the pipeline location.
- **Evidence**: Cycle 19; clean structural candidate generation stayed at filtered `Hits@3=0.724` conservatively and fell to `0.715` with stronger activation. Disease-aware upper-bound stayed at `0.912 -> 0.911` conservatively and dropped to `0.892` strongly. Tail micro filtered `Hits@3` remained `0.1667` in disease-aware evaluation.
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Tail Structural Signatures Need Candidate-Level Activation, Not Post-Hoc Bonus Injection
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Pairwise Subgraph Motifs Are Cleaner Than Flat Signatures But Still Not Sufficient

- **Category**: Debugging
- **Context**: Replacing flat structural-signature overlap with pairwise subgraph-motif overlap for tail candidate generation
- **Strategy**: Pairwise motifs can reduce arbitrary noise, but they are not automatically a useful tail evidence source. If conservative motif activation remains a no-op and stronger activation still degrades mid/head retrieval while tail stays flat, stop iterating on the same motif family.
- **Evidence**: Cycle 20; clean subgraph motifs stayed at filtered `Hits@3=0.724` conservatively and fell to `0.715` strongly. Disease-aware upper-bound stayed at `0.912 -> 0.911` conservatively and dropped to `0.897` strongly. Tail micro filtered `Hits@3` remained `0.1667`.
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Structural Candidate Generation Still Needs A Stronger Evidence Source
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Taxonomy Conditioning Can Stabilize Structural Motifs Without Unlocking Tail

- **Category**: Debugging
- **Context**: Conditioning structural motif support on matching organism/genus/kingdom buckets before candidate generation
- **Strategy**: Taxonomy conditioning is useful as a denoising check, but if it only produces a stable no-op, do not interpret that as latent tail potential. It means the conditioned structural evidence is cleaner, yet still too weak to move candidates across the top-k boundary.
- **Evidence**: Cycle 21; clean taxonomy-conditioned motifs stayed at filtered `Hits@3=0.724` in both conservative and stronger settings, while disease-aware upper-bound remained `0.912` in both settings with tail micro filtered `Hits@3=0.1667` unchanged.
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Pairwise Subgraph Motifs Are Cleaner Than Flat Signatures But Still Not Sufficient
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Coarse Function Hierarchies Can Behave Like Smoothing, Not New Evidence

- **Category**: Debugging
- **Context**: Adding an external ontology/hierarchy over function labels as family-level candidate support in multi-label KG retrieval
- **Strategy**: Before treating ontology/hierarchy as a new evidence channel, verify that it contributes finer discrimination than the current scorer. If conservative hierarchy support is a no-op and stronger activation harms tail, mid, and head retrieval, the hierarchy is too coarse and is functioning only as smoothing.
- **Evidence**: Cycle 22; clean hierarchy support stayed at filtered `Hits@3=0.724` conservatively and dropped to `0.713` strongly. Disease-aware upper-bound changed from `0.912` to `0.911` conservatively and `0.889` strongly, while tail micro filtered `Hits@3` went from `0.1667` to `0.1667` and then `0.000`.
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Taxonomy Conditioning Can Stabilize Structural Motifs Without Unlocking Tail
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

### Confidence-Gated Parent Child Ontology Propagation Preserves Tail Gains

- **Category**: Model Training
- **Context**: Ontology-enhanced multi-label KG retrieval after family-bonus and coarse graph-native hierarchy variants failed or became no-ops
- **Strategy**: Encode ontology as parent/child edges, propagate support through parent-linked sibling families inside the base scorer, and gate propagation by confidence so only coherent family evidence is allowed to influence low-support labels. Tune the gate before tuning ontology size.
- **Evidence**: Cycle 23; the confidence-gated parent/child variant matched the disease-aware baseline on filtered `Hits@3=0.912`, slightly improved filtered `Hits@5` from `0.938` to `0.939`, and doubled tail micro filtered `Hits@3` from `0.1667` to `0.3333`
- **Generality**: Broadly applicable
- **Confidence**: Single observation
- **Related Entries**: Disease-Conditioned Base Voting Is Stronger Than Post-Hoc Disease Reranking
- **Date Added**: 2026-03-29
- **Last Updated**: 2026-03-29

## Archive

*Pruned entries are moved here to preserve historical record.*
