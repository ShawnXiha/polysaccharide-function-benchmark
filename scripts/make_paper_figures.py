from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


REPO_ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = REPO_ROOT / "paper" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

COLORS = {
    "clean": "#0072B2",
    "disease": "#D55E00",
    "ontology": "#009E73",
    "neutral": "#4D4D4D",
    "tail": "#CC79A7",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def apply_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "figure.dpi": 300,
            "savefig.dpi": 300,
        }
    )


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(FIG_DIR / f"{stem}.png", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def draw_box(ax, x, y, w, h, text, fc, ec="#333333"):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.0,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(
        FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12, linewidth=1.2, color="#444444")
    )


def make_pipeline_figure() -> None:
    fig, ax = plt.subplots(figsize=(11, 3.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_box(ax, 0.02, 0.58, 0.16, 0.22, "DoLPHiN raw records\nstructure, source,\nfunction, disease, DOI", "#E8F1FA")
    draw_box(ax, 0.24, 0.58, 0.18, 0.22, "Normalization\nentity parsing\nprovenance retention", "#FDEBD0")
    draw_box(ax, 0.48, 0.56, 0.20, 0.26, "Knowledge graph\npoly / organism /\nmono / bond /\nfunction / disease / pub", "#E8F5E9")
    draw_box(ax, 0.74, 0.60, 0.22, 0.18, "Masked poly-function\nlink prediction\nfiltered ranking", "#F3E5F5")

    draw_box(ax, 0.73, 0.26, 0.10, 0.14, "Clean\nmeta-path", "#D6EAF8")
    draw_box(ax, 0.85, 0.26, 0.11, 0.14, "Disease-aware\nupper bound", "#FAD7A0")
    draw_box(ax, 0.79, 0.05, 0.15, 0.14, "Ontology-enhanced\n tail retrieval", "#D5F5E3")

    arrow(ax, 0.18, 0.69, 0.24, 0.69)
    arrow(ax, 0.42, 0.69, 0.48, 0.69)
    arrow(ax, 0.68, 0.69, 0.74, 0.69)
    arrow(ax, 0.84, 0.60, 0.78, 0.40)
    arrow(ax, 0.85, 0.60, 0.90, 0.40)
    arrow(ax, 0.86, 0.26, 0.86, 0.19)

    ax.text(0.02, 0.92, "Figure 1. DoLPHiN KG construction and evaluation pipeline", fontsize=11, fontweight="bold")
    ax.text(
        0.02,
        0.88,
        "The graph is built from normalized structural, biological, disease, and publication evidence, then evaluated with masked poly-function retrieval.",
        fontsize=8,
        color="#444444",
    )
    save(fig, "figure1_pipeline")


def make_benchmark_figure() -> None:
    stability = load_json(REPO_ROOT / "experiments" / "ontology_stability_runs" / "ontology_stability_summary.json")

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.8))

    models = ["Meta+LR", "PolyX+Meta+LR", "Meta+MLP", "Hetero", "No-msg", "Poly-MLP"]
    clean = [0.3465, 0.3317, 0.3065, 0.0464, 0.0426, 0.0466]
    x = np.arange(len(models))
    axes[0].bar(x, clean, width=0.7, color=[COLORS["clean"], "#4DB6AC", "#7E57C2", COLORS["neutral"], "#9E9E9E", "#8D6E63"])
    axes[0].set_xticks(x, models)
    axes[0].set_ylabel("Test macro-F1")
    axes[0].set_title("A. Clean function prediction")
    axes[0].set_ylim(0, 0.40)
    axes[0].tick_params(axis="x", rotation=25)
    axes[0].text(0, clean[0] + 0.012, "best clean", ha="center", fontsize=8)

    tuned_baseline = [0.8491, 0.9120, 0.9380]
    tuned_ontology = [0.8490, 0.9120, 0.9390]
    metrics = ["Filtered MRR", "Hits@3", "Hits@5"]
    x2 = np.arange(len(metrics))
    w = 0.35
    axes[1].bar(x2 - w / 2, tuned_baseline, width=w, color=COLORS["disease"], label="Disease-aware baseline")
    axes[1].bar(x2 + w / 2, tuned_ontology, width=w, color=COLORS["ontology"], label="Ontology variant")
    axes[1].set_xticks(x2, metrics)
    axes[1].set_ylim(0.75, 0.96)
    axes[1].set_title("B. Tuned upper-bound retrieval")
    axes[1].legend(frameon=False, loc="lower left")

    ablation_names = ["Hetero", "No-msg", "Poly-MLP"]
    base_vals = [0.0464, 0.0426, 0.0466]
    hybrid_vals = [0.0347, 0.0386, 0.0440]
    x3 = np.arange(len(ablation_names))
    axes[2].bar(x3 - w / 2, base_vals, width=w, color=COLORS["neutral"], label="Base graph")
    axes[2].bar(x3 + w / 2, hybrid_vals, width=w, color="#A1887F", label="Hybrid input")
    axes[2].set_xticks(x3, ablation_names)
    axes[2].set_ylabel("Test macro-F1")
    axes[2].set_ylim(0, 0.065)
    axes[2].set_title("C. GNN failure ablation")
    axes[2].legend(frameon=False, loc="upper right")

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle("Figure 2. Clean benchmarks, upper-bound retrieval, and GNN failure ablations", fontsize=11, fontweight="bold", y=1.04)
    fig.tight_layout()
    save(fig, "figure2_benchmarks")


def make_stability_figure() -> None:
    summary = load_json(REPO_ROOT / "experiments" / "ontology_stability_runs" / "ontology_stability_summary.json")
    seeds = [s["seed"] for s in summary["seed_summaries"]]
    baseline_tail = [s["baseline_tail"]["micro_filtered_hits@3"] for s in summary["seed_summaries"]]
    ontology_tail = [s["ontology_tail"]["micro_filtered_hits@3"] for s in summary["seed_summaries"]]
    deltas = [o - b for b, o in zip(baseline_tail, ontology_tail)]

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.8))

    axes[0].plot(seeds, baseline_tail, marker="o", color=COLORS["disease"], label="Baseline")
    axes[0].plot(seeds, ontology_tail, marker="o", color=COLORS["ontology"], label="Ontology")
    axes[0].set_title("A. Tail Hits@3 by seed")
    axes[0].set_xlabel("Seed")
    axes[0].set_ylabel("Tail micro filtered Hits@3")
    axes[0].legend(frameon=False)

    axes[1].axhline(0, color="#777777", linewidth=1.0)
    axes[1].bar(range(len(seeds)), deltas, color=COLORS["tail"], width=0.7)
    axes[1].set_xticks(range(len(seeds)), [str(s) for s in seeds], rotation=45)
    axes[1].set_title("B. Tail delta by seed")
    axes[1].set_xlabel("Seed")
    axes[1].set_ylabel("Ontology - baseline")

    axes[2].axis("off")
    sig = summary["significance"]
    stab = summary["stability"]
    text = (
        "C. Stability summary\n\n"
        f"Paired seeds: {summary['num_seed_pairs']}\n"
        f"Paired edges: {summary['pooled_num_edges']}\n\n"
        f"Tail Hits@3: {stab['tail_filtered_hits3']['baseline_mean']:.4f}"
        f" -> {stab['tail_filtered_hits3']['ontology_mean']:.4f}\n"
        f"Delta: {stab['tail_filtered_hits3']['delta_mean']:.4f}\n"
        f"One-sided McNemar p = {sig['tail_filtered_hits3']['mcnemar_p']['p_one_sided_ontology_better']:.5f}\n"
        f"Tail MRR delta = {sig['tail_filtered_mrr']['mean_delta']:.4f}\n"
        f"Permutation p = {sig['tail_filtered_mrr']['permutation_p']:.6f}\n"
        f"Seed consistency: {stab['tail_filtered_hits3']['ontology_ge_baseline_seeds']}/"
        f"{stab['tail_filtered_hits3']['num_seeds']} non-regression"
    )
    axes[2].text(0.02, 0.95, text, va="top", ha="left", fontsize=9)

    for ax in axes[:2]:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle("Figure 3. Stability validation of ontology-enhanced tail retrieval", fontsize=11, fontweight="bold", y=1.04)
    fig.tight_layout()
    save(fig, "figure3_stability")


def main() -> None:
    apply_style()
    make_pipeline_figure()
    make_benchmark_figure()
    make_stability_figure()
    print(json.dumps({"figure_dir": str(FIG_DIR)}, indent=2))


if __name__ == "__main__":
    main()
