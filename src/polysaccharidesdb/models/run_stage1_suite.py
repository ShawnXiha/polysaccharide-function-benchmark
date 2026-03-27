"""Run the Stage 1 baseline suite on a chosen dataset/split directory."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from polysaccharidesdb.paths import DATA_PROCESSED, EXPERIMENTS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 1 baseline suite")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DATA_PROCESSED / "dataset_v0_real.jsonl",
        help="Dataset JSONL file",
    )
    parser.add_argument(
        "--split-dir",
        type=Path,
        default=DATA_PROCESSED / "splits_real",
        help="Directory containing random/source split files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=EXPERIMENTS / "stage1_baseline" / "results" / "real_suite",
        help="Directory to store suite outputs",
    )
    return parser.parse_args()


def run_module(module: str, dataset: Path, split: Path, output: Path) -> None:
    cmd = [
        sys.executable,
        "-m",
        module,
        "--dataset",
        str(dataset),
        "--split",
        str(split),
        "--output",
        str(output),
    ]
    subprocess.run(cmd, check=True)


def split_payload_is_usable(split_path: Path) -> bool:
    with split_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if "train" in payload and "test" in payload:
        return len(payload["train"]) > 0 and len(payload["test"]) > 0
    if "splits" in payload:
        return all(len(item.get("train", [])) > 0 and len(item.get("test", [])) > 0 for item in payload["splits"])
    return False


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = {"completed": [], "skipped": [], "failed": []}

    runs = [
        ("polysaccharidesdb.models.run_majority_baseline", "majority"),
        ("polysaccharidesdb.models.run_logistic_baseline", "logistic"),
        ("polysaccharidesdb.models.run_random_forest_baseline", "random_forest"),
        ("polysaccharidesdb.models.run_sequence_ngram_baseline", "sequence_ngram"),
        ("polysaccharidesdb.models.run_sequence_transformer_baseline", "sequence_transformer"),
        ("polysaccharidesdb.models.run_graph_gcn_baseline", "graph_gcn"),
    ]
    split_files = [
        ("random", args.split_dir / "random_split.json"),
        ("source", args.split_dir / "leave_one_source_out.json"),
    ]

    for module, name in runs:
        for split_name, split_path in split_files:
            if not split_payload_is_usable(split_path):
                print(f"Skipping {name} on {split_name}: split has empty train/test partition")
                summary["skipped"].append(
                    {"model": name, "split": split_name, "reason": "empty train/test partition"}
                )
                continue
            output = args.output_dir / f"{name}_{split_name}.json"
            try:
                run_module(module=module, dataset=args.dataset, split=split_path, output=output)
                print(f"Completed {name} on {split_name}")
                summary["completed"].append({"model": name, "split": split_name, "output": str(output)})
            except subprocess.CalledProcessError as exc:
                print(f"Failed {name} on {split_name}: {exc}")
                summary["failed"].append(
                    {
                        "model": name,
                        "split": split_name,
                        "command": exc.cmd,
                        "returncode": exc.returncode,
                    }
                )

    with (args.output_dir / "suite_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
