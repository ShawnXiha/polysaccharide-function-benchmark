"""Shared feature rendering for lightweight baselines."""

from __future__ import annotations


def record_to_feature_text(record: dict) -> str:
    parts = [
        f"repr={record.get('canonical_representation', '')}",
        f"mono={record.get('monomer_composition', '')}",
        f"link={record.get('linkage', '')}",
        f"branch={record.get('branching', '')}",
        f"mod={record.get('modification', '')}",
        f"mw={record.get('mw_or_range', '')}",
        f"src={record.get('source_db', '')}",
        f"org={record.get('organism_source', '')}",
    ]
    return " ".join(parts)
