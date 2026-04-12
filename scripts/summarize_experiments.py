"""Summarize experiment JSON files into a markdown comparison table."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
OUTPUT = ROOT / "docs" / "experiment_comparison.md"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def metric(payload: dict, primary: str, fallback: str | None = None) -> float | None:
    if primary in payload:
        return payload[primary]
    if fallback and fallback in payload:
        return payload[fallback]
    return None


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.4f}"


def main() -> None:
    specs = [
        (
            "Meta-Path",
            "Clean",
            EXPERIMENTS / "meta_path_baseline_random.json",
        ),
        (
            "Meta-Path",
            "With Disease",
            EXPERIMENTS / "meta_path_baseline_random_with_disease.json",
        ),
        (
            "Hetero GNN",
            "Clean",
            EXPERIMENTS / "hetero_gnn_baseline_random_tuned.json",
        ),
        (
            "Hetero GNN",
            "With Disease Edges",
            EXPERIMENTS / "hetero_gnn_baseline_random_with_disease_tuned.json",
        ),
        (
            "Hybrid Hetero GNN",
            "Clean",
            EXPERIMENTS / "hybrid_hetero_gnn_baseline_random.json",
        ),
        (
            "Hybrid Hetero GNN",
            "Meta-Path + Disease Features",
            EXPERIMENTS / "hybrid_hetero_gnn_baseline_random_with_disease.json",
        ),
        (
            "Hybrid Hetero GNN",
            "Disease Edges + Disease Features",
            EXPERIMENTS / "hybrid_hetero_gnn_baseline_random_full_disease.json",
        ),
    ]

    lines = [
        "# Experiment Comparison",
        "",
        "| Model | Setting | Labels | Valid Macro-F1 | Test Macro-F1 | Test Exact Match |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]

    for model_name, setting, path in specs:
        payload = read_json(path)
        num_labels = payload.get("num_labels", "-")
        valid_macro_f1 = metric(payload, "valid_macro_f1")
        test_macro_f1 = metric(payload, "test_macro_f1", "macro_f1")
        test_exact = metric(payload, "test_exact_match_ratio", "exact_match_ratio")
        lines.append(
            f"| {model_name} | {setting} | {num_labels} | {fmt(valid_macro_f1)} | {fmt(test_macro_f1)} | {fmt(test_exact)} |"
        )

    lines.extend(
        [
            "",
            "## Readout",
            "",
            "- `Clean` means no disease edges and no disease meta-path features.",
            "- `With Disease` variants are stronger but less clean for causal interpretation because disease information is tightly coupled to labels.",
            "- Current strongest clean baseline is `Meta-Path`.",
            "- Current strongest overall baseline is `Meta-Path` with disease features.",
            "- Current strongest graph-neural setting is `Hybrid Hetero GNN` with disease edges and disease features.",
        ]
    )

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
