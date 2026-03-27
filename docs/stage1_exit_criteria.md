# Stage 1 Exit Criteria

## Engineering Exit

Stage 1 is engineering-complete when all of the following are true:

- dataset build works
- split generation works
- at least one baseline runs on the merged real-data scaffold
- classical / sequence / graph families are executable on the local scaffold

Current status:

- achieved

## Research Exit

Stage 1 is research-complete only when all of the following are true:

- real DoLPHiN export present
- real CSDB export present
- merged real dataset builds without major schema failures
- split generation on real dataset works
- Stage 1 baseline suite runs on the real dataset
- outputs are saved under `experiments/stage1_baseline/results/real_suite/`

Current status:

- not yet achieved

## Why Stage 2 Should Not Start Yet

Stage 2 is about tuning stable configurations for the actual experiment setup.

Right now:

- the code path is ready
- the real-data ingestion path is ready
- but the current "real" dataset is still template-derived and too small

Therefore, Stage 2 would optimize for an artificial scaffold rather than the real task.

## Immediate Trigger To End Stage 1

As soon as actual DoLPHiN and CSDB exports replace the template files, run:

```powershell
$env:PYTHONPATH='D:\projects\paper_writing\polysaccharidesdb\src'
python -m polysaccharidesdb.etl.check_real_data_readiness
python -m polysaccharidesdb.etl.build_real_dataset
python -m polysaccharidesdb.etl.build_splits --input data_processed\dataset_v0_real.jsonl --output-dir data_processed\splits_real
python -m polysaccharidesdb.etl.build_real_summary
python -m polysaccharidesdb.models.run_stage1_suite
```

If those complete on the real exports, Stage 1 can be considered complete and Stage 2 can begin.
