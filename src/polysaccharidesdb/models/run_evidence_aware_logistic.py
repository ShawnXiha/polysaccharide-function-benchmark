"""Run a minimal evidence-aware logistic method for Stage 3."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer

from polysaccharidesdb.models.dataset import index_by_poly_id, load_dataset
from polysaccharidesdb.models.evidence_aware import (
    evidence_feature_tokens,
    evidence_sample_weight,
    polysaccharide_feature_tokens,
)
from polysaccharidesdb.models.feature_text import record_to_feature_text
from polysaccharidesdb.models.multilabel_utils import ensure_2d_binary_predictions
from polysaccharidesdb.models.split_utils import expand_split_payload
from polysaccharidesdb.paths import DATA_PROCESSED, EXPERIMENTS
from polysaccharidesdb.utils.io import read_json, write_json
from polysaccharidesdb.utils.metrics import exact_match_ratio, macro_f1_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run evidence-aware logistic method")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DATA_PROCESSED / "dataset_publishable_supervised_v1.jsonl",
    )
    parser.add_argument(
        "--split",
        type=Path,
        default=DATA_PROCESSED / "splits_publishable_supervised_v1" / "random_split.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=EXPERIMENTS / "stage3_method" / "results" / "evidence_aware_random.json",
    )
    parser.add_argument(
        "--eval-split",
        type=str,
        default="valid",
        choices=["valid", "test"],
        help="Which partition from the split file to evaluate on",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--c", type=float, default=16.0)
    parser.add_argument("--min-df", type=int, default=1)
    parser.add_argument("--max-features", type=int, default=0)
    parser.add_argument("--binary", action="store_true")
    parser.add_argument("--class-weight", type=str, default="balanced")
    parser.add_argument("--disable-poly-features", action="store_true")
    parser.add_argument("--disable-evidence-features", action="store_true")
    parser.add_argument("--disable-sample-weight", action="store_true")
    parser.add_argument("--disable-mw-feature", action="store_true")
    parser.add_argument("--disable-branching-feature", action="store_true")
    parser.add_argument("--disable-modification-feature", action="store_true")
    parser.add_argument("--disable-residue-feature", action="store_true")
    parser.add_argument("--disable-source-kingdom-feature", action="store_true")
    parser.add_argument("--disable-composition-feature", action="store_true")
    parser.add_argument(
        "--final-test",
        action="store_true",
        help="Mark this run as a frozen final-test evaluation",
    )
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def render_evidence_aware_text(
    record: dict,
    use_poly_features: bool = True,
    use_evidence_features: bool = True,
    include_mw: bool = True,
    include_branching: bool = True,
    include_modification: bool = True,
    include_residue: bool = True,
    include_source_kingdom: bool = True,
    include_composition_terms: bool = True,
) -> str:
    parts = [record_to_feature_text(record)]
    if use_poly_features:
        parts.extend(
            f"poly={token}"
            for token in polysaccharide_feature_tokens(
                record,
                include_mw=include_mw,
                include_branching=include_branching,
                include_modification=include_modification,
                include_residue=include_residue,
                include_source_kingdom=include_source_kingdom,
                include_composition_terms=include_composition_terms,
            )
        )
    if use_evidence_features:
        parts.extend(f"evi={token}" for token in evidence_feature_tokens(record))
    return " ".join(parts)


def fit_binary_relevance(
    x_train,
    y_train_bin: np.ndarray,
    sample_weight: np.ndarray,
    c: float,
    class_weight: str | None,
    seed: int,
) -> list[LogisticRegression]:
    estimators: list[LogisticRegression] = []
    for label_idx in range(y_train_bin.shape[1]):
        estimator = LogisticRegression(
            max_iter=1000,
            solver="liblinear",
            C=c,
            random_state=seed,
            class_weight=class_weight,
        )
        estimator.fit(x_train, y_train_bin[:, label_idx], sample_weight=sample_weight)
        estimators.append(estimator)
    return estimators


def predict_binary_relevance(estimators: list[LogisticRegression], x_test) -> np.ndarray:
    columns = []
    for estimator in estimators:
        columns.append(estimator.predict(x_test))
    return ensure_2d_binary_predictions(np.vstack(columns).T, num_labels=len(estimators))


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    class_weight = None if args.class_weight == "none" else args.class_weight
    use_poly_features = not args.disable_poly_features
    use_evidence_features = not args.disable_evidence_features
    use_sample_weight = not args.disable_sample_weight
    include_mw = not args.disable_mw_feature
    include_branching = not args.disable_branching_feature
    include_modification = not args.disable_modification_feature
    include_residue = not args.disable_residue_feature
    include_source_kingdom = not args.disable_source_kingdom_feature
    include_composition_terms = not args.disable_composition_feature
    records = load_dataset(args.dataset)
    record_map = index_by_poly_id(records)
    split_payload = read_json(args.split)
    expanded_splits = expand_split_payload(split_payload, eval_key=args.eval_split)

    split_results = []
    for split_def in expanded_splits:
        train_records = [record_map[poly_id] for poly_id in split_def["train"]]
        test_records = [record_map[poly_id] for poly_id in split_def["test"]]

        x_train_text = [
            render_evidence_aware_text(
                record,
                use_poly_features=use_poly_features,
                use_evidence_features=use_evidence_features,
                include_mw=include_mw,
                include_branching=include_branching,
                include_modification=include_modification,
                include_residue=include_residue,
                include_source_kingdom=include_source_kingdom,
                include_composition_terms=include_composition_terms,
            )
            for record in train_records
        ]
        x_test_text = [
            render_evidence_aware_text(
                record,
                use_poly_features=use_poly_features,
                use_evidence_features=use_evidence_features,
                include_mw=include_mw,
                include_branching=include_branching,
                include_modification=include_modification,
                include_residue=include_residue,
                include_source_kingdom=include_source_kingdom,
                include_composition_terms=include_composition_terms,
            )
            for record in test_records
        ]
        y_train = [record.get("function_label", []) for record in train_records]
        y_test = [set(record.get("function_label", [])) for record in test_records]
        if use_sample_weight:
            sample_weight = np.array([evidence_sample_weight(record) for record in train_records], dtype=float)
        else:
            sample_weight = np.ones(len(train_records), dtype=float)

        vectorizer = CountVectorizer(
            token_pattern=r"(?u)\b[\w=\-]+\b",
            min_df=args.min_df,
            max_features=None if args.max_features <= 0 else args.max_features,
            binary=args.binary,
        )
        x_train = vectorizer.fit_transform(x_train_text)
        x_test = vectorizer.transform(x_test_text)

        mlb = MultiLabelBinarizer()
        y_train_bin = mlb.fit_transform(y_train)
        estimators = fit_binary_relevance(
            x_train=x_train,
            y_train_bin=y_train_bin,
            sample_weight=sample_weight,
            c=args.c,
            class_weight=class_weight,
            seed=args.seed,
        )
        y_pred_bin = predict_binary_relevance(estimators, x_test)
        y_pred = [set(labels) for labels in mlb.inverse_transform(y_pred_bin)]
        prediction_rows = [
            {
                "poly_id": record["poly_id"],
                "y_true": sorted(y_test[idx]),
                "y_pred": sorted(y_pred[idx]),
            }
            for idx, record in enumerate(test_records)
        ]

        split_results.append(
            {
                "split_name": split_def["name"],
                "eval_split": args.eval_split,
                "num_train": len(train_records),
                "num_test": len(test_records),
                "labels": sorted(mlb.classes_.tolist()),
                "vectorizer_vocab_size": int(x_train.shape[1]),
                "sample_weight_mean": float(sample_weight.mean()),
                "sample_weight_min": float(sample_weight.min()),
                "sample_weight_max": float(sample_weight.max()),
                "macro_f1": macro_f1_score(y_test, y_pred),
                "exact_match_ratio": exact_match_ratio(y_test, y_pred),
                "predictions": prediction_rows,
            }
        )

    result = {
        "dataset": str(args.dataset),
        "split": str(args.split),
        "config": {
            "eval_split": args.eval_split,
            "is_final_test": args.final_test,
            "seed": args.seed,
            "c": args.c,
            "min_df": args.min_df,
            "max_features": args.max_features,
            "binary": args.binary,
            "class_weight": args.class_weight,
            "use_poly_features": use_poly_features,
            "use_evidence_features": use_evidence_features,
            "use_sample_weight": use_sample_weight,
            "include_mw": include_mw,
            "include_branching": include_branching,
            "include_modification": include_modification,
            "include_residue": include_residue,
            "include_source_kingdom": include_source_kingdom,
            "include_composition_terms": include_composition_terms,
            "method": "evidence_aware_logistic_v1",
        },
        "results": split_results,
        "note": "logistic baseline with evidence/completeness sample weighting and polysaccharide-specific feature augmentation",
    }
    write_json(args.output, result)
    print(f"Wrote Stage 3 result to {args.output}")


if __name__ == "__main__":
    main()
