# Poly-core v1 论文草稿

## Title Options

1. `A Benchmark and Polysaccharide-Specific Representation for Multi-label Structure-Function Prediction of Natural Polysaccharides`
2. `Benchmarking Natural Polysaccharide Structure-Function Prediction with a Polysaccharide-Specific Core Representation`
3. `From Glycan-Centric Baselines to Polysaccharide-Specific Representation Learning for Natural Polysaccharide Function Prediction`

## Recommended Title

`A Benchmark and Polysaccharide-Specific Core Representation for Multi-label Structure-Function Prediction of Natural Polysaccharides`

## Abstract

Natural polysaccharides are increasingly studied for antioxidant, immunomodulatory, antitumor, and metabolic regulatory activities, yet machine learning for polysaccharide structure-function prediction remains underdeveloped. A major reason is that existing carbohydrate machine learning tools are largely glycan-centric, whereas natural polysaccharides are typically described by incomplete but heterogeneous structural evidence such as monosaccharide composition, linkage patterns, branching information, and molecular-weight ranges. We therefore build a practical benchmark for supervised multi-label function prediction from public polysaccharide resources and examine which structural signals are actually useful. Starting from public-site DoLPHiN ingestion and a filtered benchmark of 4,121 records with 18 function labels, we reproduce a range of classical, sequence, and graph baselines and establish a tuned logistic baseline as a strong anchor. We then test a family of structure-aware extensions and find that the effective gain comes not from weak evidence proxies, but from a compact polysaccharide-specific representation that explicitly encodes molecular-weight buckets, branching availability, and residue-set composition. This `poly-core v1` representation improves macro-F1 from 0.2610 for the tuned logistic baseline to 0.2678 under a fixed random-split protocol, while remaining deterministic across seeds. Controlled ablations show that molecular-weight and residue features are the dominant contributors, branching provides a smaller but consistent gain, and several superficially plausible features are neutral or harmful. These results establish a reproducible benchmark, clarify which representation components matter for current polysaccharide prediction, and provide a concrete starting point for future evidence-aligned and cross-source polysaccharide learning.

## 1. Introduction

Natural polysaccharides are multifunctional macromolecules that participate in antioxidant, immunomodulatory, antitumor, anti-inflammatory, and metabolic regulation processes. The recent release of domain resources such as DoLPHiN has made it possible to aggregate structural descriptors and reported health functions for thousands of natural polysaccharides, creating a realistic opportunity for data-driven prediction rather than purely narrative structure-function analysis. However, this opportunity is still technically immature. In contrast to proteins or small molecules, polysaccharides are rarely represented by a single clean sequence or graph. Instead, available descriptions are often heterogeneous and partially incomplete, combining monosaccharide composition, glycosidic linkages, branching descriptions, modifications, organism source, and approximate molecular-weight ranges.

This representation mismatch creates a practical challenge for machine learning. Existing carbohydrate machine learning has made real progress on glycans, including graph-based modeling and reusable software ecosystems, but these tools are largely built around glycan settings where sequence or graph structure is the primary object of analysis. Natural polysaccharide records are structurally broader and noisier. A direct transfer of glycan-centric representations therefore risks missing the signals that are most accessible in current polysaccharide databases. At the same time, claiming a large end-to-end foundation-model solution at this stage would be premature because benchmark construction, reproducible baselines, and component-level signal validation are still incomplete.

This paper takes a narrower and more defensible position. We first construct a practical supervised benchmark from public polysaccharide resources, starting with full public-site ingestion of DoLPHiN and using CSDB only as an engineering stress-test source rather than as an equal supervised source. We then reproduce a set of classical, sequence, and graph baselines under fixed evaluation protocols, and identify a tuned logistic model as a strong and stable baseline. Our central insight is that the first reliable gain does not come from a broad evidence-aware narrative, because the current supervised records do not yet contain sufficient evidence-level variation, but from a compact polysaccharide-specific structural representation that matches how natural polysaccharides are actually reported.

Our contributions are threefold. First, we release a reproducible benchmark construction and baseline pipeline for multi-label polysaccharide structure-function prediction. Second, we show that a compact polysaccharide-specific representation improves over a tuned glycan-style sparse baseline, and we quantify this gain under controlled evaluation. Third, we use Stage 4 ablations to identify which structural components truly matter, showing that molecular-weight and residue-set features are dominant, branching contributes a smaller positive effect, and several intuitively plausible features are weak or harmful. We deliberately limit our claim scope to current single-source supervised prediction and do not overclaim cross-source biological generalization, because the currently ingested CSDB slice is not label-aligned with the main task.

## 2. Method

### 2.1 Problem Setup and Overview

Given a natural polysaccharide record with structural descriptors and metadata, our goal is to predict a set of functional labels from a fixed label vocabulary. Each record is represented by a canonical textual description together with fields such as monomer composition, linkage, branching, modification, molecular weight or molecular-weight range, and organism source. The target is a multi-label set over 18 retained biological function categories.

Our method development proceeds in two steps. We first establish a strong sparse baseline using count-vectorized feature text and one-vs-rest logistic regression. We then refine that baseline with a polysaccharide-specific structural representation. The final model, `poly-core v1`, augments the baseline text with only three supported feature families: molecular-weight buckets, branching-presence signals, and residue-set tokens derived from composition and linkage descriptions. Figure 1 should summarize this pipeline from raw database ingestion through benchmark filtering, baseline tuning, structure-aware representation design, and final ablation-backed method selection.

### 2.2 Benchmark Construction

The benchmark is built from public-site ingestion of DoLPHiN and a downstream filtering process designed to make the supervised task reproducible and interpretable. We first crawl and normalize DoLPHiN records into a unified schema, then apply label normalization to map raw function strings into canonical labels. To obtain a stable supervised benchmark, we remove `unknown` labels, retain only DoLPHiN as the supervision source, and keep only labels with global frequency of at least 20. The resulting benchmark contains 4,121 records and 18 function labels.

We intentionally separate benchmark construction from engineering stress testing. A second ingestion path from CSDB is useful for pipeline validation and future cross-source work, but the currently available CSDB slice is structurally rich and label-poor relative to the target supervised task. For that reason, CSDB is excluded from the main supervised benchmark and is not used to support the core empirical claim of this paper.

### 2.3 Tuned Sparse Baseline

Our baseline starts from a simple but strong sparse text representation. For each record, we concatenate the canonical representation, monomer composition, linkage, branching, modification, molecular-weight field, source database, and organism source into a lightweight feature string. This string is vectorized with a count-based vocabulary and fed into a one-vs-rest logistic regression classifier. Stage 2 tuning shows that this baseline is deterministic on the fixed split and benefits materially from reduced regularization and balanced class weighting. The strongest tuned configuration uses `C = 16.0`, `class_weight = balanced`, and serves as the main comparison anchor throughout the rest of the paper.

This baseline is intentionally conservative. It does not assume a fully trusted structural graph, and it avoids introducing extra neural complexity before the dataset and evaluation protocol are stable. Its role is not to be biologically complete, but to provide a strong and reproducible reference point for asking which additional structural features are actually worth keeping.

### 2.4 Polysaccharide-Specific Structural Representation

A remaining challenge is that the baseline treats many polysaccharide-specific structural cues as raw text rather than as normalized signals. Natural polysaccharide records repeatedly expose three high-value cues that are only weakly standardized in the raw text: coarse molecular-weight scale, whether branching information is available, and which major residue families are present. These cues are common enough to be extracted reliably, but structured enough to be lost when left entirely to generic tokenization.

To address this mismatch, we derive a compact token set from the existing structured fields. First, we parse molecular-weight fields into coarse buckets, such as low, medium, and high molecular-weight ranges. Second, we encode whether branching information is known or missing. Third, we derive residue-family tokens from monomer composition, linkage, branching, and canonical structural strings, producing markers such as glucose-, galactose-, arabinose-, mannose-, rhamnose-, xylose-, or uronic-acid-related residue presence, together with a simple residue-diversity signal. These tokens are appended to the baseline feature text and fed into the same tuned logistic classifier.

This design is deliberately modest. It does not attempt to reconstruct a complete carbohydrate graph from partially specified text, and it does not assume explicit evidence-level annotations that the current benchmark does not contain. Instead, it aims to encode the most reliable structural regularities that recur in public polysaccharide records and that can be defended by controlled ablation.

### 2.5 From Broad Poly Features to Poly-core v1

Our first Stage 3 representation was intentionally broader. It included additional evidence-proxy features, sample weighting by structural completeness, source-kingdom tokens, modification tokens, and coarse composition-count tokens. This broader version produced a small gain over the tuned logistic baseline, but Stage 4 ablation revealed that the useful signal was concentrated in a smaller subset of components.

The final method, `poly-core v1`, therefore keeps only the three ablation-supported families: molecular-weight buckets, branching tokens, and residue-set tokens. It removes weak evidence-proxy features, sample weighting, source-kingdom context, modification features, and composition-count tokens. This simplification is important for the paper's credibility. Rather than defending every engineered feature, we keep only the components whose contribution is supported by controlled experiments.

## 3. Experiments

### 3.1 Experimental Setup

The main supervised benchmark is `dataset_publishable_supervised_v1`, which contains 4,121 DoLPHiN-derived records and 18 canonical function labels. We evaluate under a fixed random split protocol and report macro-F1 as the primary metric, because the label distribution is highly imbalanced and the main objective is balanced multi-label function prediction. We also report exact match ratio as a stricter secondary metric.

We compare trivial, classical, sequence, and graph baselines. These include a majority predictor, untuned logistic regression, random forest, a lightweight sequence n-gram model, a lightweight transformer baseline implemented with native PyTorch modules, and a graph GCN baseline. After Stage 2 tuning, logistic regression with `C = 16.0` and balanced class weighting becomes the main anchor. All reported Stage 2, Stage 3, and Stage 4 results are deterministic across seeds `11/22/33`, so the comparison is not variance-limited.

### 3.2 Main Results

Table 1 reports the main comparison on the benchmark. Based on these results, we make four observations.

First, the benchmark is nontrivial. The majority baseline reaches only `0.0397` macro-F1, which confirms that the retained label space is not solved by prior frequency alone. Untuned logistic regression improves substantially to `0.1580`, showing that even a sparse textual view of structure already contains predictive signal.

Second, stronger baseline families help, but not uniformly. Random forest improves over the untuned logistic baseline, and the untuned graph GCN reaches `0.1941` macro-F1, indicating that richer model classes can exploit some structural regularities. However, the graph family remains less stable and less competitive than a properly tuned sparse baseline under the present benchmark conditions.

Third, tuning matters more than architectural novelty at the early stage of a new benchmark. Stage 2 increases the logistic anchor from `0.1580` to `0.2610` macro-F1, largely through weaker regularization and balanced class weighting. This result justifies using tuned logistic regression, rather than an untuned neural baseline, as the main reference point for method development.

Fourth, the final `poly-core v1` representation improves over the tuned anchor, reaching `0.2678` macro-F1. The absolute gain is modest, but it is reproducible, obtained under a fixed evaluation setup, and supported by later ablations. This is the right scale of claim for a first benchmark paper: not a sweeping leap, but a controlled and interpretable improvement.

### 3.3 Stage-wise Method Development

The experiment pipeline also clarifies how the final result emerged. Stage 1 established executable baselines across classical, sequence, and graph families. Stage 2 showed that tuned logistic regression was the strongest stable anchor. Stage 3 then tested whether a broad evidence-aware extension could improve over that anchor. It could not. The full evidence-aware variant underperformed the tuned logistic baseline, and its sub-variants revealed that weak evidence proxies and broad token augmentation were not the source of gain.

This failure analysis is important because it prevents overclaiming. The current supervised benchmark does not contain meaningful variation in explicit evidence-level annotation; all retained records carry `evidence_type = unknown`. Therefore, a strong evidence-aware claim would be technically weak and rhetorically risky. Instead, the effective gain comes from a representation that better matches the structural reporting style of natural polysaccharides.

### 3.4 Ablation Study

Table 3 summarizes the key ablations. Three observations are especially important.

First, molecular-weight buckets are the single strongest component. Removing them reduces macro-F1 from `0.2654` to `0.2461`, the largest drop among all ablations. This indicates that coarse molecular-weight scale is not a minor metadata field, but one of the strongest accessible predictors in the current benchmark.

Second, residue-set tokens are also critical. Removing them reduces macro-F1 to `0.2533`, which is the second largest drop. This confirms that coarse residue-family composition, even when derived from incomplete textual descriptions rather than full chemical graphs, contains important function-related signal.

Third, not every engineered feature helps. Removing branching tokens causes a smaller but still meaningful drop to `0.2598`, so branching remains part of the supported core representation. In contrast, removing modification or source-kingdom tokens produces only small changes, and removing `composition_terms_*` tokens actually improves performance. This last result is especially useful because it allows us to simplify the method rather than merely defend it. The final `poly-core v1` model keeps the supported positive components and removes the harmful or weak ones, improving from `0.2654` to `0.2678`.

### 3.5 Stress-test and Scope Boundary

We also built a merged `DoLPHiN + CSDB` pipeline and ran leave-one-source-out experiments as an engineering stress test. This pipeline is executable and useful for future work, but it should not be overinterpreted in the current paper. The present CSDB slice is structurally valuable but not label-aligned with the main supervised task, and training on it does not provide a fair biological test of function prediction generalization.

We therefore treat cross-source evaluation as a forward-looking stress-test result rather than as the main scientific evidence. This scope boundary is deliberate. It reduces overclaiming and keeps the paper centered on a benchmark claim that is genuinely supported by the available data.

## 4. Related Work

Our work is related to three lines of prior research: carbohydrate data resources, glycan machine learning, and practical glycobioinformatics tooling.

On the data side, DoLPHiN was recently introduced as a database focused on structural and functional properties of natural polysaccharides with health benefits, making it a natural starting point for supervised polysaccharide prediction tasks. CSDB, in contrast, is a broader curated carbohydrate resource and glycoinformatics platform with deep structural coverage for bacterial, fungal, and plant glycans. These resources are complementary, but they are not interchangeable for supervised function prediction. The present paper builds on both operationally, while explicitly recognizing that only the DoLPHiN-derived subset is currently suitable as the main supervision source for our task.

On the modeling side, glycan machine learning has already shown that carbohydrate-specific inductive biases matter. SweetNet demonstrated that graph convolutional neural networks are well matched to glycans because they directly model branching and nonlinear structure. More broadly, glycan-focused toolkits such as glycowork have lowered the barrier to data handling, motif analysis, and machine learning for carbohydrate data. Our work agrees with the central lesson of this literature, namely that generic sequence treatment is often inadequate. However, our setting differs in an important way: natural polysaccharide records are frequently incomplete, heterogeneous, and only partially graph-ready. This makes compact structured tokenization a pragmatic alternative to assuming a fully resolved glycan graph.

Relative to this literature, our contribution is not a new universal carbohydrate architecture. Instead, we contribute a benchmarked and ablation-supported answer to a narrower question: which structural signals are already reliable enough to improve multi-label function prediction for natural polysaccharides under current public-data conditions. This narrower scope is also what makes the result publishable. It turns a vague ambition about polysaccharide machine learning into a reproducible empirical target.

## 5. Conclusion

We presented a reproducible benchmark and modeling pipeline for multi-label structure-function prediction of natural polysaccharides. Starting from public DoLPHiN ingestion and a filtered supervised benchmark, we reproduced a range of baseline families, established a tuned logistic regression anchor, and showed that a compact polysaccharide-specific structural representation improves over that anchor. The final `poly-core v1` method reaches `0.2678` macro-F1 and is supported by controlled ablations showing that molecular-weight, residue-set, and branching features drive the gain.

The main scientific insight is narrower than our original Stage 3 hypothesis. On the current benchmark, the decisive improvement comes from polysaccharide-specific representation rather than from evidence-aware modeling. This is not a weakness of the paper; it is a cleaner result. It identifies which signals are useful now, and it prevents us from claiming more than the present data can support.

### Limitation

Our current benchmark is intentionally conservative and single-source in its main supervised setting. Although we implemented a merged `DoLPHiN + CSDB` pipeline, the currently ingested CSDB slice is not label-aligned enough to support a strong cross-source supervised claim. In addition, explicit evidence-level annotations are largely unavailable in the retained supervised data, which limits the strength of any current evidence-aware modeling result. Future work should therefore focus on better evidence annotation, stronger source alignment, and more chemically faithful cross-database structural normalization rather than on scaling model size alone.

## Paper Figures and Tables

### Main Figures

1. Figure 1: End-to-end pipeline from raw public ingestion to `poly_core_v1`
2. Figure 2: Main result comparison across baseline families and final method
3. Figure 3: Stage 4 ablation plot showing positive and negative component contributions

### Main Tables

1. Table 1: Main comparison on `publishable_supervised_v1`
2. Table 2: Stage progression from baseline reproduction to final method
3. Table 3: Component ablations

## References

1. Xin Y, Cao Y, Yang S, et al. DoLPHiN: a proposed architecture and technical implementation of a database of structural and functional properties of natural polysaccharides with health benefits. *Food Chemistry*. 2025;495(Pt 3):146534. DOI: `10.1016/j.foodchem.2025.146534`.
2. Toukach PV, Egorova KS. Source files of the Carbohydrate Structure Database: the way to sophisticated analysis of natural glycans. *Scientific Data*. 2022;9:131. DOI: `10.1038/s41597-022-01186-9`.
3. Burkholz R, Quackenbush J, Bojar D. Using graph convolutional neural networks to learn a representation for glycans. *Cell Reports*. 2021;35(11):109251. DOI: `10.1016/j.celrep.2021.109251`.
4. Thomès L, Burkholz R, Bojar D. Glycowork: A Python package for glycan data science and machine learning. *Glycobiology*. 2021;31(10):1240-1244. DOI: `10.1093/glycob/cwab067`.
