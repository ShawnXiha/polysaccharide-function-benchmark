# Manuscript Conversion Notes: BMC Bioinformatics

## Required content changes from current draft

1. Convert the abstract into a structured abstract with:
   - `Background`
   - `Results`
   - `Conclusions`
2. Rename section flow to BMC Bioinformatics Research article style:
   - `Background`
   - `Methods`
   - `Results`
   - `Discussion`
   - `Conclusions`
   - `Declarations`
3. Insert the declarations block from [declarations_bmc_bioinformatics.md](D:/projects/paper_writing/polysaccharidesdb/submission_packages/bmc_bioinformatics/declarations_bmc_bioinformatics.md).

## Recommended scientific framing

- Primary contribution: benchmark construction plus robust evaluation of sparse and structured representations.
- Main empirical statement: tuned sparse logistic is a strong anchor; `poly-core v1` gives a modest random-split macro-F1 gain that does not persist under DOI-grouped evaluation.
- Keep weak-supervision framing explicit.

## Suggested structured abstract skeleton

### Background

Natural-polysaccharide structure-function prediction remains underdeveloped because public records are heterogeneous, incomplete, and weakly supervised.

### Results

We construct a reproducible benchmark from public polysaccharide resources, establish a tuned sparse logistic baseline as a strong anchor, and show that a compact structured augmentation yields a modest random-split macro-F1 gain from 0.2610 to 0.2678. However, paired bootstrap analysis is not decisive and a stricter DOI-grouped split reverses the advantage, while ablations identify molecular-weight, residue-set, and branching features as the main useful signals.

### Conclusions

The most reliable contribution is therefore a benchmark and feature-level insight rather than a universally stronger new model.
