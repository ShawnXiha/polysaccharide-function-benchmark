# Paper Review Self-Check

## Reject-First Summary

In its previous form, the draft was not yet submission-ready because the main comparison table underreported executed baseline families, the method naming still leaned on an `evidence-aware` story that the experiments did not support, and the current figure support remained placeholder-level. The core empirical result was credible, but the presentation left avoidable openings for reviewers to call the contribution selective, thinly contextualized, or insufficiently evidence-anchored.

## Findings

### 1. Contribution Sufficiency

- Status: `borderline but defensible`
- Assessment:
  - The absolute gain over the tuned anchor is modest: `0.2610 -> 0.2678`
  - The contribution is publishable only if framed as:
    - benchmark construction
    - strong baseline reproduction
    - compact structure-aware representation
    - ablation-supported signal identification
- Required action:
  - underclaim metric novelty
  - overdeliver on reproducibility and ablation clarity

### 2. Writing Clarity

- Status: `improved, still not final`
- Main issues found:
  - method family naming was inconsistent with the final evidence
  - the “evidence-aware” wording overstated what the benchmark supports
  - some paragraphs were still too broad in their novelty framing
- Actions taken:
  - unified the final method story around `polysaccharide-specific core representation`
  - added explicit scope-boundary language
  - added deterministic fixed-split framing in Experiments

### 3. Experimental Results Quality

- Status: `acceptable for current claim scope`
- Main issues found:
  - no explanation that Stage 2--4 results are deterministic on the fixed split
  - sequence baselines were missing from the main comparison table, making the paper look selective
- Actions taken:
  - added deterministic framing
  - reran `sequence_ngram` on the publishable benchmark
  - expanded the main comparison table to include sequence baselines

### 4. Experimental Testing Completeness

- Status: `substantially improved`
- Strengths:
  - Stage 1 baseline families executed
  - Stage 2 tuned anchor established
  - Stage 3 winning method identified
  - Stage 4 controlled ablation completed
- Remaining gaps:
  - figures are still placeholder-level
  - related work remains thinner than submission-ready

### 5. Method Design Issues

- Status: `clean after simplification`
- Main insight:
  - the broad Stage 3 method was too noisy
  - ablation simplified it into `poly_core_v1`
- Final supported design:
  - keep `MW + branching + residue`
  - remove `evidence proxy + sample weighting + source kingdom + modification + composition terms`

## Claim-Evidence Audit

### Supported claims

1. A reproducible supervised benchmark can be built from public DoLPHiN ingestion.
2. A tuned logistic baseline is a strong and stable anchor on the main benchmark.
3. A compact polysaccharide-specific core representation improves over the tuned sparse baseline.
4. MW and residue tokens are the strongest contributors, with branching providing a smaller positive gain.

### Claims that must remain narrowed

1. No strong `cross-source biological generalization` claim.
2. No strong `evidence-aware modeling` claim.
3. No claim that the current `CSDB` slice is an equal supervised source.

## Fixes Applied

1. Patched [paper_poly_core_v1.tex](D:/projects/paper_writing/polysaccharidesdb/paper_poly_core_v1.tex)
   - renamed the final story around `polysaccharide-specific core representation`
   - added deterministic-evaluation framing
   - expanded the main comparison table
2. Updated [多糖论文结果整理与主表.md](D:/projects/paper_writing/polysaccharidesdb/多糖论文结果整理与主表.md)
   - synchronized the main table with executed sequence baselines
3. Added missing benchmark run:
   - [sequence_ngram_random.json](D:/projects/paper_writing/polysaccharidesdb/experiments/stage1_baseline/results/publishable_supervised_v1/sequence_ngram_random.json)

## Remaining Pre-Submission Risks

1. Related work is still too sparse for final submission.
2. The paper still lacks finalized figures.
3. The bibliography is still draft-level and should be moved to a proper `.bib`.

## Recommended Next Steps

1. Expand related work and bibliography.
2. Produce the actual pipeline figure and ablation figure.
3. Run one more `paper-review` pass after figures are inserted.
