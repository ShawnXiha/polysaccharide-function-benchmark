"""Run paper-facing retrieval methods through a small stable CLI.

This wrapper delegates to the original experiment runner while exposing only
the final baseline and ontology configurations used in the manuscript.
"""

from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path

from polysaccharidesgraph.models.final_methods import FINAL_METHODS, method_output_path


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Run final manuscript retrieval methods")
    parser.add_argument(
        "--method",
        choices=sorted(FINAL_METHODS),
        default="ontology_parent_child_best",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-eval", type=int, default=1000)
    parser.add_argument("--save-edge-records", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--kg-dir",
        type=Path,
        default=repo_root / "data" / "processed" / "neo4j",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[3]
    method = FINAL_METHODS[args.method]
    output = args.output or method_output_path(repo_root, method.name, args.seed)

    delegated_args = [
        "run_poly_function_link_prediction",
        "--kg-dir",
        str(args.kg_dir),
        "--seed",
        str(args.seed),
        "--max-eval",
        str(args.max_eval),
        "--output",
        str(output),
        *method.args,
    ]
    if args.save_edge_records:
        delegated_args.append("--save-edge-records")

    output.parent.mkdir(parents=True, exist_ok=True)
    sys.argv = delegated_args
    runpy.run_module(
        "polysaccharidesgraph.models.run_poly_function_link_prediction",
        run_name="__main__",
    )


if __name__ == "__main__":
    main()

