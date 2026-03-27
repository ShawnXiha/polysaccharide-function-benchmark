# Per-Label Comparison: Poly-core v1 vs Tuned Logistic

- split: `default`
- result A: `experiments\revision_p0\logistic_doi_test\tuned_logistic_doi_test_seed11.json`
- result B: `experiments\revision_p0\poly_core_doi_test\poly_core_doi_test_seed11.json`

## Top F1 Gains

| Label | Support | Tuned Logistic F1 | Poly-core v1 F1 | Delta |
|---|---:|---:|---:|---:|
| anticoagulant | 36 | 0.1579 | 0.1750 | +0.0171 |
| antifatigue | 19 | 0.1765 | 0.1935 | +0.0171 |
| antidiabetic | 129 | 0.2703 | 0.2870 | +0.0167 |
| microbiota_regulation | 23 | 0.0800 | 0.0833 | +0.0033 |
| antimicrobial | 23 | 0.0465 | 0.0476 | +0.0011 |
| antioxidant | 451 | 0.5911 | 0.5922 | +0.0010 |
| antiinflammatory | 24 | 0.0000 | 0.0000 | +0.0000 |
| antiobesity | 9 | 0.0000 | 0.0000 | +0.0000 |

## Top F1 Drops

| Label | Support | Tuned Logistic F1 | Poly-core v1 F1 | Delta |
|---|---:|---:|---:|---:|
| antiaging | 24 | 0.2381 | 0.0513 | -0.1868 |
| lipid_lowering | 28 | 0.0833 | 0.0408 | -0.0425 |
| antitumor | 165 | 0.2545 | 0.2335 | -0.0210 |
| immunomodulatory | 317 | 0.3521 | 0.3475 | -0.0046 |
| antiinflammatory | 24 | 0.0000 | 0.0000 | +0.0000 |
| antiobesity | 9 | 0.0000 | 0.0000 | +0.0000 |
| antiproliferative | 6 | 0.0000 | 0.0000 | +0.0000 |
| antiviral | 5 | 0.0000 | 0.0000 | +0.0000 |

## Full Per-Label Table

| Label | Support | Tuned Logistic F1 | Poly-core v1 F1 | Delta |
|---|---:|---:|---:|---:|
| antiaging | 24 | 0.2381 | 0.0513 | -0.1868 |
| anticoagulant | 36 | 0.1579 | 0.1750 | +0.0171 |
| antidiabetic | 129 | 0.2703 | 0.2870 | +0.0167 |
| antifatigue | 19 | 0.1765 | 0.1935 | +0.0171 |
| antiinflammatory | 24 | 0.0000 | 0.0000 | +0.0000 |
| antimicrobial | 23 | 0.0465 | 0.0476 | +0.0011 |
| antiobesity | 9 | 0.0000 | 0.0000 | +0.0000 |
| antioxidant | 451 | 0.5911 | 0.5922 | +0.0010 |
| antiproliferative | 6 | 0.0000 | 0.0000 | +0.0000 |
| antitumor | 165 | 0.2545 | 0.2335 | -0.0210 |
| antiviral | 5 | 0.0000 | 0.0000 | +0.0000 |
| cholesterol_lowering | 18 | 0.0000 | 0.0000 | +0.0000 |
| immunomodulatory | 317 | 0.3521 | 0.3475 | -0.0046 |
| lipid_lowering | 28 | 0.0833 | 0.0408 | -0.0425 |
| microbiota_regulation | 23 | 0.0800 | 0.0833 | +0.0033 |
| neuroprotective | 18 | 0.0000 | 0.0000 | +0.0000 |
| organ_protective | 18 | 0.0000 | 0.0000 | +0.0000 |
| radioprotective | 12 | 0.0000 | 0.0000 | +0.0000 |
