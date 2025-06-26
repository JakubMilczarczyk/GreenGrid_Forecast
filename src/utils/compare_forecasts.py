"""Compare and visualize forecasts from model and benchmark."""

import logging
from pathlib import Path
import joblib
import polars as pl
import pandas as pd
from sklern.metrics import mean_squared_error, mean_absolute_error

logging.basicConfig(level=logging.INFO)

PROCESSED_DIR = Path(__file__).parent.parent.parent / 'data' / 'processed'
MODEL_DIR = Path(__file__).parent.parent.parent / 'models' / 'saved_models'
FEATURES_FILE = PROCESSED_DIR / 'train_features.parquet'
MODEL_FILE = MODEL_DIR / 'linear_regression_model.joblib'

def main():
    df = pl.read_parquet(FEATURES_FILE).to_pandas()
    model = joblib.load(MODEL_FILE)

    df_encoded = pd.get_dummies(df, columns=['business_type'])
    x = df_encoded.drop(columns=['actual_OZE_MWh', 'timestamp'])
    y_true = df_encoded['actual_OZE_MWh']
    y_entsoe = df_encoded['forecast_total_MWh']
    y_model = model.predict(x)

    mse_entsoe = mean_squared_error(y_true, y_entsoe)
    mse_model = mean_squared_error(y_true, y_model)
    mae_entsoe = mean_absolute_error(y_true, y_entsoe)
    mae_model = mean_absolute_error(y_true, y_model)

    logging.info(f'ENTSO-E forecast: MSE: {mse_entsoe}, MAE: {mae_entsoe}')
    logging.info(f'Model forecast: MSE: {mse_model}, MAE: {mae_model}')

if __name__ == '__main__':
    main()
