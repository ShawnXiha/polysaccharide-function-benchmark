"""Run hetero GNN baselines and failure ablations on the exported PyG graph."""

from __future__ import annotations

import argparse
import copy
import json
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch_geometric.nn import HeteroConv, SAGEConv


def macro_f1_score(y_true: list[set[str]], y_pred: list[set[str]]) -> float:
    labels = sorted({label for row in y_true for label in row} | {label for row in y_pred for label in row})
    if not labels:
        return 0.0
    f1_scores = []
    for label in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred) if label in t and label in p)
        fp = sum(1 for t, p in zip(y_true, y_pred) if label not in t and label in p)
        fn = sum(1 for t, p in zip(y_true, y_pred) if label in t and label not in p)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1_scores.append(0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall))
    return sum(f1_scores) / len(f1_scores)


def exact_match_ratio(y_true: list[set[str]], y_pred: list[set[str]]) -> float:
    return sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true) if y_true else 0.0


def decode_predictions(binary_rows: torch.Tensor, label_names: list[str]) -> list[set[str]]:
    decoded: list[set[str]] = []
    for row in binary_rows:
        decoded.append({label_names[i] for i, value in enumerate(row.tolist()) if value == 1})
    return decoded


def tune_thresholds(valid_probs: torch.Tensor, valid_truth: torch.Tensor) -> torch.Tensor:
    thresholds = torch.full((valid_truth.size(1),), 0.5, dtype=torch.float)
    candidates = torch.arange(0.1, 0.91, 0.05)
    for label_idx in range(valid_truth.size(1)):
        y_true = valid_truth[:, label_idx].int()
        if int(y_true.sum().item()) == 0:
            continue
        probs = valid_probs[:, label_idx]
        best_threshold = 0.5
        best_f1 = -1.0
        for threshold in candidates:
            y_pred = (probs >= threshold).int()
            tp = int(((y_true == 1) & (y_pred == 1)).sum().item())
            fp = int(((y_true == 0) & (y_pred == 1)).sum().item())
            fn = int(((y_true == 1) & (y_pred == 0)).sum().item())
            precision = tp / (tp + fp) if (tp + fp) else 0.0
            recall = tp / (tp + fn) if (tp + fn) else 0.0
            f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
            if f1 > best_f1:
                best_f1 = f1
                best_threshold = float(threshold.item())
        thresholds[label_idx] = best_threshold
    return thresholds


def evaluate_from_logits(
    logits: torch.Tensor,
    truth: torch.Tensor,
    label_names: list[str],
    thresholds: torch.Tensor,
) -> tuple[float, float]:
    probs = torch.sigmoid(logits)
    pred = (probs >= thresholds.unsqueeze(0)).int()
    y_true = decode_predictions(truth.int(), label_names)
    y_pred = decode_predictions(pred, label_names)
    return macro_f1_score(y_true, y_pred), exact_match_ratio(y_true, y_pred)


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Run hetero GNN baseline on exported KG")
    parser.add_argument(
        "--pyg-path",
        type=Path,
        default=repo_root / "data" / "processed" / "pyg" / "dolphin_kg_v0.pt",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "experiments" / "hetero_gnn_baseline_random.json",
    )
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


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class HeteroSAGE(nn.Module):
    def __init__(self, data, hidden_dim: int, out_dim: int, dropout: float) -> None:
        super().__init__()
        metadata = data.metadata()
        self.dropout = nn.Dropout(dropout)
        self.lin_dict = nn.ModuleDict()
        self.emb_dict = nn.ModuleDict()
        for node_type in data.node_types:
            num_nodes = int(data[node_type].x.size(0))
            in_dim = int(data[node_type].x.size(1))
            self.lin_dict[node_type] = nn.Linear(in_dim, hidden_dim)
            self.emb_dict[node_type] = nn.Embedding(num_nodes, hidden_dim)

        self.conv1 = HeteroConv(
            {edge_type: SAGEConv((-1, -1), hidden_dim) for edge_type in metadata[1]},
            aggr="sum",
        )
        self.conv2 = HeteroConv(
            {edge_type: SAGEConv((-1, -1), hidden_dim) for edge_type in metadata[1]},
            aggr="sum",
        )
        self.out = nn.Linear(hidden_dim, out_dim)

    def forward(self, data):
        x_dict = {}
        for node_type, x in data.x_dict.items():
            node_ids = data[node_type].node_id
            h = self.lin_dict[node_type](x) + self.emb_dict[node_type](node_ids)
            x_dict[node_type] = self.dropout(h.relu())
        x_dict = {k: self.dropout(v.relu()) for k, v in self.conv1(x_dict, data.edge_index_dict).items()}
        x_dict = {k: self.dropout(v.relu()) for k, v in self.conv2(x_dict, data.edge_index_dict).items()}
        return self.out(x_dict["polysaccharide"])


class HeteroNoMessage(nn.Module):
    def __init__(self, data, hidden_dim: int, out_dim: int, dropout: float) -> None:
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        self.lin_dict = nn.ModuleDict()
        self.emb_dict = nn.ModuleDict()
        for node_type in data.node_types:
            num_nodes = int(data[node_type].x.size(0))
            in_dim = int(data[node_type].x.size(1))
            self.lin_dict[node_type] = nn.Linear(in_dim, hidden_dim)
            self.emb_dict[node_type] = nn.Embedding(num_nodes, hidden_dim)
        self.out = nn.Linear(hidden_dim, out_dim)

    def forward(self, data):
        node_ids = data["polysaccharide"].node_id
        x = data["polysaccharide"].x
        h = self.lin_dict["polysaccharide"](x) + self.emb_dict["polysaccharide"](node_ids)
        return self.out(self.dropout(h.relu()))


class PolyMLP(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, dropout: float) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, out_dim),
        )

    def forward(self, data):
        return self.net(data["polysaccharide"].x)


class PolyLinear(nn.Module):
    def __init__(self, in_dim: int, out_dim: int) -> None:
        super().__init__()
        self.out = nn.Linear(in_dim, out_dim)

    def forward(self, data):
        return self.out(data["polysaccharide"].x)


def build_model(data, hidden_dim: int, out_dim: int, dropout: float, variant: str) -> nn.Module:
    if variant == "hetero_sage":
        return HeteroSAGE(data, hidden_dim=hidden_dim, out_dim=out_dim, dropout=dropout)
    if variant == "hetero_no_message":
        return HeteroNoMessage(data, hidden_dim=hidden_dim, out_dim=out_dim, dropout=dropout)
    if variant == "poly_mlp":
        return PolyMLP(
            in_dim=int(data["polysaccharide"].x.size(1)),
            hidden_dim=hidden_dim,
            out_dim=out_dim,
            dropout=dropout,
        )
    if variant == "poly_linear":
        return PolyLinear(in_dim=int(data["polysaccharide"].x.size(1)), out_dim=out_dim)
    raise ValueError(f"Unsupported model variant: {variant}")


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    payload = torch.load(args.pyg_path)
    data = payload["data"]
    metadata = payload["metadata"]
    label_names = metadata["label_names"]

    model = build_model(
        data,
        hidden_dim=args.hidden_dim,
        out_dim=len(label_names),
        dropout=args.dropout,
        variant=args.model_variant,
    )
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )
    criterion = nn.BCEWithLogitsLoss()

    train_mask = data["polysaccharide"].train_mask
    valid_mask = data["polysaccharide"].valid_mask
    test_mask = data["polysaccharide"].test_mask
    y = data["polysaccharide"].y

    best_state = None
    best_valid_macro_f1 = -1.0
    best_epoch = 0
    epochs_without_improvement = 0

    for epoch in range(1, args.epochs + 1):
        model.train()
        optimizer.zero_grad()
        logits = model(data)
        loss = criterion(logits[train_mask], y[train_mask])
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            logits = model(data)
            valid_logits = logits[valid_mask]
            valid_truth = y[valid_mask]
            thresholds = tune_thresholds(torch.sigmoid(valid_logits), valid_truth)
            valid_macro_f1, _ = evaluate_from_logits(valid_logits, valid_truth, label_names, thresholds)

        if valid_macro_f1 > best_valid_macro_f1:
            best_valid_macro_f1 = valid_macro_f1
            best_epoch = epoch
            epochs_without_improvement = 0
            best_state = {
                "model_state": copy.deepcopy(model.state_dict()),
                "thresholds": thresholds.clone(),
            }
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= args.patience:
                break

    if best_state is None:
        raise RuntimeError("Training did not produce a valid checkpoint")

    model.load_state_dict(best_state["model_state"])
    thresholds = best_state["thresholds"]

    model.eval()
    with torch.no_grad():
        logits = model(data)
        valid_logits = logits[valid_mask]
        valid_truth = y[valid_mask]
        test_logits = logits[test_mask]
        test_truth = y[test_mask]

    valid_macro_f1, valid_exact = evaluate_from_logits(valid_logits, valid_truth, label_names, thresholds)
    test_macro_f1, test_exact = evaluate_from_logits(test_logits, test_truth, label_names, thresholds)

    result = {
        "pyg_path": str(args.pyg_path),
        "hidden_dim": args.hidden_dim,
        "epochs_requested": args.epochs,
        "best_epoch": best_epoch,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "dropout": args.dropout,
        "patience": args.patience,
        "seed": args.seed,
        "model_variant": args.model_variant,
        "num_labels": len(label_names),
        "train_size": int(train_mask.sum().item()),
        "valid_size": int(valid_mask.sum().item()),
        "test_size": int(test_mask.sum().item()),
        "valid_macro_f1": valid_macro_f1,
        "valid_exact_match_ratio": valid_exact,
        "test_macro_f1": test_macro_f1,
        "test_exact_match_ratio": test_exact,
        "include_disease_edges": bool(metadata.get("include_disease_edges", False)),
        "poly_feature_dim": int(data["polysaccharide"].x.size(1)),
        "note": "Unified node classification runner with early stopping on valid macro-F1 and per-label threshold tuning.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
