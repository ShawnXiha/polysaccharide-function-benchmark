# Experiment-Craft Diagnosis: Frequency-Adjusted Disease Prior

## 1. Problem Definition

The ordinary disease prior improved disease-aware retrieval, but it still favored frequent labels. The question for this cycle was whether a simple frequency-aware correction could keep the semantic value of the prior while reducing popularity bias enough to improve retrieval quality.

## 2. What Was Tried

### Attempt 1: Mild Divisive Adjustment

- disease-aware prior base
- rerank top `20`
- prior weight `1.0`
- adjustment strength `0.5`
- mode `divide`

### Attempt 2: Aggressive Subtractive Adjustment

- rerank top `25`
- prior weight `1.25`
- adjustment strength `1.0`
- mode `subtract`

### Attempt 3: Stronger Divisive Adjustment

- rerank top `15`
- prior weight `1.0`
- adjustment strength `0.75`
- mode `divide`

## 3. Evidence

- Disease prior baseline filtered `Hits@3`: `0.878`
- Mild divisive adjustment filtered `Hits@3`: `0.880`
- Mild divisive adjustment filtered `MRR`: `0.8191`
- Aggressive subtractive adjustment filtered `Hits@3`: `0.877`
- Stronger divisive adjustment filtered `Hits@3`: `0.878`
- Tail micro filtered `Hits@3`: unchanged at `0.167` in all attempts
- Mid micro filtered `Hits@3`: unchanged at `0.400` in the successful attempt
- Head micro filtered `Hits@3`: `0.903 -> 0.905` in the successful attempt

## 4. Diagnosis

This method works, but only in a narrow and important sense. A mild divisive correction improves the disease prior because it slightly tempers the advantage of very common labels without destroying the useful compatibility signal. That is enough to improve overall filtered ranking.

The failure case is also informative. Once the correction becomes too strong, especially in subtractive form, it starts removing real signal rather than just popularity bias. The disease prior is not merely a frequency effect, so overly aggressive correction harms ranking quality.

The long-tail conclusion, however, is unchanged. The best setting did not improve the tail stratum at all. That means frequency adjustment is another calibration improvement, not the missing mechanism for rare-label recovery.

## 5. Next Action

- Keep mild divisive frequency adjustment as the preferred disease-aware calibration variant.
- Do not over-tune subtractive or high-strength penalties.
- If the long-tail goal remains primary, next test:
  - support-aware candidate generation before reranking
  - disease-conditioned support smoothing
  - hybrid candidate expansion plus conservative calibration
