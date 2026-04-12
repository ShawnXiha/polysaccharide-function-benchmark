# Stage Log: Stage 3 - Proposed Method

## Stage Info

- **Pipeline**: DoLPHiN KG poly-function masked link prediction
- **Stage**: 3: Proposed Method
- **Budget**: 12 attempts
- **Gate Condition**: Proposed method outperforms tuned clean baseline on the primary retrieval metric
- **Start Date**: 2026-03-27

## Attempt Log

| # | Hypothesis | Code Changes | Configuration | Result | Analysis | Gate Met? |
|---|-----------|-------------|--------------|--------|----------|-----------|
| 1 | Adding disease-aware meta-path features should substantially improve recovery because disease nodes inject auxiliary semantics. | Reused `build_feature_dicts(..., include_disease_features=True)` inside link prediction scorer. | `with_disease`, `top_k=50` | `MRR=0.6079`, `Hits@3=0.801`, `Hits@5=0.887` | Strong improvement over clean tuned baseline (`Hits@3=0.655`). Confirms disease-aware retrieval is a high-value side-information method. | No |
| 2 | Re-tuning `top_k` under disease-aware features may further improve retrieval. | None beyond reused scorer. | `with_disease`, `top_k=25` | `MRR=0.6097`, `Hits@3=0.814`, `Hits@5=0.893`, `mean_rank=4.548` | Slightly better than `top_k=50` on all major metrics. Gate met. [Reusable] Disease-aware kNN can materially outperform clean retrieval; re-tune neighborhood size after adding a new relation family. | Yes |

## Gate Assessment

- **Gate condition**: proposed method beats tuned clean baseline on primary metric
- **Current best result**: disease-aware `top_k=25`, `Hits@3=0.814`
- **Met?**: Yes
- **If not met**: N/A

## Key Observations

- Disease features produce the largest single gain in masked edge recovery.
- The improvement is real but must be framed carefully as auxiliary-semantic enhancement.
- The same kNN mechanism scales cleanly from clean to disease-aware settings.

## Lessons Learned

- Side-information can be decisive for link prediction even when it is too confounded for primary function-prediction claims.
- [Reusable] Keep the scorer fixed and change one relation family at a time; this makes gains easy to attribute.

## Next Stage Preparation

- [x] Gate condition verified
- [x] Results documented and saved
- [x] Trajectory log completed
- [x] Key artifacts ready for next stage
