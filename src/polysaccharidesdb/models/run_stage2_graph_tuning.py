"""Stage 2 tuning runner for the graph GCN baseline."""

from __future__ import annotations

import argparse
import statistics
import subprocess
import sys
from pathlib import Path

from polysaccharidesdb.paths import DATA_PROCESSED, EXPERIMENTS
from polysaccharidesdb.utils.io import read_json, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 2 graph tuning across seeds")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DATA_PROCESSED / "dataset_publishable_supervised_v1.jsonl",
    )
    parser.add_argument(
        "--split",
        type=Path,
        default=DATA_PROCESSED / "splits_publishable_supervised_v1" / "random_split.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=EXPERIMENTS / "stage2_tuning" / "results" / "graph_gcn",
    )
    parser.add_argument("--tag", type=str, default="baseline")
    parser.add_argument("--seeds", nargs="+", type=int, default=[11, 22, 33])
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--hidden-dim", type=int, default=16)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--batch-size", type=int, default=4)
    return parser.parse_args()


def run_one(args: argparse.Namespace, seed: int, output_path: Path) -> None:
    cmd = [
        sys.executable,
        "-m",
        "polysaccharidesdb.models.run_graph_gcn_baseline",
        "--dataset",
        str(args.dataset),
        "--split",
        str(args.split),
        "--output",
        str(output_path),
        "--seed",
        str(seed),
        "--epochs",
        str(args.epochs),
        "--hidden-dim",
        str(args.hidden_dim),
        "--lr",
        str(args.lr),
        "--batch-size",
        str(args.batch_size),
    ]
    subprocess.run(cmd, check=True)


def summarize(result_paths: list[Path]) -> dict:
    metrics = []
    for path in result_paths:
        payload = read_json(path)
        row = payload["results"][0]
        metrics.append(
            {
                "path": str(path),
                "macro_f1": row["macro_f1"],
                "exact_match_ratio": row["exact_match_ratio"],
                "config": payload.get("config", {}),
            }
        )

    macro_values = [item["macro_f1"] for item in metrics]
    exact_values = [item["exact_match_ratio"] for item in metrics]

    def rel_std(values: list[float]) -> float:
        if len(values) <= 1:
            return 0.0
        mean = statistics.mean(values)
        if mean == 0:
            return 0.0
        return statistics.stdev(values) / mean

    return {
        "runs": metrics,
        "macro_f1_mean": statistics.mean(macro_values),
        "macro_f1_std": statistics.stdev(macro_values) if len(macro_values) > 1 else 0.0,
        "macro_f1_rel_std": rel_std(macro_values),
        "exact_match_mean": statistics.mean(exact_values),
        "exact_match_std": statistics.stdev(exact_values) if len(exact_values) > 1 else 0.0,
        "exact_match_rel_std": rel_std(exact_values),
    }


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result_paths = []
    for seed in args.seeds:
        output_path = args.output_dir / f"{args.tag}_seed{seed}.json"
        run_one(args=args, seed=seed, output_path=output_path)
        result_paths.append(output_path)

    summary = {
        "tag": args.tag,
        "dataset": str(args.dataset),
        "split": str(args.split),
        "config": {
            "seeds": args.seeds,
            "epochs": args.epochs,
            "hidden_dim": args.hidden_dim,
            "lr": args.lr,
            "batch_size": args.batch_size,
        },
        "summary": summarize(result_paths),
    }
    write_json(args.output_dir / f"{args.tag}_summary.json", summary)
    print(f"Wrote tuning summary to {args.output_dir / f'{args.tag}_summary.json'}")


if __name__ == "__main__":
    main()
