"""Manifest loading helpers."""

from __future__ import annotations

from pathlib import Path

import yaml

from polysaccharidesdb.paths import ROOT


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)
    return manifest


def resolve_manifest_path(path_str: str) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        return path
    return ROOT / path
