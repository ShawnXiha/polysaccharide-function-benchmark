"""Run masked poly-function link prediction baselines on the DoLPHiN KG."""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from statistics import mean

import numpy as np

from polysaccharidesgraph.models.meta_path_features import build_feature_dicts, vectorize_feature_dicts


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Run masked poly-function link prediction")
    parser.add_argument(
        "--kg-dir",
        type=Path,
        default=repo_root / "data" / "processed" / "neo4j",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "experiments" / "poly_function_link_prediction_clean.json",
    )
    parser.add_argument("--include-disease-features", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-eval", type=int, default=1000)
    parser.add_argument("--save-edge-records", action="store_true")
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--label-idf-weighting", action="store_true")
    parser.add_argument("--rare-label-expansion", action="store_true")
    parser.add_argument("--rare-label-threshold", type=int, default=10)
    parser.add_argument("--rare-label-top-k", type=int, default=50)
    parser.add_argument("--rare-label-decay", type=float, default=0.5)
    parser.add_argument("--source-constrained-rerank", action="store_true")
    parser.add_argument("--source-rerank-top-n", type=int, default=10)
    parser.add_argument("--source-rerank-weight", type=float, default=1.0)
    parser.add_argument("--source-cluster-backoff", action="store_true")
    parser.add_argument("--source-cluster-top-n", type=int, default=10)
    parser.add_argument("--source-cluster-exact-weight", type=float, default=1.0)
    parser.add_argument("--source-cluster-genus-weight", type=float, default=0.6)
    parser.add_argument("--source-cluster-kingdom-weight", type=float, default=0.3)
    parser.add_argument("--tail-candidate-generation", action="store_true")
    parser.add_argument("--tail-label-threshold", type=int, default=10)
    parser.add_argument("--tail-candidate-top-k", type=int, default=75)
    parser.add_argument("--tail-candidate-limit", type=int, default=5)
    parser.add_argument("--tail-candidate-activation", type=float, default=1.0)
    parser.add_argument("--tail-candidate-source-exact-weight", type=float, default=1.0)
    parser.add_argument("--tail-candidate-source-genus-weight", type=float, default=0.6)
    parser.add_argument("--tail-candidate-source-kingdom-weight", type=float, default=0.3)
    parser.add_argument("--label-specific-backoff", action="store_true")
    parser.add_argument("--label-backoff-threshold", type=int, default=10)
    parser.add_argument("--label-backoff-top-n", type=int, default=15)
    parser.add_argument("--label-backoff-weight", type=float, default=0.5)
    parser.add_argument("--label-backoff-exact-weight", type=float, default=1.0)
    parser.add_argument("--label-backoff-genus-weight", type=float, default=0.6)
    parser.add_argument("--label-backoff-kingdom-weight", type=float, default=0.3)
    parser.add_argument("--disease-label-prior", action="store_true")
    parser.add_argument("--disease-prior-top-n", type=int, default=15)
    parser.add_argument("--disease-prior-weight", type=float, default=0.5)
    parser.add_argument("--disease-prior-alpha", type=float, default=1.0)
    parser.add_argument("--tail-aware-disease-prior", action="store_true")
    parser.add_argument("--tail-disease-prior-top-n", type=int, default=30)
    parser.add_argument("--tail-disease-prior-threshold", type=int, default=10)
    parser.add_argument("--tail-disease-prior-weight", type=float, default=1.0)
    parser.add_argument("--tail-disease-prior-boost", type=float, default=2.0)
    parser.add_argument("--tail-disease-prior-max-multiplier", type=float, default=4.0)
    parser.add_argument("--label-prototype-refinement", action="store_true")
    parser.add_argument("--prototype-top-n", type=int, default=15)
    parser.add_argument("--prototype-neighbors", type=int, default=5)
    parser.add_argument("--prototype-weight", type=float, default=0.5)
    parser.add_argument("--prototype-tail-threshold", type=int, default=10)
    parser.add_argument("--prototype-tail-boost", type=float, default=1.0)
    parser.add_argument("--frequency-adjusted-disease-prior", action="store_true")
    parser.add_argument("--freq-disease-prior-top-n", type=int, default=20)
    parser.add_argument("--freq-disease-prior-weight", type=float, default=1.0)
    parser.add_argument("--freq-disease-prior-strength", type=float, default=0.5)
    parser.add_argument("--freq-disease-prior-mode", choices=["divide", "subtract"], default="divide")
    parser.add_argument("--support-aware-candidate-generation", action="store_true")
    parser.add_argument("--support-candidate-top-k", type=int, default=75)
    parser.add_argument("--support-candidate-base-window", type=int, default=20)
    parser.add_argument("--support-candidate-threshold", type=int, default=50)
    parser.add_argument("--support-candidate-limit", type=int, default=6)
    parser.add_argument("--support-candidate-activation", type=float, default=0.3)
    parser.add_argument("--support-candidate-exact-weight", type=float, default=1.0)
    parser.add_argument("--support-candidate-genus-weight", type=float, default=0.6)
    parser.add_argument("--support-candidate-kingdom-weight", type=float, default=0.3)
    parser.add_argument("--integrated-support-aware-knn", action="store_true")
    parser.add_argument("--integrated-support-top-k", type=int, default=25)
    parser.add_argument("--integrated-support-extended-k", type=int, default=100)
    parser.add_argument("--integrated-support-threshold", type=int, default=50)
    parser.add_argument("--integrated-support-decay", type=float, default=0.35)
    parser.add_argument("--integrated-support-exact-weight", type=float, default=1.0)
    parser.add_argument("--integrated-support-genus-weight", type=float, default=0.6)
    parser.add_argument("--integrated-support-kingdom-weight", type=float, default=0.3)
    parser.add_argument("--explicit-tail-support-knn", action="store_true")
    parser.add_argument("--tail-support-top-k", type=int, default=25)
    parser.add_argument("--tail-support-extended-k", type=int, default=150)
    parser.add_argument("--tail-support-threshold", type=int, default=10)
    parser.add_argument("--tail-support-decay", type=float, default=0.75)
    parser.add_argument("--tail-support-exact-weight", type=float, default=1.0)
    parser.add_argument("--tail-support-genus-weight", type=float, default=0.8)
    parser.add_argument("--tail-support-kingdom-weight", type=float, default=0.5)
    parser.add_argument("--tail-support-boost", type=float, default=2.0)
    parser.add_argument("--disease-conditioned-base-vote", action="store_true")
    parser.add_argument("--disease-vote-top-k", type=int, default=25)
    parser.add_argument("--disease-vote-weight", type=float, default=0.5)
    parser.add_argument("--disease-vote-max-boost", type=float, default=3.0)
    parser.add_argument("--tail-structural-signature", action="store_true")
    parser.add_argument("--tail-signature-threshold", type=int, default=10)
    parser.add_argument("--tail-signature-top-n", type=int, default=20)
    parser.add_argument("--tail-signature-feature-limit", type=int, default=12)
    parser.add_argument("--tail-signature-weight", type=float, default=0.5)
    parser.add_argument("--tail-signature-min-local-rate", type=float, default=0.25)
    parser.add_argument("--tail-signature-max-boost", type=float, default=2.0)
    parser.add_argument("--structure-aware-candidate-generation", action="store_true")
    parser.add_argument("--structure-candidate-base-window", type=int, default=20)
    parser.add_argument("--structure-candidate-threshold", type=int, default=10)
    parser.add_argument("--structure-candidate-limit", type=int, default=5)
    parser.add_argument("--structure-candidate-activation", type=float, default=0.5)
    parser.add_argument("--label-specific-subgraph-motifs", action="store_true")
    parser.add_argument("--motif-threshold", type=int, default=10)
    parser.add_argument("--motif-feature-limit", type=int, default=20)
    parser.add_argument("--motif-min-local-rate", type=float, default=0.2)
    parser.add_argument("--motif-candidate-base-window", type=int, default=20)
    parser.add_argument("--motif-candidate-limit", type=int, default=5)
    parser.add_argument("--motif-candidate-activation", type=float, default=0.75)
    parser.add_argument("--taxonomy-conditioned-motifs", action="store_true")
    parser.add_argument("--taxonomy-motif-threshold", type=int, default=10)
    parser.add_argument("--taxonomy-motif-feature-limit", type=int, default=20)
    parser.add_argument("--taxonomy-motif-min-local-rate", type=float, default=0.2)
    parser.add_argument("--taxonomy-motif-base-window", type=int, default=20)
    parser.add_argument("--taxonomy-motif-candidate-limit", type=int, default=5)
    parser.add_argument("--taxonomy-motif-activation", type=float, default=1.0)
    parser.add_argument(
        "--hierarchy-config",
        type=Path,
        default=repo_root / "configs" / "function_hierarchy_v1.json",
    )
    parser.add_argument("--hierarchy-support", action="store_true")
    parser.add_argument("--hierarchy-base-window", type=int, default=20)
    parser.add_argument("--hierarchy-threshold", type=int, default=10)
    parser.add_argument("--hierarchy-candidate-limit", type=int, default=5)
    parser.add_argument("--hierarchy-activation", type=float, default=0.75)
    parser.add_argument("--hierarchy-min-seed-count", type=int, default=1)
    parser.add_argument("--hierarchy-specificity-power", type=float, default=1.0)
    parser.add_argument("--hierarchy-graph-native", action="store_true")
    parser.add_argument("--hierarchy-graph-weight", type=float, default=0.1)
    parser.add_argument("--hierarchy-parent-child-native", action="store_true")
    parser.add_argument("--hierarchy-confidence-threshold", type=float, default=0.0)
    parser.add_argument("--hierarchy-adaptive-power", type=float, default=1.0)
    return parser.parse_args()


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def build_knn_scores(
    poly_id: str,
    poly_ids: list[str],
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    train_poly_to_functions: dict[str, list[str]],
    function_ids: list[str],
    label_weights: dict[str, float],
    top_k: int = 50,
) -> dict[str, float]:
    target = feature_matrix[poly_idx[poly_id]]
    similarities: list[tuple[str, float]] = []
    for other_poly_id in poly_ids:
        if other_poly_id == poly_id:
            continue
        labels = train_poly_to_functions.get(other_poly_id, [])
        if not labels:
            continue
        sim = cosine_similarity(target, feature_matrix[poly_idx[other_poly_id]])
        similarities.append((other_poly_id, sim))
    similarities.sort(key=lambda item: (-item[1], item[0]))
    scores = {function_id: 0.0 for function_id in function_ids}
    for other_poly_id, sim in similarities[:top_k]:
        for function_id in train_poly_to_functions.get(other_poly_id, []):
            scores[function_id] += max(sim, 0.0) * label_weights.get(function_id, 1.0)
    return scores


def build_integrated_support_aware_knn_scores(
    poly_id: str,
    poly_ids: list[str],
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    train_poly_to_functions: dict[str, list[str]],
    function_ids: list[str],
    label_weights: dict[str, float],
    function_frequency: Counter,
    poly_to_organisms: dict[str, set[str]],
    organism_to_genus: dict[str, str],
    organism_to_kingdom: dict[str, str],
    base_top_k: int,
    extended_top_k: int,
    support_threshold: int,
    expansion_decay: float,
    exact_weight: float,
    genus_weight: float,
    kingdom_weight: float,
) -> dict[str, float]:
    target = feature_matrix[poly_idx[poly_id]]
    query_organisms = poly_to_organisms.get(poly_id, set())
    similarities: list[tuple[str, float]] = []
    for other_poly_id in poly_ids:
        if other_poly_id == poly_id:
            continue
        labels = train_poly_to_functions.get(other_poly_id, [])
        if not labels:
            continue
        sim = cosine_similarity(target, feature_matrix[poly_idx[other_poly_id]])
        similarities.append((other_poly_id, sim))
    similarities.sort(key=lambda item: (-item[1], item[0]))

    scores = {function_id: 0.0 for function_id in function_ids}
    max_rank = max(base_top_k, extended_top_k)
    for rank_idx, (other_poly_id, sim) in enumerate(similarities[:max_rank], start=1):
        contribution = max(sim, 0.0)
        if contribution <= 0:
            continue
        other_organisms = poly_to_organisms.get(other_poly_id, set())
        if rank_idx <= base_top_k:
            source_weight = 1.0
        else:
            exact_match, genus_match, kingdom_match = organism_overlap_features(
                query_organisms,
                other_organisms,
                organism_to_genus,
                organism_to_kingdom,
            )
            if query_organisms:
                if exact_match:
                    source_weight = exact_weight
                elif genus_match:
                    source_weight = genus_weight
                elif kingdom_match:
                    source_weight = kingdom_weight
                else:
                    source_weight = 0.0
            else:
                source_weight = 1.0
            if source_weight <= 0:
                continue
        for function_id in train_poly_to_functions.get(other_poly_id, []):
            weight = label_weights.get(function_id, 1.0)
            if rank_idx <= base_top_k:
                scores[function_id] += contribution * weight
                continue
            support = function_frequency.get(function_id, 0)
            if support > support_threshold:
                continue
            support_scale = 1.0 / np.sqrt(support + 1.0)
            scores[function_id] += contribution * expansion_decay * source_weight * support_scale * weight
    return scores


def build_explicit_tail_support_knn_scores(
    poly_id: str,
    poly_ids: list[str],
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    train_poly_to_functions: dict[str, list[str]],
    function_ids: list[str],
    label_weights: dict[str, float],
    function_frequency: Counter,
    poly_to_organisms: dict[str, set[str]],
    organism_to_genus: dict[str, str],
    organism_to_kingdom: dict[str, str],
    base_top_k: int,
    extended_top_k: int,
    tail_threshold: int,
    expansion_decay: float,
    exact_weight: float,
    genus_weight: float,
    kingdom_weight: float,
    tail_boost: float,
) -> dict[str, float]:
    target = feature_matrix[poly_idx[poly_id]]
    query_organisms = poly_to_organisms.get(poly_id, set())
    similarities: list[tuple[str, float]] = []
    for other_poly_id in poly_ids:
        if other_poly_id == poly_id:
            continue
        labels = train_poly_to_functions.get(other_poly_id, [])
        if not labels:
            continue
        sim = cosine_similarity(target, feature_matrix[poly_idx[other_poly_id]])
        similarities.append((other_poly_id, sim))
    similarities.sort(key=lambda item: (-item[1], item[0]))

    scores = {function_id: 0.0 for function_id in function_ids}
    max_rank = max(base_top_k, extended_top_k)
    for rank_idx, (other_poly_id, sim) in enumerate(similarities[:max_rank], start=1):
        contribution = max(sim, 0.0)
        if contribution <= 0:
            continue
        other_organisms = poly_to_organisms.get(other_poly_id, set())
        if rank_idx <= base_top_k:
            source_weight = 1.0
        else:
            exact_match, genus_match, kingdom_match = organism_overlap_features(
                query_organisms,
                other_organisms,
                organism_to_genus,
                organism_to_kingdom,
            )
            if query_organisms:
                if exact_match:
                    source_weight = exact_weight
                elif genus_match:
                    source_weight = genus_weight
                elif kingdom_match:
                    source_weight = kingdom_weight
                else:
                    source_weight = 0.0
            else:
                source_weight = 1.0
            if source_weight <= 0:
                continue
        for function_id in train_poly_to_functions.get(other_poly_id, []):
            weight = label_weights.get(function_id, 1.0)
            if rank_idx <= base_top_k:
                scores[function_id] += contribution * weight
                continue
            support = function_frequency.get(function_id, 0)
            if support > tail_threshold:
                continue
            tail_scale = 1.0 + tail_boost * max(0.0, (tail_threshold - support) / max(tail_threshold, 1))
            support_scale = tail_scale / np.sqrt(support + 1.0)
            scores[function_id] += contribution * expansion_decay * source_weight * support_scale * weight
    return scores


def build_disease_conditioned_knn_scores(
    poly_id: str,
    poly_ids: list[str],
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    train_poly_to_functions: dict[str, list[str]],
    function_ids: list[str],
    label_weights: dict[str, float],
    poly_to_diseases: dict[str, set[str]],
    disease_function_priors: dict[str, dict[str, float]],
    top_k: int,
    smoothing_weight: float,
    max_boost: float,
) -> dict[str, float]:
    target = feature_matrix[poly_idx[poly_id]]
    query_diseases = poly_to_diseases.get(poly_id, set())
    disease_priors = [disease_function_priors[disease_id] for disease_id in query_diseases if disease_id in disease_function_priors]
    num_functions = max(len(function_ids), 1)
    similarities: list[tuple[str, float]] = []
    for other_poly_id in poly_ids:
        if other_poly_id == poly_id:
            continue
        labels = train_poly_to_functions.get(other_poly_id, [])
        if not labels:
            continue
        sim = cosine_similarity(target, feature_matrix[poly_idx[other_poly_id]])
        similarities.append((other_poly_id, sim))
    similarities.sort(key=lambda item: (-item[1], item[0]))

    scores = {function_id: 0.0 for function_id in function_ids}
    for other_poly_id, sim in similarities[:top_k]:
        contribution = max(sim, 0.0)
        if contribution <= 0:
            continue
        for function_id in train_poly_to_functions.get(other_poly_id, []):
            vote = contribution * label_weights.get(function_id, 1.0)
            if disease_priors:
                compatibility = sum(prior.get(function_id, 0.0) for prior in disease_priors) / len(disease_priors)
                normalized_signal = max(compatibility * num_functions - 1.0, 0.0)
                vote *= min(max_boost, 1.0 + smoothing_weight * normalized_signal)
            scores[function_id] += vote
    return scores


def structural_signature_feature_keys(feature_dict: dict[str, float]) -> set[str]:
    allowed_prefixes = ("organism__", "monosaccharide__", "bond__")
    disallowed_suffixes = ("__degree", "__shared_poly_count")
    return {
        key
        for key, value in feature_dict.items()
        if value > 0
        and key.startswith(allowed_prefixes)
        and not key.endswith(disallowed_suffixes)
    }


def structural_feature_prefix(feature_key: str) -> str:
    return feature_key.split("__", maxsplit=1)[0]


def structural_motif_keys(structural_features: set[str]) -> set[str]:
    motifs: set[str] = set()
    ordered = sorted(structural_features)
    for left, right in combinations(ordered, 2):
        left_prefix = structural_feature_prefix(left)
        right_prefix = structural_feature_prefix(right)
        if left_prefix == right_prefix == "organism":
            continue
        motif = f"{left_prefix}|{right_prefix}::{left}&&{right}"
        motifs.add(motif)
    return motifs


def poly_taxonomy_keys(
    organism_ids: set[str],
    organism_to_genus: dict[str, str],
    organism_to_kingdom: dict[str, str],
) -> set[str]:
    keys: set[str] = set()
    for organism_id in organism_ids:
        keys.add(f"organism::{organism_id}")
        genus = organism_to_genus.get(organism_id, "")
        kingdom = organism_to_kingdom.get(organism_id, "")
        if genus:
            keys.add(f"genus::{genus}")
        if kingdom:
            keys.add(f"kingdom::{kingdom}")
    return keys


def build_tail_structural_signatures(
    poly_ids: list[str],
    feature_dicts: dict[str, dict[str, float]],
    train_poly_to_functions: dict[str, list[str]],
    function_ids: list[str],
    function_frequency: Counter,
    support_threshold: int,
    feature_limit: int,
    min_local_rate: float,
) -> dict[str, dict[str, float]]:
    poly_structural_features = {
        poly_id: structural_signature_feature_keys(feature_dicts[poly_id]) for poly_id in poly_ids
    }
    global_feature_counts: Counter = Counter()
    for poly_id in poly_ids:
        global_feature_counts.update(poly_structural_features[poly_id])
    total_polys = max(len(poly_ids), 1)

    function_to_train_polys: dict[str, list[str]] = defaultdict(list)
    for poly_id, function_list in train_poly_to_functions.items():
        for function_id in function_list:
            function_to_train_polys[function_id].append(poly_id)

    signatures: dict[str, dict[str, float]] = {}
    for function_id in function_ids:
        support = function_frequency.get(function_id, 0)
        if support == 0 or support > support_threshold:
            continue
        member_polys = function_to_train_polys.get(function_id, [])
        if not member_polys:
            continue
        local_feature_counts: Counter = Counter()
        for poly_id in member_polys:
            local_feature_counts.update(poly_structural_features[poly_id])
        weighted_features: list[tuple[str, float]] = []
        for feature_key, count in local_feature_counts.items():
            local_rate = count / len(member_polys)
            if local_rate < min_local_rate:
                continue
            global_rate = global_feature_counts.get(feature_key, 0) / total_polys
            enrichment = np.log((local_rate + 1e-6) / (global_rate + 1e-6))
            if enrichment <= 0:
                continue
            score = local_rate * enrichment
            weighted_features.append((feature_key, float(score)))
        weighted_features.sort(key=lambda item: (-item[1], item[0]))
        if not weighted_features:
            continue
        signatures[function_id] = dict(weighted_features[:feature_limit])
    return signatures


def build_tail_structural_signature_scores(
    base_scores: dict[str, float],
    poly_id: str,
    feature_dicts: dict[str, dict[str, float]],
    function_frequency: Counter,
    tail_structural_signatures: dict[str, dict[str, float]],
    rerank_top_n: int,
    support_threshold: int,
    signature_weight: float,
    max_boost: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_features = structural_signature_feature_keys(feature_dicts[poly_id])
    if not query_features:
        return reranked
    candidate_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:rerank_top_n]
        if function_frequency.get(function_id, 0) <= support_threshold
    ]
    if not candidate_ids:
        return reranked
    for function_id in candidate_ids:
        signature = tail_structural_signatures.get(function_id)
        if not signature:
            continue
        total_weight = sum(signature.values())
        if total_weight <= 0:
            continue
        matched_weight = sum(weight for feature_key, weight in signature.items() if feature_key in query_features)
        if matched_weight <= 0:
            continue
        overlap = matched_weight / total_weight
        support = function_frequency.get(function_id, 0)
        support_scale = 1.0 + max_boost * max(0.0, (support_threshold - support) / max(support_threshold, 1))
        reranked[function_id] += signature_weight * overlap * support_scale
    return reranked


def build_structure_aware_candidate_generation_scores(
    base_scores: dict[str, float],
    poly_id: str,
    feature_dicts: dict[str, dict[str, float]],
    function_frequency: Counter,
    tail_structural_signatures: dict[str, dict[str, float]],
    base_window: int,
    support_threshold: int,
    candidate_limit: int,
    activation: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_features = structural_signature_feature_keys(feature_dicts[poly_id])
    if not query_features:
        return reranked
    current_top = {
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:base_window]
    }
    candidate_scores: dict[str, float] = {}
    for function_id, signature in tail_structural_signatures.items():
        if function_id in current_top:
            continue
        support = function_frequency.get(function_id, 0)
        if support > support_threshold:
            continue
        total_weight = sum(signature.values())
        if total_weight <= 0:
            continue
        matched_weight = sum(weight for feature_key, weight in signature.items() if feature_key in query_features)
        if matched_weight <= 0:
            continue
        overlap = matched_weight / total_weight
        tail_scale = 1.0 + max(0.0, (support_threshold - support) / max(support_threshold, 1))
        candidate_scores[function_id] = overlap * tail_scale
    if not candidate_scores:
        return reranked
    selected_candidates = sorted(candidate_scores.items(), key=lambda item: (-item[1], item[0]))[:candidate_limit]
    max_score = max(score for _, score in selected_candidates)
    if max_score <= 0:
        return reranked
    for function_id, score in selected_candidates:
        reranked[function_id] += activation * (score / max_score)
    return reranked


def build_label_specific_motif_signatures(
    poly_ids: list[str],
    feature_dicts: dict[str, dict[str, float]],
    train_poly_to_functions: dict[str, list[str]],
    function_ids: list[str],
    function_frequency: Counter,
    support_threshold: int,
    feature_limit: int,
    min_local_rate: float,
) -> dict[str, dict[str, float]]:
    poly_motifs = {
        poly_id: structural_motif_keys(structural_signature_feature_keys(feature_dicts[poly_id])) for poly_id in poly_ids
    }
    global_motif_counts: Counter = Counter()
    for poly_id in poly_ids:
        global_motif_counts.update(poly_motifs[poly_id])
    total_polys = max(len(poly_ids), 1)

    function_to_train_polys: dict[str, list[str]] = defaultdict(list)
    for poly_id, function_list in train_poly_to_functions.items():
        for function_id in function_list:
            function_to_train_polys[function_id].append(poly_id)

    signatures: dict[str, dict[str, float]] = {}
    for function_id in function_ids:
        support = function_frequency.get(function_id, 0)
        if support == 0 or support > support_threshold:
            continue
        member_polys = function_to_train_polys.get(function_id, [])
        if not member_polys:
            continue
        local_motif_counts: Counter = Counter()
        for poly_id in member_polys:
            local_motif_counts.update(poly_motifs[poly_id])
        weighted_motifs: list[tuple[str, float]] = []
        for motif_key, count in local_motif_counts.items():
            local_rate = count / len(member_polys)
            if local_rate < min_local_rate:
                continue
            global_rate = global_motif_counts.get(motif_key, 0) / total_polys
            enrichment = np.log((local_rate + 1e-6) / (global_rate + 1e-6))
            if enrichment <= 0:
                continue
            weighted_motifs.append((motif_key, float(local_rate * enrichment)))
        weighted_motifs.sort(key=lambda item: (-item[1], item[0]))
        if not weighted_motifs:
            continue
        signatures[function_id] = dict(weighted_motifs[:feature_limit])
    return signatures


def build_label_specific_motif_candidate_scores(
    base_scores: dict[str, float],
    poly_id: str,
    feature_dicts: dict[str, dict[str, float]],
    function_frequency: Counter,
    motif_signatures: dict[str, dict[str, float]],
    base_window: int,
    support_threshold: int,
    candidate_limit: int,
    activation: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_motifs = structural_motif_keys(structural_signature_feature_keys(feature_dicts[poly_id]))
    if not query_motifs:
        return reranked
    current_top = {
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:base_window]
    }
    candidate_scores: dict[str, float] = {}
    for function_id, signature in motif_signatures.items():
        if function_id in current_top:
            continue
        support = function_frequency.get(function_id, 0)
        if support > support_threshold:
            continue
        total_weight = sum(signature.values())
        if total_weight <= 0:
            continue
        matched_weight = sum(weight for motif_key, weight in signature.items() if motif_key in query_motifs)
        if matched_weight <= 0:
            continue
        overlap = matched_weight / total_weight
        tail_scale = 1.0 + max(0.0, (support_threshold - support) / max(support_threshold, 1))
        candidate_scores[function_id] = overlap * tail_scale
    if not candidate_scores:
        return reranked
    selected = sorted(candidate_scores.items(), key=lambda item: (-item[1], item[0]))[:candidate_limit]
    max_score = max(score for _, score in selected)
    if max_score <= 0:
        return reranked
    for function_id, score in selected:
        reranked[function_id] += activation * (score / max_score)
    return reranked


def build_taxonomy_conditioned_motif_signatures(
    poly_ids: list[str],
    feature_dicts: dict[str, dict[str, float]],
    train_poly_to_functions: dict[str, list[str]],
    function_ids: list[str],
    function_frequency: Counter,
    poly_to_organisms: dict[str, set[str]],
    organism_to_genus: dict[str, str],
    organism_to_kingdom: dict[str, str],
    support_threshold: int,
    feature_limit: int,
    min_local_rate: float,
) -> dict[str, dict[str, dict[str, float]]]:
    poly_motifs = {
        poly_id: structural_motif_keys(structural_signature_feature_keys(feature_dicts[poly_id])) for poly_id in poly_ids
    }
    poly_taxa = {
        poly_id: poly_taxonomy_keys(poly_to_organisms.get(poly_id, set()), organism_to_genus, organism_to_kingdom)
        for poly_id in poly_ids
    }
    global_motif_counts_by_taxon: dict[str, Counter] = defaultdict(Counter)
    taxon_poly_counts: Counter = Counter()
    for poly_id in poly_ids:
        motifs = poly_motifs[poly_id]
        for taxon_key in poly_taxa[poly_id]:
            global_motif_counts_by_taxon[taxon_key].update(motifs)
            taxon_poly_counts[taxon_key] += 1

    function_to_train_polys: dict[str, list[str]] = defaultdict(list)
    for poly_id, function_list in train_poly_to_functions.items():
        for function_id in function_list:
            function_to_train_polys[function_id].append(poly_id)

    signatures: dict[str, dict[str, dict[str, float]]] = {}
    for function_id in function_ids:
        support = function_frequency.get(function_id, 0)
        if support == 0 or support > support_threshold:
            continue
        member_polys = function_to_train_polys.get(function_id, [])
        if not member_polys:
            continue
        motif_counts_by_taxon: dict[str, Counter] = defaultdict(Counter)
        member_counts_by_taxon: Counter = Counter()
        for poly_id in member_polys:
            motifs = poly_motifs[poly_id]
            for taxon_key in poly_taxa.get(poly_id, set()):
                motif_counts_by_taxon[taxon_key].update(motifs)
                member_counts_by_taxon[taxon_key] += 1
        function_signatures: dict[str, dict[str, float]] = {}
        for taxon_key, local_counts in motif_counts_by_taxon.items():
            denom = member_counts_by_taxon[taxon_key]
            if denom <= 0 or taxon_poly_counts[taxon_key] <= 1:
                continue
            weighted: list[tuple[str, float]] = []
            for motif_key, count in local_counts.items():
                local_rate = count / denom
                if local_rate < min_local_rate:
                    continue
                global_rate = global_motif_counts_by_taxon[taxon_key].get(motif_key, 0) / max(taxon_poly_counts[taxon_key], 1)
                enrichment = np.log((local_rate + 1e-6) / (global_rate + 1e-6))
                if enrichment <= 0:
                    continue
                weighted.append((motif_key, float(local_rate * enrichment)))
            weighted.sort(key=lambda item: (-item[1], item[0]))
            if weighted:
                function_signatures[taxon_key] = dict(weighted[:feature_limit])
        if function_signatures:
            signatures[function_id] = function_signatures
    return signatures


def build_taxonomy_conditioned_motif_candidate_scores(
    base_scores: dict[str, float],
    poly_id: str,
    feature_dicts: dict[str, dict[str, float]],
    function_frequency: Counter,
    taxonomy_motif_signatures: dict[str, dict[str, dict[str, float]]],
    poly_to_organisms: dict[str, set[str]],
    organism_to_genus: dict[str, str],
    organism_to_kingdom: dict[str, str],
    base_window: int,
    support_threshold: int,
    candidate_limit: int,
    activation: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_motifs = structural_motif_keys(structural_signature_feature_keys(feature_dicts[poly_id]))
    if not query_motifs:
        return reranked
    query_taxa = poly_taxonomy_keys(poly_to_organisms.get(poly_id, set()), organism_to_genus, organism_to_kingdom)
    if not query_taxa:
        return reranked
    current_top = {
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:base_window]
    }
    candidate_scores: dict[str, float] = {}
    for function_id, taxon_signatures in taxonomy_motif_signatures.items():
        if function_id in current_top:
            continue
        support = function_frequency.get(function_id, 0)
        if support > support_threshold:
            continue
        best_score = 0.0
        for taxon_key in query_taxa:
            signature = taxon_signatures.get(taxon_key)
            if not signature:
                continue
            total_weight = sum(signature.values())
            if total_weight <= 0:
                continue
            matched_weight = sum(weight for motif_key, weight in signature.items() if motif_key in query_motifs)
            if matched_weight <= 0:
                continue
            overlap = matched_weight / total_weight
            best_score = max(best_score, overlap)
        if best_score <= 0:
            continue
        tail_scale = 1.0 + max(0.0, (support_threshold - support) / max(support_threshold, 1))
        candidate_scores[function_id] = best_score * tail_scale
    if not candidate_scores:
        return reranked
    selected = sorted(candidate_scores.items(), key=lambda item: (-item[1], item[0]))[:candidate_limit]
    max_score = max(score for _, score in selected)
    if max_score <= 0:
        return reranked
    for function_id, score in selected:
        reranked[function_id] += activation * (score / max_score)
    return reranked


def build_function_hierarchy_maps(hierarchy_config: dict) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    family_to_functions: dict[str, set[str]] = {}
    function_to_families: dict[str, set[str]] = defaultdict(set)
    for family_name, function_names in hierarchy_config.get("families", {}).items():
        family_members = {name for name in function_names if name}
        if not family_members:
            continue
        family_to_functions[family_name] = family_members
        for function_name in family_members:
            function_to_families[function_name].add(family_name)
    return family_to_functions, dict(function_to_families)


def build_function_hierarchy_graph(
    hierarchy_config: dict,
) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, set[str]], dict[str, set[str]]]:
    family_to_functions, function_to_families = build_function_hierarchy_maps(hierarchy_config)
    parent_to_children: dict[str, set[str]] = defaultdict(set)
    child_to_parents: dict[str, set[str]] = defaultdict(set)
    for edge in hierarchy_config.get("parent_child_edges", []):
        if not isinstance(edge, list) or len(edge) != 2:
            continue
        parent, child = edge
        if not parent or not child:
            continue
        parent_to_children[parent].add(child)
        child_to_parents[child].add(parent)
    return family_to_functions, function_to_families, dict(parent_to_children), dict(child_to_parents)


def build_hierarchy_candidate_scores(
    base_scores: dict[str, float],
    function_names: dict[str, str],
    function_frequency: Counter,
    function_to_families: dict[str, set[str]],
    family_to_functions: dict[str, set[str]],
    base_window: int,
    support_threshold: int,
    candidate_limit: int,
    activation: float,
    min_seed_count: int,
    specificity_power: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    current_top_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:base_window]
    ]
    current_top = set(current_top_ids)
    candidate_scores: dict[str, float] = defaultdict(float)
    family_seed_counts: Counter = Counter()
    family_seed_strength: dict[str, float] = defaultdict(float)
    for source_id in current_top_ids:
        source_name = function_names[source_id]
        source_score = max(base_scores.get(source_id, 0.0), 0.0)
        if source_score <= 0:
            continue
        for family_name in function_to_families.get(source_name, set()):
            family_seed_counts[family_name] += 1
            family_seed_strength[family_name] += source_score
    for source_id in current_top_ids:
        source_name = function_names[source_id]
        source_score = max(base_scores.get(source_id, 0.0), 0.0)
        if source_score <= 0:
            continue
        for family_name in function_to_families.get(source_name, set()):
            if family_seed_counts.get(family_name, 0) < min_seed_count:
                continue
            family_members = family_to_functions.get(family_name, set())
            family_size = max(len(family_members), 1)
            specificity = 1.0 / (family_size**max(specificity_power, 0.0))
            family_strength = family_seed_strength.get(family_name, 0.0)
            for candidate_id, candidate_name in function_names.items():
                if candidate_id in current_top:
                    continue
                if candidate_name not in family_members:
                    continue
                support = function_frequency.get(candidate_id, 0)
                if support > support_threshold:
                    continue
                support_scale = 1.0 + max(0.0, (support_threshold - support) / max(support_threshold, 1))
                candidate_scores[candidate_id] += source_score * family_strength * support_scale * specificity
    if not candidate_scores:
        return reranked
    selected = sorted(candidate_scores.items(), key=lambda item: (-item[1], item[0]))[:candidate_limit]
    max_score = max(score for _, score in selected)
    if max_score <= 0:
        return reranked
    for function_id, score in selected:
        reranked[function_id] += activation * (score / max_score)
    return reranked


def build_graph_native_hierarchy_scores(
    base_scores: dict[str, float],
    function_names: dict[str, str],
    function_frequency: Counter,
    function_to_families: dict[str, set[str]],
    family_to_functions: dict[str, set[str]],
    base_window: int,
    support_threshold: int,
    min_seed_count: int,
    specificity_power: float,
    graph_weight: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    ranked_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:base_window]
    ]
    family_seed_counts: Counter = Counter()
    family_seed_strength: dict[str, float] = defaultdict(float)
    for function_id in ranked_ids:
        score = max(base_scores.get(function_id, 0.0), 0.0)
        if score <= 0:
            continue
        function_name = function_names[function_id]
        for family_name in function_to_families.get(function_name, set()):
            family_seed_counts[family_name] += 1
            family_seed_strength[family_name] += score

    for family_name, family_strength in family_seed_strength.items():
        if family_seed_counts.get(family_name, 0) < min_seed_count or family_strength <= 0:
            continue
        family_members = family_to_functions.get(family_name, set())
        family_size = max(len(family_members), 1)
        specificity = 1.0 / (family_size**max(specificity_power, 0.0))
        normalized_strength = family_strength / family_seed_counts[family_name]
        for candidate_id, candidate_name in function_names.items():
            if candidate_name not in family_members:
                continue
            support = function_frequency.get(candidate_id, 0)
            if support > support_threshold:
                continue
            support_scale = 1.0 + max(0.0, (support_threshold - support) / max(support_threshold, 1))
            reranked[candidate_id] += graph_weight * normalized_strength * specificity * support_scale
    return reranked


def build_parent_child_hierarchy_scores(
    base_scores: dict[str, float],
    function_names: dict[str, str],
    function_frequency: Counter,
    function_to_families: dict[str, set[str]],
    family_to_functions: dict[str, set[str]],
    parent_to_children: dict[str, set[str]],
    child_to_parents: dict[str, set[str]],
    base_window: int,
    support_threshold: int,
    min_seed_count: int,
    specificity_power: float,
    graph_weight: float,
    confidence_threshold: float,
    adaptive_power: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    ranked_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:base_window]
    ]
    family_seed_counts: Counter = Counter()
    family_seed_strength: dict[str, float] = defaultdict(float)
    for function_id in ranked_ids:
        score = max(base_scores.get(function_id, 0.0), 0.0)
        if score <= 0:
            continue
        function_name = function_names[function_id]
        for family_name in function_to_families.get(function_name, set()):
            family_seed_counts[family_name] += 1
            family_seed_strength[family_name] += score

    parent_strength: dict[str, float] = defaultdict(float)
    for family_name, seed_strength in family_seed_strength.items():
        if family_seed_counts.get(family_name, 0) < min_seed_count:
            continue
        for parent_name in child_to_parents.get(family_name, set()):
            parent_strength[parent_name] += seed_strength

    total_seed_strength = sum(family_seed_strength.values())
    for parent_name, aggregated_strength in parent_strength.items():
        if aggregated_strength <= 0 or total_seed_strength <= 0:
            continue
        confidence = aggregated_strength / total_seed_strength
        if confidence < confidence_threshold:
            continue
        adaptive_weight = graph_weight * (confidence**max(adaptive_power, 0.0))
        sibling_families = parent_to_children.get(parent_name, set())
        for sibling_family in sibling_families:
            family_members = family_to_functions.get(sibling_family, set())
            family_size = max(len(family_members), 1)
            specificity = 1.0 / (family_size**max(specificity_power, 0.0))
            sibling_seed_count = family_seed_counts.get(sibling_family, 0)
            local_seed_penalty = 1.0 if sibling_seed_count == 0 else 1.0 / (1.0 + sibling_seed_count)
            for candidate_id, candidate_name in function_names.items():
                if candidate_name not in family_members:
                    continue
                support = function_frequency.get(candidate_id, 0)
                if support > support_threshold:
                    continue
                support_scale = 1.0 + max(0.0, (support_threshold - support) / max(support_threshold, 1))
                reranked[candidate_id] += (
                    adaptive_weight * aggregated_strength * specificity * local_seed_penalty * support_scale
                )
    return reranked


def build_rare_label_expansion_scores(
    poly_id: str,
    poly_ids: list[str],
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    train_poly_to_functions: dict[str, list[str]],
    function_ids: list[str],
    label_weights: dict[str, float],
    function_frequency: Counter,
    base_top_k: int,
    rare_label_threshold: int,
    rare_label_top_k: int,
    rare_label_decay: float,
) -> dict[str, float]:
    target = feature_matrix[poly_idx[poly_id]]
    similarities: list[tuple[str, float]] = []
    for other_poly_id in poly_ids:
        if other_poly_id == poly_id:
            continue
        labels = train_poly_to_functions.get(other_poly_id, [])
        if not labels:
            continue
        sim = cosine_similarity(target, feature_matrix[poly_idx[other_poly_id]])
        similarities.append((other_poly_id, sim))
    similarities.sort(key=lambda item: (-item[1], item[0]))

    scores = {function_id: 0.0 for function_id in function_ids}
    max_top_k = max(base_top_k, rare_label_top_k)
    for rank_idx, (other_poly_id, sim) in enumerate(similarities[:max_top_k], start=1):
        contribution = max(sim, 0.0)
        if contribution <= 0:
            continue
        for function_id in train_poly_to_functions.get(other_poly_id, []):
            if rank_idx <= base_top_k:
                scores[function_id] += contribution * label_weights.get(function_id, 1.0)
                continue
            if (
                rank_idx <= rare_label_top_k
                and function_frequency.get(function_id, 0) <= rare_label_threshold
            ):
                scores[function_id] += contribution * rare_label_decay * label_weights.get(function_id, 1.0)
    return scores


def build_poly_to_organisms(edge_dir: Path) -> dict[str, set[str]]:
    rows = read_csv(edge_dir / "poly_organism.csv")
    poly_to_organisms: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        poly_to_organisms[row["source_id"]].add(row["target_id"])
    return poly_to_organisms


def build_poly_to_diseases(edge_dir: Path) -> dict[str, set[str]]:
    rows = read_csv(edge_dir / "poly_disease.csv")
    poly_to_diseases: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        poly_to_diseases[row["source_id"]].add(row["target_id"])
    return poly_to_diseases


def build_organism_metadata(node_dir: Path) -> tuple[dict[str, str], dict[str, str]]:
    rows = read_csv(node_dir / "organism.csv")
    organism_to_genus: dict[str, str] = {}
    organism_to_kingdom: dict[str, str] = {}
    for row in rows:
        organism_id = row["organism_id"]
        name_norm = (row.get("organism_name_norm") or "").strip()
        kingdom = (row.get("kingdom") or "").strip().lower()
        genus = ""
        if name_norm:
            genus = name_norm.split()[0].strip(".,()").lower()
        organism_to_genus[organism_id] = genus
        organism_to_kingdom[organism_id] = kingdom
    return organism_to_genus, organism_to_kingdom


def build_source_constrained_rerank_scores(
    base_scores: dict[str, float],
    poly_id: str,
    poly_ids: list[str],
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    train_poly_to_functions: dict[str, list[str]],
    poly_to_organisms: dict[str, set[str]],
    rerank_top_n: int,
    rerank_weight: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_organisms = poly_to_organisms.get(poly_id, set())
    if not query_organisms:
        return reranked

    candidate_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:rerank_top_n]
    ]
    source_bonus = {function_id: 0.0 for function_id in candidate_ids}
    target = feature_matrix[poly_idx[poly_id]]
    for other_poly_id in poly_ids:
        if other_poly_id == poly_id:
            continue
        if not (query_organisms & poly_to_organisms.get(other_poly_id, set())):
            continue
        labels = train_poly_to_functions.get(other_poly_id, [])
        if not labels:
            continue
        sim = max(cosine_similarity(target, feature_matrix[poly_idx[other_poly_id]]), 0.0)
        if sim <= 0:
            continue
        for function_id in labels:
            if function_id in source_bonus:
                source_bonus[function_id] += sim
    for function_id, bonus in source_bonus.items():
        reranked[function_id] += rerank_weight * bonus
    return reranked


def organism_overlap_features(
    query_organisms: set[str],
    other_organisms: set[str],
    organism_to_genus: dict[str, str],
    organism_to_kingdom: dict[str, str],
) -> tuple[bool, bool, bool]:
    exact_match = bool(query_organisms & other_organisms)
    query_genera = {organism_to_genus.get(org_id, "") for org_id in query_organisms if organism_to_genus.get(org_id, "")}
    other_genera = {organism_to_genus.get(org_id, "") for org_id in other_organisms if organism_to_genus.get(org_id, "")}
    genus_match = bool(query_genera & other_genera)
    query_kingdoms = {
        organism_to_kingdom.get(org_id, "")
        for org_id in query_organisms
        if organism_to_kingdom.get(org_id, "")
    }
    other_kingdoms = {
        organism_to_kingdom.get(org_id, "")
        for org_id in other_organisms
        if organism_to_kingdom.get(org_id, "")
    }
    kingdom_match = bool(query_kingdoms & other_kingdoms)
    return exact_match, genus_match, kingdom_match


def build_source_cluster_backoff_scores(
    base_scores: dict[str, float],
    poly_id: str,
    poly_ids: list[str],
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    train_poly_to_functions: dict[str, list[str]],
    poly_to_organisms: dict[str, set[str]],
    organism_to_genus: dict[str, str],
    organism_to_kingdom: dict[str, str],
    rerank_top_n: int,
    exact_weight: float,
    genus_weight: float,
    kingdom_weight: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_organisms = poly_to_organisms.get(poly_id, set())
    if not query_organisms:
        return reranked

    candidate_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:rerank_top_n]
    ]
    source_bonus = {function_id: 0.0 for function_id in candidate_ids}
    target = feature_matrix[poly_idx[poly_id]]
    for other_poly_id in poly_ids:
        if other_poly_id == poly_id:
            continue
        other_organisms = poly_to_organisms.get(other_poly_id, set())
        exact_match, genus_match, kingdom_match = organism_overlap_features(
            query_organisms,
            other_organisms,
            organism_to_genus,
            organism_to_kingdom,
        )
        if not (exact_match or genus_match or kingdom_match):
            continue
        labels = train_poly_to_functions.get(other_poly_id, [])
        if not labels:
            continue
        sim = max(cosine_similarity(target, feature_matrix[poly_idx[other_poly_id]]), 0.0)
        if sim <= 0:
            continue
        if exact_match:
            backoff_weight = exact_weight
        elif genus_match:
            backoff_weight = genus_weight
        else:
            backoff_weight = kingdom_weight
        for function_id in labels:
            if function_id in source_bonus:
                source_bonus[function_id] += sim * backoff_weight
    for function_id, bonus in source_bonus.items():
        reranked[function_id] += bonus
    return reranked


def build_tail_candidate_generation_scores(
    base_scores: dict[str, float],
    poly_id: str,
    poly_ids: list[str],
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    train_poly_to_functions: dict[str, list[str]],
    function_frequency: Counter,
    poly_to_organisms: dict[str, set[str]],
    organism_to_genus: dict[str, str],
    organism_to_kingdom: dict[str, str],
    base_top_k: int,
    tail_label_threshold: int,
    candidate_top_k: int,
    candidate_limit: int,
    activation: float,
    source_exact_weight: float,
    source_genus_weight: float,
    source_kingdom_weight: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_organisms = poly_to_organisms.get(poly_id, set())
    target = feature_matrix[poly_idx[poly_id]]
    similarities: list[tuple[str, float]] = []
    for other_poly_id in poly_ids:
        if other_poly_id == poly_id:
            continue
        labels = train_poly_to_functions.get(other_poly_id, [])
        if not labels:
            continue
        sim = cosine_similarity(target, feature_matrix[poly_idx[other_poly_id]])
        similarities.append((other_poly_id, sim))
    similarities.sort(key=lambda item: (-item[1], item[0]))

    generator_scores: dict[str, float] = defaultdict(float)
    for rank_idx, (other_poly_id, sim) in enumerate(similarities[:candidate_top_k], start=1):
        if rank_idx <= base_top_k:
            continue
        contribution = max(sim, 0.0)
        if contribution <= 0:
            continue
        other_organisms = poly_to_organisms.get(other_poly_id, set())
        exact_match, genus_match, kingdom_match = organism_overlap_features(
            query_organisms,
            other_organisms,
            organism_to_genus,
            organism_to_kingdom,
        )
        if query_organisms:
            if exact_match:
                source_weight = source_exact_weight
            elif genus_match:
                source_weight = source_genus_weight
            elif kingdom_match:
                source_weight = source_kingdom_weight
            else:
                source_weight = 0.0
        else:
            source_weight = 1.0
        for function_id in train_poly_to_functions.get(other_poly_id, []):
            if function_frequency.get(function_id, 0) > tail_label_threshold:
                continue
            generator_scores[function_id] += contribution * source_weight

    if not generator_scores:
        return reranked

    selected_tail_candidates = [
        function_id
        for function_id, _ in sorted(generator_scores.items(), key=lambda item: (-item[1], item[0]))[
            :candidate_limit
        ]
    ]
    if not selected_tail_candidates:
        return reranked

    for function_id in selected_tail_candidates:
        reranked[function_id] += activation * generator_scores[function_id]
    return reranked


def build_label_specific_backoff_scores(
    base_scores: dict[str, float],
    poly_id: str,
    poly_ids: list[str],
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    train_poly_to_functions: dict[str, list[str]],
    function_frequency: Counter,
    poly_to_organisms: dict[str, set[str]],
    organism_to_genus: dict[str, str],
    organism_to_kingdom: dict[str, str],
    rerank_top_n: int,
    label_backoff_threshold: int,
    label_backoff_weight: float,
    exact_weight: float,
    genus_weight: float,
    kingdom_weight: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_organisms = poly_to_organisms.get(poly_id, set())
    if not query_organisms:
        return reranked

    candidate_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:rerank_top_n]
        if function_frequency.get(function_id, 0) <= label_backoff_threshold
    ]
    if not candidate_ids:
        return reranked

    target = feature_matrix[poly_idx[poly_id]]
    label_bonus = {function_id: 0.0 for function_id in candidate_ids}
    label_denominator = {function_id: 0.0 for function_id in candidate_ids}
    for other_poly_id in poly_ids:
        if other_poly_id == poly_id:
            continue
        labels = train_poly_to_functions.get(other_poly_id, [])
        tracked_labels = [function_id for function_id in labels if function_id in label_bonus]
        if not tracked_labels:
            continue
        other_organisms = poly_to_organisms.get(other_poly_id, set())
        exact_match, genus_match, kingdom_match = organism_overlap_features(
            query_organisms,
            other_organisms,
            organism_to_genus,
            organism_to_kingdom,
        )
        if exact_match:
            source_weight = exact_weight
        elif genus_match:
            source_weight = genus_weight
        elif kingdom_match:
            source_weight = kingdom_weight
        else:
            source_weight = 0.0
        sim = max(cosine_similarity(target, feature_matrix[poly_idx[other_poly_id]]), 0.0)
        if sim <= 0:
            continue
        for function_id in tracked_labels:
            label_denominator[function_id] += sim
            if source_weight > 0:
                label_bonus[function_id] += sim * source_weight

    for function_id in candidate_ids:
        if label_denominator[function_id] <= 0:
            continue
        normalized_backoff = label_bonus[function_id] / label_denominator[function_id]
        reranked[function_id] += label_backoff_weight * normalized_backoff
    return reranked


def build_disease_function_priors(
    train_poly_to_functions: dict[str, list[str]],
    poly_to_diseases: dict[str, set[str]],
    function_ids: list[str],
    alpha: float,
) -> dict[str, dict[str, float]]:
    disease_function_counts: dict[str, Counter] = defaultdict(Counter)
    disease_counts: Counter = Counter()
    num_functions = len(function_ids)
    for poly_id, diseases in poly_to_diseases.items():
        labels = train_poly_to_functions.get(poly_id, [])
        if not labels or not diseases:
            continue
        for disease_id in diseases:
            disease_counts[disease_id] += len(labels)
            disease_function_counts[disease_id].update(labels)
    disease_function_priors: dict[str, dict[str, float]] = {}
    for disease_id, counts in disease_function_counts.items():
        denom = disease_counts[disease_id] + alpha * num_functions
        disease_function_priors[disease_id] = {
            function_id: (counts.get(function_id, 0) + alpha) / denom for function_id in function_ids
        }
    return disease_function_priors


def build_disease_label_prior_scores(
    base_scores: dict[str, float],
    poly_id: str,
    poly_to_diseases: dict[str, set[str]],
    disease_function_priors: dict[str, dict[str, float]],
    rerank_top_n: int,
    prior_weight: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_diseases = poly_to_diseases.get(poly_id, set())
    if not query_diseases:
        return reranked
    candidate_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:rerank_top_n]
    ]
    if not candidate_ids:
        return reranked
    disease_priors = [disease_function_priors[disease_id] for disease_id in query_diseases if disease_id in disease_function_priors]
    if not disease_priors:
        return reranked
    for function_id in candidate_ids:
        compatibility = sum(prior.get(function_id, 0.0) for prior in disease_priors) / len(disease_priors)
        reranked[function_id] += prior_weight * compatibility
    return reranked


def build_tail_aware_disease_prior_scores(
    base_scores: dict[str, float],
    poly_id: str,
    poly_to_diseases: dict[str, set[str]],
    disease_function_priors: dict[str, dict[str, float]],
    function_frequency: Counter,
    rerank_top_n: int,
    tail_threshold: int,
    prior_weight: float,
    tail_boost: float,
    max_multiplier: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_diseases = poly_to_diseases.get(poly_id, set())
    if not query_diseases:
        return reranked
    candidate_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:rerank_top_n]
        if function_frequency.get(function_id, 0) <= tail_threshold
    ]
    if not candidate_ids:
        return reranked
    disease_priors = [disease_function_priors[disease_id] for disease_id in query_diseases if disease_id in disease_function_priors]
    if not disease_priors:
        return reranked
    for function_id in candidate_ids:
        compatibility = sum(prior.get(function_id, 0.0) for prior in disease_priors) / len(disease_priors)
        support = function_frequency.get(function_id, 0)
        multiplier = 1.0 + tail_boost * max(0.0, (tail_threshold - support) / max(tail_threshold, 1))
        multiplier = min(multiplier, max_multiplier)
        reranked[function_id] += prior_weight * compatibility * multiplier
    return reranked


def build_label_prototype_refinement_scores(
    base_scores: dict[str, float],
    poly_id: str,
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    function_to_train_polys: dict[str, list[str]],
    function_centroids: dict[str, np.ndarray],
    function_frequency: Counter,
    rerank_top_n: int,
    prototype_neighbors: int,
    prototype_weight: float,
    prototype_tail_threshold: int,
    prototype_tail_boost: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    candidate_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:rerank_top_n]
    ]
    if not candidate_ids:
        return reranked

    target = feature_matrix[poly_idx[poly_id]]
    for function_id in candidate_ids:
        member_polys = function_to_train_polys.get(function_id, [])
        if not member_polys:
            continue
        similarities: list[tuple[str, float]] = []
        for member_poly_id in member_polys:
            if member_poly_id == poly_id:
                continue
            sim = cosine_similarity(target, feature_matrix[poly_idx[member_poly_id]])
            similarities.append((member_poly_id, sim))
        similarities.sort(key=lambda item: (-item[1], item[0]))
        selected = similarities[: max(1, prototype_neighbors)]
        if not selected:
            prototype = function_centroids[function_id]
        else:
            positive_weights = [max(sim, 0.0) for _, sim in selected]
            if sum(positive_weights) > 0:
                rows = np.stack([feature_matrix[poly_idx[member_poly_id]] for member_poly_id, _ in selected])
                prototype = np.average(rows, axis=0, weights=np.array(positive_weights, dtype=np.float32))
            else:
                prototype = function_centroids[function_id]
        refined_similarity = max(cosine_similarity(target, prototype), 0.0)
        centroid_similarity = max(cosine_similarity(target, function_centroids[function_id]), 0.0)
        prototype_gain = max(refined_similarity - centroid_similarity, 0.0)
        if prototype_gain <= 0:
            continue
        support = function_frequency.get(function_id, 0)
        tail_multiplier = 1.0 + prototype_tail_boost * max(
            0.0, (prototype_tail_threshold - support) / max(prototype_tail_threshold, 1)
        )
        reranked[function_id] += prototype_weight * prototype_gain * tail_multiplier
    return reranked


def build_frequency_adjusted_disease_prior_scores(
    base_scores: dict[str, float],
    poly_id: str,
    poly_to_diseases: dict[str, set[str]],
    disease_function_priors: dict[str, dict[str, float]],
    function_frequency: Counter,
    rerank_top_n: int,
    prior_weight: float,
    adjustment_strength: float,
    adjustment_mode: str,
) -> dict[str, float]:
    reranked = dict(base_scores)
    query_diseases = poly_to_diseases.get(poly_id, set())
    if not query_diseases:
        return reranked
    candidate_ids = [
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:rerank_top_n]
    ]
    if not candidate_ids:
        return reranked
    disease_priors = [disease_function_priors[disease_id] for disease_id in query_diseases if disease_id in disease_function_priors]
    if not disease_priors:
        return reranked
    max_support = max((function_frequency.get(function_id, 0) for function_id in candidate_ids), default=1)
    max_support = max(max_support, 1)
    for function_id in candidate_ids:
        compatibility = sum(prior.get(function_id, 0.0) for prior in disease_priors) / len(disease_priors)
        support = function_frequency.get(function_id, 0)
        normalized_support = support / max_support
        if adjustment_mode == "divide":
            adjusted = compatibility / (1.0 + adjustment_strength * normalized_support)
        else:
            adjusted = max(compatibility - adjustment_strength * normalized_support * compatibility, 0.0)
        reranked[function_id] += prior_weight * adjusted
    return reranked


def build_support_aware_candidate_generation_scores(
    base_scores: dict[str, float],
    poly_id: str,
    poly_ids: list[str],
    poly_idx: dict[str, int],
    feature_matrix: np.ndarray,
    train_poly_to_functions: dict[str, list[str]],
    function_frequency: Counter,
    poly_to_organisms: dict[str, set[str]],
    organism_to_genus: dict[str, str],
    organism_to_kingdom: dict[str, str],
    candidate_top_k: int,
    base_window: int,
    support_threshold: int,
    candidate_limit: int,
    activation: float,
    exact_weight: float,
    genus_weight: float,
    kingdom_weight: float,
) -> dict[str, float]:
    reranked = dict(base_scores)
    target = feature_matrix[poly_idx[poly_id]]
    query_organisms = poly_to_organisms.get(poly_id, set())
    current_top = {
        function_id
        for function_id, _ in sorted(base_scores.items(), key=lambda item: (-item[1], item[0]))[:base_window]
    }
    similarities: list[tuple[str, float]] = []
    for other_poly_id in poly_ids:
        if other_poly_id == poly_id:
            continue
        labels = train_poly_to_functions.get(other_poly_id, [])
        if not labels:
            continue
        sim = cosine_similarity(target, feature_matrix[poly_idx[other_poly_id]])
        similarities.append((other_poly_id, sim))
    similarities.sort(key=lambda item: (-item[1], item[0]))

    generator_scores: dict[str, float] = defaultdict(float)
    for rank_idx, (other_poly_id, sim) in enumerate(similarities[:candidate_top_k], start=1):
        if rank_idx <= base_window:
            continue
        contribution = max(sim, 0.0)
        if contribution <= 0:
            continue
        other_organisms = poly_to_organisms.get(other_poly_id, set())
        exact_match, genus_match, kingdom_match = organism_overlap_features(
            query_organisms,
            other_organisms,
            organism_to_genus,
            organism_to_kingdom,
        )
        if query_organisms:
            if exact_match:
                source_weight = exact_weight
            elif genus_match:
                source_weight = genus_weight
            elif kingdom_match:
                source_weight = kingdom_weight
            else:
                source_weight = 0.0
        else:
            source_weight = 1.0
        if source_weight <= 0:
            continue
        for function_id in train_poly_to_functions.get(other_poly_id, []):
            support = function_frequency.get(function_id, 0)
            if support > support_threshold or function_id in current_top:
                continue
            support_scale = 1.0 / np.sqrt(support + 1.0)
            generator_scores[function_id] += contribution * source_weight * support_scale

    if not generator_scores:
        return reranked

    selected_candidates = [
        function_id
        for function_id, _ in sorted(generator_scores.items(), key=lambda item: (-item[1], item[0]))[:candidate_limit]
    ]
    if not selected_candidates:
        return reranked

    max_bonus = max(generator_scores[function_id] for function_id in selected_candidates)
    max_bonus = max(max_bonus, 1e-8)
    for function_id in selected_candidates:
        reranked[function_id] += activation * (generator_scores[function_id] / max_bonus)
    return reranked


def rank_position(scores: dict[str, float], positive_id: str) -> int:
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    for idx, (function_id, _) in enumerate(ordered, start=1):
        if function_id == positive_id:
            return idx
    raise KeyError(f"Positive function {positive_id} missing from scores")


def hits_at_k(ranks: list[int], k: int) -> float:
    return sum(1 for rank in ranks if rank <= k) / len(ranks) if ranks else 0.0


def mean_reciprocal_rank(ranks: list[int]) -> float:
    return sum(1.0 / rank for rank in ranks) / len(ranks) if ranks else 0.0


def rank_position_filtered(scores: dict[str, float], positive_id: str, excluded_ids: set[str]) -> int:
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    rank = 0
    for function_id, _ in ordered:
        if function_id in excluded_ids:
            continue
        rank += 1
        if function_id == positive_id:
            return rank
    raise KeyError(f"Positive function {positive_id} missing from filtered scores")


def summarize_ranks(ranks: list[int]) -> dict[str, float]:
    return {
        "mrr": mean_reciprocal_rank(ranks),
        "hits@1": hits_at_k(ranks, 1),
        "hits@3": hits_at_k(ranks, 3),
        "hits@5": hits_at_k(ranks, 5),
        "mean_rank": sum(ranks) / len(ranks) if ranks else 0.0,
    }


def label_stratum(train_support: int) -> str:
    if train_support <= 10:
        return "tail_1_10"
    if train_support <= 50:
        return "mid_11_50"
    return "head_gt_50"


def main() -> None:
    args = parse_args()
    random.seed(args.seed)

    node_dir = args.kg_dir / "nodes"
    edge_dir = args.kg_dir / "edges"

    function_rows = read_csv(node_dir / "function.csv")
    function_ids = [row["function_id"] for row in function_rows]
    function_names = {row["function_id"]: row["function_name_norm"] for row in function_rows}
    hierarchy_config = read_json(args.hierarchy_config) if args.hierarchy_config.exists() else {}
    family_to_functions, function_to_families, parent_to_children, child_to_parents = build_function_hierarchy_graph(
        hierarchy_config
    )

    poly_function_rows = read_csv(edge_dir / "poly_function.csv")
    poly_to_functions: dict[str, list[str]] = defaultdict(list)
    for row in poly_function_rows:
        poly_to_functions[row["source_id"]].append(row["target_id"])

    candidate_polys = [poly_id for poly_id, funcs in poly_to_functions.items() if len(funcs) >= 2]
    if not candidate_polys:
        candidate_polys = [poly_id for poly_id, funcs in poly_to_functions.items() if len(funcs) >= 1]

    eval_polys = sorted(candidate_polys)
    random.shuffle(eval_polys)
    eval_polys = eval_polys[: min(args.max_eval, len(eval_polys))]

    masked_edges: list[tuple[str, str]] = []
    train_poly_to_functions: dict[str, list[str]] = {poly_id: list(funcs) for poly_id, funcs in poly_to_functions.items()}
    for poly_id in eval_polys:
        chosen = random.choice(train_poly_to_functions[poly_id])
        train_poly_to_functions[poly_id].remove(chosen)
        masked_edges.append((poly_id, chosen))

    poly_ids = sorted(poly_to_functions)
    poly_to_organisms = build_poly_to_organisms(edge_dir)
    poly_to_diseases = build_poly_to_diseases(edge_dir)
    organism_to_genus, organism_to_kingdom = build_organism_metadata(node_dir)
    feature_dicts = build_feature_dicts(
        poly_ids,
        args.kg_dir,
        include_disease_features=args.include_disease_features,
    )
    feature_matrix, _ = vectorize_feature_dicts(poly_ids, feature_dicts)
    poly_idx = {poly_id: idx for idx, poly_id in enumerate(poly_ids)}

    function_to_train_polys: dict[str, list[str]] = defaultdict(list)
    for poly_id, functions in train_poly_to_functions.items():
        for function_id in functions:
            function_to_train_polys[function_id].append(poly_id)

    function_centroids: dict[str, np.ndarray] = {}
    for function_id in function_ids:
        member_polys = function_to_train_polys.get(function_id, [])
        if not member_polys:
            function_centroids[function_id] = np.zeros(feature_matrix.shape[1], dtype=np.float32)
            continue
        rows = [feature_matrix[poly_idx[poly_id]] for poly_id in member_polys]
        function_centroids[function_id] = np.mean(rows, axis=0)

    function_frequency = Counter()
    for functions in train_poly_to_functions.values():
        function_frequency.update(functions)
    if args.label_idf_weighting:
        label_weights = {
            function_id: np.log((1 + len(poly_ids)) / (1 + function_frequency.get(function_id, 0))) + 1.0
            for function_id in function_ids
        }
    else:
        label_weights = {function_id: 1.0 for function_id in function_ids}
    disease_function_priors = build_disease_function_priors(
        train_poly_to_functions=train_poly_to_functions,
        poly_to_diseases=poly_to_diseases,
        function_ids=function_ids,
        alpha=args.disease_prior_alpha,
    )
    tail_structural_signatures = build_tail_structural_signatures(
        poly_ids=poly_ids,
        feature_dicts=feature_dicts,
        train_poly_to_functions=train_poly_to_functions,
        function_ids=function_ids,
        function_frequency=function_frequency,
        support_threshold=args.tail_signature_threshold,
        feature_limit=args.tail_signature_feature_limit,
        min_local_rate=args.tail_signature_min_local_rate,
    )
    motif_signatures = build_label_specific_motif_signatures(
        poly_ids=poly_ids,
        feature_dicts=feature_dicts,
        train_poly_to_functions=train_poly_to_functions,
        function_ids=function_ids,
        function_frequency=function_frequency,
        support_threshold=args.motif_threshold,
        feature_limit=args.motif_feature_limit,
        min_local_rate=args.motif_min_local_rate,
    )
    taxonomy_motif_signatures = build_taxonomy_conditioned_motif_signatures(
        poly_ids=poly_ids,
        feature_dicts=feature_dicts,
        train_poly_to_functions=train_poly_to_functions,
        function_ids=function_ids,
        function_frequency=function_frequency,
        poly_to_organisms=poly_to_organisms,
        organism_to_genus=organism_to_genus,
        organism_to_kingdom=organism_to_kingdom,
        support_threshold=args.taxonomy_motif_threshold,
        feature_limit=args.taxonomy_motif_feature_limit,
        min_local_rate=args.taxonomy_motif_min_local_rate,
    )

    baseline_names = ["popularity", "meta_path_centroid", "meta_path_knn"]
    if args.rare_label_expansion:
        baseline_names.append("meta_path_knn_rare_expand")
    if args.source_constrained_rerank:
        baseline_names.append("meta_path_knn_source_rerank")
    if args.source_cluster_backoff:
        baseline_names.append("meta_path_knn_source_cluster_backoff")
    if args.tail_candidate_generation:
        baseline_names.append("meta_path_knn_tail_candidates")
    if args.label_specific_backoff:
        baseline_names.append("meta_path_knn_label_specific_backoff")
    if args.disease_label_prior:
        baseline_names.append("meta_path_knn_disease_prior")
    if args.tail_aware_disease_prior:
        baseline_names.append("meta_path_knn_tail_aware_disease_prior")
    if args.label_prototype_refinement:
        baseline_names.append("meta_path_knn_label_prototype_refine")
    if args.frequency_adjusted_disease_prior:
        baseline_names.append("meta_path_knn_freq_adjusted_disease_prior")
    if args.support_aware_candidate_generation:
        baseline_names.append("meta_path_knn_support_aware_candidates")
    if args.integrated_support_aware_knn:
        baseline_names.append("meta_path_knn_integrated_support")
        if args.frequency_adjusted_disease_prior:
            baseline_names.append("meta_path_knn_integrated_support_freq_prior")
    if args.explicit_tail_support_knn:
        baseline_names.append("meta_path_knn_explicit_tail_support")
        if args.frequency_adjusted_disease_prior:
            baseline_names.append("meta_path_knn_explicit_tail_support_freq_prior")
    if args.disease_conditioned_base_vote:
        baseline_names.append("meta_path_knn_disease_conditioned_vote")
        if args.frequency_adjusted_disease_prior:
            baseline_names.append("meta_path_knn_disease_conditioned_vote_freq_prior")
    if args.tail_structural_signature:
        baseline_names.append("meta_path_knn_tail_structural_signature")
        if args.disease_conditioned_base_vote:
            baseline_names.append("meta_path_knn_disease_conditioned_vote_tail_structural_signature")
            if args.frequency_adjusted_disease_prior:
                baseline_names.append("meta_path_knn_disease_conditioned_vote_freq_prior_tail_structural_signature")
    if args.structure_aware_candidate_generation:
        baseline_names.append("meta_path_knn_structure_candidates")
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            baseline_names.append("meta_path_knn_disease_conditioned_vote_freq_prior_structure_candidates")
    if args.label_specific_subgraph_motifs:
        baseline_names.append("meta_path_knn_subgraph_motifs")
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            baseline_names.append("meta_path_knn_disease_conditioned_vote_freq_prior_subgraph_motifs")
    if args.taxonomy_conditioned_motifs:
        baseline_names.append("meta_path_knn_taxonomy_motifs")
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            baseline_names.append("meta_path_knn_disease_conditioned_vote_freq_prior_taxonomy_motifs")
    if args.hierarchy_support:
        baseline_names.append("meta_path_knn_hierarchy_support")
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            baseline_names.append("meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_support")
    if args.hierarchy_graph_native:
        baseline_names.append("meta_path_knn_hierarchy_graph_native")
        if args.disease_conditioned_base_vote:
            baseline_names.append("meta_path_knn_disease_conditioned_vote_hierarchy_graph_native")
            if args.frequency_adjusted_disease_prior:
                baseline_names.append("meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_graph_native")
    if args.hierarchy_parent_child_native:
        baseline_names.append("meta_path_knn_hierarchy_parent_child_native")
        if args.disease_conditioned_base_vote:
            baseline_names.append("meta_path_knn_disease_conditioned_vote_hierarchy_parent_child_native")
            if args.frequency_adjusted_disease_prior:
                baseline_names.append("meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native")
    raw_ranks: dict[str, list[int]] = {name: [] for name in baseline_names}
    filtered_ranks: dict[str, list[int]] = {name: [] for name in baseline_names}
    tracked_per_label_baselines = ["meta_path_knn"]
    if args.rare_label_expansion:
        tracked_per_label_baselines.append("meta_path_knn_rare_expand")
    if args.source_constrained_rerank:
        tracked_per_label_baselines.append("meta_path_knn_source_rerank")
    if args.source_cluster_backoff:
        tracked_per_label_baselines.append("meta_path_knn_source_cluster_backoff")
    if args.tail_candidate_generation:
        tracked_per_label_baselines.append("meta_path_knn_tail_candidates")
    if args.label_specific_backoff:
        tracked_per_label_baselines.append("meta_path_knn_label_specific_backoff")
    if args.disease_label_prior:
        tracked_per_label_baselines.append("meta_path_knn_disease_prior")
    if args.tail_aware_disease_prior:
        tracked_per_label_baselines.append("meta_path_knn_tail_aware_disease_prior")
    if args.label_prototype_refinement:
        tracked_per_label_baselines.append("meta_path_knn_label_prototype_refine")
    if args.frequency_adjusted_disease_prior:
        tracked_per_label_baselines.append("meta_path_knn_freq_adjusted_disease_prior")
    if args.support_aware_candidate_generation:
        tracked_per_label_baselines.append("meta_path_knn_support_aware_candidates")
    if args.integrated_support_aware_knn:
        tracked_per_label_baselines.append("meta_path_knn_integrated_support")
        if args.frequency_adjusted_disease_prior:
            tracked_per_label_baselines.append("meta_path_knn_integrated_support_freq_prior")
    if args.explicit_tail_support_knn:
        tracked_per_label_baselines.append("meta_path_knn_explicit_tail_support")
        if args.frequency_adjusted_disease_prior:
            tracked_per_label_baselines.append("meta_path_knn_explicit_tail_support_freq_prior")
    if args.disease_conditioned_base_vote:
        tracked_per_label_baselines.append("meta_path_knn_disease_conditioned_vote")
        if args.frequency_adjusted_disease_prior:
            tracked_per_label_baselines.append("meta_path_knn_disease_conditioned_vote_freq_prior")
    if args.tail_structural_signature:
        tracked_per_label_baselines.append("meta_path_knn_tail_structural_signature")
        if args.disease_conditioned_base_vote:
            tracked_per_label_baselines.append("meta_path_knn_disease_conditioned_vote_tail_structural_signature")
            if args.frequency_adjusted_disease_prior:
                tracked_per_label_baselines.append(
                    "meta_path_knn_disease_conditioned_vote_freq_prior_tail_structural_signature"
                )
    if args.structure_aware_candidate_generation:
        tracked_per_label_baselines.append("meta_path_knn_structure_candidates")
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            tracked_per_label_baselines.append("meta_path_knn_disease_conditioned_vote_freq_prior_structure_candidates")
    if args.label_specific_subgraph_motifs:
        tracked_per_label_baselines.append("meta_path_knn_subgraph_motifs")
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            tracked_per_label_baselines.append("meta_path_knn_disease_conditioned_vote_freq_prior_subgraph_motifs")
    if args.taxonomy_conditioned_motifs:
        tracked_per_label_baselines.append("meta_path_knn_taxonomy_motifs")
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            tracked_per_label_baselines.append("meta_path_knn_disease_conditioned_vote_freq_prior_taxonomy_motifs")
    if args.hierarchy_support:
        tracked_per_label_baselines.append("meta_path_knn_hierarchy_support")
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            tracked_per_label_baselines.append("meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_support")
    if args.hierarchy_graph_native:
        tracked_per_label_baselines.append("meta_path_knn_hierarchy_graph_native")
        if args.disease_conditioned_base_vote:
            tracked_per_label_baselines.append("meta_path_knn_disease_conditioned_vote_hierarchy_graph_native")
            if args.frequency_adjusted_disease_prior:
                tracked_per_label_baselines.append(
                    "meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_graph_native"
                )
    if args.hierarchy_parent_child_native:
        tracked_per_label_baselines.append("meta_path_knn_hierarchy_parent_child_native")
        if args.disease_conditioned_base_vote:
            tracked_per_label_baselines.append("meta_path_knn_disease_conditioned_vote_hierarchy_parent_child_native")
            if args.frequency_adjusted_disease_prior:
                tracked_per_label_baselines.append(
                    "meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native"
                )
    per_label_records: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: {
            key: []
            for baseline_name in tracked_per_label_baselines
            for key in (f"raw_{baseline_name}", f"filtered_{baseline_name}")
        }
    )
    examples: list[dict] = []
    edge_records: list[dict] = []

    for poly_id, positive_function_id in masked_edges:
        vector = feature_matrix[poly_idx[poly_id]]
        popularity_scores = {
            function_id: float(function_frequency.get(function_id, 0))
            for function_id in function_ids
        }
        centroid_scores = {
            function_id: cosine_similarity(vector, function_centroids[function_id])
            for function_id in function_ids
        }
        knn_scores = build_knn_scores(
            poly_id,
            poly_ids,
            poly_idx,
            feature_matrix,
            train_poly_to_functions,
            function_ids,
            label_weights,
            top_k=args.top_k,
        )
        integrated_support_knn_scores = None
        if args.integrated_support_aware_knn:
            integrated_support_knn_scores = build_integrated_support_aware_knn_scores(
                poly_id=poly_id,
                poly_ids=poly_ids,
                poly_idx=poly_idx,
                feature_matrix=feature_matrix,
                train_poly_to_functions=train_poly_to_functions,
                function_ids=function_ids,
                label_weights=label_weights,
                function_frequency=function_frequency,
                poly_to_organisms=poly_to_organisms,
                organism_to_genus=organism_to_genus,
                organism_to_kingdom=organism_to_kingdom,
                base_top_k=args.integrated_support_top_k,
                extended_top_k=args.integrated_support_extended_k,
                support_threshold=args.integrated_support_threshold,
                expansion_decay=args.integrated_support_decay,
                exact_weight=args.integrated_support_exact_weight,
                genus_weight=args.integrated_support_genus_weight,
                kingdom_weight=args.integrated_support_kingdom_weight,
            )
        explicit_tail_support_knn_scores = None
        if args.explicit_tail_support_knn:
            explicit_tail_support_knn_scores = build_explicit_tail_support_knn_scores(
                poly_id=poly_id,
                poly_ids=poly_ids,
                poly_idx=poly_idx,
                feature_matrix=feature_matrix,
                train_poly_to_functions=train_poly_to_functions,
                function_ids=function_ids,
                label_weights=label_weights,
                function_frequency=function_frequency,
                poly_to_organisms=poly_to_organisms,
                organism_to_genus=organism_to_genus,
                organism_to_kingdom=organism_to_kingdom,
                base_top_k=args.tail_support_top_k,
                extended_top_k=args.tail_support_extended_k,
                tail_threshold=args.tail_support_threshold,
                expansion_decay=args.tail_support_decay,
                exact_weight=args.tail_support_exact_weight,
                genus_weight=args.tail_support_genus_weight,
                kingdom_weight=args.tail_support_kingdom_weight,
                tail_boost=args.tail_support_boost,
            )
        disease_conditioned_vote_scores = None
        if args.disease_conditioned_base_vote:
            disease_conditioned_vote_scores = build_disease_conditioned_knn_scores(
                poly_id=poly_id,
                poly_ids=poly_ids,
                poly_idx=poly_idx,
                feature_matrix=feature_matrix,
                train_poly_to_functions=train_poly_to_functions,
                function_ids=function_ids,
                label_weights=label_weights,
                poly_to_diseases=poly_to_diseases,
                disease_function_priors=disease_function_priors,
                top_k=args.disease_vote_top_k,
                smoothing_weight=args.disease_vote_weight,
                max_boost=args.disease_vote_max_boost,
            )
        hierarchy_graph_native_scores = None
        if args.hierarchy_graph_native:
            hierarchy_graph_native_scores = build_graph_native_hierarchy_scores(
                base_scores=knn_scores,
                function_names=function_names,
                function_frequency=function_frequency,
                function_to_families=function_to_families,
                family_to_functions=family_to_functions,
                base_window=args.hierarchy_base_window,
                support_threshold=args.hierarchy_threshold,
                min_seed_count=args.hierarchy_min_seed_count,
                specificity_power=args.hierarchy_specificity_power,
                graph_weight=args.hierarchy_graph_weight,
            )
        disease_conditioned_vote_hierarchy_graph_native_scores = None
        if args.hierarchy_graph_native and disease_conditioned_vote_scores is not None:
            disease_conditioned_vote_hierarchy_graph_native_scores = build_graph_native_hierarchy_scores(
                base_scores=disease_conditioned_vote_scores,
                function_names=function_names,
                function_frequency=function_frequency,
                function_to_families=function_to_families,
                family_to_functions=family_to_functions,
                base_window=args.hierarchy_base_window,
                support_threshold=args.hierarchy_threshold,
                min_seed_count=args.hierarchy_min_seed_count,
                specificity_power=args.hierarchy_specificity_power,
                graph_weight=args.hierarchy_graph_weight,
            )
        hierarchy_parent_child_native_scores = None
        if args.hierarchy_parent_child_native:
            hierarchy_parent_child_native_scores = build_parent_child_hierarchy_scores(
                base_scores=knn_scores,
                function_names=function_names,
                function_frequency=function_frequency,
                function_to_families=function_to_families,
                family_to_functions=family_to_functions,
                parent_to_children=parent_to_children,
                child_to_parents=child_to_parents,
                base_window=args.hierarchy_base_window,
                support_threshold=args.hierarchy_threshold,
                min_seed_count=args.hierarchy_min_seed_count,
                specificity_power=args.hierarchy_specificity_power,
                graph_weight=args.hierarchy_graph_weight,
                confidence_threshold=args.hierarchy_confidence_threshold,
                adaptive_power=args.hierarchy_adaptive_power,
            )
        disease_conditioned_vote_hierarchy_parent_child_native_scores = None
        if args.hierarchy_parent_child_native and disease_conditioned_vote_scores is not None:
            disease_conditioned_vote_hierarchy_parent_child_native_scores = build_parent_child_hierarchy_scores(
                base_scores=disease_conditioned_vote_scores,
                function_names=function_names,
                function_frequency=function_frequency,
                function_to_families=function_to_families,
                family_to_functions=family_to_functions,
                parent_to_children=parent_to_children,
                child_to_parents=child_to_parents,
                base_window=args.hierarchy_base_window,
                support_threshold=args.hierarchy_threshold,
                min_seed_count=args.hierarchy_min_seed_count,
                specificity_power=args.hierarchy_specificity_power,
                graph_weight=args.hierarchy_graph_weight,
                confidence_threshold=args.hierarchy_confidence_threshold,
                adaptive_power=args.hierarchy_adaptive_power,
            )
        rare_expand_scores = None
        if args.rare_label_expansion:
            rare_expand_scores = build_rare_label_expansion_scores(
                poly_id=poly_id,
                poly_ids=poly_ids,
                poly_idx=poly_idx,
                feature_matrix=feature_matrix,
                train_poly_to_functions=train_poly_to_functions,
                function_ids=function_ids,
                label_weights=label_weights,
                function_frequency=function_frequency,
                base_top_k=args.top_k,
                rare_label_threshold=args.rare_label_threshold,
                rare_label_top_k=args.rare_label_top_k,
                rare_label_decay=args.rare_label_decay,
            )
        source_rerank_scores = None
        if args.source_constrained_rerank:
            source_rerank_scores = build_source_constrained_rerank_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                poly_ids=poly_ids,
                poly_idx=poly_idx,
                feature_matrix=feature_matrix,
                train_poly_to_functions=train_poly_to_functions,
                poly_to_organisms=poly_to_organisms,
                rerank_top_n=args.source_rerank_top_n,
                rerank_weight=args.source_rerank_weight,
            )
        source_cluster_scores = None
        if args.source_cluster_backoff:
            source_cluster_scores = build_source_cluster_backoff_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                poly_ids=poly_ids,
                poly_idx=poly_idx,
                feature_matrix=feature_matrix,
                train_poly_to_functions=train_poly_to_functions,
                poly_to_organisms=poly_to_organisms,
                organism_to_genus=organism_to_genus,
                organism_to_kingdom=organism_to_kingdom,
                rerank_top_n=args.source_cluster_top_n,
                exact_weight=args.source_cluster_exact_weight,
                genus_weight=args.source_cluster_genus_weight,
                kingdom_weight=args.source_cluster_kingdom_weight,
            )
        tail_candidate_scores = None
        if args.tail_candidate_generation:
            tail_candidate_scores = build_tail_candidate_generation_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                poly_ids=poly_ids,
                poly_idx=poly_idx,
                feature_matrix=feature_matrix,
                train_poly_to_functions=train_poly_to_functions,
                function_frequency=function_frequency,
                poly_to_organisms=poly_to_organisms,
                organism_to_genus=organism_to_genus,
                organism_to_kingdom=organism_to_kingdom,
                base_top_k=args.top_k,
                tail_label_threshold=args.tail_label_threshold,
                candidate_top_k=args.tail_candidate_top_k,
                candidate_limit=args.tail_candidate_limit,
                activation=args.tail_candidate_activation,
                source_exact_weight=args.tail_candidate_source_exact_weight,
                source_genus_weight=args.tail_candidate_source_genus_weight,
                source_kingdom_weight=args.tail_candidate_source_kingdom_weight,
            )
        label_specific_backoff_scores = None
        if args.label_specific_backoff:
            label_specific_backoff_scores = build_label_specific_backoff_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                poly_ids=poly_ids,
                poly_idx=poly_idx,
                feature_matrix=feature_matrix,
                train_poly_to_functions=train_poly_to_functions,
                function_frequency=function_frequency,
                poly_to_organisms=poly_to_organisms,
                organism_to_genus=organism_to_genus,
                organism_to_kingdom=organism_to_kingdom,
                rerank_top_n=args.label_backoff_top_n,
                label_backoff_threshold=args.label_backoff_threshold,
                label_backoff_weight=args.label_backoff_weight,
                exact_weight=args.label_backoff_exact_weight,
                genus_weight=args.label_backoff_genus_weight,
                kingdom_weight=args.label_backoff_kingdom_weight,
            )
        disease_prior_scores = None
        if args.disease_label_prior:
            disease_prior_scores = build_disease_label_prior_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                poly_to_diseases=poly_to_diseases,
                disease_function_priors=disease_function_priors,
                rerank_top_n=args.disease_prior_top_n,
                prior_weight=args.disease_prior_weight,
            )
        tail_aware_disease_prior_scores = None
        if args.tail_aware_disease_prior:
            tail_aware_disease_prior_scores = build_tail_aware_disease_prior_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                poly_to_diseases=poly_to_diseases,
                disease_function_priors=disease_function_priors,
                function_frequency=function_frequency,
                rerank_top_n=args.tail_disease_prior_top_n,
                tail_threshold=args.tail_disease_prior_threshold,
                prior_weight=args.tail_disease_prior_weight,
                tail_boost=args.tail_disease_prior_boost,
                max_multiplier=args.tail_disease_prior_max_multiplier,
            )
        label_prototype_scores = None
        if args.label_prototype_refinement:
            prototype_base_scores = disease_prior_scores if disease_prior_scores is not None else knn_scores
            label_prototype_scores = build_label_prototype_refinement_scores(
                base_scores=prototype_base_scores,
                poly_id=poly_id,
                poly_idx=poly_idx,
                feature_matrix=feature_matrix,
                function_to_train_polys=function_to_train_polys,
                function_centroids=function_centroids,
                function_frequency=function_frequency,
                rerank_top_n=args.prototype_top_n,
                prototype_neighbors=args.prototype_neighbors,
                prototype_weight=args.prototype_weight,
                prototype_tail_threshold=args.prototype_tail_threshold,
                prototype_tail_boost=args.prototype_tail_boost,
            )
        freq_adjusted_disease_prior_scores = None
        if args.frequency_adjusted_disease_prior:
            freq_adjusted_disease_prior_scores = build_frequency_adjusted_disease_prior_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                poly_to_diseases=poly_to_diseases,
                disease_function_priors=disease_function_priors,
                function_frequency=function_frequency,
                rerank_top_n=args.freq_disease_prior_top_n,
                prior_weight=args.freq_disease_prior_weight,
                adjustment_strength=args.freq_disease_prior_strength,
                adjustment_mode=args.freq_disease_prior_mode,
            )
        integrated_support_freq_prior_scores = None
        if args.integrated_support_aware_knn and args.frequency_adjusted_disease_prior:
            integrated_support_freq_prior_scores = build_frequency_adjusted_disease_prior_scores(
                base_scores=integrated_support_knn_scores,
                poly_id=poly_id,
                poly_to_diseases=poly_to_diseases,
                disease_function_priors=disease_function_priors,
                function_frequency=function_frequency,
                rerank_top_n=args.freq_disease_prior_top_n,
                prior_weight=args.freq_disease_prior_weight,
                adjustment_strength=args.freq_disease_prior_strength,
                adjustment_mode=args.freq_disease_prior_mode,
            )
        explicit_tail_support_freq_prior_scores = None
        if args.explicit_tail_support_knn and args.frequency_adjusted_disease_prior:
            explicit_tail_support_freq_prior_scores = build_frequency_adjusted_disease_prior_scores(
                base_scores=explicit_tail_support_knn_scores,
                poly_id=poly_id,
                poly_to_diseases=poly_to_diseases,
                disease_function_priors=disease_function_priors,
                function_frequency=function_frequency,
                rerank_top_n=args.freq_disease_prior_top_n,
                prior_weight=args.freq_disease_prior_weight,
                adjustment_strength=args.freq_disease_prior_strength,
                adjustment_mode=args.freq_disease_prior_mode,
            )
        disease_conditioned_vote_freq_prior_scores = None
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            disease_conditioned_vote_freq_prior_scores = build_frequency_adjusted_disease_prior_scores(
                base_scores=disease_conditioned_vote_scores,
                poly_id=poly_id,
                poly_to_diseases=poly_to_diseases,
                disease_function_priors=disease_function_priors,
                function_frequency=function_frequency,
                rerank_top_n=args.freq_disease_prior_top_n,
                prior_weight=args.freq_disease_prior_weight,
                adjustment_strength=args.freq_disease_prior_strength,
                adjustment_mode=args.freq_disease_prior_mode,
            )
        disease_conditioned_vote_freq_prior_hierarchy_graph_native_scores = None
        if args.hierarchy_graph_native and disease_conditioned_vote_hierarchy_graph_native_scores is not None and args.frequency_adjusted_disease_prior:
            disease_conditioned_vote_freq_prior_hierarchy_graph_native_scores = build_frequency_adjusted_disease_prior_scores(
                base_scores=disease_conditioned_vote_hierarchy_graph_native_scores,
                poly_id=poly_id,
                poly_to_diseases=poly_to_diseases,
                disease_function_priors=disease_function_priors,
                function_frequency=function_frequency,
                rerank_top_n=args.freq_disease_prior_top_n,
                prior_weight=args.freq_disease_prior_weight,
                adjustment_strength=args.freq_disease_prior_strength,
                adjustment_mode=args.freq_disease_prior_mode,
            )
        disease_conditioned_vote_freq_prior_hierarchy_parent_child_native_scores = None
        if (
            args.hierarchy_parent_child_native
            and disease_conditioned_vote_hierarchy_parent_child_native_scores is not None
            and args.frequency_adjusted_disease_prior
        ):
            disease_conditioned_vote_freq_prior_hierarchy_parent_child_native_scores = build_frequency_adjusted_disease_prior_scores(
                base_scores=disease_conditioned_vote_hierarchy_parent_child_native_scores,
                poly_id=poly_id,
                poly_to_diseases=poly_to_diseases,
                disease_function_priors=disease_function_priors,
                function_frequency=function_frequency,
                rerank_top_n=args.freq_disease_prior_top_n,
                prior_weight=args.freq_disease_prior_weight,
                adjustment_strength=args.freq_disease_prior_strength,
                adjustment_mode=args.freq_disease_prior_mode,
            )
        tail_structural_signature_scores = None
        if args.tail_structural_signature:
            tail_structural_signature_scores = build_tail_structural_signature_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                feature_dicts=feature_dicts,
                function_frequency=function_frequency,
                tail_structural_signatures=tail_structural_signatures,
                rerank_top_n=args.tail_signature_top_n,
                support_threshold=args.tail_signature_threshold,
                signature_weight=args.tail_signature_weight,
                max_boost=args.tail_signature_max_boost,
            )
        disease_conditioned_vote_tail_structural_signature_scores = None
        if args.tail_structural_signature and args.disease_conditioned_base_vote:
            disease_conditioned_vote_tail_structural_signature_scores = build_tail_structural_signature_scores(
                base_scores=disease_conditioned_vote_scores,
                poly_id=poly_id,
                feature_dicts=feature_dicts,
                function_frequency=function_frequency,
                tail_structural_signatures=tail_structural_signatures,
                rerank_top_n=args.tail_signature_top_n,
                support_threshold=args.tail_signature_threshold,
                signature_weight=args.tail_signature_weight,
                max_boost=args.tail_signature_max_boost,
            )
        disease_conditioned_vote_freq_prior_tail_structural_signature_scores = None
        if args.tail_structural_signature and args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            disease_conditioned_vote_freq_prior_tail_structural_signature_scores = build_tail_structural_signature_scores(
                base_scores=disease_conditioned_vote_freq_prior_scores,
                poly_id=poly_id,
                feature_dicts=feature_dicts,
                function_frequency=function_frequency,
                tail_structural_signatures=tail_structural_signatures,
                rerank_top_n=args.tail_signature_top_n,
                support_threshold=args.tail_signature_threshold,
                signature_weight=args.tail_signature_weight,
                max_boost=args.tail_signature_max_boost,
            )
        structure_candidate_scores = None
        if args.structure_aware_candidate_generation:
            structure_candidate_scores = build_structure_aware_candidate_generation_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                feature_dicts=feature_dicts,
                function_frequency=function_frequency,
                tail_structural_signatures=tail_structural_signatures,
                base_window=args.structure_candidate_base_window,
                support_threshold=args.structure_candidate_threshold,
                candidate_limit=args.structure_candidate_limit,
                activation=args.structure_candidate_activation,
            )
        disease_conditioned_vote_freq_prior_structure_candidate_scores = None
        if args.structure_aware_candidate_generation and args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            disease_conditioned_vote_freq_prior_structure_candidate_scores = build_structure_aware_candidate_generation_scores(
                base_scores=disease_conditioned_vote_freq_prior_scores,
                poly_id=poly_id,
                feature_dicts=feature_dicts,
                function_frequency=function_frequency,
                tail_structural_signatures=tail_structural_signatures,
                base_window=args.structure_candidate_base_window,
                support_threshold=args.structure_candidate_threshold,
                candidate_limit=args.structure_candidate_limit,
                activation=args.structure_candidate_activation,
            )
        subgraph_motif_scores = None
        if args.label_specific_subgraph_motifs:
            subgraph_motif_scores = build_label_specific_motif_candidate_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                feature_dicts=feature_dicts,
                function_frequency=function_frequency,
                motif_signatures=motif_signatures,
                base_window=args.motif_candidate_base_window,
                support_threshold=args.motif_threshold,
                candidate_limit=args.motif_candidate_limit,
                activation=args.motif_candidate_activation,
            )
        disease_conditioned_vote_freq_prior_subgraph_motif_scores = None
        if args.label_specific_subgraph_motifs and args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            disease_conditioned_vote_freq_prior_subgraph_motif_scores = build_label_specific_motif_candidate_scores(
                base_scores=disease_conditioned_vote_freq_prior_scores,
                poly_id=poly_id,
                feature_dicts=feature_dicts,
                function_frequency=function_frequency,
                motif_signatures=motif_signatures,
                base_window=args.motif_candidate_base_window,
                support_threshold=args.motif_threshold,
                candidate_limit=args.motif_candidate_limit,
                activation=args.motif_candidate_activation,
            )
        taxonomy_motif_scores = None
        if args.taxonomy_conditioned_motifs:
            taxonomy_motif_scores = build_taxonomy_conditioned_motif_candidate_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                feature_dicts=feature_dicts,
                function_frequency=function_frequency,
                taxonomy_motif_signatures=taxonomy_motif_signatures,
                poly_to_organisms=poly_to_organisms,
                organism_to_genus=organism_to_genus,
                organism_to_kingdom=organism_to_kingdom,
                base_window=args.taxonomy_motif_base_window,
                support_threshold=args.taxonomy_motif_threshold,
                candidate_limit=args.taxonomy_motif_candidate_limit,
                activation=args.taxonomy_motif_activation,
            )
        disease_conditioned_vote_freq_prior_taxonomy_motif_scores = None
        if args.taxonomy_conditioned_motifs and args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            disease_conditioned_vote_freq_prior_taxonomy_motif_scores = build_taxonomy_conditioned_motif_candidate_scores(
                base_scores=disease_conditioned_vote_freq_prior_scores,
                poly_id=poly_id,
                feature_dicts=feature_dicts,
                function_frequency=function_frequency,
                taxonomy_motif_signatures=taxonomy_motif_signatures,
                poly_to_organisms=poly_to_organisms,
                organism_to_genus=organism_to_genus,
                organism_to_kingdom=organism_to_kingdom,
                base_window=args.taxonomy_motif_base_window,
                support_threshold=args.taxonomy_motif_threshold,
                candidate_limit=args.taxonomy_motif_candidate_limit,
                activation=args.taxonomy_motif_activation,
            )
        hierarchy_support_scores = None
        if args.hierarchy_support:
            hierarchy_support_scores = build_hierarchy_candidate_scores(
                base_scores=knn_scores,
                function_names=function_names,
                function_frequency=function_frequency,
                function_to_families=function_to_families,
                family_to_functions=family_to_functions,
                base_window=args.hierarchy_base_window,
                support_threshold=args.hierarchy_threshold,
                candidate_limit=args.hierarchy_candidate_limit,
                activation=args.hierarchy_activation,
                min_seed_count=args.hierarchy_min_seed_count,
                specificity_power=args.hierarchy_specificity_power,
            )
        disease_conditioned_vote_freq_prior_hierarchy_support_scores = None
        if args.hierarchy_support and args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            disease_conditioned_vote_freq_prior_hierarchy_support_scores = build_hierarchy_candidate_scores(
                base_scores=disease_conditioned_vote_freq_prior_scores,
                function_names=function_names,
                function_frequency=function_frequency,
                function_to_families=function_to_families,
                family_to_functions=family_to_functions,
                base_window=args.hierarchy_base_window,
                support_threshold=args.hierarchy_threshold,
                candidate_limit=args.hierarchy_candidate_limit,
                activation=args.hierarchy_activation,
                min_seed_count=args.hierarchy_min_seed_count,
                specificity_power=args.hierarchy_specificity_power,
            )
        support_aware_candidate_scores = None
        if args.support_aware_candidate_generation:
            candidate_base_scores = build_support_aware_candidate_generation_scores(
                base_scores=knn_scores,
                poly_id=poly_id,
                poly_ids=poly_ids,
                poly_idx=poly_idx,
                feature_matrix=feature_matrix,
                train_poly_to_functions=train_poly_to_functions,
                function_frequency=function_frequency,
                poly_to_organisms=poly_to_organisms,
                organism_to_genus=organism_to_genus,
                organism_to_kingdom=organism_to_kingdom,
                candidate_top_k=args.support_candidate_top_k,
                base_window=args.support_candidate_base_window,
                support_threshold=args.support_candidate_threshold,
                candidate_limit=args.support_candidate_limit,
                activation=args.support_candidate_activation,
                exact_weight=args.support_candidate_exact_weight,
                genus_weight=args.support_candidate_genus_weight,
                kingdom_weight=args.support_candidate_kingdom_weight,
            )
            if args.frequency_adjusted_disease_prior:
                support_aware_candidate_scores = build_frequency_adjusted_disease_prior_scores(
                    base_scores=candidate_base_scores,
                    poly_id=poly_id,
                    poly_to_diseases=poly_to_diseases,
                    disease_function_priors=disease_function_priors,
                    function_frequency=function_frequency,
                    rerank_top_n=args.freq_disease_prior_top_n,
                    prior_weight=args.freq_disease_prior_weight,
                    adjustment_strength=args.freq_disease_prior_strength,
                    adjustment_mode=args.freq_disease_prior_mode,
                )
            elif args.disease_label_prior:
                support_aware_candidate_scores = build_disease_label_prior_scores(
                    base_scores=candidate_base_scores,
                    poly_id=poly_id,
                    poly_to_diseases=poly_to_diseases,
                    disease_function_priors=disease_function_priors,
                    rerank_top_n=args.disease_prior_top_n,
                    prior_weight=args.disease_prior_weight,
                )
            else:
                support_aware_candidate_scores = candidate_base_scores
        excluded_function_ids = set(poly_to_functions[poly_id]) - {positive_function_id}

        baseline_scores = {
            "popularity": popularity_scores,
            "meta_path_centroid": centroid_scores,
            "meta_path_knn": knn_scores,
        }
        if rare_expand_scores is not None:
            baseline_scores["meta_path_knn_rare_expand"] = rare_expand_scores
        if source_rerank_scores is not None:
            baseline_scores["meta_path_knn_source_rerank"] = source_rerank_scores
        if source_cluster_scores is not None:
            baseline_scores["meta_path_knn_source_cluster_backoff"] = source_cluster_scores
        if tail_candidate_scores is not None:
            baseline_scores["meta_path_knn_tail_candidates"] = tail_candidate_scores
        if label_specific_backoff_scores is not None:
            baseline_scores["meta_path_knn_label_specific_backoff"] = label_specific_backoff_scores
        if disease_prior_scores is not None:
            baseline_scores["meta_path_knn_disease_prior"] = disease_prior_scores
        if tail_aware_disease_prior_scores is not None:
            baseline_scores["meta_path_knn_tail_aware_disease_prior"] = tail_aware_disease_prior_scores
        if label_prototype_scores is not None:
            baseline_scores["meta_path_knn_label_prototype_refine"] = label_prototype_scores
        if freq_adjusted_disease_prior_scores is not None:
            baseline_scores["meta_path_knn_freq_adjusted_disease_prior"] = freq_adjusted_disease_prior_scores
        if integrated_support_knn_scores is not None:
            baseline_scores["meta_path_knn_integrated_support"] = integrated_support_knn_scores
        if integrated_support_freq_prior_scores is not None:
            baseline_scores["meta_path_knn_integrated_support_freq_prior"] = integrated_support_freq_prior_scores
        if explicit_tail_support_knn_scores is not None:
            baseline_scores["meta_path_knn_explicit_tail_support"] = explicit_tail_support_knn_scores
        if explicit_tail_support_freq_prior_scores is not None:
            baseline_scores["meta_path_knn_explicit_tail_support_freq_prior"] = explicit_tail_support_freq_prior_scores
        if disease_conditioned_vote_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote"] = disease_conditioned_vote_scores
        if disease_conditioned_vote_freq_prior_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_freq_prior"] = disease_conditioned_vote_freq_prior_scores
        if hierarchy_graph_native_scores is not None:
            baseline_scores["meta_path_knn_hierarchy_graph_native"] = hierarchy_graph_native_scores
        if disease_conditioned_vote_hierarchy_graph_native_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_hierarchy_graph_native"] = (
                disease_conditioned_vote_hierarchy_graph_native_scores
            )
        if disease_conditioned_vote_freq_prior_hierarchy_graph_native_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_graph_native"] = (
                disease_conditioned_vote_freq_prior_hierarchy_graph_native_scores
            )
        if hierarchy_parent_child_native_scores is not None:
            baseline_scores["meta_path_knn_hierarchy_parent_child_native"] = hierarchy_parent_child_native_scores
        if disease_conditioned_vote_hierarchy_parent_child_native_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_hierarchy_parent_child_native"] = (
                disease_conditioned_vote_hierarchy_parent_child_native_scores
            )
        if disease_conditioned_vote_freq_prior_hierarchy_parent_child_native_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native"] = (
                disease_conditioned_vote_freq_prior_hierarchy_parent_child_native_scores
            )
        if tail_structural_signature_scores is not None:
            baseline_scores["meta_path_knn_tail_structural_signature"] = tail_structural_signature_scores
        if disease_conditioned_vote_tail_structural_signature_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_tail_structural_signature"] = (
                disease_conditioned_vote_tail_structural_signature_scores
            )
        if disease_conditioned_vote_freq_prior_tail_structural_signature_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_freq_prior_tail_structural_signature"] = (
                disease_conditioned_vote_freq_prior_tail_structural_signature_scores
            )
        if structure_candidate_scores is not None:
            baseline_scores["meta_path_knn_structure_candidates"] = structure_candidate_scores
        if disease_conditioned_vote_freq_prior_structure_candidate_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_freq_prior_structure_candidates"] = (
                disease_conditioned_vote_freq_prior_structure_candidate_scores
            )
        if subgraph_motif_scores is not None:
            baseline_scores["meta_path_knn_subgraph_motifs"] = subgraph_motif_scores
        if disease_conditioned_vote_freq_prior_subgraph_motif_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_freq_prior_subgraph_motifs"] = (
                disease_conditioned_vote_freq_prior_subgraph_motif_scores
            )
        if taxonomy_motif_scores is not None:
            baseline_scores["meta_path_knn_taxonomy_motifs"] = taxonomy_motif_scores
        if disease_conditioned_vote_freq_prior_taxonomy_motif_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_freq_prior_taxonomy_motifs"] = (
                disease_conditioned_vote_freq_prior_taxonomy_motif_scores
            )
        if hierarchy_support_scores is not None:
            baseline_scores["meta_path_knn_hierarchy_support"] = hierarchy_support_scores
        if disease_conditioned_vote_freq_prior_hierarchy_support_scores is not None:
            baseline_scores["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_support"] = (
                disease_conditioned_vote_freq_prior_hierarchy_support_scores
            )
        if support_aware_candidate_scores is not None:
            baseline_scores["meta_path_knn_support_aware_candidates"] = support_aware_candidate_scores
        baseline_raw = {}
        baseline_filtered = {}
        for baseline_name, scores in baseline_scores.items():
            raw_rank = rank_position(scores, positive_function_id)
            filtered_rank = rank_position_filtered(scores, positive_function_id, excluded_function_ids)
            raw_ranks[baseline_name].append(raw_rank)
            filtered_ranks[baseline_name].append(filtered_rank)
            baseline_raw[baseline_name] = raw_rank
            baseline_filtered[baseline_name] = filtered_rank

        for baseline_name in tracked_per_label_baselines:
            per_label_records[positive_function_id][f"raw_{baseline_name}"].append(baseline_raw[baseline_name])
            per_label_records[positive_function_id][f"filtered_{baseline_name}"].append(
                baseline_filtered[baseline_name]
            )
        if args.save_edge_records:
            edge_records.append(
                {
                    "poly_id": poly_id,
                    "positive_function_id": positive_function_id,
                    "positive_function_name": function_names[positive_function_id],
                    "train_support": function_frequency.get(positive_function_id, 0),
                    "stratum": label_stratum(function_frequency.get(positive_function_id, 0)),
                    "raw_ranks": baseline_raw,
                    "filtered_ranks": baseline_filtered,
                }
            )

        if len(examples) < 10:
            if source_rerank_scores is not None:
                primary_example_scores = source_rerank_scores
            elif source_cluster_scores is not None:
                primary_example_scores = source_cluster_scores
            elif tail_candidate_scores is not None:
                primary_example_scores = tail_candidate_scores
            elif label_specific_backoff_scores is not None:
                primary_example_scores = label_specific_backoff_scores
            elif disease_prior_scores is not None:
                primary_example_scores = disease_prior_scores
            elif tail_aware_disease_prior_scores is not None:
                primary_example_scores = tail_aware_disease_prior_scores
            elif label_prototype_scores is not None:
                primary_example_scores = label_prototype_scores
            elif freq_adjusted_disease_prior_scores is not None:
                primary_example_scores = freq_adjusted_disease_prior_scores
            elif integrated_support_freq_prior_scores is not None:
                primary_example_scores = integrated_support_freq_prior_scores
            elif integrated_support_knn_scores is not None:
                primary_example_scores = integrated_support_knn_scores
            elif explicit_tail_support_freq_prior_scores is not None:
                primary_example_scores = explicit_tail_support_freq_prior_scores
            elif explicit_tail_support_knn_scores is not None:
                primary_example_scores = explicit_tail_support_knn_scores
            elif disease_conditioned_vote_freq_prior_tail_structural_signature_scores is not None:
                primary_example_scores = disease_conditioned_vote_freq_prior_tail_structural_signature_scores
            elif disease_conditioned_vote_tail_structural_signature_scores is not None:
                primary_example_scores = disease_conditioned_vote_tail_structural_signature_scores
            elif tail_structural_signature_scores is not None:
                primary_example_scores = tail_structural_signature_scores
            elif disease_conditioned_vote_freq_prior_structure_candidate_scores is not None:
                primary_example_scores = disease_conditioned_vote_freq_prior_structure_candidate_scores
            elif structure_candidate_scores is not None:
                primary_example_scores = structure_candidate_scores
            elif disease_conditioned_vote_freq_prior_subgraph_motif_scores is not None:
                primary_example_scores = disease_conditioned_vote_freq_prior_subgraph_motif_scores
            elif subgraph_motif_scores is not None:
                primary_example_scores = subgraph_motif_scores
            elif disease_conditioned_vote_freq_prior_taxonomy_motif_scores is not None:
                primary_example_scores = disease_conditioned_vote_freq_prior_taxonomy_motif_scores
            elif taxonomy_motif_scores is not None:
                primary_example_scores = taxonomy_motif_scores
            elif disease_conditioned_vote_freq_prior_hierarchy_support_scores is not None:
                primary_example_scores = disease_conditioned_vote_freq_prior_hierarchy_support_scores
            elif hierarchy_support_scores is not None:
                primary_example_scores = hierarchy_support_scores
            elif disease_conditioned_vote_freq_prior_hierarchy_graph_native_scores is not None:
                primary_example_scores = disease_conditioned_vote_freq_prior_hierarchy_graph_native_scores
            elif disease_conditioned_vote_hierarchy_graph_native_scores is not None:
                primary_example_scores = disease_conditioned_vote_hierarchy_graph_native_scores
            elif hierarchy_graph_native_scores is not None:
                primary_example_scores = hierarchy_graph_native_scores
            elif disease_conditioned_vote_freq_prior_hierarchy_parent_child_native_scores is not None:
                primary_example_scores = disease_conditioned_vote_freq_prior_hierarchy_parent_child_native_scores
            elif disease_conditioned_vote_hierarchy_parent_child_native_scores is not None:
                primary_example_scores = disease_conditioned_vote_hierarchy_parent_child_native_scores
            elif hierarchy_parent_child_native_scores is not None:
                primary_example_scores = hierarchy_parent_child_native_scores
            elif disease_conditioned_vote_freq_prior_scores is not None:
                primary_example_scores = disease_conditioned_vote_freq_prior_scores
            elif disease_conditioned_vote_scores is not None:
                primary_example_scores = disease_conditioned_vote_scores
            elif support_aware_candidate_scores is not None:
                primary_example_scores = support_aware_candidate_scores
            elif rare_expand_scores is not None:
                primary_example_scores = rare_expand_scores
            else:
                primary_example_scores = knn_scores
            top_predictions = sorted(primary_example_scores.items(), key=lambda item: (-item[1], item[0]))[:5]
            examples.append(
                {
                    "poly_id": poly_id,
                    "held_out_function_id": positive_function_id,
                    "held_out_function_name": function_names[positive_function_id],
                    "raw_ranks": baseline_raw,
                    "filtered_ranks": baseline_filtered,
                    "top5_predictions": [
                        {"function_id": function_id, "function_name": function_names[function_id], "score": score}
                        for function_id, score in top_predictions
                    ],
                }
            )

    per_label_summary: dict[str, dict[str, float | int | str]] = {}
    stratified_summary: dict[str, dict[str, dict[str, float | int]]] = {}
    for function_id, label_records in per_label_records.items():
        train_support = function_frequency.get(function_id, 0)
        summary = {
            "function_name": function_names[function_id],
            "train_support": train_support,
            "eval_support": len(label_records["filtered_meta_path_knn"]),
            "stratum": label_stratum(train_support),
        }
        for baseline_name in tracked_per_label_baselines:
            summary[f"raw_{baseline_name}_mrr"] = mean_reciprocal_rank(label_records[f"raw_{baseline_name}"])
            summary[f"raw_{baseline_name}_hits@1"] = hits_at_k(label_records[f"raw_{baseline_name}"], 1)
            summary[f"raw_{baseline_name}_hits@3"] = hits_at_k(label_records[f"raw_{baseline_name}"], 3)
            summary[f"filtered_{baseline_name}_mrr"] = mean_reciprocal_rank(
                label_records[f"filtered_{baseline_name}"]
            )
            summary[f"filtered_{baseline_name}_hits@1"] = hits_at_k(
                label_records[f"filtered_{baseline_name}"], 1
            )
            summary[f"filtered_{baseline_name}_hits@3"] = hits_at_k(
                label_records[f"filtered_{baseline_name}"], 3
            )
            summary[f"filtered_{baseline_name}_hits@5"] = hits_at_k(
                label_records[f"filtered_{baseline_name}"], 5
            )
            summary[f"filtered_{baseline_name}_mean_rank"] = mean(
                label_records[f"filtered_{baseline_name}"]
            )
        per_label_summary[function_id] = summary

    for baseline_name in tracked_per_label_baselines:
        stratified_summary[baseline_name] = {}
        for stratum_name in ("tail_1_10", "mid_11_50", "head_gt_50"):
            label_ids = [
                function_id
                for function_id, summary in per_label_summary.items()
                if summary["stratum"] == stratum_name
            ]
            if not label_ids:
                continue
            macro_filtered_mrr = mean(
                per_label_summary[function_id][f"filtered_{baseline_name}_mrr"]
                for function_id in label_ids
            )
            macro_filtered_hits3 = mean(
                per_label_summary[function_id][f"filtered_{baseline_name}_hits@3"]
                for function_id in label_ids
            )
            weighted_filtered_ranks = [
                rank
                for function_id in label_ids
                for rank in per_label_records[function_id][f"filtered_{baseline_name}"]
            ]
            stratified_summary[baseline_name][stratum_name] = {
                "num_labels": len(label_ids),
                "num_eval_edges": len(weighted_filtered_ranks),
                "macro_filtered_mrr": macro_filtered_mrr,
                "macro_filtered_hits@3": macro_filtered_hits3,
                "micro_filtered_mrr": mean_reciprocal_rank(weighted_filtered_ranks),
                "micro_filtered_hits@3": hits_at_k(weighted_filtered_ranks, 3),
                "micro_filtered_hits@5": hits_at_k(weighted_filtered_ranks, 5),
            }

    result = {
        "kg_dir": str(args.kg_dir),
        "include_disease_features": args.include_disease_features,
        "seed": args.seed,
        "num_functions": len(function_ids),
        "num_eval_edges": len(masked_edges),
        "top_k": args.top_k,
        "label_idf_weighting": args.label_idf_weighting,
        "rare_label_expansion": args.rare_label_expansion,
        "rare_label_threshold": args.rare_label_threshold,
        "rare_label_top_k": args.rare_label_top_k,
        "rare_label_decay": args.rare_label_decay,
        "source_constrained_rerank": args.source_constrained_rerank,
        "source_rerank_top_n": args.source_rerank_top_n,
        "source_rerank_weight": args.source_rerank_weight,
        "source_cluster_backoff": args.source_cluster_backoff,
        "source_cluster_top_n": args.source_cluster_top_n,
        "source_cluster_exact_weight": args.source_cluster_exact_weight,
        "source_cluster_genus_weight": args.source_cluster_genus_weight,
        "source_cluster_kingdom_weight": args.source_cluster_kingdom_weight,
        "tail_candidate_generation": args.tail_candidate_generation,
        "tail_label_threshold": args.tail_label_threshold,
        "tail_candidate_top_k": args.tail_candidate_top_k,
        "tail_candidate_limit": args.tail_candidate_limit,
        "tail_candidate_activation": args.tail_candidate_activation,
        "tail_candidate_source_exact_weight": args.tail_candidate_source_exact_weight,
        "tail_candidate_source_genus_weight": args.tail_candidate_source_genus_weight,
        "tail_candidate_source_kingdom_weight": args.tail_candidate_source_kingdom_weight,
        "label_specific_backoff": args.label_specific_backoff,
        "label_backoff_threshold": args.label_backoff_threshold,
        "label_backoff_top_n": args.label_backoff_top_n,
        "label_backoff_weight": args.label_backoff_weight,
        "label_backoff_exact_weight": args.label_backoff_exact_weight,
        "label_backoff_genus_weight": args.label_backoff_genus_weight,
        "label_backoff_kingdom_weight": args.label_backoff_kingdom_weight,
        "disease_label_prior": args.disease_label_prior,
        "disease_prior_top_n": args.disease_prior_top_n,
        "disease_prior_weight": args.disease_prior_weight,
        "disease_prior_alpha": args.disease_prior_alpha,
        "tail_aware_disease_prior": args.tail_aware_disease_prior,
        "tail_disease_prior_top_n": args.tail_disease_prior_top_n,
        "tail_disease_prior_threshold": args.tail_disease_prior_threshold,
        "tail_disease_prior_weight": args.tail_disease_prior_weight,
        "tail_disease_prior_boost": args.tail_disease_prior_boost,
        "tail_disease_prior_max_multiplier": args.tail_disease_prior_max_multiplier,
        "label_prototype_refinement": args.label_prototype_refinement,
        "prototype_top_n": args.prototype_top_n,
        "prototype_neighbors": args.prototype_neighbors,
        "prototype_weight": args.prototype_weight,
        "prototype_tail_threshold": args.prototype_tail_threshold,
        "prototype_tail_boost": args.prototype_tail_boost,
        "frequency_adjusted_disease_prior": args.frequency_adjusted_disease_prior,
        "freq_disease_prior_top_n": args.freq_disease_prior_top_n,
        "freq_disease_prior_weight": args.freq_disease_prior_weight,
        "freq_disease_prior_strength": args.freq_disease_prior_strength,
        "freq_disease_prior_mode": args.freq_disease_prior_mode,
        "support_aware_candidate_generation": args.support_aware_candidate_generation,
        "support_candidate_top_k": args.support_candidate_top_k,
        "support_candidate_base_window": args.support_candidate_base_window,
        "support_candidate_threshold": args.support_candidate_threshold,
        "support_candidate_limit": args.support_candidate_limit,
        "support_candidate_activation": args.support_candidate_activation,
        "support_candidate_exact_weight": args.support_candidate_exact_weight,
        "support_candidate_genus_weight": args.support_candidate_genus_weight,
        "support_candidate_kingdom_weight": args.support_candidate_kingdom_weight,
        "integrated_support_aware_knn": args.integrated_support_aware_knn,
        "integrated_support_top_k": args.integrated_support_top_k,
        "integrated_support_extended_k": args.integrated_support_extended_k,
        "integrated_support_threshold": args.integrated_support_threshold,
        "integrated_support_decay": args.integrated_support_decay,
        "integrated_support_exact_weight": args.integrated_support_exact_weight,
        "integrated_support_genus_weight": args.integrated_support_genus_weight,
        "integrated_support_kingdom_weight": args.integrated_support_kingdom_weight,
        "explicit_tail_support_knn": args.explicit_tail_support_knn,
        "tail_support_top_k": args.tail_support_top_k,
        "tail_support_extended_k": args.tail_support_extended_k,
        "tail_support_threshold": args.tail_support_threshold,
        "tail_support_decay": args.tail_support_decay,
        "tail_support_exact_weight": args.tail_support_exact_weight,
        "tail_support_genus_weight": args.tail_support_genus_weight,
        "tail_support_kingdom_weight": args.tail_support_kingdom_weight,
        "tail_support_boost": args.tail_support_boost,
        "disease_conditioned_base_vote": args.disease_conditioned_base_vote,
        "disease_vote_top_k": args.disease_vote_top_k,
        "disease_vote_weight": args.disease_vote_weight,
        "disease_vote_max_boost": args.disease_vote_max_boost,
        "tail_structural_signature": args.tail_structural_signature,
        "tail_signature_threshold": args.tail_signature_threshold,
        "tail_signature_top_n": args.tail_signature_top_n,
        "tail_signature_feature_limit": args.tail_signature_feature_limit,
        "tail_signature_weight": args.tail_signature_weight,
        "tail_signature_min_local_rate": args.tail_signature_min_local_rate,
        "tail_signature_max_boost": args.tail_signature_max_boost,
        "tail_signature_count": len(tail_structural_signatures),
        "structure_aware_candidate_generation": args.structure_aware_candidate_generation,
        "structure_candidate_base_window": args.structure_candidate_base_window,
        "structure_candidate_threshold": args.structure_candidate_threshold,
        "structure_candidate_limit": args.structure_candidate_limit,
        "structure_candidate_activation": args.structure_candidate_activation,
        "label_specific_subgraph_motifs": args.label_specific_subgraph_motifs,
        "motif_threshold": args.motif_threshold,
        "motif_feature_limit": args.motif_feature_limit,
        "motif_min_local_rate": args.motif_min_local_rate,
        "motif_candidate_base_window": args.motif_candidate_base_window,
        "motif_candidate_limit": args.motif_candidate_limit,
        "motif_candidate_activation": args.motif_candidate_activation,
        "motif_signature_count": len(motif_signatures),
        "taxonomy_conditioned_motifs": args.taxonomy_conditioned_motifs,
        "taxonomy_motif_threshold": args.taxonomy_motif_threshold,
        "taxonomy_motif_feature_limit": args.taxonomy_motif_feature_limit,
        "taxonomy_motif_min_local_rate": args.taxonomy_motif_min_local_rate,
        "taxonomy_motif_base_window": args.taxonomy_motif_base_window,
        "taxonomy_motif_candidate_limit": args.taxonomy_motif_candidate_limit,
        "taxonomy_motif_activation": args.taxonomy_motif_activation,
        "taxonomy_motif_signature_count": len(taxonomy_motif_signatures),
        "hierarchy_config": str(args.hierarchy_config),
        "hierarchy_support": args.hierarchy_support,
        "hierarchy_base_window": args.hierarchy_base_window,
        "hierarchy_threshold": args.hierarchy_threshold,
        "hierarchy_candidate_limit": args.hierarchy_candidate_limit,
        "hierarchy_activation": args.hierarchy_activation,
        "hierarchy_min_seed_count": args.hierarchy_min_seed_count,
        "hierarchy_specificity_power": args.hierarchy_specificity_power,
        "hierarchy_graph_native": args.hierarchy_graph_native,
        "hierarchy_graph_weight": args.hierarchy_graph_weight,
        "hierarchy_parent_child_native": args.hierarchy_parent_child_native,
        "hierarchy_confidence_threshold": args.hierarchy_confidence_threshold,
        "hierarchy_adaptive_power": args.hierarchy_adaptive_power,
        "hierarchy_family_count": len(family_to_functions),
        "hierarchy_parent_count": len(parent_to_children),
        "baselines": {
            "popularity": {
                "raw": summarize_ranks(raw_ranks["popularity"]),
                "filtered": summarize_ranks(filtered_ranks["popularity"]),
            },
            "meta_path_centroid": {
                "raw": summarize_ranks(raw_ranks["meta_path_centroid"]),
                "filtered": summarize_ranks(filtered_ranks["meta_path_centroid"]),
            },
            "meta_path_knn": {
                "raw": summarize_ranks(raw_ranks["meta_path_knn"]),
                "filtered": summarize_ranks(filtered_ranks["meta_path_knn"]),
            },
        },
        "per_label": dict(sorted(per_label_summary.items(), key=lambda item: item[0])),
        "stratified": stratified_summary,
        "examples": examples,
        "note": (
            "Each evaluation hides one known poly-function edge and ranks the held-out function among all "
            "function nodes. Filtered ranking removes the held-out polysaccharide's other true functions from "
            "the candidate list. Stratified evaluation reports tracked baseline performance by label support."
        ),
    }
    if args.rare_label_expansion:
        result["baselines"]["meta_path_knn_rare_expand"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_rare_expand"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_rare_expand"]),
        }
    if args.source_constrained_rerank:
        result["baselines"]["meta_path_knn_source_rerank"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_source_rerank"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_source_rerank"]),
        }
    if args.source_cluster_backoff:
        result["baselines"]["meta_path_knn_source_cluster_backoff"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_source_cluster_backoff"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_source_cluster_backoff"]),
        }
    if args.tail_candidate_generation:
        result["baselines"]["meta_path_knn_tail_candidates"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_tail_candidates"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_tail_candidates"]),
        }
    if args.label_specific_backoff:
        result["baselines"]["meta_path_knn_label_specific_backoff"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_label_specific_backoff"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_label_specific_backoff"]),
        }
    if args.disease_label_prior:
        result["baselines"]["meta_path_knn_disease_prior"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_disease_prior"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_disease_prior"]),
        }
    if args.tail_aware_disease_prior:
        result["baselines"]["meta_path_knn_tail_aware_disease_prior"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_tail_aware_disease_prior"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_tail_aware_disease_prior"]),
        }
    if args.label_prototype_refinement:
        result["baselines"]["meta_path_knn_label_prototype_refine"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_label_prototype_refine"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_label_prototype_refine"]),
        }
    if args.frequency_adjusted_disease_prior:
        result["baselines"]["meta_path_knn_freq_adjusted_disease_prior"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_freq_adjusted_disease_prior"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_freq_adjusted_disease_prior"]),
        }
    if args.support_aware_candidate_generation:
        result["baselines"]["meta_path_knn_support_aware_candidates"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_support_aware_candidates"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_support_aware_candidates"]),
        }
    if args.integrated_support_aware_knn:
        result["baselines"]["meta_path_knn_integrated_support"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_integrated_support"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_integrated_support"]),
        }
        if args.frequency_adjusted_disease_prior:
            result["baselines"]["meta_path_knn_integrated_support_freq_prior"] = {
                "raw": summarize_ranks(raw_ranks["meta_path_knn_integrated_support_freq_prior"]),
                "filtered": summarize_ranks(filtered_ranks["meta_path_knn_integrated_support_freq_prior"]),
            }
    if args.explicit_tail_support_knn:
        result["baselines"]["meta_path_knn_explicit_tail_support"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_explicit_tail_support"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_explicit_tail_support"]),
        }
        if args.frequency_adjusted_disease_prior:
            result["baselines"]["meta_path_knn_explicit_tail_support_freq_prior"] = {
                "raw": summarize_ranks(raw_ranks["meta_path_knn_explicit_tail_support_freq_prior"]),
                "filtered": summarize_ranks(filtered_ranks["meta_path_knn_explicit_tail_support_freq_prior"]),
            }
    if args.disease_conditioned_base_vote:
        result["baselines"]["meta_path_knn_disease_conditioned_vote"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_disease_conditioned_vote"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_disease_conditioned_vote"]),
        }
        if args.frequency_adjusted_disease_prior:
            result["baselines"]["meta_path_knn_disease_conditioned_vote_freq_prior"] = {
                "raw": summarize_ranks(raw_ranks["meta_path_knn_disease_conditioned_vote_freq_prior"]),
                "filtered": summarize_ranks(filtered_ranks["meta_path_knn_disease_conditioned_vote_freq_prior"]),
            }
    if args.tail_structural_signature:
        result["baselines"]["meta_path_knn_tail_structural_signature"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_tail_structural_signature"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_tail_structural_signature"]),
        }
        if args.disease_conditioned_base_vote:
            result["baselines"]["meta_path_knn_disease_conditioned_vote_tail_structural_signature"] = {
                "raw": summarize_ranks(raw_ranks["meta_path_knn_disease_conditioned_vote_tail_structural_signature"]),
                "filtered": summarize_ranks(
                    filtered_ranks["meta_path_knn_disease_conditioned_vote_tail_structural_signature"]
                ),
            }
            if args.frequency_adjusted_disease_prior:
                result["baselines"]["meta_path_knn_disease_conditioned_vote_freq_prior_tail_structural_signature"] = {
                    "raw": summarize_ranks(
                        raw_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_tail_structural_signature"]
                    ),
                    "filtered": summarize_ranks(
                        filtered_ranks[
                            "meta_path_knn_disease_conditioned_vote_freq_prior_tail_structural_signature"
                        ]
                    ),
                }
    if args.structure_aware_candidate_generation:
        result["baselines"]["meta_path_knn_structure_candidates"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_structure_candidates"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_structure_candidates"]),
        }
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            result["baselines"]["meta_path_knn_disease_conditioned_vote_freq_prior_structure_candidates"] = {
                "raw": summarize_ranks(raw_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_structure_candidates"]),
                "filtered": summarize_ranks(
                    filtered_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_structure_candidates"]
                ),
            }
    if args.label_specific_subgraph_motifs:
        result["baselines"]["meta_path_knn_subgraph_motifs"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_subgraph_motifs"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_subgraph_motifs"]),
        }
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            result["baselines"]["meta_path_knn_disease_conditioned_vote_freq_prior_subgraph_motifs"] = {
                "raw": summarize_ranks(raw_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_subgraph_motifs"]),
                "filtered": summarize_ranks(
                    filtered_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_subgraph_motifs"]
                ),
            }
    if args.taxonomy_conditioned_motifs:
        result["baselines"]["meta_path_knn_taxonomy_motifs"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_taxonomy_motifs"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_taxonomy_motifs"]),
        }
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            result["baselines"]["meta_path_knn_disease_conditioned_vote_freq_prior_taxonomy_motifs"] = {
                "raw": summarize_ranks(raw_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_taxonomy_motifs"]),
                "filtered": summarize_ranks(
                    filtered_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_taxonomy_motifs"]
                ),
            }
    if args.hierarchy_support:
        result["baselines"]["meta_path_knn_hierarchy_support"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_hierarchy_support"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_hierarchy_support"]),
        }
        if args.disease_conditioned_base_vote and args.frequency_adjusted_disease_prior:
            result["baselines"]["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_support"] = {
                "raw": summarize_ranks(raw_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_support"]),
                "filtered": summarize_ranks(
                    filtered_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_support"]
                ),
            }
    if args.hierarchy_graph_native:
        result["baselines"]["meta_path_knn_hierarchy_graph_native"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_hierarchy_graph_native"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_hierarchy_graph_native"]),
        }
        if args.disease_conditioned_base_vote:
            result["baselines"]["meta_path_knn_disease_conditioned_vote_hierarchy_graph_native"] = {
                "raw": summarize_ranks(raw_ranks["meta_path_knn_disease_conditioned_vote_hierarchy_graph_native"]),
                "filtered": summarize_ranks(
                    filtered_ranks["meta_path_knn_disease_conditioned_vote_hierarchy_graph_native"]
                ),
            }
            if args.frequency_adjusted_disease_prior:
                result["baselines"]["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_graph_native"] = {
                    "raw": summarize_ranks(
                        raw_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_graph_native"]
                    ),
                    "filtered": summarize_ranks(
                        filtered_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_graph_native"]
                    ),
                }
    if args.hierarchy_parent_child_native:
        result["baselines"]["meta_path_knn_hierarchy_parent_child_native"] = {
            "raw": summarize_ranks(raw_ranks["meta_path_knn_hierarchy_parent_child_native"]),
            "filtered": summarize_ranks(filtered_ranks["meta_path_knn_hierarchy_parent_child_native"]),
        }
        if args.disease_conditioned_base_vote:
            result["baselines"]["meta_path_knn_disease_conditioned_vote_hierarchy_parent_child_native"] = {
                "raw": summarize_ranks(raw_ranks["meta_path_knn_disease_conditioned_vote_hierarchy_parent_child_native"]),
                "filtered": summarize_ranks(
                    filtered_ranks["meta_path_knn_disease_conditioned_vote_hierarchy_parent_child_native"]
                ),
            }
            if args.frequency_adjusted_disease_prior:
                result["baselines"]["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native"] = {
                    "raw": summarize_ranks(
                        raw_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native"]
                    ),
                    "filtered": summarize_ranks(
                        filtered_ranks["meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native"]
                    ),
                }
    if args.save_edge_records:
        result["edge_records"] = edge_records
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if args.save_edge_records:
        summary = {
            "output": str(args.output),
            "num_eval_edges": len(edge_records),
            "baselines": sorted(result["baselines"].keys()),
        }
        print(json.dumps(summary, indent=2))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
