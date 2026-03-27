# 论文图表与 Caption 草案

## Figure 1

### Title

Pipeline from public polysaccharide ingestion to `poly-core v1`

### Caption

Overview of the proposed workflow. Public DoLPHiN records are crawled and normalized into a unified schema, filtered into the `publishable_supervised_v1` benchmark, and used to reproduce baseline families under fixed splits. A tuned logistic regression model serves as the main anchor. We then derive polysaccharide-specific structural tokens and refine them through controlled ablation, yielding the final `poly-core v1` representation.

## Table 1

### Title

Main comparison on `publishable_supervised_v1`

### Caption

Quantitative comparison on the main supervised benchmark. `Macro-F1` is the primary metric and `Exact Match` is the secondary metric. `poly-core v1` is the final ablation-refined method. The tuned logistic baseline is the strongest Stage 2 anchor.
The table should include trivial, classical, sequence, graph, and stronger simple sparse baselines to avoid selective reporting. The caption should also state that `Macro-F1` and `Exact Match` capture different failure modes in weakly supervised multi-label prediction, so they need not produce the same model ranking.

## Table 2

### Title

Stage-wise progression from benchmark reproduction to final method

### Caption

Performance progression across the four experiment stages. Stage 1 establishes executable baselines, Stage 2 identifies the strongest stable tuned baseline, Stage 3 introduces the first representation gain over the tuned anchor, and Stage 4 refines the method through controlled ablations.
The final displayed method should be `poly-core v1`, not the earlier broader Stage 3 variant.

## Table 3

### Title

Component ablation around `poly-feature-only v1`

### Caption

Controlled component ablation results. Each row removes one feature family from the Stage 3 winning configuration, except `poly-core v1`, which keeps only the ablation-supported positive components. Molecular-weight and residue tokens are the strongest contributors, while `composition_terms` are harmful.

## Figure 2

### Title

Effect of removing each poly-specific component

### Caption

Macro-F1 change after removing one feature family from `poly-feature-only v1`. The largest drops appear for molecular-weight and residue features, showing that they are the dominant positive components. Removing composition-count tokens slightly improves performance, motivating the simplified final method.

## Figure 3

### Title

Method simplification from `poly-feature-only v1` to `poly-core v1`

### Caption

Illustration of the final method refinement. Starting from a broader poly-specific feature set, Stage 4 ablation removes weak evidence proxies, sample weighting, source-kingdom tokens, modification tokens, and composition-count tokens, leaving a compact core representation built from molecular-weight, branching, and residue features.
