# Supplementary Case Studies and Error Analysis

## Scope

This note turns the revision-P0 prediction comparisons into concrete examples. The goal is not to claim mechanistic certainty for individual records, but to show the kinds of corrections and failures introduced by `poly_core_v1` relative to the tuned logistic anchor.

Prediction sources:

- random split test:
  - [tuned_logistic_random_test_seed11.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/logistic_random_test/tuned_logistic_random_test_seed11.json)
  - [poly_core_random_test_seed11.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/poly_core_random_test/poly_core_random_test_seed11.json)
- DOI-grouped split test:
  - [tuned_logistic_doi_test_seed11.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/logistic_doi_test/tuned_logistic_doi_test_seed11.json)
  - [poly_core_doi_test_seed11.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p0/poly_core_doi_test/poly_core_doi_test_seed11.json)

## Case Type A: Random-Split Corrections

### Case A1: Recovering an omitted organ-protective label

- `poly_id`: `dolphin::36019`
- true labels: `antioxidant`, `organ_protective`
- tuned logistic: `antioxidant`
- `poly_core_v1`: `antioxidant`, `organ_protective`

Record cues:

- MW: unknown
- branching token: `branching_missing`
- residue tokens: `res_ara`, `res_gal`, `res_gala`, `res_rha`

Interpretation:

- This is a clean random-split improvement where the structured token layer adds the second label without introducing extra false positives.
- The case is consistent with the paper's narrower claim that residue-set information can add value in some label-local situations.

### Case A2: Recovering a missing antioxidant label

- `poly_id`: `dolphin::33416`
- true labels: `antioxidant`, `immunomodulatory`
- tuned logistic: `immunomodulatory`
- `poly_core_v1`: `antioxidant`, `immunomodulatory`

Record cues:

- organism: `Lentinus edodes`
- MW: unknown
- residue tokens: `res_glc`, `res_man`, `res_gal`, `res_gala`

Interpretation:

- This is another random-split correction in which the structured augmentation adds a missing label instead of only pruning errors.
- The improvement remains local: it helps this record, but it does not imply broad robustness across splits.

### Case A3: Pruning an extra false-positive label

- `poly_id`: `dolphin::34576`
- true labels: `antidiabetic`
- tuned logistic: `antidiabetic`, `antioxidant`
- `poly_core_v1`: `antidiabetic`

Record cues:

- MW: `16.3 kDa` mapped to `mw_10k_100k`
- residue tokens include `res_xyl` and `res_ara`

Interpretation:

- `poly_core_v1` can help by removing an over-predicted extra label, not only by adding missing ones.
- This kind of correction explains why a small macro-F1 improvement can coexist with slightly worse exact match.

## Case Type B: Random-Split Failure

### Case B1: Losing a previously correct antioxidant prediction

- `poly_id`: `dolphin::37102`
- true labels: `antioxidant`
- tuned logistic: `antioxidant`
- `poly_core_v1`: none

Record cues:

- MW: `610 kDa` mapped to `mw_100k_1m`
- residue tokens: effectively very sparse, with only `res_glc`
- branching token: `branching_missing`

Interpretation:

- This is a direct counterexample to any overly strong method claim.
- The added structured tokens can also suppress correct sparse-baseline decisions when the feature evidence is too coarse.

## Case Type C: Grouped-Split Degradation

### Case C1: Grouped-split loss of an immunomodulatory label

- `poly_id`: `dolphin::36764`
- true labels: `antioxidant`, `immunomodulatory`
- DOI-grouped tuned logistic: `antioxidant`, `immunomodulatory`
- DOI-grouped `poly_core_v1`: `antioxidant`

Record cues:

- MW: `9.31 x 10^4 kDa` parsed into a low-MW bucket by the current parser
- residue diversity token: `residue_diversity_6`
- branching token: `branching_missing`

Interpretation:

- This case illustrates grouped-split fragility: once paper-level phrasing leakage is removed, the structured augmentation can lose a label that the tuned sparse model still recovers.
- It also shows that feature engineering and parsing quality are intertwined; any MW parsing ambiguity can become disproportionately harmful in a grouped split.

### Case C2: Grouped-split collapse on a single-label example

- `poly_id`: `dolphin::34975`
- true labels: `immunomodulatory`
- DOI-grouped tuned logistic: `immunomodulatory`
- DOI-grouped `poly_core_v1`: none

Record cues:

- MW: `134 kDa` mapped to `mw_100k_1m`
- residue tokens: `res_glc`, `res_rha`
- branching token: `branching_missing`

Interpretation:

- This is a minimal grouped-split failure: the baseline remains correct while the structured augmentation becomes over-selective and drops the only label.

### Case C3: Grouped-split success still exists, but is not dominant

- `poly_id`: `dolphin::36637`
- true labels: `anticoagulant`, `antimicrobial`, `antioxidant`, `antitumor`
- DOI-grouped tuned logistic: `antimicrobial`, `antioxidant`, `antitumor`
- DOI-grouped `poly_core_v1`: `anticoagulant`, `antimicrobial`, `antioxidant`, `antitumor`

Record cues:

- MW: `400 kDa` mapped to `mw_100k_1m`
- residue diversity token: `residue_diversity_6`
- residue tokens include `res_fuc`, `res_xyl`, `res_man`

Interpretation:

- This example is important because it prevents overcorrection in the opposite direction.
- The grouped split does not make `poly_core_v1` uniformly bad; it makes the method inconsistent and label-sensitive.

## Error Categories

The examples above suggest four concrete error categories:

1. `Useful local corrections`
   - the structured tokens sometimes add or remove a label in a way that matches the ground truth
2. `Over-pruning`
   - the augmented representation can suppress a correct sparse-baseline prediction
3. `Grouped-split fragility`
   - cases that look improved under random split may not survive DOI-grouped evaluation
4. `Parser-sensitive behavior`
   - MW bucketing and residue extraction are useful overall, but noisy parsing or coarse buckets can also amplify mistakes

## What These Cases Mean for the Paper

The case studies support the revised paper story:

- `poly_core_v1` is useful as an analytical probe into which structured signals matter
- it can improve selected records and labels
- but it is not yet robust enough to replace the tuned sparse anchor as the central predictive conclusion
