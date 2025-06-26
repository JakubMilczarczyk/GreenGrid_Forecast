"""Script to train the forecasting model."""

import logging
from pathlib import Path
import joblib
import polars as pl
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

logging.basicConfig(level=logging.INFO)

PROCESSED_DIR = Path(__file__).parent.parent.parent / 'data' / 'processed'
MODEL_DIR = Path(__file__).parent.parent.parent / 'models' / 'saved_models'
MODEL_DIR.mkdir(parents=True, exist_ok=True)
FEATURES_FILE = PROCESSED_DIR / "train_features.parquet"
MODEL_FILE = MODEL_DIR / 'linear_regression_model.joblib'

def clean_data(df: pl.DataFrame) -> pl.DataFrame:
    """Cleans the input DataFrame by removing rows with NaN values."""
    df_nulls = df.filter(pl.any_horizontal(pl.all().is_null()))
    logging.info(f"Nulls per column:\n{df.null_count()}")
    logging.info(f'Null values found: {df_nulls.shape[0]}')
    return df.drop_nulls()

def encode_and_split(df: pl.DataFrame, target_col: str, drop_cols: str) -> tuple:
    """Prepares the data for training by splitting into features and target."""
    df = df.to_pandas()
    df_encoded = pd.get_dummies(df, columns=['business_type'])
    x = df_encoded.drop(columns=drop_cols)
    y = df_encoded[target_col]
    return x, y

def train_and_evaluate(x, y):
    """Trains the model and evaluates its performance."""
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    logging.info(f'Training complete. MSE: {mse}, R2: {r2}')
    return model, mse, r2, y_test, y_pred

def main():
    """Main function to execute the training process."""
    try:
        df = pl.read_parquet(FEATURES_FILE)
        logging.info(f'Loaded training features from {FEATURES_FILE}')
        df_cleaned = clean_data(df)
        logging.info(f'Cleaned data shape: {df_cleaned.shape}')
        x, y = encode_and_split(
            df_cleaned,
            target_col='actual_OZE_MWh',
            drop_cols=['actual_OZE_MWh', 'timestamp']
            )
        model, mse, r2, y_test, y_pred = train_and_evaluate(x, y)
        joblib.dump(model, MODEL_FILE)
        logging.info(f'Model saved successfully as {MODEL_FILE}')
    except Exception as e:
        logging.error(f'Error in training: {e}')
        raise

if __name__ == '__main__':
    main()
