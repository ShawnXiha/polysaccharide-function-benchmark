"""Dataset helpers for early baselines."""

from __future__ import annotations

from polysaccharidesdb.etl.loaders import load_jsonl


def load_dataset(path) -> list[dict]:
    return load_jsonl(path)


def index_by_poly_id(records: list[dict]) -> dict[str, dict]:
    return {record["poly_id"]: record for record in records}
