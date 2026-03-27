# Stage 1 Attempt 2 Notes

## Objective

Create the smallest executable data path:

1. load local sample records
2. normalize to schema v0
3. validate required fields
4. write `dataset_v0.jsonl`
5. generate deterministic split files
6. export a simple dataset summary

## Commands

```powershell
python -m polysaccharidesdb.etl.build_dataset
python -m polysaccharidesdb.etl.build_splits
python -m polysaccharidesdb.etl.dataset_summary
```

## Expected Outputs

- `data_processed/dataset_v0.jsonl`
- `data_processed/splits/random_split.json`
- `data_processed/splits/leave_one_source_out.json`
- `data_processed/splits/leave_one_genus_out.json`
- `data_interim/dataset_v0_validation_report.json`
- `data_interim/dataset_v0_summary.json`
