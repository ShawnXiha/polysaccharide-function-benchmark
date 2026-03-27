"""Stage 2 tuning runner for the logistic baseline."""

from __future__ import annotations

import argparse
import statistics
import subprocess
import sys
from pathlib import Path

from polysaccharidesdb.paths import DATA_PROCESSED, EXPERIMENTS
from polysaccharidesdb.utils.io import read_json, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 2 logistic tuning across seeds")
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
        default=EXPERIMENTS / "stage2_tuning" / "results" / "logistic",
    )
    parser.add_argument(
        "--eval-split",
        type=str,
        default="valid",
        choices=["valid", "test"],
        help="Which partition from the split file to use during tuning",
    )
    parser.add_argument("--tag", type=str, default="baseline")
    parser.add_argument("--seeds", nargs="+", type=int, default=[11, 22, 33])
    parser.add_argument("--c", type=float, default=1.0)
    parser.add_argument("--min-df", type=int, default=1)
    parser.add_argument("--max-features", type=int, default=0)
    parser.add_argument("--binary", action="store_true")
    parser.add_argument("--class-weight", type=str, default="none")
    return parser.parse_args()


def run_one(args: argparse.Namespace, seed: int, output_path: Path) -> None:
    cmd = [
        sys.executable,
        "-m",
        "polysaccharidesdb.models.run_logistic_baseline",
        "--dataset",
        str(args.dataset),
        "--split",
        str(args.split),
        "--output",
        str(output_path),
        "--eval-split",
        str(args.eval_split),
        "--seed",
        str(seed),
        "--c",
        str(args.c),
        "--min-df",
        str(args.min_df),
        "--max-features",
        str(args.max_features),
        "--class-weight",
        str(args.class_weight),
    ]
    if args.binary:
        cmd.append("--binary")
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
                "vectorizer_vocab_size": row.get("vectorizer_vocab_size"),
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
            "eval_split": args.eval_split,
            "c": args.c,
            "min_df": args.min_df,
            "max_features": args.max_features,
            "binary": args.binary,
            "class_weight": args.class_weight,
        },
        "summary": summarize(result_paths),
    }
    write_json(args.output_dir / f"{args.tag}_summary.json", summary)
    print(f"Wrote tuning summary to {args.output_dir / f'{args.tag}_summary.json'}")


if __name__ == "__main__":
    main()
