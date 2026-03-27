# Stage 1 Real-Data Rerun

After replacing the template exports with actual DoLPHiN / CSDB / GlyTouCan exports:

## Step 1: Build merged real dataset

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesdb\src'
python -m polysaccharidesdb.etl.build_real_dataset
python -m polysaccharidesdb.etl.build_splits --input data_processed\dataset_v0_real.jsonl --output-dir data_processed\splits_real
python -m polysaccharidesdb.etl.build_real_summary
```

## Step 2: Run Stage 1 suite

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesdb\src'
python -m polysaccharidesdb.models.run_stage1_suite
```

## Expected Outputs

- merged dataset: `data_processed/dataset_v0_real.jsonl`
- summary: `data_interim/dataset_v0_real_summary.json`
- split files: `data_processed/splits_real/`
- baseline results: `experiments/stage1_baseline/results/real_suite/`
