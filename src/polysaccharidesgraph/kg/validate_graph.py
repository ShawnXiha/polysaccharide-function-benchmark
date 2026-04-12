"""Validate generated KG exports."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Validate KG CSV exports")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repo_root / "data" / "processed" / "neo4j",
    )
    return parser.parse_args()


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    args = parse_args()
    node_dir = args.output_dir / "nodes"
    edge_dir = args.output_dir / "edges"

    node_files = {
        "polysaccharide": ("polysaccharide.csv", "poly_id"),
        "organism": ("organism.csv", "organism_id"),
        "monosaccharide": ("monosaccharide.csv", "monosaccharide_id"),
        "glycosidic_bond": ("glycosidic_bond.csv", "bond_id"),
        "function": ("function.csv", "function_id"),
        "disease": ("disease.csv", "disease_id"),
        "publication": ("publication.csv", "doi"),
    }
    edge_files = {
        "poly_organism": "poly_organism.csv",
        "poly_monosaccharide": "poly_monosaccharide.csv",
        "poly_bond": "poly_bond.csv",
        "poly_function": "poly_function.csv",
        "poly_disease": "poly_disease.csv",
        "poly_publication": "poly_publication.csv",
    }

    node_ids: dict[str, set[str]] = {}
    summary: dict[str, object] = {"nodes": {}, "edges": {}, "errors": []}

    for name, (filename, id_field) in node_files.items():
        rows = read_csv(node_dir / filename)
        ids = {row[id_field] for row in rows}
        node_ids[name] = ids
        summary["nodes"][name] = {"rows": len(rows), "unique_ids": len(ids)}
        if len(rows) != len(ids):
            summary["errors"].append(f"duplicate ids detected in node file {filename}")

    edge_expected = {
        "poly_organism": ("polysaccharide", "organism"),
        "poly_monosaccharide": ("polysaccharide", "monosaccharide"),
        "poly_bond": ("polysaccharide", "glycosidic_bond"),
        "poly_function": ("polysaccharide", "function"),
        "poly_disease": ("polysaccharide", "disease"),
        "poly_publication": ("polysaccharide", "publication"),
    }

    for name, filename in edge_files.items():
        rows = read_csv(edge_dir / filename)
        source_type, target_type = edge_expected[name]
        broken = 0
        for row in rows:
            if row["source_id"] not in node_ids[source_type] or row["target_id"] not in node_ids[target_type]:
                broken += 1
        summary["edges"][name] = {"rows": len(rows), "broken_refs": broken}
        if broken:
            summary["errors"].append(f"{filename} has {broken} broken references")

    summary["ok"] = not summary["errors"]
    summary_path = args.output_dir / "kg_validation.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
