"""Source-specific normalization for real exported files."""

from __future__ import annotations

from polysaccharidesdb.etl.label_normalization import normalize_function_labels
from polysaccharidesdb.etl.loaders import load_csv


def split_labels(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


def normalize_common_record(record: dict, source_name: str) -> dict:
    raw_function_value = record.get("function_label", "").strip()
    normalized = {
        "poly_id": f"{source_name.lower()}::{record.get('source_record_id', '').strip()}",
        "source_db": source_name,
        "source_record_id": record.get("source_record_id", "").strip(),
        "raw_representation": record.get("raw_representation", "").strip(),
        "canonical_representation": record.get("canonical_representation", "").strip(),
        "monomer_composition": record.get("monomer_composition", "").strip(),
        "linkage": record.get("linkage", "").strip(),
        "branching": record.get("branching", "").strip(),
        "modification": record.get("modification", "").strip(),
        "mw_or_range": record.get("mw_or_range", "").strip(),
        "organism_source": record.get("organism_source", "").strip(),
        "function_label": normalize_function_labels(raw_function_value),
        "function_label_raw": split_labels(raw_function_value),
        "evidence_type": record.get("evidence_type", "").strip().lower(),
        "doi": record.get("doi", "").strip(),
        "license": record.get("license", "").strip(),
    }
    return normalized


def load_dolphin_export(path) -> list[dict]:
    return [normalize_common_record(record, "DoLPHiN") for record in load_csv(path)]


def load_csdb_export(path) -> list[dict]:
    return [normalize_common_record(record, "CSDB") for record in load_csv(path)]


def load_glytoucan_mapping(path) -> list[dict]:
    records = []
    for record in load_csv(path):
        records.append(
            {
                "source_db": "GlyTouCan",
                "source_record_id": record.get("source_record_id", "").strip(),
                "glytoucan_id": record.get("glytoucan_id", "").strip(),
                "canonical_representation": record.get("canonical_representation", "").strip(),
                "wurcs": record.get("wurcs", "").strip(),
                "license": record.get("license", "").strip(),
            }
        )
    return records
