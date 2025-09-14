import joblib
import os
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

DATA_DIR = Path(os.getenv("DATA_DIR", "/opt/airflow/shared/data"))
MODELS_DIR = Path(os.getenv("MODELS_DIR", "/opt/airflow/shared/models"))
FORECASTS_DIR = DATA_DIR / "forecasts"
FORECASTS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODELS_DIR / "saved_models/linear_regression_model.joblib" # TODO: change to the input model path (input from UI or API)
INPUT_DATA = DATA_DIR / "splits" / "x_test.parquet"
INPUT_TIMESTAMPS = DATA_DIR / "splits" / "timestamps.parquet"
PREDICTIONS_FILE = FORECASTS_DIR / "latest_forecast.parquet"

def run_forecast():
    model = joblib.load(MODEL_FILE)
    logging.info(f"Model loaded from {MODEL_FILE}")

    X_new = pd.read_parquet(INPUT_DATA)
    timestamps = pd.read_parquet(INPUT_TIMESTAMPS).squeeze()
    if len(X_new) != len(timestamps):
        logging.warning(
            f'Length mismatch: timestamps={len(timestamps)}, x_new={len(X_new)}'
            'Forecast fie may be misaligned.'
        )

    y_pred = model.predict(X_new)
    df = pd.DataFrame({"timestamp": timestamps, "forecast": y_pred})

    df.to_parquet(PREDICTIONS_FILE, index=False)
    logging.info(f"Forecast saved to {PREDICTIONS_FILE}")

if __name__ == "__main__":
    run_forecast()
