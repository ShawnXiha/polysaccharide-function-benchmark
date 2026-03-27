# Supplementary Benchmark Statistics and Preprocessing Note

## Scope

This note records the benchmark statistics and preprocessing decisions for the main supervised dataset used in:

- [paper_poly_core_v1.tex](/D:/projects/paper_writing/polysaccharidesdb/paper_poly_core_v1.tex)

The benchmark artifact itself is:

- [dataset_publishable_supervised_v1.jsonl](/D:/projects/paper_writing/polysaccharidesdb/data_processed/dataset_publishable_supervised_v1.jsonl)

## Benchmark Construction Rule

The benchmark is derived from the merged real-data scaffold and then filtered with the following rules:

1. Keep only records from `DoLPHiN`
2. Remove `unknown` labels
3. Keep only labels with global frequency `>= 20`

Filtering report:

- [dataset_publishable_supervised_v1_report.json](/D:/projects/paper_writing/polysaccharidesdb/data_interim/dataset_publishable_supervised_v1_report.json)

## Resulting Dataset Size

- input records before filtering: `5531`
- output benchmark records: `4121`
- retained labels: `18`
- records removed because they had no retained label: `957`
- records removed because they came from non-supervised sources: `453`

## Label Vocabulary

Retained label set:

1. `antiaging`
2. `anticoagulant`
3. `antidiabetic`
4. `antifatigue`
5. `antiinflammatory`
6. `antimicrobial`
7. `antiobesity`
8. `antioxidant`
9. `antiproliferative`
10. `antitumor`
11. `antiviral`
12. `cholesterol_lowering`
13. `immunomodulatory`
14. `lipid_lowering`
15. `microbiota_regulation`
16. `neuroprotective`
17. `organ_protective`
18. `radioprotective`

## Label Frequencies

From the filtered benchmark:

| Label | Count |
|---|---:|
| antioxidant | 2202 |
| immunomodulatory | 1532 |
| antitumor | 856 |
| antidiabetic | 510 |
| anticoagulant | 176 |
| organ_protective | 157 |
| antiinflammatory | 152 |
| lipid_lowering | 132 |
| antimicrobial | 125 |
| antiaging | 94 |
| microbiota_regulation | 91 |
| neuroprotective | 86 |
| cholesterol_lowering | 73 |
| antifatigue | 63 |
| antiviral | 54 |
| antiproliferative | 51 |
| antiobesity | 43 |
| radioprotective | 30 |

## Per-Record Label Density

- average labels per record: `1.5596`
- median labels per record: `1`

This confirms that the task is sparse multi-label prediction rather than dense multi-task annotation.

## Field Availability After Filtering

Missing-rate estimates on the 4,121-record benchmark:

| Field | Missing rate |
|---|---:|
| canonical_representation | 0.0% |
| monomer_composition | 2.4% |
| linkage | 80.9% |
| branching | 0.0% |
| modification | 100.0% |
| mw_or_range | 26.6% |
| organism_source | 0.0% |
| doi | 0.1% |

Two consequences matter for modeling:

1. linkage-complete graph reconstruction is not a realistic primary benchmark assumption
2. modification-specific modeling is weakly supported because the filtered benchmark effectively contains no usable modification field

## Weak-Supervision Note

The benchmark should not be interpreted as a fully observed true-negative dataset.

- Labels are inherited from what was reported in the literature.
- A missing function label is therefore closer to `unreported` than to `confirmed absent`.
- The task is best interpreted as weakly supervised multi-label prediction with positive-and-unlabeled characteristics.

This is why the main paper treats macro-F1 and exact match as comparative benchmark metrics under a fixed protocol, not as absolute measures of biological truth.

## Split Files

Current revision-P0 split files:

- random split:
  - [random_split.json](/D:/projects/paper_writing/polysaccharidesdb/data_processed/splits_publishable_supervised_v2/random_split.json)
- DOI-grouped split:
  - [doi_grouped_split.json](/D:/projects/paper_writing/polysaccharidesdb/data_processed/splits_publishable_supervised_v2/doi_grouped_split.json)

Current partition sizes:

| Split file | Train | Valid | Test |
|---|---:|---:|---:|
| random | 2472 | 824 | 825 |
| DOI-grouped | 2474 | 831 | 816 |

The DOI-grouped split was checked to ensure that the same DOI never appears in more than one partition.

## Preprocessing Summary

The current benchmark preprocessing pipeline includes:

1. public-site ingestion
2. schema normalization
3. label normalization
4. source filtering to `DoLPHiN`
5. removal of `unknown`
6. low-frequency label filtering
7. deterministic split generation

## Artifact Pointers

- benchmark summary:
  - [dataset_publishable_supervised_v1_summary.json](/D:/projects/paper_writing/polysaccharidesdb/data_interim/dataset_publishable_supervised_v1_summary.json)
- revision-P0 findings:
  - [revision_p0_findings.md](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/revision_p0_findings.md)
- reproducibility note:
  - [supplement_reproducibility_poly_core_v1.md](/D:/projects/paper_writing/polysaccharidesdb/supplement_reproducibility_poly_core_v1.md)
