"""Function-label normalization helpers."""

from __future__ import annotations

import re


CANONICAL_PATTERNS: list[tuple[str, list[str]]] = [
    ("immunomodulatory", [r"immunoregulation", r"immunomodulat"]),
    ("antioxidant", [r"anti[\-\s_]?oxid", r"\babts\b", r"\bdpph\b"]),
    ("antitumor", [r"anti[\-\s_]?tumou?r", r"anti[\-\s_]?cancer"]),
    ("antidiabetic", [r"anti[\-\s_]?diabet", r"insulin", r"glycemic"]),
    ("antiinflammatory", [r"anti[\-\s_]?inflamm", r"\binflammatory\b"]),
    ("microbiota_regulation", [r"microbiota", r"microbiome", r"gut flora"]),
    ("antimicrobial", [r"anti[\-\s_]?microbial", r"antibacterial", r"antifungal"]),
    ("antiaging", [r"anti[\-\s_]?aging", r"antiage"]),
    ("antifatigue", [r"anti[\-\s_]?fatigue"]),
    ("anticoagulant", [r"anti[\-\s_]?coagulation", r"anticoagul"]),
    ("antiviral", [r"antiviral", r"\btmv\b", r"viral"]),
    ("neuroprotective", [r"neurological", r"neuroprotect"]),
    ("organ_protective", [r"organ protection", r"organ[_\s\-]?protect", r"hepatoprotect", r"renoprotect"]),
    ("antiobesity", [r"anti[\-\s_]?obes", r"preventing obesity"]),
    ("lipid_lowering", [r"anti[\-\s_]?hyperlipidem", r"lipid lowering"]),
    ("cholesterol_lowering", [r"anti[\-\s_]?hypercholester", r"cholesterol lowering"]),
    ("antihypoxic", [r"anti[\-\s_]?hypoxia", r"antihypox"]),
    ("radioprotective", [r"anti[\-\s_]?radiation", r"radioprotect"]),
    ("antiproliferative", [r"anti[\-\s_]?proliferation", r"antiprolifer"]),
    ("moisture_absorption", [r"moisture absorption"]),
    ("anemia_improving", [r"improving anemia", r"reducing inflammatory damage"]),
    ("antinociceptive", [r"anti[\-\s_]?nociceptive"]),
    ("anticomplement", [r"anticomplement"]),
    ("osteogenic", [r"osteogenic", r"bone quality"]),
    ("angiogenesis_inhibition", [r"anti[\-\s_]?angiogenic", r"angiogenesis inhibitor", r"microvascular"]),
    ("drug_delivery", [r"drug delivery", r"drug carrier", r"delivery carrier", r"gene therapy", r"tissue engineering"]),
    ("emulsifying", [r"emulsif", r"stabilizer", r"thickening", r"gelling", r"film[-\s_]?forming"]),
    ("plant_defense", [r"defense responses", r"plant protectant", r"pathogens", r"biostimulant"]),
    ("whitening", [r"whitening"]),
    ("reproductive_support", [r"recurrent spontaneous abortion"]),
]


def slugify_label(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return re.sub(r"_+", "_", value)


def normalize_function_labels(raw_value: str) -> list[str]:
    text = (raw_value or "").strip().lower()
    if not text:
        return ["unknown"]

    # Remove measurement-heavy parentheses before token detection.
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("_", " ")
    text = text.replace(";", " ").replace(",", " ")
    text = text.replace("|", " ").replace("/", " ")
    text = re.sub(r"\s+", " ", text).strip()

    labels: list[str] = []
    for canonical, patterns in CANONICAL_PATTERNS:
        if any(re.search(pattern, text) for pattern in patterns):
            labels.append(canonical)

    if labels:
        return sorted(set(labels))

    if len(text) > 80:
        return ["unknown"]
    if len(text.split()) > 6:
        return ["unknown"]
    fallback = slugify_label(text)
    if not fallback or len(fallback) > 48:
        return ["unknown"]
    return [fallback]
