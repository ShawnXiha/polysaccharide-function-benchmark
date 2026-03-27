"""Simple normalization helpers for dataset v0."""

from __future__ import annotations


def normalize_record(record: dict) -> dict:
    """Apply minimal normalization without overwriting raw fields."""
    normalized = dict(record)
    normalized["source_db"] = str(normalized["source_db"]).strip()
    normalized["source_record_id"] = str(normalized["source_record_id"]).strip()
    normalized["poly_id"] = str(normalized["poly_id"]).strip()
    normalized["canonical_representation"] = str(
        normalized["canonical_representation"]
    ).strip()
    normalized["evidence_type"] = str(normalized["evidence_type"]).strip().lower()
    if isinstance(normalized.get("function_label"), str):
        normalized["function_label"] = [normalized["function_label"]]
    return normalized
