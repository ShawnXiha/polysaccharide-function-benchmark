"""Run a lightweight sequence transformer baseline using PyTorch only."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

from polysaccharidesdb.models.dataset import index_by_poly_id, load_dataset
from polysaccharidesdb.models.split_utils import expand_split_payload
from polysaccharidesdb.paths import DATA_PROCESSED, EXPERIMENTS
from polysaccharidesdb.utils.io import read_json, write_json
from polysaccharidesdb.utils.metrics import exact_match_ratio, macro_f1_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run lightweight transformer baseline")
    parser.add_argument("--dataset", type=Path, default=DATA_PROCESSED / "dataset_v0.jsonl")
    parser.add_argument("--split", type=Path, default=DATA_PROCESSED / "splits" / "random_split.json")
    parser.add_argument(
        "--output",
        type=Path,
        default=EXPERIMENTS / "stage1_baseline" / "results" / "sequence_transformer_random.json",
    )
    parser.add_argument("--epochs", type=int, default=60)
    parser.add_argument("--max-len", type=int, default=64)
    return parser.parse_args()


def canonical_sequence(record: dict) -> str:
    return str(record.get("canonical_representation", "")).strip()


def build_char_vocab(records: list[dict]) -> dict[str, int]:
    vocab = {"<pad>": 0, "<unk>": 1}
    for record in records:
        for ch in canonical_sequence(record):
            if ch not in vocab:
                vocab[ch] = len(vocab)
    return vocab


def encode_sequence(text: str, vocab: dict[str, int], max_len: int) -> tuple[list[int], list[int]]:
    ids = [vocab.get(ch, vocab["<unk>"]) for ch in text[:max_len]]
    mask = [1] * len(ids)
    while len(ids) < max_len:
        ids.append(vocab["<pad>"])
        mask.append(0)
    return ids, mask


class SequenceDataset(Dataset):
    def __init__(
        self,
        records: list[dict],
        vocab: dict[str, int],
        label_to_idx: dict[str, int],
        max_len: int,
    ) -> None:
        self.items = []
        for record in records:
            token_ids, mask = encode_sequence(canonical_sequence(record), vocab, max_len)
            y = torch.zeros(len(label_to_idx), dtype=torch.float)
            for label in record.get("function_label", []):
                if label in label_to_idx:
                    y[label_to_idx[label]] = 1.0
            self.items.append(
                {
                    "input_ids": torch.tensor(token_ids, dtype=torch.long),
                    "mask": torch.tensor(mask, dtype=torch.float),
                    "labels": y,
                }
            )

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        return self.items[idx]


class TinyTransformerClassifier(nn.Module):
    def __init__(self, vocab_size: int, num_labels: int, hidden_dim: int = 32, nhead: int = 4) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_dim, padding_idx=0)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=nhead,
            dim_feedforward=64,
            dropout=0.1,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=2)
        self.classifier = nn.Linear(hidden_dim, num_labels)

    def forward(self, input_ids: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        x = self.embedding(input_ids)
        key_padding_mask = mask == 0
        x = self.encoder(x, src_key_padding_mask=key_padding_mask)
        mask_expanded = mask.unsqueeze(-1)
        pooled = (x * mask_expanded).sum(dim=1) / mask_expanded.sum(dim=1).clamp(min=1.0)
        return self.classifier(pooled)


def train_model(train_dataset: SequenceDataset, vocab_size: int, num_labels: int, epochs: int) -> TinyTransformerClassifier:
    model = TinyTransformerClassifier(vocab_size=vocab_size, num_labels=num_labels)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
    criterion = nn.BCEWithLogitsLoss()
    loader = DataLoader(train_dataset, batch_size=min(4, len(train_dataset)), shuffle=True)

    model.train()
    for _ in range(epochs):
        for batch in loader:
            optimizer.zero_grad()
            logits = model(batch["input_ids"], batch["mask"])
            loss = criterion(logits, batch["labels"])
            loss.backward()
            optimizer.step()
    return model


def evaluate_model(model: TinyTransformerClassifier, dataset: SequenceDataset, labels: list[str]) -> tuple[float, float]:
    loader = DataLoader(dataset, batch_size=min(4, len(dataset)), shuffle=False)
    model.eval()
    y_true: list[set[str]] = []
    y_pred: list[set[str]] = []
    with torch.no_grad():
        for batch in loader:
            logits = model(batch["input_ids"], batch["mask"])
            preds = (torch.sigmoid(logits) >= 0.5).int()
            truths = batch["labels"].int()
            for truth_row, pred_row in zip(truths, preds):
                y_true.append({labels[i] for i, value in enumerate(truth_row.tolist()) if value == 1})
                y_pred.append({labels[i] for i, value in enumerate(pred_row.tolist()) if value == 1})
    return macro_f1_score(y_true, y_pred), exact_match_ratio(y_true, y_pred)


def main() -> None:
    args = parse_args()
    torch.manual_seed(42)
    records = load_dataset(args.dataset)
    record_map = index_by_poly_id(records)
    split_payload = read_json(args.split)
    expanded_splits = expand_split_payload(split_payload)

    all_labels = sorted({label for record in records for label in record.get("function_label", [])})
    label_to_idx = {label: idx for idx, label in enumerate(all_labels)}
    vocab = build_char_vocab(records)

    split_results = []
    for split_def in expanded_splits:
        train_records = [record_map[poly_id] for poly_id in split_def["train"]]
        test_records = [record_map[poly_id] for poly_id in split_def["test"]]

        train_dataset = SequenceDataset(train_records, vocab, label_to_idx, args.max_len)
        test_dataset = SequenceDataset(test_records, vocab, label_to_idx, args.max_len)

        model = train_model(train_dataset, vocab_size=len(vocab), num_labels=len(all_labels), epochs=args.epochs)
        macro_f1, exact_match = evaluate_model(model, test_dataset, all_labels)

        split_results.append(
            {
                "split_name": split_def["name"],
                "num_train": len(train_records),
                "num_test": len(test_records),
                "labels": all_labels,
                "macro_f1": macro_f1,
                "exact_match_ratio": exact_match,
            }
        )

    result = {
        "dataset": str(args.dataset),
        "split": str(args.split),
        "results": split_results,
        "note": "lightweight transformer encoder over canonical representation without external transformers dependency",
    }
    write_json(args.output, result)
    print(f"Wrote baseline result to {args.output}")


if __name__ == "__main__":
    main()
