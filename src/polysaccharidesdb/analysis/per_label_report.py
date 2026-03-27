"""Generate per-label comparison reports from prediction JSON files."""

from __future__ import annotations

import argparse
from pathlib import Path

from polysaccharidesdb.utils.io import read_json, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build per-label comparison report")
    parser.add_argument("--result-a", type=Path, required=True, help="Baseline result JSON")
    parser.add_argument("--result-b", type=Path, required=True, help="Comparison result JSON")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--label-a", type=str, default="Baseline")
    parser.add_argument("--label-b", type=str, default="Comparison")
    parser.add_argument("--split-name", type=str, default="default")
    parser.add_argument("--top-k", type=int, default=8)
    return parser.parse_args()


def get_split_row(payload: dict, split_name: str) -> dict:
    for row in payload.get("results", []):
        if row.get("split_name") == split_name:
            return row
    raise ValueError(f"Split '{split_name}' not found")


def label_metrics(predictions: list[dict], label: str) -> dict:
    tp = fp = fn = support = 0
    for item in predictions:
        y_true = set(item["y_true"])
        y_pred = set(item["y_pred"])
        if label in y_true:
            support += 1
        if label in y_true and label in y_pred:
            tp += 1
        elif label not in y_true and label in y_pred:
            fp += 1
        elif label in y_true and label not in y_pred:
            fn += 1
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return {
        "support": support,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def markdown_table(rows: list[dict], label_a: str, label_b: str) -> str:
    lines = [
        f"| Label | Support | {label_a} F1 | {label_b} F1 | Delta |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['label']} | {row['support']} | {row['f1_a']:.4f} | {row['f1_b']:.4f} | {row['delta_f1']:+.4f} |"
        )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    payload_a = read_json(args.result_a)
    payload_b = read_json(args.result_b)
    row_a = get_split_row(payload_a, args.split_name)
    row_b = get_split_row(payload_b, args.split_name)

    preds_a = row_a["predictions"]
    preds_b = row_b["predictions"]
    order_a = [item["poly_id"] for item in preds_a]
    order_b = [item["poly_id"] for item in preds_b]
    if order_a != order_b:
        raise ValueError("Prediction files are not aligned")

    labels = sorted(set(row_a["labels"]) | set(row_b["labels"]))
    per_label_rows = []
    for label in labels:
        metrics_a = label_metrics(preds_a, label)
        metrics_b = label_metrics(preds_b, label)
        per_label_rows.append(
            {
                "label": label,
                "support": metrics_a["support"],
                "f1_a": metrics_a["f1"],
                "f1_b": metrics_b["f1"],
                "precision_a": metrics_a["precision"],
                "recall_a": metrics_a["recall"],
                "precision_b": metrics_b["precision"],
                "recall_b": metrics_b["recall"],
                "delta_f1": metrics_b["f1"] - metrics_a["f1"],
            }
        )

    top_gain = sorted(per_label_rows, key=lambda item: item["delta_f1"], reverse=True)[: args.top_k]
    top_drop = sorted(per_label_rows, key=lambda item: item["delta_f1"])[: args.top_k]
    report = {
        "result_a": str(args.result_a),
        "result_b": str(args.result_b),
        "label_a": args.label_a,
        "label_b": args.label_b,
        "split_name": args.split_name,
        "per_label": per_label_rows,
        "top_gain": top_gain,
        "top_drop": top_drop,
    }
    write_json(args.output_json, report)

    lines = [
        f"# Per-Label Comparison: {args.label_b} vs {args.label_a}",
        "",
        f"- split: `{args.split_name}`",
        f"- result A: `{args.result_a}`",
        f"- result B: `{args.result_b}`",
        "",
        "## Top F1 Gains",
        "",
        markdown_table(top_gain, args.label_a, args.label_b),
        "",
        "## Top F1 Drops",
        "",
        markdown_table(top_drop, args.label_a, args.label_b),
        "",
        "## Full Per-Label Table",
        "",
        markdown_table(per_label_rows, args.label_a, args.label_b),
        "",
    ]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote per-label report to {args.output_json} and {args.output_md}")


if __name__ == "__main__":
    main()
