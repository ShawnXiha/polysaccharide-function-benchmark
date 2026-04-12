from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
KG_DIR = REPO_ROOT / "data" / "processed" / "neo4j"
EXPERIMENT_DIR = REPO_ROOT / "experiments" / "case_study_pipeline"
EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, encoding: str | None = "utf-8") -> dict:
    encodings = [encoding] if encoding else []
    encodings.extend(["utf-8", "utf-16", "utf-16-le", "utf-16-be"])
    last_error: Exception | None = None
    seen: set[str] = set()
    for enc in encodings:
        if enc in seen or enc is None:
            continue
        seen.add(enc)
        try:
            return json.loads(path.read_text(encoding=enc))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    raise RuntimeError(f"Failed to load JSON from {path}") from last_error


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_node_map(path: Path, id_key: str, name_key: str) -> dict[str, str]:
    return {row[id_key]: row.get(name_key, "") for row in read_csv(path)}


def build_edge_map(path: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for row in read_csv(path):
        out[row["source_id"]].append(row["target_id"])
    return out


def format_preview(values: list[str], limit: int = 4) -> str:
    if not values:
        return ""
    preview = values[:limit]
    if len(values) > limit:
        preview.append(f"...(+{len(values) - limit})")
    return "; ".join(preview)


def evidence_score(row: dict) -> int:
    return sum(
        int(bool(row[key]))
        for key in [
            "organisms",
            "monosaccharides",
            "bonds",
            "diseases",
            "publications",
        ]
    )


def main() -> None:
    clean = load_json(EXPERIMENT_DIR / "clean_case_records_seed42.json")
    ontology_seed = load_json(REPO_ROOT / "experiments" / "ontology_stability_runs" / "ontology_seed11.json", encoding="utf-16")
    baseline_seed = load_json(REPO_ROOT / "experiments" / "ontology_stability_runs" / "baseline_seed11.json", encoding="utf-16")
    stability = load_json(REPO_ROOT / "experiments" / "ontology_stability_runs" / "ontology_stability_summary.json")

    poly_name = build_node_map(KG_DIR / "nodes" / "polysaccharide.csv", "poly_id", "name")
    organism_name = build_node_map(KG_DIR / "nodes" / "organism.csv", "organism_id", "organism_name_norm")
    mono_name = build_node_map(KG_DIR / "nodes" / "monosaccharide.csv", "monosaccharide_id", "mono_name_norm")
    bond_name = build_node_map(KG_DIR / "nodes" / "glycosidic_bond.csv", "bond_id", "bond_signature")
    disease_name = build_node_map(KG_DIR / "nodes" / "disease.csv", "disease_id", "disease_name_norm")
    publication_name = build_node_map(KG_DIR / "nodes" / "publication.csv", "doi", "doi")

    poly_to_org = build_edge_map(KG_DIR / "edges" / "poly_organism.csv")
    poly_to_mono = build_edge_map(KG_DIR / "edges" / "poly_monosaccharide.csv")
    poly_to_bond = build_edge_map(KG_DIR / "edges" / "poly_bond.csv")
    poly_to_disease = build_edge_map(KG_DIR / "edges" / "poly_disease.csv")
    poly_to_pub = build_edge_map(KG_DIR / "edges" / "poly_publication.csv")

    clean_examples = {
        (row["poly_id"], row["held_out_function_id"]): row
        for row in clean.get("examples", [])
    }
    ontology_examples = {
        (row["poly_id"], row["held_out_function_id"]): row
        for row in ontology_seed.get("examples", [])
    }
    rescue_counter: Counter[tuple[str, str]] = Counter()
    rescue_example_key_to_seed: dict[tuple[str, str], int] = {}
    rescue_record_by_key: dict[tuple[str, str], tuple[dict, dict]] = {}
    for seed_summary in stability["seed_summaries"]:
        seed = seed_summary["seed"]
        baseline_path = REPO_ROOT / "experiments" / "ontology_stability_runs" / f"baseline_seed{seed}.json"
        ontology_path = REPO_ROOT / "experiments" / "ontology_stability_runs" / f"ontology_seed{seed}.json"
        baseline_payload = load_json(baseline_path, encoding="utf-16")
        ontology_payload = load_json(ontology_path, encoding="utf-16")
        base_records = {
            (row["poly_id"], row["positive_function_id"]): row
            for row in baseline_payload.get("edge_records", [])
        }
        onto_records = {
            (row["poly_id"], row["positive_function_id"]): row
            for row in ontology_payload.get("edge_records", [])
        }
        for key, base_row in base_records.items():
            onto_row = onto_records.get(key)
            if onto_row is None:
                continue
            base_rank = base_row["filtered_ranks"].get("meta_path_knn_disease_conditioned_vote_freq_prior")
            onto_rank = onto_row["filtered_ranks"].get("meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native")
            if base_rank is None or onto_rank is None:
                continue
            if base_rank > 3 and onto_rank <= 3:
                rescue_counter[key] += 1
                rescue_example_key_to_seed.setdefault(key, seed)
                rescue_record_by_key.setdefault(key, (base_row, onto_row))

    candidates: list[dict] = []

    for row in clean.get("edge_records", []):
        clean_rank = row["filtered_ranks"].get("meta_path_knn")
        if clean_rank is None:
            continue
        key = (row["poly_id"], row["positive_function_id"])
        category = None
        if clean_rank <= 3:
            category = "clean_success"
        elif clean_rank > 10:
            category = "clean_failure"
        else:
            continue
        example = clean_examples.get((row["poly_id"], row["positive_function_id"])) or clean_examples.get(
            (row["poly_id"], row.get("held_out_function_id", ""))
        )
        orgs = [organism_name.get(v, v) for v in poly_to_org.get(row["poly_id"], [])]
        monos = [mono_name.get(v, v) for v in poly_to_mono.get(row["poly_id"], [])]
        bonds = [bond_name.get(v, v) for v in poly_to_bond.get(row["poly_id"], [])]
        diseases = [disease_name.get(v, v) for v in poly_to_disease.get(row["poly_id"], [])]
        pubs = [publication_name.get(v, v) for v in poly_to_pub.get(row["poly_id"], [])]
        candidate = {
            "category": category,
            "poly_id": row["poly_id"],
            "poly_name": poly_name.get(row["poly_id"], ""),
            "function_id": row["positive_function_id"],
            "function_name": row["positive_function_name"],
            "stratum": row["stratum"],
            "train_support": row["train_support"],
            "clean_filtered_rank": clean_rank,
            "baseline_filtered_rank": "",
            "ontology_filtered_rank": "",
            "rescue_count_16seeds": "",
            "top5_predictions": json.dumps(example.get("top5_predictions", []), ensure_ascii=False) if example else "",
            "organisms": format_preview(orgs),
            "monosaccharides": format_preview(monos),
            "bonds": format_preview(bonds),
            "diseases": format_preview(diseases),
            "publications": format_preview(pubs),
        }
        candidate["evidence_score"] = evidence_score(candidate)
        candidates.append(candidate)

    for key, count in rescue_counter.items():
        base_row, onto_row = rescue_record_by_key[key]
        example_seed = rescue_example_key_to_seed[key]
        example_payload = load_json(
            REPO_ROOT / "experiments" / "ontology_stability_runs" / f"ontology_seed{example_seed}.json",
            encoding="utf-16",
        )
        example_map = {
            (row["poly_id"], row["held_out_function_id"]): row
            for row in example_payload.get("examples", [])
        }
        example = example_map.get(key)
        base_rank = base_row["filtered_ranks"].get("meta_path_knn_disease_conditioned_vote_freq_prior")
        onto_rank = onto_row["filtered_ranks"].get("meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native")
        orgs = [organism_name.get(v, v) for v in poly_to_org.get(base_row["poly_id"], [])]
        monos = [mono_name.get(v, v) for v in poly_to_mono.get(base_row["poly_id"], [])]
        bonds = [bond_name.get(v, v) for v in poly_to_bond.get(base_row["poly_id"], [])]
        diseases = [disease_name.get(v, v) for v in poly_to_disease.get(base_row["poly_id"], [])]
        pubs = [publication_name.get(v, v) for v in poly_to_pub.get(base_row["poly_id"], [])]
        candidate = {
            "category": "ontology_rescue",
            "poly_id": base_row["poly_id"],
            "poly_name": poly_name.get(base_row["poly_id"], ""),
            "function_id": base_row["positive_function_id"],
            "function_name": base_row["positive_function_name"],
            "stratum": base_row["stratum"],
            "train_support": base_row["train_support"],
            "clean_filtered_rank": "",
            "baseline_filtered_rank": base_rank,
            "ontology_filtered_rank": onto_rank,
            "rescue_count_16seeds": count,
            "top5_predictions": json.dumps(example.get("top5_predictions", []), ensure_ascii=False) if example else "",
            "organisms": format_preview(orgs),
            "monosaccharides": format_preview(monos),
            "bonds": format_preview(bonds),
            "diseases": format_preview(diseases),
            "publications": format_preview(pubs),
        }
        candidate["evidence_score"] = evidence_score(candidate)
        candidates.append(candidate)

    for base_row in baseline_seed.get("edge_records", []):
        key = (base_row["poly_id"], base_row["positive_function_id"])
        onto_row = next(
            (
                row
                for row in ontology_seed.get("edge_records", [])
                if row["poly_id"] == base_row["poly_id"] and row["positive_function_id"] == base_row["positive_function_id"]
            ),
            None,
        )
        if onto_row is None:
            continue
        base_rank = base_row["filtered_ranks"].get("meta_path_knn_disease_conditioned_vote_freq_prior")
        onto_rank = onto_row["filtered_ranks"].get("meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native")
        if base_rank is None or onto_rank is None:
            continue
        if base_rank > 10 and onto_rank > 10:
            category = "ontology_failure"
        else:
            continue
        example = ontology_examples.get((base_row["poly_id"], base_row["positive_function_id"]))
        orgs = [organism_name.get(v, v) for v in poly_to_org.get(base_row["poly_id"], [])]
        monos = [mono_name.get(v, v) for v in poly_to_mono.get(base_row["poly_id"], [])]
        bonds = [bond_name.get(v, v) for v in poly_to_bond.get(base_row["poly_id"], [])]
        diseases = [disease_name.get(v, v) for v in poly_to_disease.get(base_row["poly_id"], [])]
        pubs = [publication_name.get(v, v) for v in poly_to_pub.get(base_row["poly_id"], [])]
        candidate = {
            "category": category,
            "poly_id": base_row["poly_id"],
            "poly_name": poly_name.get(base_row["poly_id"], ""),
            "function_id": base_row["positive_function_id"],
            "function_name": base_row["positive_function_name"],
            "stratum": base_row["stratum"],
            "train_support": base_row["train_support"],
            "clean_filtered_rank": "",
            "baseline_filtered_rank": base_rank,
            "ontology_filtered_rank": onto_rank,
            "rescue_count_16seeds": rescue_counter.get(key, 0),
            "top5_predictions": json.dumps(example.get("top5_predictions", []), ensure_ascii=False) if example else "",
            "organisms": format_preview(orgs),
            "monosaccharides": format_preview(monos),
            "bonds": format_preview(bonds),
            "diseases": format_preview(diseases),
            "publications": format_preview(pubs),
        }
        candidate["evidence_score"] = evidence_score(candidate)
        candidates.append(candidate)

    candidates.sort(
        key=lambda row: (
            {"ontology_rescue": 0, "clean_success": 1, "ontology_failure": 2, "clean_failure": 3}.get(row["category"], 9),
            -int(row["rescue_count_16seeds"] or 0),
            -int(row["evidence_score"]),
            int(row["baseline_filtered_rank"] or row["clean_filtered_rank"] or 999),
        )
    )

    csv_path = EXPERIMENT_DIR / "case_study_candidates.csv"
    fieldnames = [
        "category",
        "poly_id",
        "poly_name",
        "function_id",
        "function_name",
        "stratum",
        "train_support",
        "clean_filtered_rank",
        "baseline_filtered_rank",
        "ontology_filtered_rank",
        "rescue_count_16seeds",
        "evidence_score",
        "organisms",
        "monosaccharides",
        "bonds",
        "diseases",
        "publications",
        "top5_predictions",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidates)

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in candidates:
        grouped[row["category"]].append(row)

    md_lines = [
        "# Case Study Candidate Pool",
        "",
        "This file groups candidate cases for biology-facing case studies. Candidates are screened from the clean masked-link benchmark and the paired ontology stability runs, then enriched with KG evidence previews.",
        "",
    ]
    for category in ["ontology_rescue", "clean_success", "ontology_failure", "clean_failure"]:
        rows = grouped.get(category, [])[:8]
        md_lines.append(f"## {category}")
        md_lines.append("")
        if not rows:
            md_lines.append("No candidates found.")
            md_lines.append("")
            continue
        for idx, row in enumerate(rows, start=1):
            md_lines.append(
                (
                    f"{idx}. `{row['poly_id']}` / `{row['function_name']}` / stratum `{row['stratum']}` / "
                    f"support `{row['train_support']}` / evidence `{row['evidence_score']}` / "
                    f"clean `{row['clean_filtered_rank'] or '-'}` / "
                    f"baseline `{row['baseline_filtered_rank'] or '-'}` / "
                    f"ontology `{row['ontology_filtered_rank'] or '-'}` / "
                    f"rescue16 `{row['rescue_count_16seeds'] or '-'}`"
                )
            )
            if row["organisms"]:
                md_lines.append(f"   organisms: {row['organisms']}")
            if row["monosaccharides"]:
                md_lines.append(f"   monosaccharides: {row['monosaccharides']}")
            if row["bonds"]:
                md_lines.append(f"   bonds: {row['bonds']}")
            if row["diseases"]:
                md_lines.append(f"   diseases: {row['diseases']}")
            if row["publications"]:
                md_lines.append(f"   publications: {row['publications']}")
        md_lines.append("")

    (EXPERIMENT_DIR / "case_study_candidates.md").write_text("\n".join(md_lines), encoding="utf-8")
    summary = {
        "csv": str(csv_path),
        "markdown": str(EXPERIMENT_DIR / "case_study_candidates.md"),
        "counts": {category: len(rows) for category, rows in grouped.items()},
    }
    (EXPERIMENT_DIR / "case_study_candidates_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
