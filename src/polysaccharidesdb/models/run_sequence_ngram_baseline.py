"""Run a lightweight sequence-only n-gram baseline."""

from __future__ import annotations

import argparse
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

from polysaccharidesdb.models.dataset import index_by_poly_id, load_dataset
from polysaccharidesdb.models.multilabel_utils import ensure_2d_binary_predictions
from polysaccharidesdb.models.split_utils import expand_split_payload
from polysaccharidesdb.paths import DATA_PROCESSED, EXPERIMENTS
from polysaccharidesdb.utils.io import read_json, write_json
from polysaccharidesdb.utils.metrics import exact_match_ratio, macro_f1_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run sequence n-gram baseline")
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
        default=EXPERIMENTS / "stage1_baseline" / "results" / "sequence_ngram_random.json",
    )
    return parser.parse_args()


def canonical_sequence(record: dict) -> str:
    return str(record.get("canonical_representation", "")).strip()


def main() -> None:
    args = parse_args()
    records = load_dataset(args.dataset)
    record_map = index_by_poly_id(records)
    split_payload = read_json(args.split)
    expanded_splits = expand_split_payload(split_payload)

    split_results = []
    for split_def in expanded_splits:
        train_records = [record_map[poly_id] for poly_id in split_def["train"]]
        test_records = [record_map[poly_id] for poly_id in split_def["test"]]

        x_train_text = [canonical_sequence(record) for record in train_records]
        x_test_text = [canonical_sequence(record) for record in test_records]
        y_train = [record.get("function_label", []) for record in train_records]
        y_test = [set(record.get("function_label", [])) for record in test_records]

        vectorizer = CountVectorizer(analyzer="char", ngram_range=(2, 4))
        x_train = vectorizer.fit_transform(x_train_text)
        x_test = vectorizer.transform(x_test_text)

        mlb = MultiLabelBinarizer()
        y_train_bin = mlb.fit_transform(y_train)

        classifier = OneVsRestClassifier(
            LogisticRegression(max_iter=1000, solver="liblinear")
        )
        classifier.fit(x_train, y_train_bin)

        y_pred_bin = ensure_2d_binary_predictions(
            classifier.predict(x_test),
            num_labels=len(mlb.classes_),
        )
        y_pred = [set(labels) for labels in mlb.inverse_transform(y_pred_bin)]

        split_results.append(
            {
                "split_name": split_def["name"],
                "num_train": len(train_records),
                "num_test": len(test_records),
                "labels": sorted(mlb.classes_.tolist()),
                "macro_f1": macro_f1_score(y_test, y_pred),
                "exact_match_ratio": exact_match_ratio(y_test, y_pred),
            }
        )

    result = {
        "dataset": str(args.dataset),
        "split": str(args.split),
        "results": split_results,
        "note": "sequence-only baseline using character n-grams over canonical_representation",
    }
    write_json(args.output, result)
    print(f"Wrote baseline result to {args.output}")


if __name__ == "__main__":
    main()
