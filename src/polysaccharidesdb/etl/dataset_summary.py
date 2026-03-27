"""Compute simple dataset statistics for Stage 1 sanity checks."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from polysaccharidesdb.etl.loaders import load_jsonl
from polysaccharidesdb.paths import DATA_INTERIM, DATA_PROCESSED


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize dataset v0")
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "dataset_v0.jsonl",
        help="Dataset JSONL file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_INTERIM / "dataset_v0_summary.json",
        help="Output summary JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = load_jsonl(args.input)

    source_counts = Counter(record["source_db"] for record in records)
    evidence_counts = Counter(record["evidence_type"] for record in records)
    label_counts = Counter()
    for record in records:
        for label in record.get("function_label", []):
            label_counts[label] += 1

    summary = {
        "num_records": len(records),
        "source_counts": dict(source_counts),
        "evidence_counts": dict(evidence_counts),
        "label_counts": dict(label_counts),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)

    print(f"Wrote summary to {args.output}")


if __name__ == "__main__":
    main()
