"""Run a simple logistic-regression baseline with lightweight feature text."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

from polysaccharidesdb.models.dataset import index_by_poly_id, load_dataset
from polysaccharidesdb.models.feature_text import record_to_feature_text
from polysaccharidesdb.models.multilabel_utils import ensure_2d_binary_predictions
from polysaccharidesdb.models.split_utils import expand_split_payload
from polysaccharidesdb.paths import DATA_PROCESSED, EXPERIMENTS
from polysaccharidesdb.utils.io import read_json, write_json
from polysaccharidesdb.utils.metrics import exact_match_ratio, macro_f1_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run logistic regression baseline")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DATA_PROCESSED / "dataset_v0.jsonl",
    )
    parser.add_argument(
        "--split",
        type=Path,
        default=DATA_PROCESSED / "splits" / "random_split.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=EXPERIMENTS / "stage1_baseline" / "results" / "logistic_random.json",
    )
    parser.add_argument(
        "--eval-split",
        type=str,
        default="test",
        choices=["valid", "test"],
        help="Which partition from the split file to evaluate on",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--c", type=float, default=1.0)
    parser.add_argument("--min-df", type=int, default=1)
    parser.add_argument("--max-features", type=int, default=0)
    parser.add_argument("--binary", action="store_true")
    parser.add_argument("--class-weight", type=str, default="none")
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    class_weight = None if args.class_weight == "none" else args.class_weight
    records = load_dataset(args.dataset)
    record_map = index_by_poly_id(records)
    split_payload = read_json(args.split)
    expanded_splits = expand_split_payload(split_payload, eval_key=args.eval_split)

    split_results = []
    for split_def in expanded_splits:
        train_records = [record_map[poly_id] for poly_id in split_def["train"]]
        test_records = [record_map[poly_id] for poly_id in split_def["test"]]

        x_train_text = [record_to_feature_text(record) for record in train_records]
        x_test_text = [record_to_feature_text(record) for record in test_records]
        y_train = [record.get("function_label", []) for record in train_records]
        y_test = [set(record.get("function_label", [])) for record in test_records]

        vectorizer = CountVectorizer(
            token_pattern=r"(?u)\b[\w=\-]+\b",
            min_df=args.min_df,
            max_features=None if args.max_features <= 0 else args.max_features,
            binary=args.binary,
        )
        x_train = vectorizer.fit_transform(x_train_text)
        x_test = vectorizer.transform(x_test_text)

        mlb = MultiLabelBinarizer()
        y_train_bin = mlb.fit_transform(y_train)

        base_estimator = LogisticRegression(
            max_iter=1000,
            solver="liblinear",
            C=args.c,
            random_state=args.seed,
            class_weight=class_weight,
        )
        classifier = OneVsRestClassifier(base_estimator)
        classifier.fit(x_train, y_train_bin)

        y_pred_bin = ensure_2d_binary_predictions(
            classifier.predict(x_test),
            num_labels=len(mlb.classes_),
        )
        y_pred = [set(labels) for labels in mlb.inverse_transform(y_pred_bin)]
        prediction_rows = [
            {
                "poly_id": record["poly_id"],
                "y_true": sorted(y_test[idx]),
                "y_pred": sorted(y_pred[idx]),
            }
            for idx, record in enumerate(test_records)
        ]

        split_results.append(
            {
                "split_name": split_def["name"],
                "eval_split": args.eval_split,
                "num_train": len(train_records),
                "num_test": len(test_records),
                "labels": sorted(mlb.classes_.tolist()),
                "vectorizer_vocab_size": int(x_train.shape[1]),
                "macro_f1": macro_f1_score(y_test, y_pred),
                "exact_match_ratio": exact_match_ratio(y_test, y_pred),
                "predictions": prediction_rows,
            }
        )

    result = {
        "dataset": str(args.dataset),
        "split": str(args.split),
        "config": {
            "eval_split": args.eval_split,
            "seed": args.seed,
            "c": args.c,
            "min_df": args.min_df,
            "max_features": args.max_features,
            "binary": args.binary,
            "class_weight": args.class_weight,
        },
        "results": split_results,
    }
    write_json(args.output, result)
    print(f"Wrote baseline result to {args.output}")


if __name__ == "__main__":
    main()
