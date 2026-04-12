# Stage Log: Stage 4 - Ablation Study

## Stage Info

- **Pipeline**: DoLPHiN KG poly-function masked link prediction
- **Stage**: 4: Ablation Study
- **Budget**: 18 attempts
- **Gate Condition**: Each claimed gain has a controlled comparison showing what helped and what hurt
- **Start Date**: 2026-03-27

## Attempt Log

| # | Hypothesis | Code Changes | Configuration | Result | Analysis | Gate Met? |
|---|-----------|-------------|--------------|--------|----------|-----------|
| 1 | `idf` label weighting may reduce popularity bias and help long-tail function recovery. | Added `--label-idf-weighting` to kNN scorer. | `clean`, `top_k=25`, `idf=True` | `MRR=0.4405`, `Hits@3=0.558`, `Hits@5=0.737` | Hypothesis refuted. Reweighting hurt both rank and retrieval quality in the clean setting. | No |
| 2 | The same `idf` weighting may still help in the disease-aware setting. | Reused same code path. | `with_disease`, `top_k=25`, `idf=True` | `MRR=0.5934`, `Hits@3=0.780`, `Hits@5=0.881` | Still worse than no-idf (`Hits@3=0.814`). `idf` is not a useful component here. | No |
| 3 | Disease features are the dominant contributor among tested modifications. | None beyond comparing controlled runs. | `clean top_k=10` vs `with_disease top_k=25` vs `with_disease top_k=25 + idf` | `Hits@3`: `0.655 -> 0.814 -> 0.780` | Clear contribution pattern: disease features help, `idf` hurts. Gate met. [Reusable] In label-skewed KG retrieval, local prevalence can be signal rather than bias; naive inverse-frequency corrections may remove useful evidence. | Yes |
| 4 | Multi-label masked link prediction should use filtered ranking, otherwise other true functions act like false competitors. | Added `filtered` rank computation that removes the same polysaccharide's other true functions from the candidate set. | `clean`, `top_k=10`; `with_disease`, `top_k=25` | clean kNN `MRR: 0.4806 -> 0.6168`, `Hits@3: 0.655 -> 0.743`; disease-aware kNN `MRR: 0.6097 -> 0.8119`, `Hits@3: 0.814 -> 0.875` | Confirmed. Unfiltered ranking was underestimating retrieval quality in this multi-label setting. Future reporting should always include filtered metrics as the primary protocol. | Yes |
| 5 | Global averages may hide long-tail failure; per-label stratified evaluation should expose head/mid/tail behavior. | Added per-label kNN metrics and label-support strata: `tail_1_10`, `mid_11_50`, `head_gt_50`. | Same runs as Attempt 4 | clean filtered micro `Hits@3`: tail `0.167`, mid `0.375`, head `0.762`; disease-aware filtered micro `Hits@3`: tail `0.167`, mid `0.400`, head `0.899` | Confirmed. Most gains are concentrated in high-support labels. Long-tail function recovery remains the main unresolved bottleneck. | Yes |

## Gate Assessment

- **Gate condition**: controlled comparisons support the main claims
- **Current best result**: disease-aware `top_k=25`, no idf
- **Met?**: Yes
- **If not met**: N/A

## Key Observations

- Disease features consistently help.
- `idf` weighting consistently hurts.
- Centroid scoring remains a failed design choice relative to local voting.
- Filtered ranking is the correct primary protocol for this multi-label task.
- Head labels dominate overall gains; tail labels remain weak even after disease augmentation.

## Lessons Learned

- [Reusable] Do not assume long-tail reweighting helps when the task is neighbor-based retrieval with meaningful local frequency structure.
- [Reusable] In multi-label edge recovery, always report filtered metrics; raw ranks can misclassify other true labels as errors.
- [Reusable] Add per-label or support-stratified metrics before claiming a retrieval method is broadly effective.
- The ablation result is simple and strong enough to support a paper claim.

## Next Stage Preparation

- [x] Gate condition verified
- [x] Results documented and saved
- [x] Trajectory log completed
- [x] Key artifacts ready for next stage
