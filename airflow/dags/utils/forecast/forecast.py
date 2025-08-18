import joblib
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

DATA_DIR = Path("/opt/airflow/data")
MODELS_DIR = Path("/opt/airflow/models")
FORECASTS_DIR = DATA_DIR / "forecasts"
FORECASTS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODELS_DIR / "saved_models/linear_regression_model.joblib" # TODO: change to the input model path (input from UI or API)
INPUT_FILE = DATA_DIR / "train_features.parquet"           # TODO: change to the actual input file path
PREDICTIONS_FILE = FORECASTS_DIR / "latest_forecast.parquet"

def run_forecast():
    model = joblib.load(MODEL_FILE)
    X_new = pd.read_parquet(INPUT_FILE)
    y_pred = model.predict(X_new)
    df = pd.DataFrame({"timestamp": X_new.index, "forecast": y_pred})
    df.to_parquet(PREDICTIONS_FILE, index=False)
    logging.info(f"Forecast saved to {PREDICTIONS_FILE}")

if __name__ == "__main__":
    run_forecast()
