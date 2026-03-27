# Next Action

## Single Highest-Value Action

Replace:

- `data_raw/dolphin_export.csv`
- `data_raw/csdb_export.csv`

with actual exported source files.

## Then Run

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesdb\src'
python -m polysaccharidesdb.etl.check_real_data_readiness
python -m polysaccharidesdb.etl.build_real_dataset
python -m polysaccharidesdb.etl.build_splits --input data_processed\dataset_v0_real.jsonl --output-dir data_processed\splits_real
python -m polysaccharidesdb.etl.build_real_summary
python -m polysaccharidesdb.models.run_stage1_suite
```

## Interpretation

- if readiness is `false`, fix source exports first
- if readiness is `true` and the suite finishes, Stage 1 is done
- only then should Stage 2 tuning begin
