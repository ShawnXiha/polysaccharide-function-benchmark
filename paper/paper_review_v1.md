# Paper Self-Review v1

## Reject-First Summary

This draft has a credible core story and stronger evidence than earlier versions, but it is not submission-ready yet. The main risk is not lack of results; it is that the paper currently blends three contribution types --- resource construction, clean benchmark diagnosis, and ontology-tail analysis --- without fully separating what is primary evidence from what is secondary support. A skeptical reviewer could still say that the paper mixes task settings, relies on a tuned split for some headline numbers, and lacks enough biology-facing case analysis to justify publication in a bioinformatics or glycobiology-facing venue.

## Major Findings

### 1. The main contribution is still split across two tasks, which weakens first-pass reviewer trust.

- **Why it matters**: The paper now has a stronger clean benchmark story, but the title, abstract, and experiments still combine clean multi-label function prediction and masked `poly-function` link prediction. A reviewer may ask which task is the true primary contribution.
- **Where**: `paper/manuscript_v1.tex`, Abstract, Introduction, Experiments.
- **Fix**: Make one task primary in the first page framing. The clean unified-split function prediction benchmark should likely be the main benchmark, while masked link prediction should be presented as the retrieval-focused extension that motivates ontology-tail analysis.

### 2. The paper still lacks biology-facing case studies, which leaves the biological significance under-supported.

- **Why it matters**: The methodology and benchmark logic are much stronger now, but the manuscript still reads primarily as a KG/retrieval paper. For biological reviewers, there is not yet enough concrete evidence that the graph captures meaningful structure-function patterns in specific polysaccharide examples.
- **Where**: `paper/manuscript_v1.tex`, Experiments, Discussion.
- **Fix**: Add 2--4 case studies showing one successful clean retrieval case, one ontology-rescued tail case, and one representative failure. Each case should tie predicted functions back to organism/monosaccharide/bond evidence and, when possible, DOI provenance.

### 3. The current baseline table is stronger, but the paper still does not explain enough about why exact match behaves oddly in some GNN ablations.

- **Why it matters**: In Table `gnn-ablation`, the hybrid no-message ablation has very low macro-F1 but a relatively large exact match. A reviewer could flag this as suspicious or indicative of thresholding artifacts.
- **Where**: `paper/manuscript_v1.tex`, Table `gnn-ablation`, Experiments.
- **Fix**: Add one sentence explaining that exact match is brittle in this multi-label setting and can be inflated by sparse predicted label sets even when macro-F1 remains poor. If possible, add average predicted label cardinality for these rows in supplementary material.

### 4. The tuned-split versus pooled-paired protocol distinction is improved, but the paper still needs one explicit sentence telling readers which result should be cited as the primary ontology claim.

- **Why it matters**: The manuscript now distinguishes the protocols correctly, but a hurried reviewer may still wonder whether the tail gain is being claimed from the tuned split or from the paired significance analysis.
- **Where**: `paper/manuscript_v1.tex`, Experiments, Table `main-results`, Table `stability`.
- **Fix**: Add one explicit sentence such as: "We treat the paired 16-seed analysis as the primary evidence for ontology stability, and the tuned split only as an interpretable representative operating point."

## Minor Findings

### 5. The title is much better aligned, but it may still be slightly too broad for the actual contribution mix.

- **Where**: `paper/manuscript_v1.tex`, title.
- **Suggestion**: Consider a more benchmark-first title, e.g. emphasizing "benchmark" or "retrieval benchmark" if targeting bioinformatics venues.

### 6. The Method section could benefit from one short implementation-details pointer.

- **Where**: `paper/manuscript_v1.tex`, Methods.
- **Suggestion**: Add one sentence noting where code/configs live and what artifacts are available, especially if you plan a resource-oriented submission.

### 7. Figure 2 is now much better aligned with the paper, but Panel C would be easier to parse if the caption explicitly said "message passing adds little."

- **Where**: `paper/manuscript_v1.tex`, Figure 2 caption.
- **Suggestion**: Make the interpretation sentence more explicit.

## Trust Assessment

- **Contribution sufficiency**: Moderate to strong, if framed as a KG resource + benchmark + negative/positive mechanism paper rather than a new general method paper.
- **Writing clarity**: Improved, but still needs stronger task hierarchy.
- **Experimental quality**: Stronger after the shallow baselines and GNN ablations.
- **Experimental completeness**: Good for benchmark/ablation logic; still missing biology-facing cases.
- **Method design soundness**: Stronger now that `full vs no-message` has been tested directly.

## Recommended Next Actions

1. Add biology-facing case studies.
2. Clarify which task is primary on the first page.
3. Add one sentence on the ontology primary-evidence protocol.
4. Add a short explanation for the exact-match behavior in GNN ablations.
