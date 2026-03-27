"""Evidence-aware utilities for Stage 3 methods."""

from __future__ import annotations

import re


_MISSING_PATTERNS = (
    "",
    "unknown",
    "none",
    "na",
    "n/a",
    "not available",
    "not reported",
    "not provided",
    "no relevant information could be found in the literature.",
)


def _normalize_text(value: object) -> str:
    return str(value or "").strip().lower()


def is_informative_text(value: object) -> bool:
    text = _normalize_text(value)
    if not text:
        return False
    return text not in _MISSING_PATTERNS


def parse_mw_value(value: object) -> float | None:
    text = str(value or "").strip().lower().replace("脳", "x")
    if not text:
        return None

    sci_match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*x\s*10\s*([0-9]+)", text)
    if sci_match:
        base = float(sci_match.group(1))
        exponent = int(sci_match.group(2))
        return base * (10**exponent)

    number_match = re.search(r"([0-9]+(?:\.[0-9]+)?)", text)
    if not number_match:
        return None

    value_num = float(number_match.group(1))
    if "mda" in text:
        return value_num * 1_000_000
    if "kda" in text:
        return value_num * 1_000
    if "da" in text:
        return value_num
    return value_num


def mw_bucket(value: object) -> str:
    mw = parse_mw_value(value)
    if mw is None:
        return "mw_unknown"
    if mw < 10_000:
        return "mw_lt_10k"
    if mw < 100_000:
        return "mw_10k_100k"
    if mw < 1_000_000:
        return "mw_100k_1m"
    return "mw_ge_1m"


def extract_residue_tokens(record: dict) -> list[str]:
    text = " ".join(
        str(record.get(field, ""))
        for field in ("monomer_composition", "linkage", "branching", "canonical_representation")
    ).lower()
    residue_map = {
        "glucose": "res_glc",
        "glcp": "res_glc",
        "galactose": "res_gal",
        "galp": "res_gal",
        "galacturonic acid": "res_gala",
        "gala": "res_gala",
        "mannose": "res_man",
        "manp": "res_man",
        "arabinose": "res_ara",
        "araf": "res_ara",
        "arap": "res_ara",
        "rhamnose": "res_rha",
        "rhap": "res_rha",
        "fucose": "res_fuc",
        "fucp": "res_fuc",
        "xylose": "res_xyl",
        "xylp": "res_xyl",
        "glucuronic acid": "res_glca",
        "glca": "res_glca",
    }
    found = {token for pattern, token in residue_map.items() if pattern in text}
    return sorted(found)


def polysaccharide_feature_tokens(
    record: dict,
    include_mw: bool = True,
    include_branching: bool = True,
    include_modification: bool = True,
    include_residue: bool = True,
    include_source_kingdom: bool = True,
    include_composition_terms: bool = True,
) -> list[str]:
    tokens: list[str] = []
    if include_mw:
        tokens.append(mw_bucket(record.get("mw_or_range", "")))

    branching_text = record.get("branching", "")
    if include_branching:
        if is_informative_text(branching_text):
            tokens.append("branching_known")
        else:
            tokens.append("branching_missing")

    modification_text = str(record.get("modification", "")).lower()
    if include_modification:
        if is_informative_text(modification_text):
            tokens.append("mod_known")
            if "sulf" in modification_text:
                tokens.append("mod_sulfated")
            if "acet" in modification_text:
                tokens.append("mod_acetylated")
            if "phosph" in modification_text:
                tokens.append("mod_phosphorylated")
        else:
            tokens.append("mod_missing")

    mono_text = str(record.get("monomer_composition", ""))
    residue_tokens = extract_residue_tokens(record) if include_residue else []
    if include_residue:
        tokens.extend(residue_tokens)
        if residue_tokens:
            tokens.append(f"residue_diversity_{min(len(residue_tokens), 6)}")

    percentage_count = len(re.findall(r"\d+(?:\.\d+)?%", mono_text))
    if include_composition_terms and percentage_count:
        tokens.append(f"composition_terms_{min(percentage_count, 6)}")

    org_text = str(record.get("organism_source", "")).lower()
    if include_source_kingdom:
        if any(term in org_text for term in ("fung", "mushroom", "myce")):
            tokens.append("source_kingdom_fungi")
        elif any(term in org_text for term in ("alga", "seaweed")):
            tokens.append("source_kingdom_algae")
        elif org_text:
            tokens.append("source_kingdom_other")

    return sorted(set(tokens))


def evidence_feature_tokens(record: dict) -> list[str]:
    tokens: list[str] = []
    doi_known = is_informative_text(record.get("doi", ""))
    tokens.append("doi_known" if doi_known else "doi_missing")

    for field, short_name in (
        ("monomer_composition", "mono"),
        ("linkage", "link"),
        ("branching", "branch"),
        ("modification", "mod"),
        ("mw_or_range", "mw"),
        ("organism_source", "org"),
    ):
        tokens.append(f"{short_name}_{'known' if is_informative_text(record.get(field, '')) else 'missing'}")

    return tokens


def structural_completeness_score(record: dict) -> float:
    checks = [
        is_informative_text(record.get("doi", "")),
        is_informative_text(record.get("monomer_composition", "")),
        is_informative_text(record.get("linkage", "")),
        is_informative_text(record.get("branching", "")),
        is_informative_text(record.get("modification", "")),
        is_informative_text(record.get("mw_or_range", "")),
        is_informative_text(record.get("organism_source", "")),
    ]
    return sum(1.0 for flag in checks if flag) / len(checks)


def evidence_sample_weight(record: dict) -> float:
    completeness = structural_completeness_score(record)
    label_count = max(1, len(record.get("function_label", [])))
    weight = 0.75 + 0.75 * completeness
    if label_count > 1:
        weight += 0.05
    return round(weight, 4)
