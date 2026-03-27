"""Schema definitions and validation helpers."""

from __future__ import annotations

from dataclasses import dataclass


REQUIRED_FIELDS = [
    "poly_id",
    "source_db",
    "source_record_id",
    "raw_representation",
    "canonical_representation",
    "function_label",
    "evidence_type",
    "doi",
    "license",
]

RECOMMENDED_FIELDS = [
    "monomer_composition",
    "linkage",
    "branching",
    "modification",
    "mw_or_range",
    "organism_source",
]

VALID_EVIDENCE_TYPES = {"in_vitro", "animal", "clinical", "unknown"}


@dataclass
class ValidationIssue:
    level: str
    field: str
    message: str


def validate_record(record: dict) -> list[ValidationIssue]:
    """Validate a single record against schema v0."""
    issues: list[ValidationIssue] = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            issues.append(ValidationIssue("error", field, "missing required field"))
        elif record[field] in (None, ""):
            issues.append(ValidationIssue("error", field, "required field is empty"))

    evidence_type = record.get("evidence_type")
    if evidence_type and evidence_type not in VALID_EVIDENCE_TYPES:
        issues.append(
            ValidationIssue(
                "error",
                "evidence_type",
                f"invalid evidence_type '{evidence_type}'",
            )
        )

    function_label = record.get("function_label")
    if function_label is not None and not isinstance(function_label, (list, str)):
        issues.append(
            ValidationIssue(
                "error",
                "function_label",
                "function_label must be string or list",
            )
        )

    for field in RECOMMENDED_FIELDS:
        if field not in record:
            issues.append(ValidationIssue("warning", field, "recommended field missing"))

    return issues
