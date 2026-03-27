"""Classical baseline implementations."""

from __future__ import annotations

from collections import Counter


class MajorityMultilabelBaseline:
    """Predict the most common label set in the training split."""

    def fit(self, records: list[dict]) -> "MajorityMultilabelBaseline":
        label_sets = [tuple(sorted(record.get("function_label", []))) for record in records]
        if not label_sets:
            self.majority_labels = tuple()
            return self
        counts = Counter(label_sets)
        self.majority_labels = counts.most_common(1)[0][0]
        return self

    def predict(self, records: list[dict]) -> list[set[str]]:
        majority = set(getattr(self, "majority_labels", tuple()))
        return [set(majority) for _ in records]
