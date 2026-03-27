# Supplementary Stronger Simple Baselines

## Scope

This note records two additional simple baselines requested during revision:

1. `TF-IDF + logistic regression`
2. `TF-IDF + linear SVM`

The purpose is not to exhaustively tune all sparse models, but to check whether the main paper is missing strong straightforward text baselines.

## Implementations

- TF-IDF logistic runner:
  - [run_tfidf_logistic_baseline.py](/D:/projects/paper_writing/polysaccharidesdb/src/polysaccharidesdb/models/run_tfidf_logistic_baseline.py)
- Linear SVM runner:
  - [run_linear_svm_baseline.py](/D:/projects/paper_writing/polysaccharidesdb/src/polysaccharidesdb/models/run_linear_svm_baseline.py)

Both models use the same combined structured text rendering as the sparse logistic anchor, but replace the count-vectorized representation with TF-IDF features over 1--2 grams.

## Results

### Random test split

| Method | Macro-F1 | Exact Match |
|---|---:|---:|
| tuned logistic | 0.2610 | 0.2606 |
| `poly_core_v1` | 0.2678 | 0.2570 |
| TF-IDF + logistic | 0.2514 | 0.2897 |
| TF-IDF + linear SVM | 0.2521 | 0.2921 |

Artifacts:

- [tfidf_logistic_random_test.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p1/tfidf_logistic_random_test.json)
- [linear_svm_random_test.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p1/linear_svm_random_test.json)

### DOI-grouped test split

| Method | Macro-F1 | Exact Match |
|---|---:|---:|
| tuned logistic | 0.1250 | 0.1164 |
| `poly_core_v1` | 0.1140 | 0.1066 |
| TF-IDF + logistic | 0.1247 | 0.1605 |
| TF-IDF + linear SVM | 0.1248 | 0.1630 |

Artifacts:

- [tfidf_logistic_doi_test.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p1/tfidf_logistic_doi_test.json)
- [linear_svm_doi_test.json](/D:/projects/paper_writing/polysaccharidesdb/experiments/revision_p1/linear_svm_doi_test.json)

## Interpretation

Three points matter:

1. The tuned count-based logistic anchor remains the strongest simple baseline on `macro-F1`.
2. The TF-IDF baselines materially improve `exact match`, especially under the DOI-grouped split.
3. The additional baselines reinforce that the paper's strongest conclusion is not "our method beats every simple baseline", but rather:
   - the benchmark supports multiple competitive sparse baselines
   - metric choice matters
   - `poly_core_v1` is a structured augmentation with a macro-F1-oriented, split-sensitive profile

## Consequence for the Paper

These baselines strengthen the revised story:

- they reduce the risk that the paper ignored obvious sparse alternatives
- they further justify using the tuned logistic anchor as a serious benchmark reference
- they make it harder to overclaim `poly_core_v1` as the uniquely best simple approach

In a revised main-text comparison, they are best treated as supplementary competitive sparse baselines rather than as the new central anchor.
