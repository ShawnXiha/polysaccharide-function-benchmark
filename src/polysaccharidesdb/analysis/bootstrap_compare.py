"""Paired bootstrap comparison for multi-label predictions."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from polysaccharidesdb.utils.io import read_json, write_json
from polysaccharidesdb.utils.metrics import exact_match_ratio, macro_f1_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Paired bootstrap comparison between two result files")
    parser.add_argument("--result-a", type=Path, required=True, help="Baseline result JSON")
    parser.add_argument("--result-b", type=Path, required=True, help="Comparison result JSON")
    parser.add_argument("--output", type=Path, required=True, help="Output JSON")
    parser.add_argument("--metric", type=str, default="macro_f1", choices=["macro_f1", "exact_match"])
    parser.add_argument("--split-name", type=str, default="default", help="Split name to compare")
    parser.add_argument("--num-bootstrap", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def get_split_row(payload: dict, split_name: str) -> dict:
    for row in payload.get("results", []):
        if row.get("split_name") == split_name:
            return row
    raise ValueError(f"Split '{split_name}' not found in result payload")


def metric_value(metric_name: str, y_true: list[set[str]], y_pred: list[set[str]]) -> float:
    if metric_name == "macro_f1":
        return macro_f1_score(y_true, y_pred)
    if metric_name == "exact_match":
        return exact_match_ratio(y_true, y_pred)
    raise ValueError(f"Unsupported metric: {metric_name}")


def percentile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return 0.0
    idx = min(len(sorted_values) - 1, max(0, int(q * (len(sorted_values) - 1))))
    return sorted_values[idx]


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)

    payload_a = read_json(args.result_a)
    payload_b = read_json(args.result_b)
    row_a = get_split_row(payload_a, args.split_name)
    row_b = get_split_row(payload_b, args.split_name)

    preds_a = row_a.get("predictions", [])
    preds_b = row_b.get("predictions", [])
    if len(preds_a) != len(preds_b):
        raise ValueError("Prediction payloads have different lengths")

    order_a = [item["poly_id"] for item in preds_a]
    order_b = [item["poly_id"] for item in preds_b]
    if order_a != order_b:
        raise ValueError("Prediction payloads are not aligned by poly_id")

    y_true = [set(item["y_true"]) for item in preds_a]
    y_pred_a = [set(item["y_pred"]) for item in preds_a]
    y_pred_b = [set(item["y_pred"]) for item in preds_b]

    observed_a = metric_value(args.metric, y_true, y_pred_a)
    observed_b = metric_value(args.metric, y_true, y_pred_b)
    observed_delta = observed_b - observed_a

    n = len(y_true)
    deltas: list[float] = []
    for _ in range(args.num_bootstrap):
        indices = [rng.randrange(n) for _ in range(n)]
        sample_true = [y_true[idx] for idx in indices]
        sample_pred_a = [y_pred_a[idx] for idx in indices]
        sample_pred_b = [y_pred_b[idx] for idx in indices]
        delta = metric_value(args.metric, sample_true, sample_pred_b) - metric_value(
            args.metric, sample_true, sample_pred_a
        )
        deltas.append(delta)

    deltas_sorted = sorted(deltas)
    ci_low = percentile(deltas_sorted, 0.025)
    ci_high = percentile(deltas_sorted, 0.975)
    p_two_sided = 2 * min(
        sum(1 for value in deltas if value <= 0.0) / len(deltas),
        sum(1 for value in deltas if value >= 0.0) / len(deltas),
    )
    p_two_sided = min(1.0, p_two_sided)

    result = {
        "metric": args.metric,
        "split_name": args.split_name,
        "num_examples": n,
        "num_bootstrap": args.num_bootstrap,
        "result_a": str(args.result_a),
        "result_b": str(args.result_b),
        "observed_a": observed_a,
        "observed_b": observed_b,
        "observed_delta_b_minus_a": observed_delta,
        "delta_ci_95": [ci_low, ci_high],
        "p_two_sided": p_two_sided,
    }
    write_json(args.output, result)
    print(f"Wrote bootstrap comparison to {args.output}")


if __name__ == "__main__":
    main()
