from pathlib import Path
import pandas as pd
from typing import Optional
from config import TRAIN_FEATURES_PATH, LATEST_FORECAST_PATH, API_BASE_URL
from services.api_client import PredictionServiceApiClient
from utils.mock_generator import generate_mock_merged_df
import logging

logger = logging.getLogger(__name__)


def _read_parquet_safe(path: Path) -> Optional[pd.DataFrame]:
    try:
        if path.exists():
            df = pd.read_parquet(path)
            logger.info(f"Loaded parquet from {path}")
            return df
        logger.info(f"File not found: {path}")
    except Exception as e:
        logger.exception(f"Error reading parquet {path}: {e}")
    return None


def load_merged_dataframe(return_source=False) -> tuple:
    """
    Ładuje i scala dane z plików Parquet:
    - train_features.parquet (zawiera rzeczywiste i ENTSO-E)
    - latest_forecast.parquet (prognozy modelu)
    Zwraca DataFrame z kolumnami: timestamp, actual_OZE_MWh, entsoe_benchmark_MWh, model_forecast
    Fallback: API lub mock.
    """
    df_features = _read_parquet_safe(Path(TRAIN_FEATURES_PATH))
    df_forecast = _read_parquet_safe(Path(LATEST_FORECAST_PATH))

    if df_features is not None and not df_features.empty:
        df_features = df_features.copy()
        # Upewnij się, że timestamp jest typu datetime
        if "timestamp" in df_features.columns:
            df_features["timestamp"] = pd.to_datetime(df_features["timestamp"])
        else:
            logger.warning("train_features missing 'timestamp' column")
            df = generate_mock_merged_df()
            return (df, "Mock") if return_source else df

        # Sprawdź i popraw nazwy kolumn
        # Rzeczywiste
        if "actual_OZE_MWh" not in df_features.columns and "actual" in df_features.columns:
            df_features = df_features.rename(columns={"actual": "actual_OZE_MWh"})
        # Benchmark ENTSO-E
        if "entsoe_benchmark_MWh" not in df_features.columns and "forecast_total_MWh" in df_features.columns:
            df_features = df_features.rename(columns={"forecast_total_MWh": "entsoe_benchmark_MWh"})

        # Jeśli dostępny forecast modelu, scal po timestamp
        if df_forecast is not None and not df_forecast.empty:
            df_forecast = df_forecast.copy()
            if "timestamp" in df_forecast.columns:
                df_forecast["timestamp"] = pd.to_datetime(df_forecast["timestamp"])
            else:
                logger.warning("latest_forecast missing 'timestamp' column")
                df = df_features.sort_values("timestamp")
                return (df, "Plik Parquet") if return_source else df

            # Prognoza modelu
            if "forecast" in df_forecast.columns:
                df_forecast = df_forecast.rename(columns={"forecast": "model_forecast"})
            elif "model_forecast" not in df_forecast.columns:
                logger.warning("latest_forecast missing 'forecast' column")
                df = df_features.sort_values("timestamp")
                return (df, "Plik Parquet") if return_source else df

            # Scal dane
            df_merged = pd.merge(
                df_features,
                df_forecast[["timestamp", "model_forecast"]],
                on="timestamp",
                how="outer"
            )

            # OGRANICZENIE: tylko daty z forecastu
            forecast_dates = set(df_forecast["timestamp"].dt.date)
            df_merged = df_merged[df_merged["timestamp"].dt.date.isin(forecast_dates)]

            df_merged = df_merged.sort_values("timestamp")
            return (df_merged, "Plik Parquet") if return_source else df_merged

        df = df_features.sort_values("timestamp")
        return (df, "Plik Parquet") if return_source else df

    # Fallback: API
    try:
        client = PredictionServiceApiClient(API_BASE_URL)
        resp = client.get_results()
        if resp:
            df_api = pd.DataFrame(resp)
            logger.info("Loaded data from Prediction API")
            if "timestamp" in df_api.columns:
                df_api["timestamp"] = pd.to_datetime(df_api["timestamp"])
            df_api = df_api.sort_values("timestamp")
            return (df_api, "API") if return_source else df_api
    except Exception:
        logger.exception("Prediction API not available or returned error")

    # Ostateczny fallback: mock
    logger.warning("Using mock data as fallback")
    df = generate_mock_merged_df()
    return (df, "Mock") if return_source else df
