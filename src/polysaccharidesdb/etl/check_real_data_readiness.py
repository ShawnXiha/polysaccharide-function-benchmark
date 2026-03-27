"""Check whether real exported data is ready for a meaningful Stage 1 rerun."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from polysaccharidesdb.etl.manifest import load_manifest, resolve_manifest_path
from polysaccharidesdb.paths import CONFIGS


REQUIRED_COLUMNS = {
    "DoLPHiN": {
        "source_record_id",
        "raw_representation",
        "canonical_representation",
        "function_label",
        "evidence_type",
        "doi",
    },
    "CSDB": {
        "source_record_id",
        "raw_representation",
        "canonical_representation",
        "function_label",
        "evidence_type",
        "doi",
    },
    "GlyTouCan": {
        "source_record_id",
        "glytoucan_id",
        "canonical_representation",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check readiness of real exported data")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=CONFIGS / "data" / "source_manifest_v0.yaml",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data_interim") / "real_data_readiness.json",
    )
    return parser.parse_args()


def inspect_csv(path: Path) -> tuple[list[str], int]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = sum(1 for _ in reader)
    return fieldnames, rows


def main() -> None:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    report = {"manifest": str(args.manifest), "sources": [], "ready_for_real_stage1": True}

    for source in manifest["sources"]:
        if not source.get("enabled", False):
            continue
        source_name = source["name"]
        path = resolve_manifest_path(source["path"])
        source_report = {
            "name": source_name,
            "path": str(path),
            "exists": path.exists(),
            "row_count": 0,
            "missing_columns": [],
            "looks_like_template_only": False,
            "usable": False,
        }

        if not path.exists():
            source_report["missing_columns"] = sorted(REQUIRED_COLUMNS[source_name])
            source_report["usable"] = False
            report["ready_for_real_stage1"] = False
            report["sources"].append(source_report)
            continue

        fieldnames, row_count = inspect_csv(path)
        source_report["row_count"] = row_count
        source_report["missing_columns"] = sorted(REQUIRED_COLUMNS[source_name] - set(fieldnames))
        source_report["looks_like_template_only"] = row_count <= 1
        source_report["usable"] = (
            len(source_report["missing_columns"]) == 0 and row_count > 1
        ) or (source_name == "GlyTouCan" and len(source_report["missing_columns"]) == 0 and row_count >= 1)

        if source_name != "GlyTouCan" and not source_report["usable"]:
            report["ready_for_real_stage1"] = False

        report["sources"].append(source_report)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)

    print(f"Wrote readiness report to {args.output}")
    print(f"ready_for_real_stage1={report['ready_for_real_stage1']}")


if __name__ == "__main__":
    main()
