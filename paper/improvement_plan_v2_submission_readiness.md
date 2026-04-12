# Improvement Plan v2: Submission Readiness and Evidence Integrity

This plan converts `systematic_review_v3_paper_code_peer.md` into a concrete execution sequence.

## P0: Evidence Integrity Blockers

Goal: make the main scientific claims defensible.

### P0.1 Remove clean-setting disease-derived `poly_x` leakage

Status update 2026-04-12:

- Code fix completed in `src/polysaccharidesgraph/kg/export_pyg.py`.
- Default clean export now writes `poly_feature_dim = 354` and `num_disease_derived_poly_features = 0`.
- Disease-aware export writes `poly_feature_dim = 355` and contains exactly one disease-derived feature: `degree__disease`.
- Feature schemas are now written next to PyG payloads as `*.feature_schema.json`.
- Clean shallow baselines and clean GNN ablations were rerun on the corrected payload.
- Result change: `meta_path + logreg` is now the strongest leakage-controlled clean baseline (`macro-F1 = 0.3465`); corrected `poly_x + meta_path + logreg` drops to `0.3317`.
- Main manuscript and Figure 2 were updated accordingly.
- Remaining work: synchronize BMC and Database submission packages with the corrected main manuscript.

Actions:

1. Modify `export_pyg.py` so disease degree is excluded from clean `poly_x`.
2. Add an explicit feature-schema JSON next to each PyG export.
3. Create two explicit exports:
   - `dolphin_kg_v0_clean.pt`
   - `dolphin_kg_v0_with_disease.pt`
4. Rerun clean shallow baselines:
   - `meta_path + logreg`
   - `poly_x + logreg`
   - `poly_x + meta_path + logreg`
   - `meta_path + mlp`
5. Rerun clean GNN/no-message ablations if feature dimensionality changes.
6. Update Figure 2, Table 2, Table 3, and the Abstract.

Exit criteria:

- Clean `poly_x` has no disease-derived field.
- The paper reports only rerun clean results.
- A test asserts that clean feature schemas contain no disease features.

### P0.2 Reconcile manuscript claims with rerun results

Actions:

1. If `poly_x + meta_path + logreg` remains best, keep the current story.
2. If performance drops materially, revise the clean story to emphasize `meta_path + logreg` as the strongest leakage-free clean baseline.
3. Update all affected PDFs and submission packages.

Exit criteria:

- No claim in Abstract/Introduction depends on stale pre-fix results.

## P1: Reproducibility and Release Packaging

Goal: make the benchmark re-runnable by a reviewer.

### P1.1 Restore version control and clean generated artifacts

Status update 2026-04-12:

- Added `.gitignore` for Python caches, local virtual environments, uv cache, and LaTeX intermediates.
- Removed `__pycache__` and `.pycache_tmp` artifacts from `src/` and `scripts/`.
- `git init` is still blocked because `.git` has a persistent explicit Deny ACL that prevents `HEAD.lock` creation. This is an environment/ACL blocker, not a source-code issue.

Actions:

1. Restore or initialize git in the project root.
2. Add `.gitignore` for:
   - `__pycache__/`
   - `*.pyc`
   - LaTeX aux/log files where appropriate
   - local `.venv*`
3. Remove stale cache directories.
4. Create a release branch or tag for the submission candidate.

Exit criteria:

- `git status --short` works.
- No Python bytecode artifacts are tracked.

### P1.2 Declare dependencies

Status update 2026-04-12:

- Updated `pyproject.toml` with runtime dependencies: `numpy`, `scikit-learn`, `matplotlib`, `torch`, and `torch-geometric`.
- Added `dev` optional dependencies for `pytest` and `ruff`.
- Added pytest config with `testpaths = ["tests"]` and `pythonpath = ["src"]`.

Actions:

1. Update `pyproject.toml` with runtime dependencies:
   - `numpy`
   - `torch`
   - `torch-geometric`
   - `scikit-learn`
   - `matplotlib`
   - `networkx` if used in case figures
2. Add optional groups:
   - `dev`: `pytest`, `ruff`
   - `paper`: LaTeX instructions, not necessarily Python deps
3. Generate or document the environment lock strategy.

Exit criteria:

- Fresh environment can run a smoke command.
- README install instructions match `pyproject.toml`.

### P1.3 Add smoke tests

Status update 2026-04-12:

- Added tests for normalization helpers, disease-free clean feature schema, disease-aware schema marking, and ranking/statistical helpers.
- `python -m pytest tests -q -p no:cacheprovider` passes with `11 passed`.
- AST parse check for `src`, `scripts`, and `tests` passes.

Actions:

1. Add tests for:
   - function normalization
   - disease-free clean feature schema
   - filtered ranking logic
   - hierarchy parent/child propagation on a toy graph
   - KG validation on a tiny fixture
2. Add a `pytest` command to README.
3. Add a `scripts/smoke_reproduce_submission.ps1` runner.

Exit criteria:

- `pytest` passes.
- `python -m compileall` passes after cache cleanup.

## P2: Code Structure Improvements

Goal: make the released code reviewable and maintainable.

### P2.1 Refactor link-prediction runner

Status update 2026-04-12:

- Added `src/polysaccharidesgraph/models/final_methods.py` to isolate manuscript-facing retrieval configurations from the exploratory long-tail workbench.
- Added `src/polysaccharidesgraph/models/run_final_retrieval.py` as a stable wrapper for the final disease-aware baseline and ontology best variant.
- Added `docs/code_structure_review.md` documenting stable public entry points and identifying `run_poly_function_link_prediction.py` as an experiment-workbench backend.
- Smoke-ran both wrapper methods with `--max-eval 10`; both executed successfully.
- Remaining work: full modular refactor of the 3,000-line exploratory runner is still pending and should be treated as a post-P1/P2 cleanup task before public release if time allows.

Actions:

1. Split `run_poly_function_link_prediction.py` into modules:
   - `data.py`
   - `ranking.py`
   - `scorers/base_knn.py`
   - `scorers/disease.py`
   - `scorers/ontology.py`
   - `cli/run_link_prediction.py`
2. Move failed exploratory scorers to `archive/` or keep them behind documented experiment configs.
3. Replace the long boolean flag matrix with YAML/JSON config files.

Exit criteria:

- Final paper method can be run from one minimal config.
- Exploratory failed methods do not obscure the final method implementation.

### P2.2 Harden artifact loading

Actions:

1. Add trust-boundary notes for `.pt` files.
2. Prefer safer serializations for portable metadata where possible.
3. Add checksum manifest for release artifacts.

Exit criteria:

- README explains which files are trusted generated artifacts.
- Reviewers can verify artifact integrity.

### P2.3 Fix submission sync workflow

Actions:

1. Make `sync_submission_with_supplement.ps1` LaTeX-safe for placeholders.
2. Add post-sync validation that compiles both venue packages.
3. Prevent overwriting manually filled author/funding metadata unless explicitly requested.

Exit criteria:

- Sync script is safe to rerun after author metadata is filled.

## P3: Paper Improvements

Goal: increase reviewer trust and reduce preventable objections.

### P3.1 Split mixed metric table

Status update 2026-04-12:

- Replaced the mixed main results table with two separate tables:
  - `Table~\ref{tab:clean-diagnostic}` for leakage-controlled clean function-prediction diagnostics.
  - `Table~\ref{tab:retrieval-results}` for representative tuned masked retrieval results.
- Added metric direction indicators and tail Hits@3 in the retrieval table.
- Synced the revised table structure to BMC and Database packages.

Actions:

1. Replace current Table 2 with:
   - clean diagnostic table
   - retrieval table
2. Add tail metric to the retrieval table.
3. Add metric direction indicators.

Exit criteria:

- No table mixes node classification metrics and ranking metrics in generic columns.

### P3.2 Add confidence intervals

Status update 2026-04-12:

- Added 95% bootstrap CI values from `ontology_stability_summary.json` to the paired stability table.
- Synced the CI-enhanced table to BMC and Database packages.

Actions:

1. Extract bootstrap CIs from `ontology_stability_summary.json`.
2. Add CI columns or parenthetical intervals to Table 4.
3. Update Figure 3 caption to mention paired CIs if shown.

Exit criteria:

- Stability table reports effect sizes, CIs, and p-values.

### P3.3 Document hierarchy construction

Status update 2026-04-12:

- Added Supplementary Table S3 documenting the task-specific parent/family/function hierarchy.
- Updated Methods to state that the final hierarchy contains 11 intermediate function families and 11 parent-to-family edges.
- Synced the updated supplement to BMC and Database packages.

Actions:

1. Add Supplementary Table S3:
   - parent label
   - child label
   - rationale
   - whether used by final ontology method
2. State hierarchy edge count in Methods.

Exit criteria:

- Manual ontology construction is auditable.

### P3.4 Strengthen biology-facing evidence

Status update 2026-04-12:

- Added four DOI-backed case-study references to the bibliography.
- Updated the Biological Case Studies section to cite the source publications for BEP, galactofucan, APP90-2, and CZGS-1.
- Expanded Supplementary Table S1 from evidence-only rows into evidence plus biological interpretation.
- Synced references and supplement updates to BMC and Database packages.

Actions:

1. Add DOI provenance links in Supplementary Table S1 as URLs.
2. Add one sentence per case connecting evidence to a known biological interpretation.
3. If possible, add one external citation for the `osteogenic` or `anticoagulant` case.

Exit criteria:

- Case studies read less like retrieval examples and more like biological evidence chains.

## P4: Submission Package Finalization

Goal: make the package upload-ready.

### P4.1 Fill metadata

Actions:

1. Fill:
   - author names
   - affiliations
   - corresponding author
   - ORCID
   - funding
   - competing interests
   - author contributions
   - acknowledgements
2. Insert public repository URL and database URL.

Exit criteria:

- No `INSERT`, `First Author`, or `Author names withheld` placeholders remain.

### P4.2 Compile final packages

Actions:

1. Compile:
   - main manuscript
   - main supplement
   - BMC manuscript
   - BMC supplement
   - Database manuscript
   - Database supplement
2. Run `bibtex` where needed.
3. Archive final PDFs and source files.

Exit criteria:

- All final PDFs compile without unresolved citations or references.

## Suggested Execution Order

1. P0.1 clean feature leakage fix and rerun.
2. P0.2 manuscript result reconciliation.
3. P1.1 git and cache cleanup.
4. P1.2 dependency declaration.
5. P1.3 smoke tests.
6. P3 table/CI/hierarchy paper improvements.
7. P4 submission metadata and final compile.

Do not spend time on new model ideas before P0 and P1 are complete.
