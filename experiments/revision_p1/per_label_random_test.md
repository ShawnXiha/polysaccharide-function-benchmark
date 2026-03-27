# Per-Label Comparison: Poly-core v1 vs Tuned Logistic

- split: `default`
- result A: `experiments\revision_p0\logistic_random_test\tuned_logistic_random_test_seed11.json`
- result B: `experiments\revision_p0\poly_core_random_test\poly_core_random_test_seed11.json`

## Top F1 Gains

| Label | Support | Tuned Logistic F1 | Poly-core v1 F1 | Delta |
|---|---:|---:|---:|---:|
| antimicrobial | 31 | 0.2745 | 0.3673 | +0.0928 |
| neuroprotective | 16 | 0.3571 | 0.4286 | +0.0714 |
| microbiota_regulation | 26 | 0.1000 | 0.1429 | +0.0429 |
| organ_protective | 41 | 0.1311 | 0.1695 | +0.0383 |
| antiobesity | 12 | 0.0800 | 0.0870 | +0.0070 |
| antitumor | 168 | 0.4650 | 0.4693 | +0.0043 |
| antiaging | 23 | 0.1053 | 0.1053 | +0.0000 |
| antidiabetic | 94 | 0.4222 | 0.4222 | +0.0000 |

## Top F1 Drops

| Label | Support | Tuned Logistic F1 | Poly-core v1 F1 | Delta |
|---|---:|---:|---:|---:|
| anticoagulant | 28 | 0.3934 | 0.3529 | -0.0405 |
| lipid_lowering | 24 | 0.1277 | 0.0909 | -0.0368 |
| antiviral | 9 | 0.1333 | 0.1111 | -0.0222 |
| antifatigue | 10 | 0.1333 | 0.1176 | -0.0157 |
| immunomodulatory | 312 | 0.5878 | 0.5782 | -0.0097 |
| antioxidant | 459 | 0.7222 | 0.7166 | -0.0055 |
| antiinflammatory | 27 | 0.2712 | 0.2667 | -0.0045 |
| antiaging | 23 | 0.1053 | 0.1053 | +0.0000 |

## Full Per-Label Table

| Label | Support | Tuned Logistic F1 | Poly-core v1 F1 | Delta |
|---|---:|---:|---:|---:|
| antiaging | 23 | 0.1053 | 0.1053 | +0.0000 |
| anticoagulant | 28 | 0.3934 | 0.3529 | -0.0405 |
| antidiabetic | 94 | 0.4222 | 0.4222 | +0.0000 |
| antifatigue | 10 | 0.1333 | 0.1176 | -0.0157 |
| antiinflammatory | 27 | 0.2712 | 0.2667 | -0.0045 |
| antimicrobial | 31 | 0.2745 | 0.3673 | +0.0928 |
| antiobesity | 12 | 0.0800 | 0.0870 | +0.0070 |
| antioxidant | 459 | 0.7222 | 0.7166 | -0.0055 |
| antiproliferative | 10 | 0.1176 | 0.1176 | +0.0000 |
| antitumor | 168 | 0.4650 | 0.4693 | +0.0043 |
| antiviral | 9 | 0.1333 | 0.1111 | -0.0222 |
| cholesterol_lowering | 16 | 0.2759 | 0.2759 | +0.0000 |
| immunomodulatory | 312 | 0.5878 | 0.5782 | -0.0097 |
| lipid_lowering | 24 | 0.1277 | 0.0909 | -0.0368 |
| microbiota_regulation | 26 | 0.1000 | 0.1429 | +0.0429 |
| neuroprotective | 16 | 0.3571 | 0.4286 | +0.0714 |
| organ_protective | 41 | 0.1311 | 0.1695 | +0.0383 |
| radioprotective | 4 | 0.0000 | 0.0000 | +0.0000 |
