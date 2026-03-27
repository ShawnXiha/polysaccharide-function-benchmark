# Manuscript Conversion Notes: Journal of Cheminformatics

## Required content changes from current draft

1. Add a `Scientific Contribution` subsection to the abstract with no more than 3 sentences.
2. Rename section flow to match the Methodology article type more closely:
   - `Introduction`
   - `Results`
   - `Discussion` or `Results and Discussion`
   - `Conclusions`
   - `Methods/Experimental`
   - `Declarations`
3. Insert the declarations block from [declarations_joc.md](D:/projects/paper_writing/polysaccharidesdb/submission_packages/journal_of_cheminformatics/declarations_joc.md).

## Recommended scientific framing

- Primary claim: reproducible benchmark and interpretable signal analysis.
- Secondary claim: `poly-core v1` gives a modest random-split macro-F1 improvement but does not support a strong grouped-generalization claim.
- Do not frame the paper as a universally stronger model paper.

## Suggested abstract-level Scientific Contribution text

This study introduces a reproducible benchmark for multi-label structure-function prediction of natural polysaccharides from public resources. It shows that a tuned sparse logistic baseline is a strong anchor under current public-data conditions and that the apparent benefit of structured augmentation is modest and split-sensitive. Controlled ablations further identify molecular-weight, residue-set, and branching features as the main usable structural signals in the current benchmark.
