"""Feature schema builders for KG exports."""

from __future__ import annotations


def build_poly_feature_schema(mono_ids: list[str], bond_ids: list[str], include_disease_features: bool) -> list[dict]:
    """Return ordered polysaccharide feature metadata for reproducible exports."""
    schema: list[dict] = [
        {
            "name": "degree__organism",
            "source_relation": "poly_organism",
            "disease_derived": False,
        },
        {
            "name": "degree__monosaccharide",
            "source_relation": "poly_monosaccharide",
            "disease_derived": False,
        },
        {
            "name": "degree__glycosidic_bond",
            "source_relation": "poly_bond",
            "disease_derived": False,
        },
        {
            "name": "degree__publication",
            "source_relation": "poly_publication",
            "disease_derived": False,
        },
    ]
    if include_disease_features:
        schema.append(
            {
                "name": "degree__disease",
                "source_relation": "poly_disease",
                "disease_derived": True,
            }
        )
    schema.extend(
        [
            {
                "name": "mw_signal",
                "source_field": "mw_or_range_raw",
                "disease_derived": False,
            },
            {
                "name": "branching__has_text",
                "source_field": "branching_raw",
                "disease_derived": False,
            },
            {
                "name": "branching__no_relevant_information",
                "source_field": "branching_raw",
                "disease_derived": False,
            },
            {
                "name": "branching__text_length_capped",
                "source_field": "branching_raw",
                "disease_derived": False,
            },
        ]
    )
    schema.extend(
        {
            "name": f"monosaccharide_ratio__{mono_id}",
            "source_relation": "poly_monosaccharide",
            "source_node_id": mono_id,
            "disease_derived": False,
        }
        for mono_id in mono_ids
    )
    schema.extend(
        {
            "name": f"bond_presence__{bond_id}",
            "source_relation": "poly_bond",
            "source_node_id": bond_id,
            "disease_derived": False,
        }
        for bond_id in bond_ids
    )
    return schema

