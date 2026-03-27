"""Minimal metrics for early-stage baseline checks."""

from __future__ import annotations


def macro_f1_score(y_true: list[set[str]], y_pred: list[set[str]]) -> float:
    labels = sorted({label for row in y_true for label in row} | {label for row in y_pred for label in row})
    if not labels:
        return 0.0

    f1_scores = []
    for label in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred) if label in t and label in p)
        fp = sum(1 for t, p in zip(y_true, y_pred) if label not in t and label in p)
        fn = sum(1 for t, p in zip(y_true, y_pred) if label in t and label not in p)

        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 0.0 if (precision + recall) == 0 else 2 * precision * recall / (precision + recall)
        f1_scores.append(f1)

    return sum(f1_scores) / len(f1_scores)


def exact_match_ratio(y_true: list[set[str]], y_pred: list[set[str]]) -> float:
    if not y_true:
        return 0.0
    return sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true)
