# Experiment-Craft Diagnosis: Label-Specific Backoff

## 1. Problem Definition

Earlier source-aware reranking improved overall precision but left tail labels unchanged. Tail candidate generation could raise rare labels, but only by damaging the stable head-label ranking. This cycle tested whether the right intervention point is the label itself: apply backoff only to low-support labels and leave high-support labels untouched.

## 2. What Was Tried

### Attempt 1: Conservative Label-Specific Backoff

- clean `top_k=10`
- label threshold `10`
- rerank top `15`
- label backoff weight `0.5`
- exact / genus / kingdom weights `1.0 / 0.6 / 0.3`

### Attempt 2: Slightly Stronger Label-Specific Backoff

- same setup
- label backoff weight `1.0`

## 3. Evidence

- Baseline clean filtered `Hits@3`: `0.743`
- Label-specific backoff filtered `Hits@3`: `0.744`
- Baseline tail micro filtered `Hits@3`: `0.167`
- Label-specific backoff tail micro filtered `Hits@3`: `0.333`
- Mid micro filtered `Hits@3`: unchanged at `0.375`
- Head micro filtered `Hits@3`: unchanged at `0.762`

Representative label-level improvement:

- `anticomplement`: filtered rank improved from `7` to `3`

## 4. Diagnosis

This method works because it avoids the global calibration problem that broke the previous long-tail methods. It does not inject new candidates and it does not apply a universal source backoff bonus. Instead, it asks a narrower question: among labels that are already low-support, which ones have source-consistent evidence strong enough to justify a small boost?

That selectivity matters. Head labels are left almost unchanged, so the strong base kNN ranking is preserved. At the same time, a few tail labels can move upward when their own training instances show meaningful source overlap. This is why the method produces a real tail gain without the precision collapse seen in tail candidate generation.

## 5. Next Action

- Keep label-specific backoff as the preferred clean long-tail variant.
- Test whether the effect survives under disease-aware features.
- If larger tail gains are needed, combine label-specific backoff with richer label priors rather than broader candidate injection.
