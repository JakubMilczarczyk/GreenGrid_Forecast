from pathlib import Path
import pandas as pd

SPLITS_DIR = Path(__file__).parent.parent.parent / "data" / "splits"
FORECASTS_FILE = Path(__file__).parent.parent.parent / "data" / "forecasts" / "model_predictions.parquet"   # TODO change to .csv

def load_data_and_predictions():
    """Loads model predictions and ground truth."""
    df = pd.read_parquet(FORECASTS_FILE)        # TODO change to pd.read_csv
    timestamps = pd.to_datetime(df["timestamp"])
    y_true = df["y_true"]
    y_entsoe = df["y_entsoe"]
    y_model = df["y_model"]
    return timestamps, y_true, y_entsoe, y_model
