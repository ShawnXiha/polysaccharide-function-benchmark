## Joint Pre-Submission Review v2

### Review Setup

This review combines four lenses:

- `peer-review`: reviewer-style assessment of methodology, statistics, and reporting
- `scholar-evaluation`: dimension-based scoring of academic quality
- `scientific-critical-thinking`: evidence quality, bias, and claim-validity analysis
- `paper-review`: adversarial self-review focused on submission risk

### Overall Verdict

The manuscript is now substantially stronger than earlier versions and has a credible submission path, but it still reads as a `major revision before submission` paper rather than a fully closed manuscript. The strongest parts are the disciplined boundary-setting, the explicit negative result on current hetero GNNs, and the paired multi-seed ontology stability analysis. The main remaining weakness is that the paper still combines a resource paper, a benchmark paper, and a selective ontology-method paper in one story. The claims are much better aligned than before, but the manuscript still needs a tighter primary task hierarchy and a cleaner presentation of what the paper wants reviewers to remember first.

### Major Issues

#### 1. The primary task is still not singular enough on the first page.

The manuscript says the primary task is masked `poly-function` link prediction, but the strongest clean headline result is a unified-split multi-label function-prediction benchmark. This creates a framing split between what the paper says it studies and what the clean benchmark table actually emphasizes. A reviewer can still ask whether this is mainly a retrieval benchmark paper or mainly a function-prediction benchmark paper.

- Evidence: [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L39), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L76), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L102)
- Recommended fix: pick one explicit sentence in the Introduction and one in the Methods that says: the main benchmark is `masked poly-function retrieval`, while the unified-split classifier study is the clean diagnostic benchmark for graph signal quality. Or invert that hierarchy consistently if you prefer the benchmark paper framing.

#### 2. Reproducibility is improved, but not yet strong enough for a resource-focused reviewer.

The manuscript describes normalization and leakage control clearly at a conceptual level, but it still does not expose enough concrete implementation detail for a third party to reproduce the benchmark from the paper alone. The current text does not specify where the exact hierarchy file, benchmark splits, edge records, and evaluation scripts are released, nor does it summarize the key hyperparameters of the strongest shallow baseline.

- Evidence: [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L60), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L91), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L97)
- Recommended fix: add a short reproducibility paragraph in Methods or a dedicated `Code and Data Availability` paragraph naming released artifacts: graph export, split definition, function hierarchy config, edge-level records, and experiment scripts.

#### 3. The shallow-baseline result is convincing, but the benchmark table still underplays the comparison logic.

Table 2 shows `Poly-X + Meta-path + LogReg` as the strongest clean model, but the paper does not yet spell out why this baseline is the fairest comparator to the GNNs. A reviewer may still say the GNNs are being compared to a feature-engineered system with privileged inputs unless the relationship between `poly_x`, sparse meta-path features, and node-local GNN inputs is stated more concretely.

- Evidence: [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L91), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L102), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L159)
- Recommended fix: explicitly state whether `poly_x` is available to both shallow and neural models, whether the hybrid GNN receives the same meta-path block, and why the comparison is diagnostic rather than adversarial.

#### 4. The ontology claim is statistically careful, but the evidence base is still narrow.

The paper does a good job distinguishing tuned split from paired pooled evaluation. However, the positive claim rests on a single ontology mechanism, a manually curated hierarchy, and one narrow low-support operating regime. That is acceptable, but the manuscript should frame this more explicitly as a mechanism study than as a generally validated ontology method.

- Evidence: [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L69), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L108), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L227)
- Recommended fix: in the Abstract and Conclusion, replace any residual broad wording with language like `mechanism-level evidence`, `task-specific hierarchy`, or `proof-of-principle tail intervention`.

#### 5. Biology-facing evidence is better than before, but still too thin for a biology-leaning venue.

The paper now has case studies and a local subgraph figure, which is real progress. But the biology-facing section still reads as interpretation of retrieval outcomes rather than as a biological analysis with concrete mechanistic support. There are only two paragraph-level cases, and the clean success examples are not tied to literature provenance strongly enough in the prose.

- Evidence: [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L113), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L115), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L117)
- Recommended fix: add 1 short supplementary table listing the case-study polysaccharides, held-out function, rank changes, and supporting organism/monosaccharide/bond/publication evidence.

### Moderate Issues

#### 6. Statistical reporting is mostly sound, but effect-size language should be standardized.

The paper correctly says the global ontology effect is practically negligible even when statistically detectable. That is the right interpretation. But the manuscript uses several nearby phrasings: `nearly unchanged`, `preserves`, `practically negligible`, and `does not create a new overall best model`. A reviewer may still feel the language is slightly hand-managed unless one standard sentence is reused consistently.

- Evidence: [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L29), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L108), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L235)
- Recommended fix: define one canonical wording, for example: `global aggregate ranking changes are statistically detectable in some metrics but practically negligible in effect size`.

#### 7. Figure 2 and Table 2 still compete for the same narrative role.

Figure 2 already gives the benchmark story, while Table 2 repeats much of it. This is not wrong, but the figure and table should be more deliberately differentiated: the figure should tell the story, while the table should serve as the exact numeric reference.

- Evidence: [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L122), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L153)
- Recommended fix: in the text, cite Figure 2 first for interpretation and Table 2 second for exact values.

#### 8. The title still leans slightly method-forward relative to the strongest contribution.

The current title is much better than the earlier ontology-heavy framing, but it still starts from `Interpretable Function Retrieval and Tail-Sensitive Ontology Propagation`, which centers the method story before the KG/benchmark resource story.

- Evidence: [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L21)
- Recommended fix: consider a benchmark/resource-first title variant for database or bioinformatics venues.

### Minor Issues

#### 9. The GNN ablation table would benefit from predicted-label cardinality in supplementary material.

This would make the exact-match behavior much easier to interpret and would pre-empt reviewer suspicion.

- Evidence: [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L172), [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L195)

#### 10. The Methods section would benefit from one sentence on software and environment.

Even a short note with Python version, core libraries, and repository location would help reproducibility.

- Evidence: [manuscript_v1.tex](/D:/projects/paper_writing/polysaccharidesgraph/paper/manuscript_v1.tex#L52)

### ScholarEval Scores

Scores use a 1--5 scale.

- Problem formulation: 4.0
- Literature framing: 3.8
- Methodology and design: 3.9
- Data and benchmark construction: 4.2
- Analysis and interpretation: 4.0
- Results and evidence presentation: 3.8
- Scholarly writing: 4.0
- Reproducibility and transparency: 3.5

Overall score: 3.9 / 5

Interpretation: strong draft with a plausible submission path, but still one revision cycle short of a confident journal-ready package.

### Scientific Critical Thinking Assessment

#### Claim Validity

- The paper is strongest when it claims that the current KG supports interpretable retrieval and that current message passing is not yet competitive on this graph.
- The paper is adequately supported when it claims ontology helps selectively in the long tail under a disease-aware upper-bound regime.
- The paper would become overclaimed if it implied broad ontology effectiveness, general GNN failure for polysaccharide graphs, or comprehensive biological interpretability.

#### Main Bias and Evidence Risks

- Manual hierarchy construction risk: the ontology mechanism depends on a task-specific hierarchy whose construction remains only partially specified.
- Benchmark framing risk: mixing clean function prediction and masked retrieval may make the paper look less controlled than it is.
- Reporting risk: reproducibility artifacts are not yet foregrounded enough for a resource paper.
- Biological interpretation risk: the case studies still rely more on graph plausibility than on deep external validation.

#### Evidence Quality Judgment

- Clean benchmark claim: moderate-to-strong evidence
- GNN failure diagnosis: moderate evidence, strengthened by no-message ablation
- Ontology tail gain: moderate evidence with good paired statistics, but still mechanism-specific
- Broad biological utility: moderate evidence, not yet strong

### Priority Revision Plan

#### Highest priority

1. Resolve the primary-task hierarchy explicitly in the first page and Methods.
2. Add a concise reproducibility paragraph naming released artifacts and code locations.
3. Clarify fairness of the shallow-baseline versus GNN comparison.

#### Medium priority

4. Add a supplementary case-study evidence table.
5. Standardize effect-size wording for the ontology result.
6. Make the figure-versus-table narrative roles more deliberate.

#### Lower priority

7. Consider a benchmark-first alternative title.
8. Add software/environment details and predicted-label cardinality in supplement.

### Submission Readiness

Current status: `major revision before submission`, but no longer because the paper lacks a story. The remaining work is mostly about tightening trust: task hierarchy, reproducibility visibility, comparator fairness, and biology-facing evidence packaging.
