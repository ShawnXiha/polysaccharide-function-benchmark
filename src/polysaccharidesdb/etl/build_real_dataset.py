"""Build dataset v0 from source-specific real-data exports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from polysaccharidesdb.etl.manifest import load_manifest, resolve_manifest_path
from polysaccharidesdb.etl.normalize import normalize_record
from polysaccharidesdb.etl.schema import validate_record
from polysaccharidesdb.etl.source_loaders import (
    load_csdb_export,
    load_dolphin_export,
    load_glytoucan_mapping,
)
from polysaccharidesdb.paths import CONFIGS


SOURCE_LOADERS = {
    "DoLPHiN": load_dolphin_export,
    "CSDB": load_csdb_export,
    "GlyTouCan": load_glytoucan_mapping,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build real dataset from source exports")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=CONFIGS / "data" / "source_manifest_v0.yaml",
        help="Path to source manifest YAML",
    )
    return parser.parse_args()


def merge_glytoucan(records: list[dict], mapping_rows: list[dict]) -> list[dict]:
    mapping = {
        row["source_record_id"]: row
        for row in mapping_rows
        if row.get("source_record_id")
    }
    merged = []
    for record in records:
        row = dict(record)
        extra = mapping.get(row["source_record_id"])
        if extra:
            row["glytoucan_id"] = extra.get("glytoucan_id", "")
            if not row.get("canonical_representation"):
                row["canonical_representation"] = extra.get("canonical_representation", "")
            row["wurcs"] = extra.get("wurcs", "")
        merged.append(row)
    return merged


def main() -> None:
    args = parse_args()
    manifest = load_manifest(args.manifest)

    primary_records: list[dict] = []
    glytoucan_rows: list[dict] = []
    source_counts: dict[str, int] = {}

    for source in manifest["sources"]:
        if not source.get("enabled", False):
            continue
        source_name = source["name"]
        source_path = resolve_manifest_path(source["path"])
        loader = SOURCE_LOADERS[source_name]
        rows = loader(source_path)
        source_counts[source_name] = len(rows)
        if source_name == "GlyTouCan":
            glytoucan_rows.extend(rows)
        else:
            primary_records.extend(rows)

    if glytoucan_rows:
        primary_records = merge_glytoucan(primary_records, glytoucan_rows)

    normalized_records = []
    issues_report = []
    for record in primary_records:
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

    dataset_path = resolve_manifest_path(manifest["output"]["dataset"])
    report_path = resolve_manifest_path(manifest["output"]["report"])

    dataset_path.parent.mkdir(parents=True, exist_ok=True)
    with dataset_path.open("w", encoding="utf-8") as handle:
        for record in normalized_records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "manifest": str(args.manifest),
                "dataset": str(dataset_path),
                "num_records": len(normalized_records),
                "source_counts": source_counts,
                "records": issues_report,
            },
            handle,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Wrote {len(normalized_records)} records to {dataset_path}")
    print(f"Validation report saved to {report_path}")


if __name__ == "__main__":
    main()
