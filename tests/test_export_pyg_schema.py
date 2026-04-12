from polysaccharidesgraph.kg.feature_schema import build_poly_feature_schema


def test_clean_poly_schema_has_no_disease_features() -> None:
    schema = build_poly_feature_schema(
        mono_ids=["mono:a", "mono:b"],
        bond_ids=["bond:x"],
        include_disease_features=False,
    )
    assert all(not item.get("disease_derived") for item in schema)
    assert "degree__disease" not in {item["name"] for item in schema}


def test_disease_aware_poly_schema_marks_disease_feature() -> None:
    schema = build_poly_feature_schema(
        mono_ids=["mono:a"],
        bond_ids=["bond:x"],
        include_disease_features=True,
    )
    disease_features = [item for item in schema if item.get("disease_derived")]
    assert [item["name"] for item in disease_features] == ["degree__disease"]
