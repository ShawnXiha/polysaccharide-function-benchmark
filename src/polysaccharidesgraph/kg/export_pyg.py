"""Export the DoLPHiN KG as a PyG HeteroData training payload."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import torch
from torch_geometric.data import HeteroData

from polysaccharidesgraph.kg.feature_schema import build_poly_feature_schema
from polysaccharidesgraph.kg.normalize import clean_text


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    source_root = repo_root.parent / "polysaccharidesdb"
    parser = argparse.ArgumentParser(description="Export DoLPHiN KG to PyG HeteroData")
    parser.add_argument(
        "--kg-dir",
        type=Path,
        default=repo_root / "data" / "processed" / "neo4j",
    )
    parser.add_argument(
        "--dataset-jsonl",
        type=Path,
        default=source_root / "data_processed" / "dataset_dolphin_only.jsonl",
    )
    parser.add_argument(
        "--split-json",
        type=Path,
        default=source_root / "data_processed" / "splits_dolphin_only" / "random_split.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "data" / "processed" / "pyg" / "dolphin_kg_v0.pt",
    )
    parser.add_argument(
        "--include-disease-edges",
        action="store_true",
        help="Include polysaccharide-disease edges in message passing graph",
    )
    return parser.parse_args()


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            rows.append(json.loads(line))
    return rows


def build_edge_index(rows: list[dict], src_map: dict[str, int], dst_map: dict[str, int]) -> torch.Tensor:
    edges = []
    for row in rows:
        src = row["source_id"]
        dst = row["target_id"]
        if src in src_map and dst in dst_map:
            edges.append([src_map[src], dst_map[dst]])
    if not edges:
        return torch.empty((2, 0), dtype=torch.long)
    return torch.tensor(edges, dtype=torch.long).t().contiguous()


def build_masks(poly_ids: list[str], split_payload: dict) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    poly_index = {poly_id: idx for idx, poly_id in enumerate(poly_ids)}
    train_mask = torch.zeros(len(poly_ids), dtype=torch.bool)
    valid_mask = torch.zeros(len(poly_ids), dtype=torch.bool)
    test_mask = torch.zeros(len(poly_ids), dtype=torch.bool)

    for poly_id in split_payload.get("train", []):
        if poly_id in poly_index:
            train_mask[poly_index[poly_id]] = True
    for poly_id in split_payload.get("valid", []):
        if poly_id in poly_index:
            valid_mask[poly_index[poly_id]] = True
    for poly_id in split_payload.get("test", []):
        if poly_id in poly_index:
            test_mask[poly_index[poly_id]] = True
    return train_mask, valid_mask, test_mask


def parse_mw_signal(value: str) -> float:
    text = clean_text(value).lower().replace(",", "")
    numbers = [float(match) for match in re.findall(r"\d+(?:\.\d+)?", text)]
    if not numbers:
        return 0.0
    mw = numbers[0]
    if "10 3" in text or "10^3" in text or "kda" in text:
        return mw
    return mw


def branching_flags(value: str) -> list[float]:
    text = clean_text(value).lower()
    if not text:
        return [0.0, 0.0, 0.0]
    no_info = "no relevant information" in text
    has_branch_text = not no_info and len(text) > 0
    return [
        1.0 if has_branch_text else 0.0,
        1.0 if no_info else 0.0,
        float(min(len(text), 200)) / 200.0,
    ]


def main() -> None:
    args = parse_args()
    node_dir = args.kg_dir / "nodes"
    edge_dir = args.kg_dir / "edges"

    polys = read_csv(node_dir / "polysaccharide.csv")
    organisms = read_csv(node_dir / "organism.csv")
    monos = read_csv(node_dir / "monosaccharide.csv")
    bonds = read_csv(node_dir / "glycosidic_bond.csv")
    diseases = read_csv(node_dir / "disease.csv")
    publications = read_csv(node_dir / "publication.csv")

    poly_ids = [row["poly_id"] for row in polys]
    organism_ids = [row["organism_id"] for row in organisms]
    mono_ids = [row["monosaccharide_id"] for row in monos]
    bond_ids = [row["bond_id"] for row in bonds]
    disease_ids = [row["disease_id"] for row in diseases]
    publication_ids = [row["doi"] for row in publications]

    poly_map = {node_id: idx for idx, node_id in enumerate(poly_ids)}
    organism_map = {node_id: idx for idx, node_id in enumerate(organism_ids)}
    mono_map = {node_id: idx for idx, node_id in enumerate(mono_ids)}
    bond_map = {node_id: idx for idx, node_id in enumerate(bond_ids)}
    disease_map = {node_id: idx for idx, node_id in enumerate(disease_ids)}
    publication_map = {node_id: idx for idx, node_id in enumerate(publication_ids)}

    dataset_records = load_jsonl(args.dataset_jsonl)
    label_names = sorted(
        {
            clean_text(label)
            for record in dataset_records
            for label in record.get("function_label", [])
            if clean_text(label)
        }
    )
    label_to_idx = {label: idx for idx, label in enumerate(label_names)}
    poly_label_map = {record["poly_id"]: record.get("function_label", []) for record in dataset_records}

    data = HeteroData()
    data["polysaccharide"].node_id = torch.arange(len(poly_ids), dtype=torch.long)
    data["organism"].node_id = torch.arange(len(organism_ids), dtype=torch.long)
    data["monosaccharide"].node_id = torch.arange(len(mono_ids), dtype=torch.long)
    data["glycosidic_bond"].node_id = torch.arange(len(bond_ids), dtype=torch.long)
    data["disease"].node_id = torch.arange(len(disease_ids), dtype=torch.long)
    data["publication"].node_id = torch.arange(len(publication_ids), dtype=torch.long)

    edge_rows = {
        "organism": read_csv(edge_dir / "poly_organism.csv"),
        "monosaccharide": read_csv(edge_dir / "poly_monosaccharide.csv"),
        "glycosidic_bond": read_csv(edge_dir / "poly_bond.csv"),
        "publication": read_csv(edge_dir / "poly_publication.csv"),
        "disease": read_csv(edge_dir / "poly_disease.csv"),
    }
    poly_degree_counts: dict[str, dict[str, int]] = {poly_id: {} for poly_id in poly_ids}
    for relation_name, rows in edge_rows.items():
        counts: dict[str, int] = {}
        for row in rows:
            counts[row["source_id"]] = counts.get(row["source_id"], 0) + 1
        for poly_id in poly_ids:
            poly_degree_counts[poly_id][relation_name] = counts.get(poly_id, 0)

    mono_ratio_map: dict[str, dict[str, float]] = {poly_id: {} for poly_id in poly_ids}
    for row in edge_rows["monosaccharide"]:
        poly_id = row["source_id"]
        mono_id = row["target_id"]
        ratio = float(row.get("ratio_percent", 0.0) or 0.0)
        mono_ratio_map.setdefault(poly_id, {})[mono_id] = ratio / 100.0

    bond_presence_map: dict[str, set[str]] = {poly_id: set() for poly_id in poly_ids}
    for row in edge_rows["glycosidic_bond"]:
        bond_presence_map.setdefault(row["source_id"], set()).add(row["target_id"])

    poly_row_map = {row["poly_id"]: row for row in polys}
    poly_feature_schema = build_poly_feature_schema(
        mono_ids=mono_ids,
        bond_ids=bond_ids,
        include_disease_features=args.include_disease_edges,
    )
    poly_x = []
    for poly_id in poly_ids:
        poly_row = poly_row_map[poly_id]
        base_features = [
            float(poly_degree_counts[poly_id]["organism"]),
            float(poly_degree_counts[poly_id]["monosaccharide"]),
            float(poly_degree_counts[poly_id]["glycosidic_bond"]),
            float(poly_degree_counts[poly_id]["publication"]),
        ]
        if args.include_disease_edges:
            base_features.append(float(poly_degree_counts[poly_id]["disease"]))
        base_features.append(parse_mw_signal(poly_row.get("mw_or_range_raw", "")))
        branch_features = branching_flags(poly_row.get("branching_raw", ""))
        mono_features = [mono_ratio_map.get(poly_id, {}).get(mono_id, 0.0) for mono_id in mono_ids]
        bond_features = [1.0 if bond_id in bond_presence_map.get(poly_id, set()) else 0.0 for bond_id in bond_ids]
        poly_x.append(base_features + branch_features + mono_features + bond_features)
    data["polysaccharide"].x = torch.tensor(poly_x, dtype=torch.float)
    if len(poly_feature_schema) != int(data["polysaccharide"].x.size(1)):
        raise RuntimeError(
            "Polysaccharide feature schema length does not match exported tensor width: "
            f"{len(poly_feature_schema)} != {int(data['polysaccharide'].x.size(1))}"
        )

    for node_type in ["organism", "monosaccharide", "glycosidic_bond", "disease", "publication"]:
        num_nodes = data[node_type].node_id.numel()
        data[node_type].x = torch.ones((num_nodes, 1), dtype=torch.float)

    y = torch.zeros((len(poly_ids), len(label_names)), dtype=torch.float)
    for poly_id, labels in poly_label_map.items():
        if poly_id not in poly_map:
            continue
        row_idx = poly_map[poly_id]
        for label in labels:
            label = clean_text(label)
            if label in label_to_idx:
                y[row_idx, label_to_idx[label]] = 1.0
    data["polysaccharide"].y = y

    split_payload = json.loads(args.split_json.read_text(encoding="utf-8"))
    train_mask, valid_mask, test_mask = build_masks(poly_ids, split_payload)
    data["polysaccharide"].train_mask = train_mask
    data["polysaccharide"].valid_mask = valid_mask
    data["polysaccharide"].test_mask = test_mask

    relation_specs = [
        ("isolated_from", "organism", edge_rows["organism"], organism_map),
        ("has_monosaccharide", "monosaccharide", edge_rows["monosaccharide"], mono_map),
        ("has_glycosidic_bond", "glycosidic_bond", edge_rows["glycosidic_bond"], bond_map),
        ("supported_by", "publication", edge_rows["publication"], publication_map),
    ]
    if args.include_disease_edges:
        relation_specs.append(("associated_with_disease", "disease", edge_rows["disease"], disease_map))

    for rel_name, target_type, rows, target_map in relation_specs:
        edge_index = build_edge_index(rows, poly_map, target_map)
        data["polysaccharide", rel_name, target_type].edge_index = edge_index
        data[target_type, f"rev_{rel_name}", "polysaccharide"].edge_index = edge_index.flip(0)

    payload = {
        "data": data,
        "metadata": {
            "label_names": label_names,
            "poly_ids": poly_ids,
            "include_disease_edges": args.include_disease_edges,
            "poly_feature_names": [item["name"] for item in poly_feature_schema],
            "poly_feature_schema_path": str(args.output.with_suffix(".feature_schema.json")),
            "split_json": str(args.split_json),
            "dataset_jsonl": str(args.dataset_jsonl),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(payload, args.output)
    feature_schema_payload = {
        "output": str(args.output),
        "include_disease_edges": args.include_disease_edges,
        "poly_feature_dim": int(data["polysaccharide"].x.size(1)),
        "num_disease_derived_poly_features": sum(
            1 for item in poly_feature_schema if item.get("disease_derived")
        ),
        "poly_feature_schema": poly_feature_schema,
    }
    schema_path = args.output.with_suffix(".feature_schema.json")
    schema_path.write_text(json.dumps(feature_schema_payload, indent=2), encoding="utf-8")
    summary = {
        "output": str(args.output),
        "node_types": {node_type: int(data[node_type].node_id.numel()) for node_type in data.node_types},
        "edge_types": {
            "__".join(edge_type): int(data[edge_type].edge_index.size(1))
            for edge_type in data.edge_types
        },
        "num_labels": len(label_names),
        "include_disease_edges": args.include_disease_edges,
        "num_disease_derived_poly_features": feature_schema_payload["num_disease_derived_poly_features"],
        "poly_feature_schema": str(schema_path),
        "train_nodes": int(train_mask.sum().item()),
        "valid_nodes": int(valid_mask.sum().item()),
        "test_nodes": int(test_mask.sum().item()),
        "poly_feature_dim": int(data["polysaccharide"].x.size(1)),
    }
    summary_path = args.output.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
