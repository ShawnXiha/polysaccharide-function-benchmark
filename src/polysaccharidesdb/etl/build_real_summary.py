"""Summarize the merged real dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

from polysaccharidesdb.etl.dataset_summary import main as summary_main
from polysaccharidesdb.paths import DATA_INTERIM, DATA_PROCESSED


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize real dataset")
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "dataset_v0_real.jsonl",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_INTERIM / "dataset_v0_real_summary.json",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # Reuse the existing summary CLI implementation pattern by patching argv.
    import sys

    args = parse_args()
    sys.argv = [
        "dataset_summary",
        "--input",
        str(args.input),
        "--output",
        str(args.output),
    ]
    summary_main()
