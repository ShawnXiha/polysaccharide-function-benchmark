# Real Data Ingestion Plan

## Goal

Replace the local toy scaffold with real exported records from:

- DoLPHiN
- CSDB
- GlyTouCan mapping table

## Files

- manifest: `configs/data/source_manifest_v0.yaml`
- raw data instructions: `data_raw/README_real_data.md`
- source templates:
  - `data_raw/dolphin_export.template.csv`
  - `data_raw/csdb_export.template.csv`
  - `data_raw/glytoucan_mapping.template.csv`

## Build Command

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesdb\src'
python -m polysaccharidesdb.etl.build_real_dataset
```

## Output

- `data_processed/dataset_v0_real.jsonl`
- `data_interim/dataset_v0_real_validation_report.json`

## Recommended Next Steps

1. manually export the smallest real subset first
2. run `build_real_dataset`
3. generate splits for the real dataset
4. rerun all Stage 1 baselines on the real dataset
