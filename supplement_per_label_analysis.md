# Supplementary Per-Label Analysis

## Scope

This note compares per-label F1 between the tuned logistic anchor and `poly_core_v1` using the final test predictions from revision-P0.

Source reports:

- random split:
  - [per_label_random_test.md](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p1/per_label_random_test.md)
  - [per_label_random_test.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p1/per_label_random_test.json)
- DOI-grouped split:
  - [per_label_doi_test.md](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p1/per_label_doi_test.md)
  - [per_label_doi_test.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p1/per_label_doi_test.json)

## Random-Split Pattern

Under the random test split, the aggregate macro-F1 improvement of `poly_core_v1` is not uniform across labels. The largest positive changes are concentrated in:

| Label | Support | Logistic F1 | Poly-core F1 | Delta |
|---|---:|---:|---:|---:|
| antimicrobial | 31 | 0.2745 | 0.3673 | +0.0928 |
| neuroprotective | 16 | 0.3571 | 0.4286 | +0.0714 |
| microbiota_regulation | 26 | 0.1000 | 0.1429 | +0.0429 |
| organ_protective | 41 | 0.1311 | 0.1695 | +0.0383 |

At the same time, several labels weaken:

| Label | Support | Logistic F1 | Poly-core F1 | Delta |
|---|---:|---:|---:|---:|
| anticoagulant | 28 | 0.3934 | 0.3529 | -0.0405 |
| lipid_lowering | 24 | 0.1277 | 0.0909 | -0.0368 |
| antiviral | 9 | 0.1333 | 0.1111 | -0.0222 |
| antifatigue | 10 | 0.1333 | 0.1176 | -0.0157 |

Interpretation:

- the random-split macro-F1 gain comes from a small subset of labels rather than broad uniform improvement
- many of the largest positive deltas occur on relatively low-support labels, so they should be interpreted cautiously

## DOI-Grouped Pattern

Under the stricter DOI-grouped test split, the label-level pattern becomes less favorable for `poly_core_v1`.

Largest grouped-split gains:

| Label | Support | Logistic F1 | Poly-core F1 | Delta |
|---|---:|---:|---:|---:|
| anticoagulant | 36 | 0.1579 | 0.1750 | +0.0171 |
| antifatigue | 19 | 0.1765 | 0.1935 | +0.0171 |
| antidiabetic | 129 | 0.2703 | 0.2870 | +0.0167 |

Largest grouped-split drops:

| Label | Support | Logistic F1 | Poly-core F1 | Delta |
|---|---:|---:|---:|---:|
| antiaging | 24 | 0.2381 | 0.0513 | -0.1868 |
| lipid_lowering | 28 | 0.0833 | 0.0408 | -0.0425 |
| antitumor | 165 | 0.2545 | 0.2335 | -0.0210 |

Interpretation:

- grouped-split degradation is not a diffuse small effect; it includes at least one substantial label-level collapse (`antiaging`)
- this reinforces the paper's revised claim that the current feature augmentation is informative but not robustly general

## What This Means for the Paper

The per-label analysis supports a narrower and more defensible story:

1. `poly_core_v1` is not a uniformly stronger classifier across labels
2. its random-split gain is concentrated in a few labels
3. grouped-split robustness is label-dependent and can break sharply
4. the more stable contribution is the feature-level insight from ablation, not a blanket model-improvement claim

## Recommendation for Main-Text Use

The main paper should summarize this section conservatively:

- mention that random-split gains are label-concentrated rather than uniform
- note that grouped-split degradation is especially visible for a few labels
- keep the full table in supplementary material rather than in the main body
