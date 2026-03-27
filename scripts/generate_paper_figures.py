"""Generate manuscript figures for the poly-core v1 paper."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"


PALETTE = {
    "blue": "#4C78A8",
    "green": "#59A14F",
    "orange": "#F28E2B",
    "red": "#E15759",
    "purple": "#B07AA1",
    "gray": "#9D9D9D",
    "black": "#222222",
}


def apply_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.labelsize": 10,
            "axes.titlesize": 11,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "figure.dpi": 160,
            "savefig.dpi": 300,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def save_figure(fig: plt.Figure, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / f"{stem}.png", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def draw_box(ax, xy, w, h, text, fc, ec=PALETTE["black"], fontsize=9):
    box = FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.2,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(box)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fontsize)


def draw_arrow(ax, start, end, color=PALETTE["black"]):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=13,
            linewidth=1.5,
            color=color,
            shrinkA=4,
            shrinkB=4,
        )
    )


def make_pipeline_figure() -> None:
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_box(ax, (0.03, 0.58), 0.18, 0.18, "Public DoLPHiN\nsite ingestion", "#DCEAF7")
    draw_box(ax, (0.27, 0.58), 0.18, 0.18, "Schema + label\nnormalization", "#E7F4E4")
    draw_box(ax, (0.51, 0.58), 0.18, 0.18, "Publishable benchmark\n4121 records / 18 labels", "#FCE8D2")
    draw_box(ax, (0.75, 0.58), 0.2, 0.18, "Stage 2 tuned logistic\nanchor", "#F7E4E8")

    draw_box(ax, (0.20, 0.18), 0.2, 0.2, "Poly-specific feature\ndesign", "#E9E3F6")
    draw_box(ax, (0.44, 0.18), 0.2, 0.2, "Stage 4 ablation\nvalidation", "#FFF0C9")
    draw_box(ax, (0.68, 0.18), 0.24, 0.2, "Final method:\npoly-core v1\n(MW + branching + residue)", "#E4F3EF")

    draw_arrow(ax, (0.21, 0.67), (0.27, 0.67), PALETTE["blue"])
    draw_arrow(ax, (0.45, 0.67), (0.51, 0.67), PALETTE["green"])
    draw_arrow(ax, (0.69, 0.67), (0.75, 0.67), PALETTE["orange"])

    draw_arrow(ax, (0.60, 0.58), (0.52, 0.39), PALETTE["purple"])
    draw_arrow(ax, (0.84, 0.58), (0.80, 0.39), PALETTE["red"])
    draw_arrow(ax, (0.40, 0.28), (0.44, 0.28), PALETTE["purple"])
    draw_arrow(ax, (0.64, 0.28), (0.68, 0.28), PALETTE["green"])

    ax.text(0.12, 0.82, "Data", ha="center", fontsize=10, fontweight="bold")
    ax.text(0.60, 0.82, "Benchmark + Baseline", ha="center", fontsize=10, fontweight="bold")
    ax.text(0.56, 0.43, "Method refinement", ha="center", fontsize=10, fontweight="bold")

    save_figure(fig, "figure1_pipeline")


def make_main_results_figure() -> None:
    methods = [
        "Majority",
        "Logistic\nuntuned",
        "Random\nForest",
        "Sequence\nn-gram",
        "Sequence\nTransformer",
        "Graph\nGCN",
        "Logistic\ntuned",
        "Poly-core\nv1",
    ]
    macro = [0.0397, 0.1580, 0.1752, 0.2035, 0.0397, 0.1941, 0.2610, 0.2678]
    colors = [
        PALETTE["gray"],
        PALETTE["blue"],
        PALETTE["green"],
        PALETTE["orange"],
        PALETTE["orange"],
        PALETTE["purple"],
        PALETTE["red"],
        PALETTE["black"],
    ]

    fig, ax = plt.subplots(figsize=(8.8, 4.2))
    x = np.arange(len(methods))
    ax.bar(x, macro, color=colors, width=0.72)
    ax.set_ylabel("Macro-F1")
    ax.set_ylim(0, 0.31)
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.axhline(0.2610, color=PALETTE["red"], linestyle="--", linewidth=1.2, alpha=0.8)
    ax.text(6.2, 0.267, "tuned logistic = 0.2610", color=PALETTE["red"], fontsize=8)
    for xi, yi in zip(x, macro):
        ax.text(xi, yi + 0.006, f"{yi:.3f}", ha="center", va="bottom", fontsize=7)
    ax.set_title("Main comparison on publishable_supervised_v1")
    save_figure(fig, "figure2_main_results")


def make_ablation_figure() -> None:
    labels = [
        "Reference: poly-feature-only v1",
        "Remove MW",
        "Remove residue",
        "Remove branching",
        "Remove modification",
        "Remove source kingdom",
        "Remove composition terms",
        "Final: poly-core v1",
    ]
    values = [0.2654, 0.2461, 0.2533, 0.2598, 0.2619, 0.2621, 0.2669, 0.2678]
    colors = [
        PALETTE["blue"],
        PALETTE["red"],
        PALETTE["red"],
        PALETTE["orange"],
        PALETTE["gray"],
        PALETTE["gray"],
        PALETTE["green"],
        PALETTE["black"],
    ]

    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    y = np.arange(len(labels))
    ax.barh(y, values, color=colors, height=0.68)
    ax.set_xlabel("Macro-F1")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(0.24, 0.272)
    ax.invert_yaxis()
    ax.axvline(0.2654, color=PALETTE["blue"], linestyle="--", linewidth=1.2, alpha=0.8)
    ax.text(0.26555, 6.8, "reference", color=PALETTE["blue"], fontsize=8)
    for yi, vi in zip(y, values):
        ax.text(vi + 0.0005, yi, f"{vi:.4f}", va="center", fontsize=7)
    ax.set_title("Component ablation around poly-feature-only v1")
    save_figure(fig, "figure3_ablation")


def main() -> None:
    apply_style()
    make_pipeline_figure()
    make_main_results_figure()
    make_ablation_figure()


if __name__ == "__main__":
    main()
