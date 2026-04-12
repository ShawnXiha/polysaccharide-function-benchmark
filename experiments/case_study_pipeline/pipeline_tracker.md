# Case Study Pipeline Tracker

## Project Info

- **Project**: Biology-facing case studies for the DoLPHiN KG manuscript
- **Research Goal**: Select 2--4 case studies that demonstrate clean retrieval success, ontology-rescued tail behavior, and representative failure modes using concrete graph evidence.
- **Start Date**: 2026-03-29
- **Source Artifacts**:
  - `experiments/case_study_pipeline/clean_case_records_seed42.json`
  - `experiments/ontology_stability_runs/*.json`
  - `data/processed/neo4j/nodes/*.csv`
  - `data/processed/neo4j/edges/*.csv`

## Pipeline Status

| Stage | Status | Notes |
|-------|--------|-------|
| 1. Candidate pool construction | Complete | clean, ontology rescue, ontology failure, and clean failure candidates exported |
| 2. Final case shortlist | Complete | four manuscript-facing cases selected |
| 3. Case summary drafting | Complete | short manuscript-facing summaries drafted for the four selected cases |
| 4. Figure/table design | Complete | local subgraph figure finalized as `paper/figures/figure4_case_subgraphs.(png|pdf)` |

## Current Decision

- Use one ontology rescue case, two clean success cases, and one representative failure case.
- Favor cases with complete evidence previews across organism, monosaccharide, bond, disease, and DOI provenance.
- Use a local subgraph figure rather than a ranking-only chart so the biology-facing evidence channels remain visible in the manuscript.
