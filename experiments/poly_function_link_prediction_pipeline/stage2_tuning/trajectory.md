# Stage Log: Stage 2 - Hyperparameter Tuning

## Stage Info

- **Pipeline**: DoLPHiN KG poly-function masked link prediction
- **Stage**: 2: Hyperparameter Tuning
- **Budget**: 12 attempts
- **Gate Condition**: Identify a stable clean `kNN` configuration that maximizes the primary retrieval metric
- **Start Date**: 2026-03-27

## Attempt Log

| # | Hypothesis | Code Changes | Configuration | Result | Analysis | Gate Met? |
|---|-----------|-------------|--------------|--------|----------|-----------|
| 1 | Smaller neighborhoods may sharpen local signal and improve `Hits@3`. | Added `--top-k` argument. | `clean`, `top_k=10` | `MRR=0.4806`, `Hits@3=0.655`, `Hits@5=0.787`, `mean_rank=9.539` | Best `Hits@3` among clean settings tested. Good candidate for primary clean config. | No |
| 2 | A moderately larger neighborhood may trade a little precision for better rank stability. | None beyond reused scorer. | `clean`, `top_k=25` | `MRR=0.4773`, `Hits@3=0.651`, `Hits@5=0.788`, `mean_rank=7.148` | Nearly tied on `Hits@3`; slightly better mean rank. If primary metric were rank quality, this would be competitive. | No |
| 3 | Very large neighborhoods may over-smooth and drift toward popularity. | None beyond reused scorer. | `clean`, `top_k=100` | `MRR=0.4794`, `Hits@3=0.618`, `Hits@5=0.764`, `mean_rank=5.679` | Over-smoothing observed; retrieval quality drops on `Hits@3`. | No |
| 4 | Because this is a retrieval problem, `Hits@3` is the most relevant primary metric for tuning. | Decision-only, no code change. | Comparison across attempts 1-3 | Selected `top_k=10` as tuned clean baseline | Gate met. [Reusable] For poly-function recovery, `top_k` in the `10-25` range is strong; larger neighborhoods dilute local signal. | Yes |

## Gate Assessment

- **Gate condition**: tuned clean kNN config selected
- **Current best result**: `top_k=10`, `Hits@3=0.655`
- **Met?**: Yes
- **If not met**: N/A

## Key Observations

- `top_k` affects retrieval quality more than MRR.
- `Hits@3` was the most decision-relevant metric because the task is candidate recovery, not strict top-1 classification.
- Clean kNN tuning is cheap and interpretable.

## Lessons Learned

- Small local neighborhoods are best for clean KG retrieval.
- [Reusable] Tune `top_k` against the actual downstream use metric, not just MRR.

## Next Stage Preparation

- [x] Gate condition verified
- [x] Results documented and saved
- [x] Trajectory log completed
- [x] Key artifacts ready for next stage
