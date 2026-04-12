"""Normalization helpers for DoLPHiN-derived records."""

from __future__ import annotations

import hashlib
import re
from typing import Iterable


def stable_id(prefix: str, value: str) -> str:
    """Build a stable compact id from normalized text."""
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}:{digest}"


def clean_text(value: str | None) -> str:
    text = (value or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def split_semicolon(value: str | None) -> list[str]:
    text = clean_text(value)
    if not text:
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def normalize_function(value: str) -> str:
    text = clean_text(value).lower()
    mapping = {
        "immunoregulation": "immunomodulatory",
        "anti-tumour": "antitumor",
        "anti-tumor": "antitumor",
        "anti-oxidant": "antioxidant",
    }
    return mapping.get(text, text.replace(" ", "_"))


def split_diseases(value: str | None) -> list[str]:
    text = clean_text(value)
    if not text:
        return []
    normalized = text.replace(";", ",")
    normalized = re.sub(r"\s*,\s*", ",", normalized)
    return [part.strip() for part in normalized.split(",") if part.strip()]


def extract_disease_code(value: str) -> str:
    text = clean_text(value)
    match = re.match(r"^([A-Z0-9./-]+)-", text)
    if not match:
        return ""
    return match.group(1)


_MONO_RE = re.compile(r"^\s*([A-Za-z][A-Za-z\- ]*?)\s+([0-9]+(?:\.[0-9]+)?)%\s*$")


def parse_monomer_composition(value: str | None) -> list[tuple[str, float]]:
    parsed: list[tuple[str, float]] = []
    for part in split_semicolon(value):
        match = _MONO_RE.match(part)
        if not match:
            continue
        name = clean_text(match.group(1)).lower()
        ratio = float(match.group(2))
        parsed.append((name, ratio))
    return parsed


def normalize_bond(value: str) -> str:
    text = clean_text(value)
    replacements = {
        "¦Б": "alpha",
        "¦В": "beta",
        "Ўъ": "->",
        "鈫?": "->",
        "尾-": "",
        "伪-": "",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return clean_text(text)


def unique_preserve_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered
