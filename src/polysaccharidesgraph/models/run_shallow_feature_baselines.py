"""Run standard shallow multilabel baselines on KG-derived feature matrices."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from polysaccharidesgraph.models.meta_path_features import build_feature_dicts, vectorize_feature_dicts
from polysaccharidesgraph.models.run_hetero_gnn_baseline import (
    exact_match_ratio,
    macro_f1_score,
)


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Run shallow baselines on KG feature matrices")
    parser.add_argument(
        "--pyg-path",
        type=Path,
        default=repo_root / "data" / "processed" / "pyg" / "dolphin_kg_v0.pt",
    )
    parser.add_argument(
        "--kg-dir",
        type=Path,
        default=repo_root / "data" / "processed" / "neo4j",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "experiments" / "shallow_feature_baseline_meta_path_logreg.json",
    )
    parser.add_argument(
        "--feature-source",
        choices=("meta_path", "poly_x", "poly_x_meta"),
        default="meta_path",
    )
    parser.add_argument(
        "--model-family",
        choices=("logreg", "sgd_logloss", "mlp"),
        default="logreg",
    )
    parser.add_argument("--include-disease-features", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def tune_thresholds(valid_scores: np.ndarray, valid_truth: np.ndarray) -> np.ndarray:
    thresholds = np.full((valid_truth.shape[1],), 0.5, dtype=np.float32)
    for label_idx in range(valid_truth.shape[1]):
        y_true = valid_truth[:, label_idx].astype(np.int32)
        if int(y_true.sum()) == 0:
            continue
        scores = valid_scores[:, label_idx]
        if scores.min() >= 0.0 and scores.max() <= 1.0:
            candidates = np.arange(0.1, 0.91, 0.05)
        else:
            candidates = np.linspace(float(scores.min()), float(scores.max()), num=17)
        best_threshold = 0.5
        best_f1 = -1.0
        for threshold in candidates:
            y_pred = (scores >= threshold).astype(np.int32)
            tp = int(np.logical_and(y_true == 1, y_pred == 1).sum())
            fp = int(np.logical_and(y_true == 0, y_pred == 1).sum())
            fn = int(np.logical_and(y_true == 1, y_pred == 0).sum())
            precision = tp / (tp + fp) if (tp + fp) else 0.0
            recall = tp / (tp + fn) if (tp + fn) else 0.0
            f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
            if f1 > best_f1:
                best_f1 = f1
                best_threshold = float(threshold)
        thresholds[label_idx] = best_threshold
    return thresholds


def decode_predictions(binary_rows: np.ndarray, label_names: list[str]) -> list[set[str]]:
    decoded: list[set[str]] = []
    for row in binary_rows:
        decoded.append({label_names[i] for i, value in enumerate(row.tolist()) if value == 1})
    return decoded


def evaluate_scores(
    scores: np.ndarray,
    truth: np.ndarray,
    label_names: list[str],
    thresholds: np.ndarray,
) -> tuple[float, float]:
    pred = (scores >= thresholds.reshape(1, -1)).astype(np.int32)
    y_true = decode_predictions(truth.astype(np.int32), label_names)
    y_pred = decode_predictions(pred, label_names)
    return macro_f1_score(y_true, y_pred), exact_match_ratio(y_true, y_pred)


def build_feature_matrix(
    payload: dict,
    kg_dir: Path,
    feature_source: str,
    include_disease_features: bool,
) -> tuple[np.ndarray, dict[str, int]]:
    data = payload["data"]
    metadata = payload["metadata"]
    poly_x = data["polysaccharide"].x.detach().cpu().numpy().astype(np.float32)
    dims = {"poly_x_dim": int(poly_x.shape[1])}

    if feature_source == "poly_x":
        return poly_x, dims

    poly_ids = metadata["poly_ids"]
    feature_dicts = build_feature_dicts(
        poly_ids,
        kg_dir,
        include_disease_features=include_disease_features,
    )
    meta_x, _ = vectorize_feature_dicts(poly_ids, feature_dicts)
    meta_x = meta_x.astype(np.float32)
    dims["meta_path_dim"] = int(meta_x.shape[1])

    if feature_source == "meta_path":
        return meta_x, dims

    return np.concatenate([poly_x, meta_x], axis=1), dims


def build_estimator(model_family: str, seed: int) -> OneVsRestClassifier:
    if model_family == "logreg":
        estimator = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    LogisticRegression(
                        max_iter=1500,
                        solver="liblinear",
                        class_weight="balanced",
                        random_state=seed,
                    ),
                ),
            ]
        )
    elif model_family == "sgd_logloss":
        estimator = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    SGDClassifier(
                        loss="log",
                        alpha=1e-4,
                        max_iter=2000,
                        tol=1e-3,
                        class_weight="balanced",
                        random_state=seed,
                    ),
                ),
            ]
        )
    elif model_family == "mlp":
        estimator = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "clf",
                    MLPClassifier(
                        hidden_layer_sizes=(256, 128),
                        activation="relu",
                        alpha=1e-4,
                        batch_size=128,
                        learning_rate_init=1e-3,
                        max_iter=300,
                        early_stopping=False,
                        n_iter_no_change=20,
                        random_state=seed,
                    ),
                ),
            ]
        )
    else:
        raise ValueError(f"Unsupported model family: {model_family}")
    return OneVsRestClassifier(estimator)


def get_score_matrix(model: OneVsRestClassifier, x: np.ndarray) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(x), dtype=np.float32)
    if hasattr(model, "decision_function"):
        return np.asarray(model.decision_function(x), dtype=np.float32)
    raise RuntimeError("Model does not expose predict_proba or decision_function")


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    payload = torch.load(args.pyg_path)
    data = payload["data"]
    metadata = payload["metadata"]
    label_names = metadata["label_names"]

    x, dims = build_feature_matrix(
        payload,
        kg_dir=args.kg_dir,
        feature_source=args.feature_source,
        include_disease_features=args.include_disease_features,
    )
    y = data["polysaccharide"].y.detach().cpu().numpy().astype(np.float32)
    train_mask = data["polysaccharide"].train_mask.detach().cpu().numpy().astype(bool)
    valid_mask = data["polysaccharide"].valid_mask.detach().cpu().numpy().astype(bool)
    test_mask = data["polysaccharide"].test_mask.detach().cpu().numpy().astype(bool)

    model = build_estimator(args.model_family, seed=args.seed)
    model.fit(x[train_mask], y[train_mask])
    valid_scores = get_score_matrix(model, x[valid_mask])
    test_scores = get_score_matrix(model, x[test_mask])
    thresholds = tune_thresholds(valid_scores, y[valid_mask])
    valid_macro_f1, valid_exact = evaluate_scores(valid_scores, y[valid_mask], label_names, thresholds)
    test_macro_f1, test_exact = evaluate_scores(test_scores, y[test_mask], label_names, thresholds)

    result = {
        "pyg_path": str(args.pyg_path),
        "kg_dir": str(args.kg_dir),
        "feature_source": args.feature_source,
        "model_family": args.model_family,
        "include_disease_features": args.include_disease_features,
        "seed": args.seed,
        "num_labels": len(label_names),
        "train_size": int(train_mask.sum()),
        "valid_size": int(valid_mask.sum()),
        "test_size": int(test_mask.sum()),
        "feature_dim": int(x.shape[1]),
        "valid_macro_f1": valid_macro_f1,
        "valid_exact_match_ratio": valid_exact,
        "test_macro_f1": test_macro_f1,
        "test_exact_match_ratio": test_exact,
        "threshold_mean": float(np.mean(thresholds)),
        "threshold_min": float(np.min(thresholds)),
        "threshold_max": float(np.max(thresholds)),
        "note": "Shallow multilabel baseline with validation threshold tuning on a unified train/valid/test split.",
    }
    result.update(dims)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
