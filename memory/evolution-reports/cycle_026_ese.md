# Evolution Report: Cycle 026 - ESE

**Date**: 2026-03-29
**Trigger**: Biology-facing case-study mining workflow completed through candidate construction, shortlist selection, and short summary drafting
**Source Artifacts**:
- `scripts/build_case_study_candidates.py`
- `experiments/case_study_pipeline/clean_case_records_seed42.json`
- `experiments/case_study_pipeline/case_study_candidates.csv`
- `experiments/case_study_pipeline/case_study_shortlist.md`
- `experiments/case_study_pipeline/case_study_summaries_v1.md`

## Success Classification

- **Type**: Reusable strategy extraction
- **Direction**: evidence-grounded case-study preparation for scientific writing

## Reasoning

The main lesson from this cycle is that manuscript case studies should be constructed as a data-processing problem before they are written as prose. Directly selecting examples from headline metrics is brittle and usually produces cases with poor evidence density. A better workflow is:

1. collect edge-level records from the actual evaluation outputs
2. enrich each candidate with local KG evidence previews
3. group candidates into manuscript-relevant categories
4. only then choose representative cases

In the current project, this workflow made the case-study section much easier to justify. Instead of browsing examples manually, it produced a structured pool with:

- `743` clean successes
- `1` ontology rescue
- `46` ontology failures
- `172` clean failures

This immediately exposed the fact that only one stable ontology rescue exists in the current paired pool, which is exactly the kind of constraint that should shape the paper's narrative.

## Changes Made

### Added

- `Build Biology-Facing Case Studies From Edge Records Before Writing Narratives`

### Updated

- The manuscript preparation workflow now has a principled route for selecting biology-facing examples.

### Removed

- None

## Impact on Future Cycles

- Always build a candidate pool before drafting case-study prose.
- Track category counts (`success`, `rescue`, `failure`) so the paper does not overstate how common a phenomenon is.
- When a special-case gain is rare, surface that rarity early and build the narrative around it rather than around a generic claim.

## Raw Evidence Summary

- candidate CSV: `experiments/case_study_pipeline/case_study_candidates.csv`
- shortlist: `experiments/case_study_pipeline/case_study_shortlist.md`
- summary draft: `experiments/case_study_pipeline/case_study_summaries_v1.md`
- counts: `743` clean successes, `1` ontology rescue, `46` ontology failures, `172` clean failures
