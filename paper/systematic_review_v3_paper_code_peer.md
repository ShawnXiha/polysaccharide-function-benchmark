# Systematic Review v3: Paper, Story, Methods, Structure, and Code

Review lenses used: `paper-review`, `peer-review`, and `code-review`.

Scope reviewed:

- Main manuscript: `paper/manuscript_v1.tex`
- Supplement: `paper/supplementary_v1.tex`
- BMC and Database submission packages
- KG construction/export code under `src/polysaccharidesgraph/kg`
- Experiment/model scripts under `src/polysaccharidesgraph/models`
- Paper-generation and submission sync scripts under `scripts`

## Overall Verdict

The project has a credible publishable core, but it is not yet submission-locked. The paper story is now much more disciplined than earlier versions: it no longer overclaims a new globally dominant model, and it positions the work as a DoLPHiN-derived KG resource plus benchmark diagnosis plus selective ontology tail intervention. The strongest current risk is no longer narrative confusion; it is evidence integrity and reproducibility. In particular, the code currently appears to include disease-derived degree information in `poly_x` even in the nominal clean feature export, which conflicts with the manuscript's clean-setting claim.

Recommendation: `REQUEST CHANGES` before submission. The paper can move to submission after the P0 blockers in the improvement plan are resolved and the clean benchmark is rerun.

## Major Findings

### HIGH 1. Clean-setting leakage risk in exported `poly_x`

The manuscript states that disease-derived features and edges are excluded in the clean setting. However, `export_pyg.py` always reads `poly_disease.csv` into `edge_rows` and always includes `poly_degree_counts[poly_id]["disease"]` in the base polysaccharide feature vector. This means `poly_x` contains a disease-degree feature even when disease edges are not included in message passing. Because the strongest clean baseline is `Poly-X + Meta-path + LogReg`, this may contaminate the clean result.

Evidence:

- `paper/manuscript_v1.tex`, leakage-control claim around lines 82--93.
- `src/polysaccharidesgraph/kg/export_pyg.py`, disease rows are loaded in `edge_rows`, lines 162--168.
- `src/polysaccharidesgraph/kg/export_pyg.py`, disease degree is included in `base_features`, lines 192--198.
- `paper/manuscript_v1.tex`, strongest clean baseline reported in Table 2, lines 153--167.

Why it matters:

This is the most serious review issue because it can undermine the central clean benchmark claim. Even if disease degree is only a scalar count and not disease identity, it is still disease-derived information and conflicts with the paper's stated clean/disease-aware boundary.

Required fix:

Create separate clean and disease-aware `poly_x` exports. In clean mode, remove disease degree from `poly_x` or set it to zero and document the feature schema. Rerun at least:

- `export_pyg.py`
- `run_shallow_feature_baselines.py` for `poly_x`, `meta_path`, and `poly_x_meta`
- clean GNN and no-message ablations if `poly_x` changes
- Figure 2 and Table 2

### HIGH 2. Reproducibility package is incomplete as code, despite paper prose

The manuscript now promises a reproducibility bundle, but the repository packaging does not yet support reliable third-party re-execution. `pyproject.toml` declares no runtime dependencies, the workspace is not currently a git repository, no test suite is present, and compilation fails because Python cannot write into existing `__pycache__` locations.

Evidence:

- `pyproject.toml`, dependencies are empty, lines 1--6.
- `git status` failed with `fatal: not a git repository`.
- `rg --files -g "test_*.py" -g "*_test.py"` found no tests.
- `python -m compileall -q src scripts` failed with repeated `PermissionError` writing `__pycache__`.
- `paper/manuscript_v1.tex`, reproducibility promise appears in `Code and Artifact Availability`, lines 235--238.

Why it matters:

For BMC Bioinformatics or Database, this is a major trust issue. A resource/benchmark paper needs a minimal installable environment, release tag, artifact map, and smoke tests.

Required fix:

Add real dependencies, create a lockfile or environment export, add smoke tests, and restore version control before submission.

### HIGH 3. Large monolithic experiment runner is not maintainable enough for a benchmark release

`run_poly_function_link_prediction.py` has a 1,445-line `main()` and a 141-line argument parser. It contains many experimental branches, failed method variants, scorer names, and hyperparameter flags in one executable. This is acceptable for research iteration but too fragile for a public benchmark release.

Evidence:

- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`, `parse_args()` lines 19--159.
- `src/polysaccharidesgraph/models/run_poly_function_link_prediction.py`, `main()` lines 1688--3132.
- Function-size scan found `main:1688-3132 (1445 lines)`.

Why it matters:

The current code is hard to audit, hard to test, and easy to break when changing one scorer. It also makes it difficult for readers to identify which implementation corresponds to the paper's final method.

Required fix:

Refactor into a scorer registry and config-driven runner:

- `data_loading.py`
- `scorers/base_knn.py`
- `scorers/disease_conditioned.py`
- `scorers/ontology_parent_child.py`
- `evaluation/ranking.py`
- `cli/run_link_prediction.py`

Keep failed exploratory scorers out of the default public runner or move them to `archive/`.

### HIGH 4. Submission packages still contain unresolved metadata placeholders

Both venue packages are structurally compiled, but they are not upload-ready because author metadata, repository URL, Database URL, funding, ORCID, and declarations remain placeholders.

Evidence:

- `paper/manuscript_v1.tex`, author line still says `Author names withheld for draft preparation`, line 22.
- `submission_packages/bmc_bioinformatics/paper_bmc_bioinformatics.tex`, repository placeholder remains.
- `submission_packages/database/paper_database.tex`, Database URL placeholder remains.
- `submission_packages/*/submission_checklist.md` still has unchecked metadata/funding items.

Why it matters:

This is not a scientific flaw but blocks actual submission. It also weakens reproducibility claims until the repository URL is real.

Required fix:

Fill author metadata and persistent artifact URLs, then run final `pdflatex -> bibtex -> pdflatex -> pdflatex` for each package.

## Medium Findings

### MEDIUM 1. Table 2 mixes tasks and metrics in a way that still invites confusion

Table 2 combines node-level multi-label function prediction and masked link prediction under generic `Metric 1 / Metric 2 / Metric 3` columns. The caption clarifies protocol boundaries, but the table layout itself still makes the comparison look more direct than it is.

Evidence:

- `paper/manuscript_v1.tex`, Table 2 lines 153--167.

Recommended fix:

Split Table 2 into two tables or use task-specific columns:

- Clean diagnostic table: `Macro-F1`, `Exact match`, `Feature set`, `Protocol`
- Retrieval table: `Filtered MRR`, `Hits@3`, `Hits@5`, `Tail Hits@3`, `Protocol`

### MEDIUM 2. Statistical reporting needs confidence intervals in the main stability table

The stability script computes bootstrap confidence intervals, but Table 4 reports point estimates and p-values without CIs. Because the global effect is described as practically negligible, CIs would make that argument stronger.

Evidence:

- `scripts/summarize_ontology_stability.py`, bootstrap CI computed at lines 42--53 and aggregated at lines 212--243.
- `paper/manuscript_v1.tex`, Table 4 lines 240--253 lacks CI columns.

Recommended fix:

Add CI for `Filtered MRR delta`, `Filtered Hits@3 delta`, `Tail Hits@3 delta`, and `Tail MRR delta`.

### MEDIUM 3. Function hierarchy construction is still under-specified

The paper states that the hierarchy is task-oriented and sparse, but does not provide the actual parent/child edge count, curation procedure, or a representative hierarchy table in the main paper or supplement.

Evidence:

- `paper/manuscript_v1.tex`, hierarchy construction lines 66--71.
- `configs/function_hierarchy_v3_parent_child.json` contains the actual implementation artifact.

Recommended fix:

Add a supplementary hierarchy table with columns `parent`, `child`, `rationale`, and `support level`. Also state the number of parent/child edges.

### MEDIUM 4. Normalization layer contains mojibake-specific replacements without tests

`normalize_bond()` contains replacements such as `娄袘`, `娄袙`, `袔褗`, `閳?`, `灏?`, and `浼?`. These may be necessary due to source encoding artifacts, but without tests and documentation, reviewers may see this as brittle manual cleaning.

Evidence:

- `src/polysaccharidesgraph/kg/normalize.py`, lines 72--84.

Recommended fix:

Add tests with raw input/output examples and a short data-cleaning note in the supplement.

### MEDIUM 5. `torch.load` is used on `.pt` payloads without a trust-boundary note

The code loads PyTorch `.pt` payloads with `torch.load`. This is acceptable for trusted local artifacts, but it should be treated as unsafe for arbitrary user-supplied files.

Evidence:

- `src/polysaccharidesgraph/models/run_hetero_gnn_baseline.py`, line 215.
- `src/polysaccharidesgraph/models/run_shallow_feature_baselines.py`, line 210.
- `src/polysaccharidesgraph/models/run_hybrid_hetero_gnn_baseline.py`, line 56.

Recommended fix:

Document that `.pt` files are trusted internal artifacts, or migrate portable benchmark payloads to safer formats where practical. If supported by the installed PyTorch version, use `weights_only` where applicable.

### MEDIUM 6. Submission sync script can overwrite manual fixes and still contains stale unsafe placeholders

The sync script is useful, but it still writes placeholder strings containing underscores such as `[INSERT_PUBLIC_REPOSITORY_URL]`, which previously caused LaTeX failures. It also regenerates venue manuscripts from the main manuscript and can overwrite manual venue-specific corrections.

Evidence:

- `scripts/sync_submission_with_supplement.ps1`, lines 34--43 and 47--62.

Recommended fix:

Either make the script idempotent and LaTeX-safe or replace it with a checked build script that validates generated files after writing.

## Paper Story Review

Strengths:

- The story is now appropriately bounded: KG resource, clean diagnostic benchmark, disease-aware upper bound, ontology as selective tail mechanism.
- The paper honestly reports negative results and avoids claiming GNNs are generally useless.
- The paired 16-seed ontology validation is stronger than typical single-split reporting.

Remaining story risks:

- The primary benchmark is named as masked retrieval, but the most visible clean headline is still a function-prediction table.
- The word `ontology` remains in the title, but the ontology contribution is a selective proof-of-principle mechanism rather than the broadest contribution.
- The biology-facing case studies are helpful but still thin for a glycobiology-facing venue.

Story recommendation:

For `Database`, lead with resource and benchmark. For `BMC Bioinformatics`, lead with benchmark and diagnostic insight. In both cases, treat ontology as a secondary but statistically supported tail result.

## Method and Statistics Review

Strengths:

- Clean and disease-aware settings are clearly separated in the prose.
- Filtered ranking is appropriate for the multi-label masked edge setting.
- Paired edge-level stability analysis is a good design choice.
- Negative experiments are documented in memory and pipeline files.

Concerns:

- Clean feature leakage must be resolved before trusting the headline clean result.
- No source/organism-level split is reported; organism- or publication-level leakage remains a possible reviewer concern.
- No confidence intervals are shown in the main stability table.
- One-sided tests are justified by the tail-specific hypothesis, but the paper should clearly distinguish exploratory method search from confirmatory final testing.

## Figure and Table Review

Strengths:

- Figure 1 gives a clear pipeline overview.
- Figure 2 now aligns with the updated evidence hierarchy.
- Figure 3 supports stability rather than just a single split.
- Figure 4 is useful for biology-facing interpretation.

Concerns:

- Table 2 mixes task types and metrics.
- Table 3 GNN ablation would be clearer with predicted label cardinality or a supplement pointer.
- Supplement Table S1 still has some overfull warnings due long IDs and DOI strings.

## Code Review Summary

Files reviewed: core Python modules in `src/`, paper scripts in `scripts/`, project config, and submission sync script.

CRITICAL: 0

HIGH: 4

- Clean-setting disease-derived `poly_x` feature risk.
- Missing reproducible environment and dependency declaration.
- No test suite or CI/smoke-test entrypoint.
- Monolithic link-prediction runner unsuitable for public benchmark maintenance.

MEDIUM: 6

- `torch.load` trust boundary.
- Mojibake normalization lacks tests.
- Sync script can overwrite manual fixes and contains stale unsafe placeholders.
- Table/figure generation scripts are hard-coded to current result files.
- Current workspace lacks git metadata.
- Compileall fails due `__pycache__` permission/state.

LOW: 4

- README still describes an early executable increment rather than the full benchmark.
- Some package checklists still contain manual placeholders.
- Paper table underfull warnings remain.
- Supplement table layout could be cleaner.

Code recommendation: `REQUEST CHANGES`.

## Verification Performed

- LaTeX main manuscript compiles.
- BMC and Database manuscripts compile.
- Supplement PDFs compile.
- `python -m compileall -q src scripts` fails due `PermissionError` in `__pycache__`.
- Git status cannot be checked because this directory is not currently a git repository.
- No test files were found.

## Bottom Line

The paper is scientifically close, but the clean benchmark must be rerun after removing disease-derived `poly_x` leakage. The codebase also needs a reproducibility pass before the paper can honestly be submitted as a benchmark/resource package. The strongest next step is not more model invention; it is cleaning the evidence boundary, packaging, and tests.
