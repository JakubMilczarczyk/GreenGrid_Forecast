import logging
from pathlib import Path
import json
import joblib
import polars as pl
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

logging.basicConfig(level=logging.INFO)

SPLITS_DIR = Path(__file__).parent.parent.parent / 'data' / 'splits'
MODEL_DIR = Path(__file__).parent.parent.parent / 'models' / 'saved_models'
MODEL_DIR.mkdir(parents=True, exist_ok=True)
METRICS_DIR = Path(__file__).parent.parent.parent / 'models' / 'metrics'
METRICS_DIR.mkdir(parents=True, exist_ok=True)
FORECASTS_DIR = Path(__file__).parent.parent.parent / "data" / "forecasts"
FORECASTS_DIR.mkdir(parents=True, exist_ok=True)
PREDICTIONS_FILE = FORECASTS_DIR / "model_predictions.parquet"  # TODO change to .csv
MODEL_FILE = MODEL_DIR / 'linear_regression_model.joblib'
METRICS_FILE = METRICS_DIR / 'linear_regression_model_metrics.json'
Y_ENTSOE_FILE = SPLITS_DIR / "y_entsoe.parquet"         # TODO change to .csv
TIMESTAMPS_FILE = SPLITS_DIR / "timestamps.parquet"     # TODO change to .csv

def load_data(
    x_train_file: Path,
    y_train_file: Path,
    x_test_file: Path,
    y_test_file: Path,
    y_entsoe_file: Path,
    timestamps_file: Path
    ) -> tuple:
    """Loads training data from parquet files."""       # TODO change to .csv for all
    x_train = pd.read_parquet(x_train_file) 
    y_train = pd.read_parquet(y_train_file).squeeze()
    x_test = pd.read_parquet(x_test_file)
    y_test = pd.read_parquet(y_test_file).squeeze()
    logging.info(f'Loaded training data shapes: x_train: {x_train.shape}, y_train: {y_train.shape}')
    logging.info(f'Loaded test data shapes: x_test: {x_test.shape}, y_test: {y_test.shape}')
    y_entsoe = pd.read_parquet(y_entsoe_file).squeeze()
    timestamps = pd.read_parquet(timestamps_file).squeeze()
    logging.info(f'Loaded ENTSO-E forecast and timestamps shapes: y_entsoe: {y_entsoe.shape}, timestamps: {timestamps.shape}')
    return x_train, y_train, x_test, y_test, y_entsoe, timestamps

def train(x_train: pd.DataFrame, y_train: pd.Series, x_test: pd.DataFrame, y_test: pd.Series) -> tuple:
    """Trains the model and evaluates its performance."""
    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    return model, y_test, y_pred

def evaluate(y_test: pd.Series, y_pred: pd.Series) -> dict:
    """Evaluates the model's performance and returns metrics."""
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    logging.info(f'Evaluation metrics - MSE: {mse}, R2: {r2}, MAE: {mae}')
    return {
        'mse': mse,
        'r2': r2,
        'mae': mae
    }

def save_model(model: LinearRegression, model_file: Path) -> None:
    """Saves the trained model to a file."""
    joblib.dump(model, model_file)
    logging.info(f'Model saved to {model_file}')

def save_metrics(metrics: dict, metrics_file: Path) -> None:
    """Saves the evaluation metrics to a JSON file."""
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f)
    df = pd.DataFrame(metrics)
    df.to_csv(metrics_file.with_suffix('.csv'), index=False)
    logging.info(f'Metrics saved to {metrics_file}')

def save_predictions(
        timestamps: pd.Series,
        y_true: pd.Series,
        y_model: pd.Series,
        y_entsoe: pd.Series,
        predictions_file: Path
    ) -> None:
    """Saves the predictions to a file."""
    df = pd.DataFrame({
        'timestamp': timestamps,
        'y_true': y_true,
        'y_model': y_model,
        'y_entsoe': y_entsoe
    })
    df.to_parquet(predictions_file, index=False)    # TODO change to .csv
    logging.info(f'Predictions saved to {predictions_file}')

def main():
    """Main function to execute the training process."""
    try:
        x_train_file = SPLITS_DIR / "x_train.parquet"   # TODO change to .csv for all
        y_train_file = SPLITS_DIR / "y_train.parquet"
        x_test_file = SPLITS_DIR / "x_test.parquet"
        y_test_file = SPLITS_DIR / "y_test.parquet"
        y_entsoe_file = SPLITS_DIR / "y_entsoe.parquet"
        timestamps_file = SPLITS_DIR / "timestamps.parquet"

        x_train, y_train, x_test, y_test, y_entsoe, timestamps = load_data(
            x_train_file, y_train_file, x_test_file, y_test_file,
            y_entsoe_file, timestamps_file
        )
        
        model, y_test, y_pred = train(x_train, y_train, x_test, y_test)
        
        save_model(model, MODEL_FILE)

        mse_benchmark = mean_squared_error(y_test, y_entsoe)
        mae_benchmark = mean_absolute_error(y_test, y_entsoe)
        model_metrics = evaluate(y_test, y_pred)
        metrics = {
            'model': model_metrics,
            'benchmark': {
                'mse': mse_benchmark,
                'mae': mae_benchmark
            }
        }
        save_metrics(metrics, METRICS_FILE)

        save_predictions(
            timestamps=timestamps,
            y_true=y_test,
            y_model=y_pred,
            y_entsoe=y_entsoe, 
            predictions_file=PREDICTIONS_FILE
        )

    except Exception as e:
        logging.error(f'Error during model training: {e}')

if __name__ == "__main__":
    main()
