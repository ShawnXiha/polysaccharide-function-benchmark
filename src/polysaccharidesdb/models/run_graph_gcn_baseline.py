"""Run a minimal graph baseline with torch-geometric."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv, global_mean_pool

from polysaccharidesdb.models.dataset import index_by_poly_id, load_dataset
from polysaccharidesdb.models.graph_features import TOKENS, build_vocab
from polysaccharidesdb.models.split_utils import expand_split_payload
from polysaccharidesdb.paths import DATA_PROCESSED, EXPERIMENTS
from polysaccharidesdb.utils.io import read_json, write_json
from polysaccharidesdb.utils.metrics import exact_match_ratio, macro_f1_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run graph GCN baseline")
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
        default=EXPERIMENTS / "stage1_baseline" / "results" / "graph_gcn_random.json",
    )
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--hidden-dim", type=int, default=16)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--batch-size", type=int, default=4)
    return parser.parse_args()


def record_to_graph(record: dict, vocab: dict[str, int], label_to_idx: dict[str, int]) -> Data:
    root_token = f"repr={record.get('canonical_representation', '')}"

    node_tokens = [root_token] + [f"{field}={record.get(field, '')}" for field in TOKENS]
    x = torch.tensor([[vocab.get(token, 0)] for token in node_tokens], dtype=torch.long)

    edge_index = []
    for node_idx in range(1, len(node_tokens)):
        edge_index.append([0, node_idx])
        edge_index.append([node_idx, 0])
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()

    y = torch.zeros((1, len(label_to_idx)), dtype=torch.float)
    for label in record.get("function_label", []):
        if label in label_to_idx:
            y[0, label_to_idx[label]] = 1.0

    return Data(x=x, edge_index=edge_index, y=y)


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class GCNGraphClassifier(nn.Module):
    def __init__(self, vocab_size: int, num_labels: int, hidden_dim: int = 16) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_dim)
        self.conv1 = GCNConv(hidden_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.classifier = nn.Linear(hidden_dim, num_labels)

    def forward(self, data: Data) -> torch.Tensor:
        x = self.embedding(data.x.squeeze(-1))
        x = self.conv1(x, data.edge_index).relu()
        x = self.conv2(x, data.edge_index).relu()
        x = global_mean_pool(x, data.batch)
        return self.classifier(x)


def train_model(
    train_graphs: list[Data],
    vocab_size: int,
    num_labels: int,
    epochs: int,
    hidden_dim: int,
    lr: float,
    batch_size: int,
) -> GCNGraphClassifier:
    model = GCNGraphClassifier(vocab_size=vocab_size, num_labels=num_labels, hidden_dim=hidden_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.BCEWithLogitsLoss()
    loader = DataLoader(train_graphs, batch_size=min(batch_size, len(train_graphs)), shuffle=True)

    model.train()
    for _ in range(epochs):
        for batch in loader:
            optimizer.zero_grad()
            logits = model(batch)
            loss = criterion(logits, batch.y.view_as(logits))
            loss.backward()
            optimizer.step()
    return model


def evaluate_model(model: GCNGraphClassifier, test_graphs: list[Data], labels: list[str]) -> tuple[float, float]:
    model.eval()
    loader = DataLoader(test_graphs, batch_size=min(4, len(test_graphs)), shuffle=False)
    y_true: list[set[str]] = []
    y_pred: list[set[str]] = []
    with torch.no_grad():
        for batch in loader:
            logits = model(batch)
            preds = (torch.sigmoid(logits) >= 0.5).int()
            truths = batch.y.int()
            for truth_row, pred_row in zip(truths, preds):
                y_true.append({labels[i] for i, value in enumerate(truth_row.tolist()) if value == 1})
                y_pred.append({labels[i] for i, value in enumerate(pred_row.tolist()) if value == 1})
    return macro_f1_score(y_true, y_pred), exact_match_ratio(y_true, y_pred)


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    records = load_dataset(args.dataset)
    record_map = index_by_poly_id(records)
    split_payload = read_json(args.split)
    expanded_splits = expand_split_payload(split_payload)

    split_results = []
    for split_def in expanded_splits:
        train_records = [record_map[poly_id] for poly_id in split_def["train"]]
        test_records = [record_map[poly_id] for poly_id in split_def["test"]]

        all_labels = sorted({label for record in train_records for label in record.get("function_label", [])})
        label_to_idx = {label: idx for idx, label in enumerate(all_labels)}
        vocab = build_vocab(train_records)

        train_graphs = [record_to_graph(record, vocab, label_to_idx) for record in train_records]
        test_graphs = [record_to_graph(record, vocab, label_to_idx) for record in test_records]

        model = train_model(
            train_graphs=train_graphs,
            vocab_size=len(vocab),
            num_labels=len(all_labels),
            epochs=args.epochs,
            hidden_dim=args.hidden_dim,
            lr=args.lr,
            batch_size=args.batch_size,
        )
        macro_f1, exact_match = evaluate_model(model, test_graphs, all_labels)

        split_results.append(
            {
                "split_name": split_def["name"],
                "num_train": len(train_records),
                "num_test": len(test_records),
                "labels": all_labels,
                "vocab_size": len(vocab),
                "vocab_built_from": "train",
                "macro_f1": macro_f1,
                "exact_match_ratio": exact_match,
            }
        )

    result = {
        "dataset": str(args.dataset),
        "split": str(args.split),
        "config": {
            "seed": args.seed,
            "epochs": args.epochs,
            "hidden_dim": args.hidden_dim,
            "lr": args.lr,
            "batch_size": args.batch_size,
        },
        "results": split_results,
        "note": "minimal graph baseline using tokenized star graphs and GCN",
    }
    write_json(args.output, result)
    print(f"Wrote baseline result to {args.output}")


if __name__ == "__main__":
    main()
