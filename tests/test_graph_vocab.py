from polysaccharidesdb.models.graph_features import TOKENS, build_vocab


def make_record(poly_id: str, marker: str) -> dict:
    record = {
        "poly_id": poly_id,
        "canonical_representation": f"repr-{marker}",
        "function_label": ["label_a"],
    }
    for field in TOKENS:
        record[field] = f"{field}-{marker}"
    return record


def test_graph_vocab_is_built_from_training_records_only() -> None:
    train_record = make_record("train-1", "train")
    test_record = make_record("test-1", "test")

    vocab = build_vocab([train_record])

    assert "repr=repr-train" in vocab
    assert "repr=repr-test" not in vocab
    for field in TOKENS:
        assert f"{field}={train_record[field]}" in vocab
        assert f"{field}={test_record[field]}" not in vocab
