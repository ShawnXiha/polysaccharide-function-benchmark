from scripts.summarize_ontology_stability import hit_at_k, mcnemar_exact, reciprocal_rank


def test_rank_helpers() -> None:
    assert reciprocal_rank(4) == 0.25
    assert hit_at_k(3, 3) == 1.0
    assert hit_at_k(4, 3) == 0.0


def test_mcnemar_handles_no_discordant_pairs() -> None:
    result = mcnemar_exact(0, 0)
    assert result["discordant"] == 0
    assert result["p_two_sided"] == 1.0
    assert result["p_one_sided_ontology_better"] == 1.0


def test_mcnemar_directional_p_value() -> None:
    result = mcnemar_exact(5, 0)
    assert result["discordant"] == 5
    assert result["p_one_sided_ontology_better"] == 1 / 32

