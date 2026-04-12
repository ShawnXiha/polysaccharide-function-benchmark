"""Run frozen final-test comparisons for the manuscript's main sparse methods."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from polysaccharidesdb.paths import DATA_PROCESSED, EXPERIMENTS
from polysaccharidesdb.utils.io import write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run frozen final-test evaluations for tuned logistic and poly-core v1"
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DATA_PROCESSED / "dataset_publishable_supervised_v1.jsonl",
    )
    parser.add_argument(
        "--split",
        type=Path,
        default=DATA_PROCESSED / "splits_publishable_supervised_v2" / "random_split.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=EXPERIMENTS / "final_test",
    )
    parser.add_argument("--seed", type=int, default=11)
    return parser.parse_args()


def run_command(cmd: list[str]) -> None:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    logistic_output = args.output_dir / "tuned_logistic_test.json"
    poly_core_output = args.output_dir / "poly_core_v1_test.json"

    logistic_cmd = [
        sys.executable,
        "-m",
        "polysaccharidesdb.models.run_logistic_baseline",
        "--dataset",
        str(args.dataset),
        "--split",
        str(args.split),
        "--output",
        str(logistic_output),
        "--eval-split",
        "test",
        "--final-test",
        "--seed",
        str(args.seed),
        "--c",
        "16",
        "--class-weight",
        "balanced",
    ]

    poly_core_cmd = [
        sys.executable,
        "-m",
        "polysaccharidesdb.models.run_evidence_aware_logistic",
        "--dataset",
        str(args.dataset),
        "--split",
        str(args.split),
        "--output",
        str(poly_core_output),
        "--eval-split",
        "test",
        "--final-test",
        "--seed",
        str(args.seed),
        "--c",
        "16",
        "--class-weight",
        "balanced",
        "--disable-evidence-features",
        "--disable-sample-weight",
        "--disable-modification-feature",
        "--disable-source-kingdom-feature",
        "--disable-composition-feature",
    ]

    run_command(logistic_cmd)
    run_command(poly_core_cmd)

    manifest = {
        "dataset": str(args.dataset),
        "split": str(args.split),
        "seed": args.seed,
        "eval_split": "test",
        "is_final_test": True,
        "outputs": {
            "tuned_logistic": str(logistic_output),
            "poly_core_v1": str(poly_core_output),
        },
        "note": "Frozen final-test suite. Development/tuning runners default to validation.",
    }
    write_json(args.output_dir / "final_test_manifest.json", manifest)
    print(f"Wrote final-test manifest to {args.output_dir / 'final_test_manifest.json'}")


if __name__ == "__main__":
    main()
