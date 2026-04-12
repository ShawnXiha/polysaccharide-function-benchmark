"""Build a minimal KG v0 export from the existing DoLPHiN JSONL files."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from polysaccharidesgraph.kg.normalize import (
    clean_text,
    extract_disease_code,
    normalize_bond,
    normalize_function,
    parse_monomer_composition,
    split_diseases,
    split_semicolon,
    stable_id,
    unique_preserve_order,
)


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    default_source_root = repo_root.parent / "polysaccharidesdb"
    parser = argparse.ArgumentParser(description="Build DoLPHiN KG v0 CSV exports")
    parser.add_argument(
        "--dataset-jsonl",
        type=Path,
        default=default_source_root / "data_processed" / "dataset_dolphin_only.jsonl",
    )
    parser.add_argument(
        "--raw-jsonl",
        type=Path,
        default=default_source_root / "data_interim" / "dolphin_raw_records.jsonl",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repo_root / "data" / "processed" / "neo4j",
    )
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            records.append(json.loads(line))
    return records


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_neo4j_node_csv(path: Path, rows: list[dict], id_field: str, label: str, property_fields: list[str]) -> None:
    neo4j_rows: list[dict] = []
    fieldnames = [f"{id_field}:ID", ":LABEL", *property_fields]
    for row in rows:
        neo4j_row = {f"{id_field}:ID": row[id_field], ":LABEL": label}
        for field in property_fields:
            neo4j_row[field] = row.get(field, "")
        neo4j_rows.append(neo4j_row)
    write_csv(path, neo4j_rows, fieldnames)


def write_neo4j_edge_csv(path: Path, rows: list[dict], extra_fields: list[str]) -> None:
    neo4j_rows: list[dict] = []
    fieldnames = [":START_ID", ":END_ID", ":TYPE", *extra_fields]
    for row in rows:
        neo4j_row = {
            ":START_ID": row["source_id"],
            ":END_ID": row["target_id"],
            ":TYPE": row["edge_type"],
        }
        for field in extra_fields:
            neo4j_row[field] = row.get(field, "")
        neo4j_rows.append(neo4j_row)
    write_csv(path, neo4j_rows, fieldnames)


def build_graph(dataset_records: list[dict], raw_by_id: dict[str, dict]) -> dict[str, list[dict]]:
    polysaccharides: list[dict] = []
    organisms: dict[str, dict] = {}
    monosaccharides: dict[str, dict] = {}
    bonds: dict[str, dict] = {}
    functions: dict[str, dict] = {}
    diseases: dict[str, dict] = {}
    publications: dict[str, dict] = {}

    edge_poly_organism: list[dict] = []
    edge_poly_mono: list[dict] = []
    edge_poly_bond: list[dict] = []
    edge_poly_function: list[dict] = []
    edge_poly_disease: list[dict] = []
    edge_poly_publication: list[dict] = []

    for record in dataset_records:
        poly_id = record["poly_id"]
        raw_record = raw_by_id.get(record["source_record_id"], {})

        polysaccharides.append(
            {
                "poly_id": poly_id,
                "source_db": record.get("source_db", ""),
                "source_record_id": record.get("source_record_id", ""),
                "name": clean_text(raw_record.get("polysaccharide_name", "")),
                "raw_representation": record.get("raw_representation", ""),
                "canonical_representation": record.get("canonical_representation", ""),
                "mw_or_range_raw": record.get("mw_or_range", ""),
                "branching_raw": record.get("branching", ""),
            }
        )

        organism_name = clean_text(record.get("organism_source", ""))
        if organism_name:
            organism_id = stable_id("organism", organism_name.lower())
            organisms.setdefault(
                organism_id,
                {
                    "organism_id": organism_id,
                    "organism_name_raw": organism_name,
                    "organism_name_norm": organism_name,
                    "taxonomy_id": "",
                    "kingdom": "",
                },
            )
            edge_poly_organism.append(
                {"source_id": poly_id, "target_id": organism_id, "edge_type": "ISOLATED_FROM"}
            )

        for mono_name, ratio in parse_monomer_composition(record.get("monomer_composition")):
            mono_id = stable_id("mono", mono_name)
            monosaccharides.setdefault(
                mono_id,
                {
                    "monosaccharide_id": mono_id,
                    "mono_name_raw": mono_name,
                    "mono_name_norm": mono_name,
                    "mono_family": "",
                },
            )
            edge_poly_mono.append(
                {
                    "source_id": poly_id,
                    "target_id": mono_id,
                    "edge_type": "HAS_MONOSACCHARIDE",
                    "ratio_percent": f"{ratio:.2f}",
                }
            )

        for bond_text in unique_preserve_order(
            normalize_bond(value) for value in split_semicolon(record.get("linkage"))
        ):
            if not bond_text:
                continue
            bond_id = stable_id("bond", bond_text.lower())
            bonds.setdefault(
                bond_id,
                {
                    "bond_id": bond_id,
                    "bond_text_raw": bond_text,
                    "bond_signature": bond_text,
                    "anomericity": "alpha" if "alpha" in bond_text.lower() else ("beta" if "beta" in bond_text.lower() else ""),
                    "donor_residue": "",
                    "acceptor_position": "",
                },
            )
            edge_poly_bond.append(
                {"source_id": poly_id, "target_id": bond_id, "edge_type": "HAS_GLYCOSIDIC_BOND"}
            )

        for function_label in record.get("function_label", []):
            function_name = normalize_function(function_label)
            if not function_name:
                continue
            function_id = stable_id("function", function_name)
            functions.setdefault(
                function_id,
                {
                    "function_id": function_id,
                    "function_name_norm": function_name,
                    "function_group": "",
                },
            )
            edge_poly_function.append(
                {
                    "source_id": poly_id,
                    "target_id": function_id,
                    "edge_type": "ASSOCIATED_WITH_FUNCTION",
                    "source_db": record.get("source_db", ""),
                }
            )

        for disease_name in split_diseases(raw_record.get("related_diseases")):
            disease_id = stable_id("disease", disease_name.lower())
            diseases.setdefault(
                disease_id,
                {
                    "disease_id": disease_id,
                    "disease_name_raw": disease_name,
                    "disease_name_norm": disease_name,
                    "icd11_code": extract_disease_code(disease_name),
                    "disease_group": "",
                },
            )
            edge_poly_disease.append(
                {
                    "source_id": poly_id,
                    "target_id": disease_id,
                    "edge_type": "ASSOCIATED_WITH_DISEASE",
                    "source_db": record.get("source_db", ""),
                }
            )

        doi = clean_text(record.get("doi"))
        if doi:
            publications.setdefault(doi, {"doi": doi, "title": "", "year": "", "journal": ""})
            edge_poly_publication.append(
                {
                    "source_id": poly_id,
                    "target_id": doi,
                    "edge_type": "SUPPORTED_BY",
                    "source_record_id": record.get("source_record_id", ""),
                }
            )

    return {
        "nodes_polysaccharide": polysaccharides,
        "nodes_organism": list(organisms.values()),
        "nodes_monosaccharide": list(monosaccharides.values()),
        "nodes_bond": list(bonds.values()),
        "nodes_function": list(functions.values()),
        "nodes_disease": list(diseases.values()),
        "nodes_publication": list(publications.values()),
        "edges_poly_organism": edge_poly_organism,
        "edges_poly_mono": edge_poly_mono,
        "edges_poly_bond": edge_poly_bond,
        "edges_poly_function": edge_poly_function,
        "edges_poly_disease": edge_poly_disease,
        "edges_poly_publication": edge_poly_publication,
    }


def main() -> None:
    args = parse_args()
    dataset_records = load_jsonl(args.dataset_jsonl)
    raw_records = load_jsonl(args.raw_jsonl)
    raw_by_id = {record["source_record_id"]: record for record in raw_records}
    graph = build_graph(dataset_records, raw_by_id)

    node_dir = args.output_dir / "nodes"
    edge_dir = args.output_dir / "edges"
    neo4j_bulk_dir = args.output_dir / "bulk_import"

    write_csv(
        node_dir / "polysaccharide.csv",
        graph["nodes_polysaccharide"],
        [
            "poly_id",
            "source_db",
            "source_record_id",
            "name",
            "raw_representation",
            "canonical_representation",
            "mw_or_range_raw",
            "branching_raw",
        ],
    )
    write_csv(
        node_dir / "organism.csv",
        graph["nodes_organism"],
        ["organism_id", "organism_name_raw", "organism_name_norm", "taxonomy_id", "kingdom"],
    )
    write_csv(
        node_dir / "monosaccharide.csv",
        graph["nodes_monosaccharide"],
        ["monosaccharide_id", "mono_name_raw", "mono_name_norm", "mono_family"],
    )
    write_csv(
        node_dir / "glycosidic_bond.csv",
        graph["nodes_bond"],
        ["bond_id", "bond_text_raw", "bond_signature", "anomericity", "donor_residue", "acceptor_position"],
    )
    write_csv(
        node_dir / "function.csv",
        graph["nodes_function"],
        ["function_id", "function_name_norm", "function_group"],
    )
    write_csv(
        node_dir / "disease.csv",
        graph["nodes_disease"],
        ["disease_id", "disease_name_raw", "disease_name_norm", "icd11_code", "disease_group"],
    )
    write_csv(
        node_dir / "publication.csv",
        graph["nodes_publication"],
        ["doi", "title", "year", "journal"],
    )

    write_neo4j_node_csv(
        neo4j_bulk_dir / "nodes" / "polysaccharide.csv",
        graph["nodes_polysaccharide"],
        "poly_id",
        "Polysaccharide",
        [
            "source_db",
            "source_record_id",
            "name",
            "raw_representation",
            "canonical_representation",
            "mw_or_range_raw",
            "branching_raw",
        ],
    )
    write_neo4j_node_csv(
        neo4j_bulk_dir / "nodes" / "organism.csv",
        graph["nodes_organism"],
        "organism_id",
        "Organism",
        ["organism_name_raw", "organism_name_norm", "taxonomy_id", "kingdom"],
    )
    write_neo4j_node_csv(
        neo4j_bulk_dir / "nodes" / "monosaccharide.csv",
        graph["nodes_monosaccharide"],
        "monosaccharide_id",
        "Monosaccharide",
        ["mono_name_raw", "mono_name_norm", "mono_family"],
    )
    write_neo4j_node_csv(
        neo4j_bulk_dir / "nodes" / "glycosidic_bond.csv",
        graph["nodes_bond"],
        "bond_id",
        "GlycosidicBond",
        ["bond_text_raw", "bond_signature", "anomericity", "donor_residue", "acceptor_position"],
    )
    write_neo4j_node_csv(
        neo4j_bulk_dir / "nodes" / "function.csv",
        graph["nodes_function"],
        "function_id",
        "Function",
        ["function_name_norm", "function_group"],
    )
    write_neo4j_node_csv(
        neo4j_bulk_dir / "nodes" / "disease.csv",
        graph["nodes_disease"],
        "disease_id",
        "Disease",
        ["disease_name_raw", "disease_name_norm", "icd11_code", "disease_group"],
    )
    write_neo4j_node_csv(
        neo4j_bulk_dir / "nodes" / "publication.csv",
        graph["nodes_publication"],
        "doi",
        "Publication",
        ["title", "year", "journal"],
    )

    write_csv(edge_dir / "poly_organism.csv", graph["edges_poly_organism"], ["source_id", "target_id", "edge_type"])
    write_csv(edge_dir / "poly_monosaccharide.csv", graph["edges_poly_mono"], ["source_id", "target_id", "edge_type", "ratio_percent"])
    write_csv(edge_dir / "poly_bond.csv", graph["edges_poly_bond"], ["source_id", "target_id", "edge_type"])
    write_csv(edge_dir / "poly_function.csv", graph["edges_poly_function"], ["source_id", "target_id", "edge_type", "source_db"])
    write_csv(edge_dir / "poly_disease.csv", graph["edges_poly_disease"], ["source_id", "target_id", "edge_type", "source_db"])
    write_csv(edge_dir / "poly_publication.csv", graph["edges_poly_publication"], ["source_id", "target_id", "edge_type", "source_record_id"])

    write_neo4j_edge_csv(neo4j_bulk_dir / "edges" / "poly_organism.csv", graph["edges_poly_organism"], [])
    write_neo4j_edge_csv(neo4j_bulk_dir / "edges" / "poly_monosaccharide.csv", graph["edges_poly_mono"], ["ratio_percent"])
    write_neo4j_edge_csv(neo4j_bulk_dir / "edges" / "poly_bond.csv", graph["edges_poly_bond"], [])
    write_neo4j_edge_csv(neo4j_bulk_dir / "edges" / "poly_function.csv", graph["edges_poly_function"], ["source_db"])
    write_neo4j_edge_csv(neo4j_bulk_dir / "edges" / "poly_disease.csv", graph["edges_poly_disease"], ["source_db"])
    write_neo4j_edge_csv(neo4j_bulk_dir / "edges" / "poly_publication.csv", graph["edges_poly_publication"], ["source_record_id"])

    stats = {
        "nodes": {
            "polysaccharide": len(graph["nodes_polysaccharide"]),
            "organism": len(graph["nodes_organism"]),
            "monosaccharide": len(graph["nodes_monosaccharide"]),
            "glycosidic_bond": len(graph["nodes_bond"]),
            "function": len(graph["nodes_function"]),
            "disease": len(graph["nodes_disease"]),
            "publication": len(graph["nodes_publication"]),
        },
        "edges": {
            "poly_organism": len(graph["edges_poly_organism"]),
            "poly_monosaccharide": len(graph["edges_poly_mono"]),
            "poly_bond": len(graph["edges_poly_bond"]),
            "poly_function": len(graph["edges_poly_function"]),
            "poly_disease": len(graph["edges_poly_disease"]),
            "poly_publication": len(graph["edges_poly_publication"]),
        },
    }
    stats_path = args.output_dir / "kg_stats.json"
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    stats_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    report_lines = [
        "# KG Build Report",
        "",
        "## Nodes",
        *(f"- {name}: {count}" for name, count in stats["nodes"].items()),
        "",
        "## Edges",
        *(f"- {name}: {count}" for name, count in stats["edges"].items()),
        "",
        "## Notes",
        "- disease nodes reflect split base categories, not raw multi-disease strings",
        "- Neo4j bulk import files are written under `bulk_import/`",
        "- publication nodes currently use DOI only; title/year/journal are placeholders",
    ]
    (args.output_dir / "kg_build_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
