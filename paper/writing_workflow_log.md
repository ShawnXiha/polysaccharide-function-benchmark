# Writing Workflow Log

## 2026-03-29

Started the paper-writing workflow with a manuscript-first strategy. The first pass fixed the paper story around three claims: the DoLPHiN-derived KG is already predictive, clean meta-path retrieval is stronger than current hetero GNN baselines, and ontology support becomes useful only as confidence-gated parent/child propagation for tail-sensitive retrieval.

The initial writing assets created in this cycle are:

- `paper/outline_v1.md`
- `paper/manuscript_draft_v1.md`
- `paper/figures_tables_plan_v1.md`
- `paper/tables_v1.md`

The figure plan is intentionally aligned with the strongest available evidence rather than the broadest possible story. Figure 1 explains the graph construction and evaluation pipeline. Figure 2 summarizes the main benchmark and positions disease-aware retrieval as an upper bound. Figure 3 is reserved for the ontology stability validation, which is the strongest supplementary claim.

The next writing step is to generate the first figure set and then revise the manuscript around concrete captions and table references.

After figure generation, the manuscript was revised to behave more like a submission draft rather than a narrative memo. A dedicated `Related Work` section was added to position the paper against polysaccharide resources, biological knowledge-graph prediction, and ontology-aware long-tail methods. The previous single limitation paragraph was expanded into a more explicit scope-bounding `Limitations` section. Figure and table references were then inserted into the main text so that the story now points directly to specific display items instead of describing results in isolation.

The current manuscript-facing assets are:

- `paper/manuscript_draft_v1.md`
- `paper/captions_v1.md`
- `paper/tables_v1.md`
- `paper/figures/figure1_pipeline.png`
- `paper/figures/figure2_benchmarks.png`
- `paper/figures/figure3_stability.png`

The next pass converted the Markdown draft into a LaTeX manuscript skeleton with executable figure and table environments. The resulting `paper/manuscript_v1.tex` now compiles locally with `pdflatex`, includes the three main figures, includes the three main tables, and carries cross-references for the central results. A placeholder bibliography scaffold was also added so the manuscript can move directly into citation completion instead of requiring a structural rewrite later.

The bibliography scaffold was then replaced with real references covering DoLPHiN itself, glycan database resources, biomedical knowledge-graph prediction, and hierarchy-aware long-tail learning. The LaTeX manuscript was rebuilt through the full `pdflatex -> bibtex -> pdflatex -> pdflatex` cycle, and the resulting PDF now contains resolved citations rather than placeholder bibliography entries.

After the clean benchmark revision experiments finished, the manuscript story was tightened again around the strongest supported claims. The old clean benchmark framing based mainly on meta-path retrieval was updated to a stronger and more standard baseline story: under the unified split, the best clean model is now `poly_x + meta_path + logreg`, not a GNN. The function-prediction tables and discussion were rewritten accordingly, and a new GNN failure-ablation table was added to make the `full vs no-message` diagnosis explicit instead of leaving it as prose.

Figure 2 was also redesigned to match this revised evidence hierarchy. Its left panel now emphasizes clean shallow baselines, the center panel keeps the tuned disease-aware upper-bound comparison, and the right panel visualizes the GNN failure ablation rather than reusing another ontology-only view. This change aligns the figure set with the paper's actual contribution balance: resource plus benchmark first, ontology tail gain second.

After a second joint pre-submission review combining reviewer-style critique, quantitative scholarly scoring, evidence-quality analysis, and adversarial self-review, the manuscript was revised again around trust and framing rather than around new experiments. The title was changed to a benchmark-first form, the Abstract and Introduction were updated to make masked `poly-function` retrieval the primary task and unified-split function prediction the clean diagnostic benchmark, and the Methods section was expanded to clarify fairness between shallow feature models and the hybrid GNN inputs.

The same revision pass also tightened statistical language for the ontology result, standardizing the interpretation that global aggregate changes are statistically detectable in some metrics but practically negligible in effect size, while the tail-sensitive gain remains the substantive positive result. A dedicated `Code and Artifact Availability` section was added to foreground reproducibility, and a new supplementary note file was created to summarize the biology-facing case-study evidence and the interpretation of exact-match behavior in the GNN ablation.

The current review-driven writing assets now additionally include:

- `paper/paper_review_v2_joint.md`
- `paper/supplementary_notes_v1.md`

## 2026-04-12

Ran a combined `paper-review`, `peer-review`, and `code-review` pass over the manuscript, submission packages, and benchmark code. The most important finding is an evidence-boundary issue: the exported `poly_x` feature vector currently includes disease degree even in nominal clean exports, while the manuscript says disease-derived features are excluded from the clean setting. This must be resolved before the clean `poly_x + meta_path + logreg` headline can be treated as submission-ready.

The review also identified release-readiness gaps: the project directory is not currently a git repository, `pyproject.toml` declares no real runtime dependencies, there are no tests, and Python compile checks fail because of `__pycache__` permission/state problems. These are not necessarily scientific flaws, but they are substantial reproducibility risks for a benchmark/resource submission.

The resulting review and action plan are:

- `paper/systematic_review_v3_paper_code_peer.md`
- `paper/improvement_plan_v2_submission_readiness.md`

Started P0 remediation by fixing the clean `poly_x` leakage in `src/polysaccharidesgraph/kg/export_pyg.py`. The exporter now builds an explicit ordered feature schema and only includes `degree__disease` when `--include-disease-edges` is enabled. The default clean export was regenerated as `data/processed/pyg/dolphin_kg_v0.pt` with `poly_feature_dim = 354` and `num_disease_derived_poly_features = 0`; the explicit disease-aware export remains `poly_feature_dim = 355` with `degree__disease` as the only disease-derived feature. The next required step is to rerun clean shallow baselines and GNN/no-message ablations against the corrected payload.

Reran the clean shallow baselines and clean neural ablations on the corrected disease-free payload. The headline changed: `meta_path + logreg` is now the strongest leakage-controlled clean baseline with test macro-F1 `0.3465`, while `poly_x + meta_path + logreg` drops to `0.3317` after removing the disease-derived `poly_x` feature. The GNN diagnosis remains stable: corrected clean `hetero_sage`, `hetero_no_message`, and `poly_mlp` remain around `0.04--0.05` macro-F1. The main manuscript and Figure 2 were updated to reflect these corrected results.

Started P1 reproducibility cleanup. Added `.gitignore`, declared real runtime and dev dependencies in `pyproject.toml`, added smoke tests for normalization, feature-schema boundaries, and ranking/statistical helpers, and updated README with dependency and test commands. Removed Python cache directories after the ACL issue was partially resolved. `python -m pytest tests -q -p no:cacheprovider` passes with `11 passed`, and AST parsing of `src`, `scripts`, and `tests` succeeds. Git initialization remains blocked by a persistent explicit Deny ACL on `.git` that prevents `HEAD.lock` creation; this is now the remaining P1 environment blocker.

Started P2 code-structure remediation without rewriting the full exploratory runner. Added `final_methods.py` to isolate the manuscript-facing disease-aware baseline and ontology best variant, and added `run_final_retrieval.py` as a stable public wrapper around the existing experiment backend. Documented the public entry points in `docs/code_structure_review.md`. Smoke-ran both final wrapper methods with `--max-eval 10`; both executed successfully. The large `run_poly_function_link_prediction.py` remains the experiment-workbench backend and should be modularized later if the project is packaged as a long-term public benchmark.

Completed a P3 manuscript clarity pass. The mixed main-results table was split into a clean diagnostic function-prediction table and a separate masked retrieval table, preventing node-classification metrics and ranking metrics from sharing generic columns. The retrieval table now includes tail Hits@3 and metric direction indicators. The ontology stability table now reports 95% bootstrap confidence intervals for the global and tail deltas. The updated tables were compiled in the main manuscript and synced to both BMC and Database submission packages.

Completed the remaining P3 hierarchy and case-study strengthening tasks. The Methods section now states the hierarchy size, and Supplementary Table S3 documents the parent category, child family, mapped DoLPHiN labels, and curation rationale. The Biological Case Studies section now cites DOI-backed source publications for the BEP, galactofucan, APP90-2, and CZGS-1 examples, and Supplementary Table S1 now includes biological interpretation in addition to graph evidence. The new references were added to the bibliography and synced to the BMC and Database packages.

Created a Chinese general-audience slide deck and talk script based on the latest paper story. The deck uses an application-driven narrative and explains the work as turning scattered polysaccharide evidence into an interpretable evidence map. It contains 15 main slides and 3 backup Q&A slides. Generated files are `paper/slides/polysaccharide_kg_general_audience_cn.pptx` and `paper/slides/polysaccharide_kg_general_audience_cn_talk_script.md`. A structural PPTX check confirmed 18 slides with text content on every slide; thumbnail rendering was blocked by local Windows temp-directory permissions and lack of a usable Office/LibreOffice conversion path.
