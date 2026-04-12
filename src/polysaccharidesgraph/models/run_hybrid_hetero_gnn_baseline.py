"""Run a hybrid hetero GNN baseline with appended meta-path features."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from polysaccharidesgraph.models.meta_path_features import build_feature_dicts, vectorize_feature_dicts
from polysaccharidesgraph.models.run_hetero_gnn_baseline import main as hetero_main


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Run hybrid hetero GNN with appended meta-path features")
    parser.add_argument(
        "--pyg-path",
        type=Path,
        default=repo_root / "data" / "processed" / "pyg" / "dolphin_kg_v0.pt",
    )
    parser.add_argument(
        "--kg-dir",
        type=Path,
        default=repo_root / "data" / "processed" / "neo4j",
    )
    parser.add_argument(
        "--hybrid-pyg-path",
        type=Path,
        default=repo_root / "data" / "processed" / "pyg" / "dolphin_kg_v0_hybrid.pt",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "experiments" / "hybrid_hetero_gnn_baseline_random.json",
    )
    parser.add_argument("--include-disease-features", action="store_true")
    parser.add_argument("--hidden-dim", type=int, default=128)
    parser.add_argument("--epochs", type=int, default=120)
    parser.add_argument("--lr", type=float, default=0.005)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--patience", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--model-variant",
        choices=("hetero_sage", "hetero_no_message", "poly_mlp", "poly_linear"),
        default="hetero_sage",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = torch.load(args.pyg_path)
    data = payload["data"]
    metadata = payload["metadata"]

    poly_ids = metadata["poly_ids"]
    feature_dicts = build_feature_dicts(
        poly_ids,
        args.kg_dir,
        include_disease_features=args.include_disease_features,
    )
    matrix, vectorizer = vectorize_feature_dicts(poly_ids, feature_dicts)
    meta_x = torch.from_numpy(matrix)
    data["polysaccharide"].x = torch.cat([data["polysaccharide"].x, meta_x], dim=1)

    metadata = dict(metadata)
    metadata["hybrid_meta_path_features"] = True
    metadata["include_meta_path_disease_features"] = args.include_disease_features
    metadata["meta_path_feature_dim"] = int(meta_x.size(1))

    hybrid_payload = {"data": data, "metadata": metadata}
    args.hybrid_pyg_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(hybrid_payload, args.hybrid_pyg_path)
    args.hybrid_pyg_path.with_suffix(".summary.json").write_text(
        json.dumps(
            {
                "hybrid_pyg_path": str(args.hybrid_pyg_path),
                "meta_path_feature_dim": int(meta_x.size(1)),
                "include_disease_features": args.include_disease_features,
                "poly_feature_dim_after_concat": int(data["polysaccharide"].x.size(1)),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    import sys

    sys.argv = [
        "run_hetero_gnn_baseline",
        "--pyg-path",
        str(args.hybrid_pyg_path),
        "--output",
        str(args.output),
        "--hidden-dim",
        str(args.hidden_dim),
        "--epochs",
        str(args.epochs),
        "--lr",
        str(args.lr),
        "--weight-decay",
        str(args.weight_decay),
        "--dropout",
        str(args.dropout),
        "--patience",
        str(args.patience),
        "--seed",
        str(args.seed),
        "--model-variant",
        str(args.model_variant),
    ]
    hetero_main()


if __name__ == "__main__":
    main()
