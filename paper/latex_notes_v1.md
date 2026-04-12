# LaTeX Notes v1

## Current Files

- `paper/manuscript_v1.tex`
- `paper/references_placeholder.bib`

## Current State

This is a manuscript-shaped LaTeX draft with:

- title, abstract, and section structure
- inserted figure environments for Figures 1--3
- inserted table environments for Tables 1--3
- labels and cross-references
- bibliography scaffold

## Remaining Work

- replace placeholder bibliography with real references
- adapt document class to the target venue
- tighten table widths if a conference template is narrower
- optionally move `Related Work` before `Methods` if the venue expects that order

## Suggested Build Command

```powershell
pdflatex manuscript_v1.tex
bibtex manuscript_v1
pdflatex manuscript_v1.tex
pdflatex manuscript_v1.tex
```
