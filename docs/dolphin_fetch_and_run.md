# DoLPHiN fetch and Stage 1 bootstrap

## Fetch DoLPHiN pages

```powershell
$env:PYTHONPATH='src'
python -m polysaccharidesdb.etl.fetch_dolphin --page-size 100
```

For a quicker smoke test:

```powershell
$env:PYTHONPATH='src'
python -m polysaccharidesdb.etl.fetch_dolphin --page-size 100 --max-records 200
```

## Build a DoLPHiN-only dataset

```powershell
$env:PYTHONPATH='src'
python -m polysaccharidesdb.etl.build_real_dataset --manifest configs/data/source_manifest_dolphin_only.yaml
python -m polysaccharidesdb.etl.build_splits --input data_processed/dataset_dolphin_only.jsonl --output-dir data_processed/splits_dolphin_only
python -m polysaccharidesdb.etl.dataset_summary --input data_processed/dataset_dolphin_only.jsonl --output data_interim/dataset_dolphin_only_summary.json
```

## Start Stage 1 baselines

```powershell
$env:PYTHONPATH='src'
python -m polysaccharidesdb.models.run_stage1_suite --dataset data_processed/dataset_dolphin_only.jsonl --split-dir data_processed/splits_dolphin_only --output-dir experiments/stage1_baseline/results/dolphin_only_suite
```

`leave_one_source_out` will be skipped for a DoLPHiN-only dataset. `random_split` remains usable.
