"""Pure graph-feature helpers shared by graph baselines and tests."""

from __future__ import annotations


TOKENS = [
    "monomer_composition",
    "linkage",
    "branching",
    "modification",
    "mw_or_range",
    "organism_source",
]


def build_vocab(records: list[dict]) -> dict[str, int]:
    """Build a graph-token vocabulary from training records only."""
    vocab = {"<unk>": 0}
    for record in records:
        root_token = f"repr={record.get('canonical_representation', '')}"
        if root_token not in vocab:
            vocab[root_token] = len(vocab)
        for field in TOKENS:
            token = f"{field}={record.get(field, '')}"
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab
