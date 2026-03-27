# ETL

Planned modules:

- `loaders.py`: source-specific loading
- `normalize.py`: canonicalization and field cleanup
- `build_dataset.py`: dataset assembly
- `build_splits.py`: deterministic split generation
- `dataset_summary.py`: dataset statistics for sanity checks
- `schema.py`: schema v0 validation
- `source_loaders.py`: DoLPHiN / CSDB / GlyTouCan export normalization
- `manifest.py`: manifest loading and path resolution
- `build_real_dataset.py`: merge builder for real exported files
- `build_real_summary.py`: summary wrapper for the merged real dataset
- `check_real_data_readiness.py`: readiness gate before rerunning Stage 1 on real exports
