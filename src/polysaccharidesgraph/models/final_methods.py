"""Named final method configurations used by the manuscript.

The original link-prediction runner contains many exploratory scorers from the
experiment pipeline. This module isolates the paper-facing configurations so a
reader can find and rerun the final baseline/ontology methods without scanning
every failed variant.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class RetrievalMethodConfig:
    """CLI arguments for one paper-facing retrieval method."""

    name: str
    description: str
    args: tuple[str, ...] = field(default_factory=tuple)
    primary_score_key: str = "meta_path_knn"


DISEASE_AWARE_BASELINE = RetrievalMethodConfig(
    name="disease_aware_freq_prior",
    description="Disease-conditioned kNN vote with frequency-adjusted disease prior.",
    args=(
        "--include-disease-features",
        "--disease-conditioned-base-vote",
        "--disease-vote-top-k",
        "25",
        "--disease-vote-weight",
        "1.0",
        "--disease-vote-max-boost",
        "5.0",
        "--frequency-adjusted-disease-prior",
        "--freq-disease-prior-top-n",
        "20",
        "--freq-disease-prior-weight",
        "1.0",
        "--freq-disease-prior-strength",
        "0.5",
        "--freq-disease-prior-mode",
        "divide",
    ),
    primary_score_key="meta_path_knn_disease_conditioned_vote_freq_prior",
)


ONTOLOGY_PARENT_CHILD_BEST = RetrievalMethodConfig(
    name="ontology_parent_child_best",
    description="Confidence-gated parent/child ontology variant used as the tail-sensitive method.",
    args=(
        *DISEASE_AWARE_BASELINE.args,
        "--hierarchy-parent-child-native",
        "--hierarchy-config",
        "configs/function_hierarchy_v3_parent_child.json",
        "--hierarchy-base-window",
        "20",
        "--hierarchy-threshold",
        "10",
        "--hierarchy-min-seed-count",
        "2",
        "--hierarchy-specificity-power",
        "2.0",
        "--hierarchy-graph-weight",
        "0.1",
        "--hierarchy-confidence-threshold",
        "0.25",
        "--hierarchy-adaptive-power",
        "1.5",
    ),
    primary_score_key="meta_path_knn_disease_conditioned_vote_freq_prior_hierarchy_parent_child_native",
)


FINAL_METHODS = {
    DISEASE_AWARE_BASELINE.name: DISEASE_AWARE_BASELINE,
    ONTOLOGY_PARENT_CHILD_BEST.name: ONTOLOGY_PARENT_CHILD_BEST,
}


def method_output_path(repo_root: Path, method_name: str, seed: int) -> Path:
    """Return a standard output path for final method reruns."""
    return repo_root / "experiments" / "final_methods" / f"{method_name}_seed{seed}.json"

