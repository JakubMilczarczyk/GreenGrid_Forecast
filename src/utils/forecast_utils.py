from pathlib import Path
import joblib
import polars as pl
import pandas as pd

PROCESSED_DIR = Path(__file__).parent.parent.parent / 'data' / 'processed'
MODEL_DIR = Path(__file__).parent.parent.parent / 'models' / 'saved_models'
FEATURES_FILE = PROCESSED_DIR / 'train_features.parquet'
MODEL_FILE = MODEL_DIR / 'linear_regression_model.joblib'

def load_data_and_predictions():
    df = pl.read_parquet(FEATURES_FILE).to_pandas()
    model = joblib.load(MODEL_FILE)
    df_encoded = pd.get_dummies(df, columns=['business_type'])
    x = df_encoded.drop(columns=['actual_OZE_MWh', 'timestamp'])
    y_true = df_encoded['actual_OZE_MWh']
    y_entsoe = df_encoded['forecast_total_MWh']
    y_model = model.predict(x)
    timestamps = df['timestamp']
    return timestamps, y_true, y_entsoe, y_model