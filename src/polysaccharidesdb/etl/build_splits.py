"""Generate deterministic split files for benchmark datasets."""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

from polysaccharidesdb.etl.loaders import load_jsonl
from polysaccharidesdb.paths import DATA_PROCESSED


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build deterministic dataset splits")
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_PROCESSED / "dataset_v0.jsonl",
        help="Dataset JSONL file",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DATA_PROCESSED / "splits",
        help="Directory to store split files",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--train-frac", type=float, default=0.6, help="Train fraction for random split")
    parser.add_argument("--valid-frac", type=float, default=0.2, help="Validation fraction for random split")
    return parser.parse_args()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def build_random_split(poly_ids: list[str], rng: random.Random, train_frac: float, valid_frac: float) -> dict:
    shuffled = poly_ids[:]
    rng.shuffle(shuffled)
    n = len(shuffled)
    train_end = max(1, int(train_frac * n))
    valid_end = max(train_end + 1, int((train_frac + valid_frac) * n))
    valid_end = min(valid_end, n - 1) if n >= 3 else valid_end
    return {
        "train": shuffled[:train_end],
        "valid": shuffled[train_end:valid_end],
        "test": shuffled[valid_end:],
    }


def informative_group_value(value: object) -> str | None:
    text = str(value or "").strip().lower()
    if not text or text in {"unknown", "unfound", "none", "na", "n/a", "not found"}:
        return None
    return text


def build_grouped_split(
    records: list[dict],
    rng: random.Random,
    train_frac: float,
    valid_frac: float,
    group_field: str,
) -> dict:
    groups: dict[str, list[str]] = defaultdict(list)
    for record in records:
        group_value = informative_group_value(record.get(group_field))
        if group_value is None:
            # Treat unknown group values as record-specific groups to avoid creating
            # an artificial giant cluster such as "unfound".
            group_value = f"singleton::{record['poly_id']}"
        groups[group_value].append(record["poly_id"])

    group_keys = list(groups.keys())
    rng.shuffle(group_keys)

    total_records = len(records)
    target_train = int(train_frac * total_records)
    target_valid = int(valid_frac * total_records)

    train_ids: list[str] = []
    valid_ids: list[str] = []
    test_ids: list[str] = []
    valid_group_buckets: list[list[str]] = []

    for group_key in group_keys:
        bucket = groups[group_key]
        if len(train_ids) < target_train:
            train_ids.extend(bucket)
        elif len(valid_ids) < target_valid:
            valid_ids.extend(bucket)
            valid_group_buckets.append(bucket)
        else:
            test_ids.extend(bucket)

    # If greedy assignment produced an empty test partition, move the last valid group.
    if not test_ids and valid_group_buckets:
        spill = valid_group_buckets.pop()
        valid_ids = [poly_id for poly_id in valid_ids if poly_id not in set(spill)]
        test_ids.extend(spill)

    return {
        "group_field": group_field,
        "train": train_ids,
        "valid": valid_ids,
        "test": test_ids,
    }


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    records = load_jsonl(args.input)
    poly_ids = [record["poly_id"] for record in records]

    random_split = build_random_split(
        poly_ids=poly_ids,
        rng=rng,
        train_frac=args.train_frac,
        valid_frac=args.valid_frac,
    )
    write_json(args.output_dir / "random_split.json", random_split)

    doi_grouped_split = build_grouped_split(
        records=records,
        rng=random.Random(args.seed),
        train_frac=args.train_frac,
        valid_frac=args.valid_frac,
        group_field="doi",
    )
    write_json(args.output_dir / "doi_grouped_split.json", doi_grouped_split)

    source_groups: dict[str, list[str]] = defaultdict(list)
    genus_groups: dict[str, list[str]] = defaultdict(list)
    for record in records:
        source_groups[record["source_db"]].append(record["poly_id"])
        organism_source = record.get("organism_source", "unknown")
        genus = str(organism_source).split("_")[0]
        genus_groups[genus].append(record["poly_id"])

    source_splits = []
    for source_db, held_out in sorted(source_groups.items()):
        train = [poly_id for poly_id in poly_ids if poly_id not in held_out]
        source_splits.append({"held_out_source": source_db, "train": train, "test": held_out})
    write_json(args.output_dir / "leave_one_source_out.json", {"splits": source_splits})

    genus_splits = []
    for genus, held_out in sorted(genus_groups.items()):
        train = [poly_id for poly_id in poly_ids if poly_id not in held_out]
        genus_splits.append({"held_out_genus": genus, "train": train, "test": held_out})
    write_json(args.output_dir / "leave_one_genus_out.json", {"splits": genus_splits})

    print(f"Wrote split files to {args.output_dir}")


if __name__ == "__main__":
    main()
