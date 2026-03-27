# Paper Review Self-Check Round 3

## Reject-First Summary

The draft is now materially stronger than the earlier version: the figures are real, the bibliography is formalized, the main table no longer hides executed baseline families, and the method story is aligned with the actual experiments. It is still not fully submission-ready, but the remaining risks are narrower. They are now mostly about presentation discipline: making the fairness framing impossible to misread, tightening reproducibility wording, and deciding whether the current related-work depth is sufficient for the target venue.

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

- Status: `substantially improved`
- Main issues found:
  - earlier versions used an `evidence-aware` framing that overstated what the benchmark supports
  - fairness wording around tuned vs. untuned baselines needed to be explicit
  - reproducibility details were previously underspecified
- Actions taken:
  - unified the final method story around `polysaccharide-specific core representation`
  - added explicit scope-boundary and fairness language
  - added deterministic fixed-split framing in Experiments
  - added split-size and implementation-detail paragraphs

### 3. Experimental Results Quality

- Status: `credible for current claim scope`
- Main issues found:
  - earlier versions did not explain that Stage 2--4 results are deterministic on the fixed split
  - sequence baselines were initially missing from the main comparison table, making the paper look selective
  - the Stage 3 failure-to-success trajectory was previously implicit
- Actions taken:
  - added deterministic framing
  - reran `sequence_ngram` on the publishable benchmark
  - expanded the main comparison table to include sequence baselines
  - added a dedicated Stage 3 evolution table

### 4. Experimental Testing Completeness

- Status: `strong for a benchmark paper`
- Strengths:
  - Stage 1 baseline families executed
  - Stage 2 tuned anchor established
  - Stage 3 winning method identified
  - Stage 4 controlled ablation completed
  - figures and bibliography are now real rather than placeholder-level
- Remaining gaps:
  - the paper still relies on a single-source supervised benchmark for its main claim
  - cross-source results remain an engineering stress test rather than a main scientific result

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

### Claims That Must Remain Narrowed

1. No strong `cross-source biological generalization` claim.
2. No strong `evidence-aware modeling` claim.
3. No claim that the current `CSDB` slice is an equal supervised source.

## Remaining Pre-Submission Risks

1. The main table still mixes a tuned anchor with mostly untuned comparison families, so the fairness framing must remain explicit in the text and caption.
2. Related work may still be thin for a stronger venue even though it is now adequate for a domain-oriented benchmark submission.
3. The benchmark story is scientifically narrow by design; if the target venue expects stronger biological generalization claims, the paper will need either better label-aligned cross-source data or a stricter benchmark-positioning narrative.

## Recommended Next Steps

1. Run one more LaTeX compile and a final `paper-review` pass against the updated draft.
2. Decide whether to add a short appendix or supplement note for full token definitions and artifact locations.
3. Tighten venue-specific positioning before submission rather than expanding claims.
