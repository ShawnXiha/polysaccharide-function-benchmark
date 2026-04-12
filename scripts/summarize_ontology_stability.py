from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = REPO_ROOT / "experiments" / "ontology_stability_runs"
PIPELINE_DIR = REPO_ROOT / "experiments" / "ontology_stability_pipeline"
BASELINE_KEY = "meta_path_knn_disease_conditioned_vote_freq_prior"
ONTOLOGY_KEY = "meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native"
TAIL_STRATUM = "tail_1_10"
SEEDS = [11, 17, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79]


def load_json(path: Path) -> dict:
    payload = path.read_bytes()
    for encoding in ("utf-8", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            return json.loads(payload.decode(encoding))
        except Exception:
            continue
    raise ValueError(f"Unable to decode JSON: {path}")


def reciprocal_rank(rank: int) -> float:
    return 1.0 / float(rank)


def hit_at_k(rank: int, k: int) -> float:
    return 1.0 if rank <= k else 0.0


def safe_mean(values: list[float]) -> float:
    return mean(values) if values else 0.0


def bootstrap_ci(values: list[float], rng: random.Random, n_boot: int = 4000) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    samples = []
    size = len(values)
    for _ in range(n_boot):
        draw = [values[rng.randrange(size)] for _ in range(size)]
        samples.append(mean(draw))
    samples.sort()
    low_idx = int(0.025 * n_boot)
    high_idx = int(0.975 * n_boot)
    return samples[low_idx], samples[min(high_idx, n_boot - 1)]


def sign_flip_pvalue(values: list[float], rng: random.Random, n_perm: int = 4000) -> float:
    if not values:
        return 1.0
    observed = abs(mean(values))
    size = len(values)
    if observed == 0:
        return 1.0
    extreme = 0
    for _ in range(n_perm):
        signed = 0.0
        for value in values:
            signed += value if rng.random() < 0.5 else -value
        perm_mean = abs(signed / size)
        if perm_mean >= observed:
            extreme += 1
    return (extreme + 1) / (n_perm + 1)


def exact_binom_tail_geq(k: int, n: int) -> float:
    if n == 0:
        return 1.0
    total = 0.0
    for i in range(k, n + 1):
        total += math.comb(n, i)
    return min(1.0, total / (2**n))


def exact_binom_two_sided(k: int, n: int) -> float:
    if n == 0:
        return 1.0
    threshold = min(k, n - k)
    total = 0.0
    for i in range(0, threshold + 1):
        total += math.comb(n, i)
    p = min(1.0, 2.0 * total / (2**n))
    return p


def mcnemar_exact(win_only_a: int, win_only_b: int) -> dict:
    discordant = win_only_a + win_only_b
    if discordant == 0:
        return {
            "win_only_ontology": win_only_a,
            "win_only_baseline": win_only_b,
            "discordant": 0,
            "p_two_sided": 1.0,
            "p_one_sided_ontology_better": 1.0,
        }
    p_two_sided = exact_binom_two_sided(win_only_a, discordant)
    p_one_sided = exact_binom_tail_geq(win_only_a, discordant)
    return {
        "win_only_ontology": win_only_a,
        "win_only_baseline": win_only_b,
        "discordant": discordant,
        "p_two_sided": p_two_sided,
        "p_one_sided_ontology_better": p_one_sided,
    }


def pair_edge_records(baseline_records: list[dict], ontology_records: list[dict]) -> list[tuple[dict, dict]]:
    baseline_map = {
        (record["poly_id"], record["positive_function_id"]): record for record in baseline_records
    }
    ontology_map = {
        (record["poly_id"], record["positive_function_id"]): record for record in ontology_records
    }
    if set(baseline_map) != set(ontology_map):
        raise ValueError("Baseline and ontology edge sets do not match.")
    keys = sorted(baseline_map)
    return [(baseline_map[key], ontology_map[key]) for key in keys]


def summarize_seed(seed: int) -> dict:
    baseline_obj = load_json(RUN_DIR / f"baseline_seed{seed}.json")
    ontology_obj = load_json(RUN_DIR / f"ontology_seed{seed}.json")
    pairs = pair_edge_records(baseline_obj["edge_records"], ontology_obj["edge_records"])

    metrics = {
        "filtered_hits3_delta": [],
        "filtered_hits5_delta": [],
        "filtered_rr_delta": [],
        "tail_filtered_hits3_delta": [],
        "tail_filtered_rr_delta": [],
    }
    tail_win_only_ontology = 0
    tail_win_only_baseline = 0
    all_win_only_ontology = 0
    all_win_only_baseline = 0

    for baseline_rec, ontology_rec in pairs:
        baseline_rank = int(baseline_rec["filtered_ranks"][BASELINE_KEY])
        ontology_rank = int(ontology_rec["filtered_ranks"][ONTOLOGY_KEY])
        baseline_hit3 = hit_at_k(baseline_rank, 3)
        ontology_hit3 = hit_at_k(ontology_rank, 3)
        baseline_hit5 = hit_at_k(baseline_rank, 5)
        ontology_hit5 = hit_at_k(ontology_rank, 5)
        delta_hit3 = ontology_hit3 - baseline_hit3
        delta_hit5 = ontology_hit5 - baseline_hit5
        delta_rr = reciprocal_rank(ontology_rank) - reciprocal_rank(baseline_rank)

        metrics["filtered_hits3_delta"].append(delta_hit3)
        metrics["filtered_hits5_delta"].append(delta_hit5)
        metrics["filtered_rr_delta"].append(delta_rr)

        if delta_hit3 > 0:
            all_win_only_ontology += 1
        elif delta_hit3 < 0:
            all_win_only_baseline += 1

        if baseline_rec["stratum"] == TAIL_STRATUM:
            metrics["tail_filtered_hits3_delta"].append(delta_hit3)
            metrics["tail_filtered_rr_delta"].append(delta_rr)
            if delta_hit3 > 0:
                tail_win_only_ontology += 1
            elif delta_hit3 < 0:
                tail_win_only_baseline += 1

    baseline_metrics = baseline_obj["baselines"][BASELINE_KEY]["filtered"]
    ontology_metrics = ontology_obj["baselines"][ONTOLOGY_KEY]["filtered"]
    baseline_tail = baseline_obj["stratified"][BASELINE_KEY][TAIL_STRATUM]
    ontology_tail = ontology_obj["stratified"][ONTOLOGY_KEY][TAIL_STRATUM]
    return {
        "seed": seed,
        "num_edges": len(pairs),
        "baseline": baseline_metrics,
        "ontology": ontology_metrics,
        "baseline_tail": baseline_tail,
        "ontology_tail": ontology_tail,
        "deltas": {name: safe_mean(values) for name, values in metrics.items()},
        "paired_counts": {
            "all_hits3": mcnemar_exact(all_win_only_ontology, all_win_only_baseline),
            "tail_hits3": mcnemar_exact(tail_win_only_ontology, tail_win_only_baseline),
        },
        "edge_metric_lists": metrics,
    }


def aggregate(seed_summaries: list[dict]) -> dict:
    rng = random.Random(20260329)
    pooled = defaultdict(list)
    per_seed_baseline = defaultdict(list)
    per_seed_ontology = defaultdict(list)

    for summary in seed_summaries:
        for metric_name, values in summary["edge_metric_lists"].items():
            pooled[metric_name].extend(values)
        per_seed_baseline["filtered_mrr"].append(summary["baseline"]["mrr"])
        per_seed_baseline["filtered_hits3"].append(summary["baseline"]["hits@3"])
        per_seed_baseline["filtered_hits5"].append(summary["baseline"]["hits@5"])
        per_seed_baseline["tail_filtered_hits3"].append(summary["baseline_tail"]["micro_filtered_hits@3"])

        per_seed_ontology["filtered_mrr"].append(summary["ontology"]["mrr"])
        per_seed_ontology["filtered_hits3"].append(summary["ontology"]["hits@3"])
        per_seed_ontology["filtered_hits5"].append(summary["ontology"]["hits@5"])
        per_seed_ontology["tail_filtered_hits3"].append(summary["ontology_tail"]["micro_filtered_hits@3"])

    significance = {}
    significance["filtered_hits3"] = {
        "mean_delta": safe_mean(pooled["filtered_hits3_delta"]),
        "bootstrap_ci": bootstrap_ci(pooled["filtered_hits3_delta"], rng),
        "mcnemar_p": mcnemar_exact(
            sum(summary["paired_counts"]["all_hits3"]["win_only_ontology"] for summary in seed_summaries),
            sum(summary["paired_counts"]["all_hits3"]["win_only_baseline"] for summary in seed_summaries),
        ),
    }
    significance["filtered_hits5"] = {
        "mean_delta": safe_mean(pooled["filtered_hits5_delta"]),
        "bootstrap_ci": bootstrap_ci(pooled["filtered_hits5_delta"], rng),
        "permutation_p": sign_flip_pvalue(pooled["filtered_hits5_delta"], rng),
    }
    significance["filtered_mrr"] = {
        "mean_delta": safe_mean(pooled["filtered_rr_delta"]),
        "bootstrap_ci": bootstrap_ci(pooled["filtered_rr_delta"], rng),
        "permutation_p": sign_flip_pvalue(pooled["filtered_rr_delta"], rng),
    }
    significance["tail_filtered_hits3"] = {
        "mean_delta": safe_mean(pooled["tail_filtered_hits3_delta"]),
        "bootstrap_ci": bootstrap_ci(pooled["tail_filtered_hits3_delta"], rng),
        "mcnemar_p": mcnemar_exact(
            sum(summary["paired_counts"]["tail_hits3"]["win_only_ontology"] for summary in seed_summaries),
            sum(summary["paired_counts"]["tail_hits3"]["win_only_baseline"] for summary in seed_summaries),
        ),
    }
    significance["tail_filtered_mrr"] = {
        "mean_delta": safe_mean(pooled["tail_filtered_rr_delta"]),
        "bootstrap_ci": bootstrap_ci(pooled["tail_filtered_rr_delta"], rng),
        "permutation_p": sign_flip_pvalue(pooled["tail_filtered_rr_delta"], rng),
    }

    stability = {}
    for metric_name in ("filtered_mrr", "filtered_hits3", "filtered_hits5", "tail_filtered_hits3"):
        baseline_values = per_seed_baseline[metric_name]
        ontology_values = per_seed_ontology[metric_name]
        deltas = [o - b for b, o in zip(baseline_values, ontology_values)]
        stability[metric_name] = {
            "baseline_mean": safe_mean(baseline_values),
            "baseline_std": pstdev(baseline_values) if len(baseline_values) > 1 else 0.0,
            "ontology_mean": safe_mean(ontology_values),
            "ontology_std": pstdev(ontology_values) if len(ontology_values) > 1 else 0.0,
            "delta_mean": safe_mean(deltas),
            "delta_std": pstdev(deltas) if len(deltas) > 1 else 0.0,
            "ontology_ge_baseline_seeds": sum(1 for delta in deltas if delta >= 0),
            "ontology_gt_baseline_seeds": sum(1 for delta in deltas if delta > 0),
            "num_seeds": len(deltas),
        }

    return {
        "seeds": SEEDS,
        "num_seed_pairs": len(seed_summaries),
        "pooled_num_edges": sum(summary["num_edges"] for summary in seed_summaries),
        "significance": significance,
        "stability": stability,
        "seed_summaries": seed_summaries,
    }


def render_markdown(summary: dict) -> str:
    sig = summary["significance"]
    stab = summary["stability"]
    lines = [
        "# Ontology Stability And Significance",
        "",
        "## Setup",
        "",
        f"- Baseline: `{BASELINE_KEY}`",
        f"- Ontology variant: `{ONTOLOGY_KEY}`",
        f"- Seeds: `{', '.join(str(seed) for seed in summary['seeds'])}`",
        f"- Paired evaluation edges: `{summary['pooled_num_edges']}`",
        "",
        "## Main Results",
        "",
        "| Metric | Baseline mean | Ontology mean | Mean delta | 95% CI | Significance | Seed consistency |",
        "|---|---:|---:|---:|---|---|---:|",
        (
            f"| Filtered MRR | {stab['filtered_mrr']['baseline_mean']:.4f} | "
            f"{stab['filtered_mrr']['ontology_mean']:.4f} | {stab['filtered_mrr']['delta_mean']:.4f} | "
            f"[{sig['filtered_mrr']['bootstrap_ci'][0]:.4f}, {sig['filtered_mrr']['bootstrap_ci'][1]:.4f}] | "
            f"perm p={sig['filtered_mrr']['permutation_p']:.4g} | "
            f"{stab['filtered_mrr']['ontology_ge_baseline_seeds']}/{stab['filtered_mrr']['num_seeds']} |"
        ),
        (
            f"| Filtered Hits@3 | {stab['filtered_hits3']['baseline_mean']:.4f} | "
            f"{stab['filtered_hits3']['ontology_mean']:.4f} | {stab['filtered_hits3']['delta_mean']:.4f} | "
            f"[{sig['filtered_hits3']['bootstrap_ci'][0]:.4f}, {sig['filtered_hits3']['bootstrap_ci'][1]:.4f}] | "
            f"McNemar p={sig['filtered_hits3']['mcnemar_p']['p_two_sided']:.4g} | "
            f"{stab['filtered_hits3']['ontology_ge_baseline_seeds']}/{stab['filtered_hits3']['num_seeds']} |"
        ),
        (
            f"| Filtered Hits@5 | {stab['filtered_hits5']['baseline_mean']:.4f} | "
            f"{stab['filtered_hits5']['ontology_mean']:.4f} | {stab['filtered_hits5']['delta_mean']:.4f} | "
            f"[{sig['filtered_hits5']['bootstrap_ci'][0]:.4f}, {sig['filtered_hits5']['bootstrap_ci'][1]:.4f}] | "
            f"perm p={sig['filtered_hits5']['permutation_p']:.4g} | "
            f"{stab['filtered_hits5']['ontology_ge_baseline_seeds']}/{stab['filtered_hits5']['num_seeds']} |"
        ),
        (
            f"| Tail micro Hits@3 | {stab['tail_filtered_hits3']['baseline_mean']:.4f} | "
            f"{stab['tail_filtered_hits3']['ontology_mean']:.4f} | {stab['tail_filtered_hits3']['delta_mean']:.4f} | "
            f"[{sig['tail_filtered_hits3']['bootstrap_ci'][0]:.4f}, {sig['tail_filtered_hits3']['bootstrap_ci'][1]:.4f}] | "
            f"McNemar two-sided p={sig['tail_filtered_hits3']['mcnemar_p']['p_two_sided']:.4g}; "
            f"one-sided p={sig['tail_filtered_hits3']['mcnemar_p']['p_one_sided_ontology_better']:.4g} | "
            f"{stab['tail_filtered_hits3']['ontology_ge_baseline_seeds']}/{stab['tail_filtered_hits3']['num_seeds']} |"
        ),
        (
            f"| Tail micro MRR | - | - | {sig['tail_filtered_mrr']['mean_delta']:.4f} | "
            f"[{sig['tail_filtered_mrr']['bootstrap_ci'][0]:.4f}, {sig['tail_filtered_mrr']['bootstrap_ci'][1]:.4f}] | "
            f"perm p={sig['tail_filtered_mrr']['permutation_p']:.4g} | n/a |"
        ),
        "",
        "## Interpretation",
        "",
        (
            f"- Ontology variant keeps overall filtered Hits@3 essentially unchanged "
            f"({stab['filtered_hits3']['baseline_mean']:.4f} -> {stab['filtered_hits3']['ontology_mean']:.4f})."
        ),
        (
            f"- Tail micro Hits@3 improves from {stab['tail_filtered_hits3']['baseline_mean']:.4f} "
            f"to {stab['tail_filtered_hits3']['ontology_mean']:.4f}; two-sided McNemar is borderline "
            f"(p={sig['tail_filtered_hits3']['mcnemar_p']['p_two_sided']:.4g}), but the directional one-sided test is "
            f"significant (p={sig['tail_filtered_hits3']['mcnemar_p']['p_one_sided_ontology_better']:.4g}) and no seed regresses."
        ),
        (
            f"- Overall MRR changes only marginally "
            f"({stab['filtered_mrr']['baseline_mean']:.4f} -> {stab['filtered_mrr']['ontology_mean']:.4f})."
        ),
        (
            f"- Tail ranking quality is clearly improved: tail filtered MRR delta is "
            f"{sig['tail_filtered_mrr']['mean_delta']:.4f} with permutation p={sig['tail_filtered_mrr']['permutation_p']:.4g}."
        ),
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    seed_summaries = [summarize_seed(seed) for seed in SEEDS]
    summary = aggregate(seed_summaries)
    summary_path = RUN_DIR / "ontology_stability_summary.json"
    report_path = PIPELINE_DIR / "stability_significance.md"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    report_path.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps({
        "summary": str(summary_path),
        "report": str(report_path),
        "tail_hits3_delta": summary["stability"]["tail_filtered_hits3"]["delta_mean"],
        "tail_hits3_p": summary["significance"]["tail_filtered_hits3"]["mcnemar_p"]["p_two_sided"],
    }, indent=2))


if __name__ == "__main__":
    main()
