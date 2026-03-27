"""Build dataset v0 from local source files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from polysaccharidesdb.etl.loaders import load_jsonl
from polysaccharidesdb.etl.normalize import normalize_record
from polysaccharidesdb.etl.schema import validate_record
from polysaccharidesdb.paths import DATA_INTERIM, DATA_PROCESSED, DATA_RAW


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build polysaccharide dataset v0")
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_RAW / "sample_manual_records.jsonl",
        help="Input JSONL file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_PROCESSED / "dataset_v0.jsonl",
        help="Output dataset JSONL",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DATA_INTERIM / "dataset_v0_validation_report.json",
        help="Validation report JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_records = load_jsonl(args.input)
    normalized_records = []
    issues_report = []

    for record in raw_records:
        normalized = normalize_record(record)
        issues = validate_record(normalized)
        normalized_records.append(normalized)
        issues_report.append(
            {
                "poly_id": normalized.get("poly_id"),
                "issues": [
                    {"level": issue.level, "field": issue.field, "message": issue.message}
                    for issue in issues
                ],
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for record in normalized_records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "input": str(args.input),
                "output": str(args.output),
                "num_records": len(normalized_records),
                "records": issues_report,
            },
            handle,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Wrote {len(normalized_records)} records to {args.output}")
    print(f"Validation report saved to {args.report}")


if __name__ == "__main__":
    main()
