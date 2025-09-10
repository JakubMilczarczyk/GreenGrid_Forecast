import os
from pathlib import Path

# Environment-backed configuration with safe defaults.
BASE_DIR = Path(__file__).resolve().parent.parent

APP_TITLE = os.getenv("UI_TITLE", "GreenGrid Forecast - Dashboard")
API_BASE_URL = os.getenv("PREDICTION_API_URL", "http://localhost:8000")

# Shared paths (mounted into containers as /opt/shared/* in your compose)
# These should match .env values in your main project if mounted
SHARED_BASE = Path(os.getenv("SHARED_BASE", str(BASE_DIR.parent / "shared")))

# Default data locations under shared
TRAIN_FEATURES_PATH = Path(os.getenv("TRAIN_FEATURES_PATH", str(SHARED_BASE / "data" / "processed" / "train_features.parquet")))
LATEST_FORECAST_PATH = Path(os.getenv("LATEST_FORECAST_PATH", str(SHARED_BASE / "data" / "forecasts" / "latest_forecast.parquet")))
