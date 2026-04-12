# Stage Log: Stage 1 - Initial Implementation

## Stage Info

- **Pipeline**: DoLPHiN KG poly-function masked link prediction
- **Stage**: 1: Initial Implementation
- **Budget**: 20 attempts
- **Gate Condition**: Executable masked-edge evaluation is in place and at least one clean KG method clearly exceeds centroid scoring
- **Start Date**: 2026-03-27

## Attempt Log

| # | Hypothesis | Code Changes | Configuration | Result | Analysis | Gate Met? |
|---|-----------|-------------|--------------|--------|----------|-----------|
| 1 | A simple popularity baseline is needed as a sanity floor for masked edge recovery. | Added `run_poly_function_link_prediction.py` with masked edge evaluation and popularity ranking. | `clean`, `num_eval_edges=1000` | `MRR=0.4835`, `Hits@3=0.525`, `Hits@5=0.752` | The task is non-trivial but highly frequency-skewed; any proposed method must beat this on at least one ranking metric. | No |
| 2 | Function centroid scoring over meta-path features should recover masked edges better than popularity. | Added centroid scoring over function prototype vectors. | `clean`, same eval split | `MRR=0.0538`, `Hits@3=0.014`, `Hits@5=0.024` | Hypothesis refuted. Global centroids wash out local label structure and collapse toward irrelevant frequent functions. | No |
| 3 | Local kNN voting over the same meta-path features will preserve local KG signal better than centroids. | Added `meta_path_knn` scoring. | `clean`, `top_k=50` | `MRR=0.4743`, `Hits@3=0.639`, `Hits@5=0.762` | kNN strongly beats centroid and improves retrieval over popularity on `Hits@3`/`Hits@5`. Stage gate met. [Reusable] Prefer local neighborhood voting over global label centroids for sparse multi-label KG recovery. | Yes |

## Gate Assessment

- **Gate condition**: executable masked-edge evaluation with a viable clean KG method
- **Current best result**: clean `meta_path_knn`, `Hits@3=0.639`
- **Met?**: Yes
- **If not met**: N/A

## Key Observations

- Popularity is a strong baseline because label distribution is highly skewed.
- Centroid scoring is a poor fit for this graph because function neighborhoods are multimodal.
- kNN recovers local structure without introducing a model-training burden.

## Lessons Learned

- Locality matters more than global prototypes in this task.
- Clean graph-derived features already contain useful signal even without disease information.
- [Reusable] When a KG task is dominated by local relational similarity, try kNN propagation before KGE/GNN.

## Next Stage Preparation

- [x] Gate condition verified
- [x] Results documented and saved
- [x] Trajectory log completed
- [x] Key artifacts ready for next stage
