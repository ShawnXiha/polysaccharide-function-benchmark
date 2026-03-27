"""Run a majority multilabel baseline on a selected split."""

from __future__ import annotations

import argparse
from pathlib import Path

from polysaccharidesdb.models.classical import MajorityMultilabelBaseline
from polysaccharidesdb.models.dataset import index_by_poly_id, load_dataset
from polysaccharidesdb.models.split_utils import expand_split_payload
from polysaccharidesdb.paths import DATA_PROCESSED, EXPERIMENTS
from polysaccharidesdb.utils.io import read_json, write_json
from polysaccharidesdb.utils.metrics import exact_match_ratio, macro_f1_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run majority baseline")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DATA_PROCESSED / "dataset_v0.jsonl",
        help="Dataset JSONL path",
    )
    parser.add_argument(
        "--split",
        type=Path,
        default=DATA_PROCESSED / "splits" / "random_split.json",
        help="Split JSON path",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=EXPERIMENTS / "stage1_baseline" / "results" / "majority_random.json",
        help="Output result JSON",
    )
    return parser.parse_args()


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

        model = MajorityMultilabelBaseline().fit(train_records)
        y_true = [set(record.get("function_label", [])) for record in test_records]
        y_pred = model.predict(test_records)

        split_results.append(
            {
                "split_name": split_def["name"],
                "num_train": len(train_records),
                "num_test": len(test_records),
                "majority_labels": sorted(model.majority_labels),
                "macro_f1": macro_f1_score(y_true, y_pred),
                "exact_match_ratio": exact_match_ratio(y_true, y_pred),
            }
        )

    result = {
        "dataset": str(args.dataset),
        "split": str(args.split),
        "results": split_results,
    }
    write_json(args.output, result)
    print(f"Wrote baseline result to {args.output}")


if __name__ == "__main__":
    main()
