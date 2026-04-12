"""Shared graph-derived feature builders for meta-path style baselines."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.feature_extraction import DictVectorizer


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_adjacency(rows: list[dict]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    poly_to_neighbor: dict[str, set[str]] = defaultdict(set)
    neighbor_to_poly: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        poly_id = row["source_id"]
        neighbor_id = row["target_id"]
        poly_to_neighbor[poly_id].add(neighbor_id)
        neighbor_to_poly[neighbor_id].add(poly_id)
    return poly_to_neighbor, neighbor_to_poly


def build_feature_dicts(
    poly_ids: list[str],
    kg_dir: Path,
    include_disease_features: bool = False,
) -> dict[str, dict[str, float]]:
    edge_dir = kg_dir / "edges"
    relation_files = [
        ("organism", "poly_organism.csv"),
        ("monosaccharide", "poly_monosaccharide.csv"),
        ("bond", "poly_bond.csv"),
        ("publication", "poly_publication.csv"),
    ]
    if include_disease_features:
        relation_files.append(("disease", "poly_disease.csv"))

    features = {poly_id: {} for poly_id in poly_ids}

    for relation_name, filename in relation_files:
        rows = read_csv(edge_dir / filename)
        poly_to_neighbor, neighbor_to_poly = build_adjacency(rows)
        for poly_id in poly_ids:
            neighbors = poly_to_neighbor.get(poly_id, set())
            features[poly_id][f"{relation_name}__degree"] = float(len(neighbors))
            shared_polys: set[str] = set()
            for neighbor_id in neighbors:
                features[poly_id][f"{relation_name}__{neighbor_id}"] = 1.0
                shared_polys.update(neighbor_to_poly.get(neighbor_id, set()))
            shared_polys.discard(poly_id)
            features[poly_id][f"{relation_name}__shared_poly_count"] = float(len(shared_polys))

    return features


def vectorize_feature_dicts(
    poly_ids: list[str],
    feature_dicts: dict[str, dict[str, float]],
) -> tuple[np.ndarray, DictVectorizer]:
    vectorizer = DictVectorizer(sparse=False)
    matrix = vectorizer.fit_transform([feature_dicts[poly_id] for poly_id in poly_ids])
    return matrix.astype(np.float32), vectorizer
