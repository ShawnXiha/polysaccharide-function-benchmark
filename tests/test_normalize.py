from polysaccharidesgraph.kg.normalize import (
    normalize_bond,
    normalize_function,
    parse_monomer_composition,
    split_diseases,
    stable_id,
)


def test_stable_id_is_deterministic() -> None:
    assert stable_id("function", "antioxidant") == stable_id("function", "antioxidant")
    assert stable_id("function", "antioxidant").startswith("function:")


def test_normalize_function_aliases() -> None:
    assert normalize_function("Anti-tumor") == "antitumor"
    assert normalize_function("immunoregulation") == "immunomodulatory"
    assert normalize_function("Anti oxidant") == "anti_oxidant"


def test_parse_monomer_composition() -> None:
    parsed = parse_monomer_composition("Glucose 50%; Galactose 25.5%; invalid")
    assert parsed == [("glucose", 50.0), ("galactose", 25.5)]


def test_split_diseases_handles_commas_and_semicolons() -> None:
    assert split_diseases("A; B, C") == ["A", "B", "C"]


def test_normalize_bond_repairs_known_mojibake_tokens() -> None:
    assert "alpha" in normalize_bond("\u00a6\u0411-D-Glcp")
    assert "beta" in normalize_bond("\u00a6\u0412-D-Galp")
    assert "->" in normalize_bond("\u040e\u044a")


def test_normalize_bond_preserves_unknown_tokens() -> None:
    assert normalize_bond("unknown-bond-token") == "unknown-bond-token"
