"""Helpers for split file formats."""

from __future__ import annotations


def expand_split_payload(split_payload: dict, eval_key: str = "test") -> list[dict]:
    """Return normalized split definitions from a payload.

    Parameters
    ----------
    split_payload:
        JSON payload describing one or more splits.
    eval_key:
        Which partition to evaluate on. For standard train/valid/test payloads this
        is usually ``"valid"`` during development and ``"test"`` for final reporting.
    """
    if "train" in split_payload and eval_key in split_payload:
        normalized = {
            "name": "default",
            "train": split_payload["train"],
            "test": split_payload[eval_key],
        }
        if "valid" in split_payload:
            normalized["valid"] = split_payload["valid"]
        return [normalized]

    if "splits" in split_payload:
        normalized = []
        for idx, item in enumerate(split_payload["splits"], start=1):
            name = item.get("held_out_source") or item.get("held_out_genus") or f"split_{idx}"
            if eval_key not in item:
                raise ValueError(f"Requested eval partition '{eval_key}' missing in split '{name}'")
            normalized.append(
                {
                    "name": name,
                    "train": item["train"],
                    "test": item[eval_key],
                    "valid": item.get("valid", []),
                }
            )
        return normalized

    raise ValueError("Unsupported split payload format")
