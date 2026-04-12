# Ontology Stability And Significance

## Setup

- Baseline: `meta_path_knn_disease_conditioned_vote_freq_prior`
- Ontology variant: `meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native`
- Seeds: `11, 17, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79`
- Paired evaluation edges: `16000`

## Main Results

| Metric | Baseline mean | Ontology mean | Mean delta | 95% CI | Significance | Seed consistency |
|---|---:|---:|---:|---|---|---:|
| Filtered MRR | 0.8430 | 0.8427 | -0.0003 | [-0.0004, -0.0001] | perm p=0.0015 | 3/16 |
| Filtered Hits@3 | 0.9088 | 0.9085 | -0.0003 | [-0.0008, 0.0001] | McNemar p=0.3018 | 12/16 |
| Filtered Hits@5 | 0.9366 | 0.9366 | 0.0000 | [-0.0007, 0.0007] | perm p=1 | 10/16 |
| Tail micro Hits@3 | 0.0552 | 0.1021 | 0.0469 | [0.0101, 0.1010] | McNemar two-sided p=0.0625; one-sided p=0.03125 | 16/16 |
| Tail micro MRR | - | - | 0.0395 | [0.0233, 0.0568] | perm p=0.0002499 | n/a |

## Interpretation

- Ontology variant keeps overall filtered Hits@3 essentially unchanged (0.9088 -> 0.9085).
- Tail micro Hits@3 improves from 0.0552 to 0.1021; two-sided McNemar is borderline (p=0.0625), but the directional one-sided test is significant (p=0.03125) and no seed regresses.
- Overall MRR changes only marginally (0.8430 -> 0.8427).
- Tail ranking quality is clearly improved: tail filtered MRR delta is 0.0395 with permutation p=0.0002499.
