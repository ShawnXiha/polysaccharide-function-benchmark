from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


REPO_ROOT = Path(__file__).resolve().parents[1]
KG_DIR = REPO_ROOT / "data" / "processed" / "neo4j"
FIG_DIR = REPO_ROOT / "paper" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

COLORS = {
    "poly": "#1f4e79",
    "organism": "#4c956c",
    "monosaccharide": "#56b4e9",
    "bond": "#f6aa1c",
    "disease": "#c0392b",
    "publication": "#7f8c8d",
    "function": "#8e44ad",
    "ontology": "#d81b60",
    "edge": "#6c757d",
}


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_node_map(path: Path, id_key: str, label_key: str) -> dict[str, str]:
    return {row[id_key]: row.get(label_key, "") for row in read_csv(path)}


def build_edge_map(path: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for row in read_csv(path):
        out.setdefault(row["source_id"], []).append(row["target_id"])
    return out


def wrap_label(text: str, width: int = 16) -> str:
    text = str(text)
    if len(text) <= width:
        return text
    parts = []
    while len(text) > width:
        cut = text.rfind(" ", 0, width)
        if cut <= 0:
            cut = width
        parts.append(text[:cut].strip())
        text = text[cut:].strip()
    if text:
        parts.append(text)
    return "\n".join(parts)


def draw_edge(ax, start: tuple[float, float], end: tuple[float, float], color: str = COLORS["edge"], style: str = "-"):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-",
        linewidth=1.2,
        color=color,
        linestyle=style,
        alpha=0.9,
        zorder=1,
    )
    ax.add_patch(arrow)


def draw_node(ax, xy: tuple[float, float], label: str, color: str, size: float = 1700, text_color: str = "white"):
    ax.scatter([xy[0]], [xy[1]], s=size, c=color, edgecolors="white", linewidths=1.5, zorder=3)
    ax.text(xy[0], xy[1], wrap_label(label), ha="center", va="center", fontsize=8, color=text_color, zorder=4)


def apply_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 10,
            "figure.dpi": 300,
            "savefig.dpi": 300,
        }
    )


def get_case_data() -> dict[str, dict]:
    candidates = list(csv.DictReader((REPO_ROOT / "experiments" / "case_study_pipeline" / "case_study_candidates.csv").open(encoding="utf-8")))
    by_key = {(row["category"], row["poly_id"]): row for row in candidates}
    rescue = dict(by_key[("ontology_rescue", "dolphin::34783")])
    failure = dict(by_key[("clean_failure", "dolphin::33382")])
    failure_ontology = by_key[("ontology_failure", "dolphin::33382")]
    failure["baseline_filtered_rank"] = failure_ontology["baseline_filtered_rank"]
    failure["ontology_filtered_rank"] = failure_ontology["ontology_filtered_rank"]
    return {
        "rescue": rescue,
        "failure": failure,
    }


def parse_preview(text: str, limit: int = 4) -> list[str]:
    if not text:
        return []
    items = [item.strip() for item in text.split(";")]
    out = []
    for item in items:
        if not item or item.startswith("...("):
            continue
        out.append(item)
        if len(out) >= limit:
            break
    return out


def panel(ax, row: dict, title: str, ontology: bool) -> None:
    poly_name = row["poly_name"] or row["poly_id"]
    function_name = row["function_name"]
    organisms = parse_preview(row["organisms"], limit=1)
    monos = parse_preview(row["monosaccharides"], limit=4)
    bonds = parse_preview(row["bonds"], limit=4)
    diseases = parse_preview(row["diseases"], limit=2)
    pubs = parse_preview(row["publications"], limit=1)

    positions = {
        "poly": (0.0, 0.0),
        "organism": (-2.7, 1.2),
        "disease": (-2.7, -1.2),
        "function": (2.3, 0.0),
    }
    mono_pos = [(-1.4, 2.0), (-0.3, 2.25), (0.8, 2.0), (1.8, 1.6)]
    bond_pos = [(-1.4, -1.8), (-0.2, -2.2), (1.0, -1.9), (2.0, -1.4)]

    ax.set_xlim(-4.1, 4.15)
    ax.set_ylim(-2.8, 2.8)
    ax.axis("off")

    draw_node(ax, positions["poly"], wrap_label(poly_name, 16), COLORS["poly"], size=2400)
    draw_node(ax, positions["function"], function_name, COLORS["function"], size=1900)
    draw_edge(ax, positions["poly"], positions["function"])

    if organisms:
        draw_node(ax, positions["organism"], organisms[0], COLORS["organism"], size=1650)
        draw_edge(ax, positions["poly"], positions["organism"])
    if diseases:
        draw_node(ax, positions["disease"], diseases[0], COLORS["disease"], size=1650)
        draw_edge(ax, positions["poly"], positions["disease"])
    for idx, mono in enumerate(monos):
        pos = mono_pos[idx]
        draw_node(ax, pos, mono, COLORS["monosaccharide"], size=1100, text_color="black")
        draw_edge(ax, positions["poly"], pos)
    for idx, bond in enumerate(bonds):
        pos = bond_pos[idx]
        draw_node(ax, pos, bond, COLORS["bond"], size=1100, text_color="black")
        draw_edge(ax, positions["poly"], pos)

    if ontology:
        family = "reprod.\nregen."
        parent = "tissue\nprotect."
        family_pos = (1.5, 1.5)
        parent_pos = (1.5, 2.4)
        draw_node(ax, family_pos, family, COLORS["ontology"], size=1180)
        draw_node(ax, parent_pos, parent, COLORS["ontology"], size=1050)
        draw_edge(ax, family_pos, positions["function"], color=COLORS["ontology"], style="--")
        draw_edge(ax, parent_pos, family_pos, color=COLORS["ontology"], style="--")
        rank_text = (
            f"Tail label\nsupport = {row['train_support']}\n"
            f"Baseline rank = {row['baseline_filtered_rank']}\n"
            f"Ontology rank = {row['ontology_filtered_rank']}\n"
            f"Rescue count = {row['rescue_count_16seeds']}/16 seeds"
        )
        rank_xy = (2.75, -1.72)
    else:
        rank_text = (
            f"Head label\nsupport = {row['train_support']}\n"
            f"Clean rank = {row['clean_filtered_rank']}\n"
            f"Disease-aware rank = {row['baseline_filtered_rank']}\n"
            f"Ontology rank = {row['ontology_filtered_rank']}"
        )
        rank_xy = (2.55, 2.55)

    ax.text(
        rank_xy[0],
        rank_xy[1],
        rank_text,
        ha="right",
        va="top",
        fontsize=8,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "#f8f9fa", "edgecolor": "#c0c0c0"},
    )
    ax.text(-4.0, 2.55, title, fontsize=10, fontweight="bold", ha="left", va="top")
    if pubs:
        ax.text(
            -3.95,
            -2.55,
            f"DOI: {pubs[0]}",
            ha="left",
            va="bottom",
            fontsize=7.5,
            color=COLORS["publication"],
        )


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(FIG_DIR / f"{stem}.png", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    apply_style()
    cases = get_case_data()
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.2))
    panel(axes[0], cases["rescue"], "A. Ontology-rescued tail case", ontology=True)
    panel(axes[1], cases["failure"], "B. Persistent failure case", ontology=False)
    fig.suptitle(
        "Figure 4. Local case-study subgraphs for ontology rescue and persistent failure",
        fontsize=11,
        fontweight="bold",
        y=1.02,
    )
    save(fig, "figure4_case_subgraphs")
    summary = {
        "output_png": str(FIG_DIR / "figure4_case_subgraphs.png"),
        "output_pdf": str(FIG_DIR / "figure4_case_subgraphs.pdf"),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
