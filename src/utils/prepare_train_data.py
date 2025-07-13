import logging
from pathlib import Path
import polars as pl
import pandas as pd
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)

PROCESSED_DIR = Path(__file__).parent.parent.parent / 'data' / 'processed'
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
SPLITS_DIR = Path(__file__).parent.parent.parent / 'data' / 'splits'
SPLITS_DIR.mkdir(parents=True, exist_ok=True)
FEATURES_FILE = PROCESSED_DIR / "train_features.parquet"
X_TRAIN_FILE = SPLITS_DIR / "x_train.parquet"
Y_TRAIN_FILE = SPLITS_DIR / "y_train.parquet"
X_TEST_FILE = SPLITS_DIR / "x_test.parquet"
Y_TEST_FILE = SPLITS_DIR / "y_test.parquet"
Y_ENTSOE_FILE = SPLITS_DIR / "y_entsoe.parquet"
TS_TEST_FILE = SPLITS_DIR / "timestamps.parquet"

def clean_data(df: pl.DataFrame) -> pl.DataFrame:
    """Removes rows where target column 'actual_OZE_MWh' is null."""
    logging.info(f'Nulls per column:\n{df.null_count()}')
    df_cleaned = df.filter(pl.col('actual_OZE_MWh').is_not_null())
    logging.info(f'Rows with "actual_OZE_MWh": {df_cleaned.shape[0]}')
    return df_cleaned

def main():
    """Main function to execute the data preparation process."""
    try:
        df = pl.read_parquet(FEATURES_FILE)
        df_cleaned = clean_data(df)

        df_full = df_cleaned.to_pandas()
        forecast_total = df_full['forecast_total_MWh']
        timestamps = df_full['timestamp']

        df_encoded = pd.get_dummies(df_full, columns=['business_type'])

        num_cols = df_encoded.select_dtypes(include=['float64', 'int64']).columns
        df_encoded[num_cols] = df_encoded[num_cols].fillna(df_encoded[num_cols].mean())

        x = df_encoded.drop(columns=['actual_OZE_MWh', 'timestamp', 'forecast_total_MWh'])
        y = df_encoded['actual_OZE_MWh']
        y_entsoe = df_encoded['forecast_total_MWh']
        timestamps = df_encoded['timestamp']

        x_train, x_test, y_train, y_test, y_entsoe_train, y_entsoe_test, ts_train, ts_test = train_test_split(
            x, y, y_entsoe, timestamps, test_size=0.2, random_state=42
        )

        x_train.to_parquet(X_TRAIN_FILE, index=False)
        y_train.to_frame().to_parquet(Y_TRAIN_FILE, index=False)
        x_test.to_parquet(X_TEST_FILE, index=False)
        y_test.to_frame().to_parquet(Y_TEST_FILE, index=False)
        y_entsoe_test.to_frame(name="forecast_total_MWh").to_parquet(Y_ENTSOE_FILE, index=False)
        ts_test.to_frame(name="timestamp").to_parquet(TS_TEST_FILE, index=False)

        logging.info('Data preparation complete. Files saved.')
    except Exception as e:
        logging.error(f'Error during data preparation: {e}')

if __name__ == "__main__":
    main()
