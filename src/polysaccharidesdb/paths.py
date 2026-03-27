from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data_raw"
DATA_INTERIM = ROOT / "data_interim"
DATA_PROCESSED = ROOT / "data_processed"
CONFIGS = ROOT / "configs"
DOCS = ROOT / "docs"
EXPERIMENTS = ROOT / "experiments"
