"""Build filtered datasets for publishable supervised evaluation."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from polysaccharidesdb.etl.loaders import load_jsonl
from polysaccharidesdb.paths import DATA_INTERIM, DATA_PROCESSED


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build publishable filtered datasets")
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "dataset_v0_real.jsonl",
        help="Merged dataset JSONL",
    )
    parser.add_argument(
        "--output-dataset",
        type=Path,
        default=DATA_PROCESSED / "dataset_publishable_supervised_v1.jsonl",
        help="Filtered supervised dataset JSONL",
    )
    parser.add_argument(
        "--output-report",
        type=Path,
        default=DATA_INTERIM / "dataset_publishable_supervised_v1_report.json",
        help="Filtering report JSON",
    )
    parser.add_argument(
        "--min-label-count",
        type=int,
        default=20,
        help="Minimum global frequency required to keep a label",
    )
    parser.add_argument(
        "--supervised-sources",
        nargs="+",
        default=["DoLPHiN"],
        help="Sources allowed in the supervised benchmark",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = load_jsonl(args.input)

    label_counts = Counter()
    for record in records:
        for label in record.get("function_label", []):
            if label != "unknown":
                label_counts[label] += 1

    kept_labels = sorted(
        label for label, count in label_counts.items() if count >= args.min_label_count
    )
    kept_label_set = set(kept_labels)
    supervised_sources = set(args.supervised_sources)

    filtered_records: list[dict] = []
    removed_by_reason = Counter()
    per_source_counts = Counter()
    per_source_label_counts: dict[str, Counter] = defaultdict(Counter)

    for record in records:
        if record.get("source_db") not in supervised_sources:
            removed_by_reason["source_not_supervised"] += 1
            continue

        labels = [
            label
            for label in record.get("function_label", [])
            if label in kept_label_set
        ]
        if not labels:
            removed_by_reason["no_kept_labels"] += 1
            continue

        row = dict(record)
        row["function_label"] = sorted(set(labels))
        filtered_records.append(row)
        per_source_counts[row["source_db"]] += 1
        for label in row["function_label"]:
            per_source_label_counts[row["source_db"]][label] += 1

    args.output_dataset.parent.mkdir(parents=True, exist_ok=True)
    with args.output_dataset.open("w", encoding="utf-8") as handle:
        for record in filtered_records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    report = {
        "input_dataset": str(args.input),
        "output_dataset": str(args.output_dataset),
        "min_label_count": args.min_label_count,
        "supervised_sources": sorted(supervised_sources),
        "num_input_records": len(records),
        "num_output_records": len(filtered_records),
        "kept_labels": kept_labels,
        "kept_label_count": len(kept_labels),
        "removed_by_reason": dict(removed_by_reason),
        "output_source_counts": dict(per_source_counts),
        "output_label_counts_by_source": {
            source: dict(counter) for source, counter in per_source_label_counts.items()
        },
    }
    args.output_report.parent.mkdir(parents=True, exist_ok=True)
    with args.output_report.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)

    print(f"Wrote {len(filtered_records)} filtered records to {args.output_dataset}")
    print(f"Filtering report saved to {args.output_report}")


if __name__ == "__main__":
    main()
