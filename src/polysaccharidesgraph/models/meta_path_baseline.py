"""Graph-derived meta-path style baseline for multilabel function prediction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer

from polysaccharidesgraph.models.meta_path_features import build_feature_dicts


def macro_f1_score(y_true: list[set[str]], y_pred: list[set[str]]) -> float:
    labels = sorted({label for row in y_true for label in row} | {label for row in y_pred for label in row})
    if not labels:
        return 0.0
    f1_scores = []
    for label in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred) if label in t and label in p)
        fp = sum(1 for t, p in zip(y_true, y_pred) if label not in t and label in p)
        fn = sum(1 for t, p in zip(y_true, y_pred) if label in t and label not in p)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1_scores.append(0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall))
    return sum(f1_scores) / len(f1_scores)


def exact_match_ratio(y_true: list[set[str]], y_pred: list[set[str]]) -> float:
    return sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true) if y_true else 0.0


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    source_root = repo_root.parent / "polysaccharidesdb"
    parser = argparse.ArgumentParser(description="Run a meta-path style KG baseline")
    parser.add_argument("--kg-dir", type=Path, default=repo_root / "data" / "processed" / "neo4j")
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
        default=repo_root / "experiments" / "meta_path_baseline_random.json",
    )
    parser.add_argument("--include-disease-features", action="store_true")
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            rows.append(json.loads(line))
    return rows


def main() -> None:
    args = parse_args()
    dataset = load_jsonl(args.dataset_jsonl)
    record_map = {record["poly_id"]: record for record in dataset}
    poly_ids = [record["poly_id"] for record in dataset]
    global_labels = sorted({label for record in dataset for label in record.get("function_label", [])})
    feature_dicts = build_feature_dicts(poly_ids, args.kg_dir, include_disease_features=args.include_disease_features)

    split_payload = json.loads(args.split_json.read_text(encoding="utf-8"))
    train_ids = [poly_id for poly_id in split_payload.get("train", []) if poly_id in record_map]
    test_ids = [poly_id for poly_id in split_payload.get("test", []) if poly_id in record_map]

    train_labels = [record_map[poly_id].get("function_label", []) for poly_id in train_ids]
    test_labels = [record_map[poly_id].get("function_label", []) for poly_id in test_ids]

    mlb = MultiLabelBinarizer(classes=global_labels)
    y_train = mlb.fit_transform(train_labels)

    pipeline = Pipeline(
        [
            ("vectorizer", DictVectorizer()),
            (
                "clf",
                OneVsRestClassifier(
                    LogisticRegression(max_iter=1000, solver="liblinear", class_weight="balanced")
                ),
            ),
        ]
    )

    X_train = [feature_dicts[poly_id] for poly_id in train_ids]
    X_test = [feature_dicts[poly_id] for poly_id in test_ids]
    pipeline.fit(X_train, y_train)
    y_pred_bin = pipeline.predict(X_test)

    y_true = [set(labels) for labels in test_labels]
    y_pred = [
        {mlb.classes_[idx] for idx, value in enumerate(row.tolist()) if value == 1}
        for row in y_pred_bin
    ]

    result = {
        "dataset_jsonl": str(args.dataset_jsonl),
        "split_json": str(args.split_json),
        "kg_dir": str(args.kg_dir),
        "train_size": len(train_ids),
        "test_size": len(test_ids),
        "num_labels": len(mlb.classes_),
        "macro_f1": macro_f1_score(y_true, y_pred),
        "exact_match_ratio": exact_match_ratio(y_true, y_pred),
        "include_disease_features": args.include_disease_features,
        "note": "Features are graph-derived relation incidences plus 2-hop shared-polys counts.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
