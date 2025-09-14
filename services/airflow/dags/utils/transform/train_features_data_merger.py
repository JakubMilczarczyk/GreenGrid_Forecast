"""Script to merge all datasets to one and save it to parquete"""

import logging
import os
from pathlib import Path
import polars as pl
from utils.schema_validator import validate_df 

logging.basicConfig(level=logging.INFO)

# Constants
DATA_DIR = Path(os.getenv("DATA_DIR", "/opt/airflow/shared/data"))
PROCESSED_DIR = DATA_DIR / "processed"
if not os.path.exists(PROCESSED_DIR):
    os.makedirs(PROCESSED_DIR)

OUTPUT_FILE_PATH = os.path.join(PROCESSED_DIR, 'train_features.parquet')       # TODO change to .csv
OZE_CODES = ['B11', 'B13', 'B15', 'B16', 'B17', 'B18', 'B19']

def load_and_prepare_generation(path: Path) -> pl.DataFrame:
    df = pl.read_csv(path)

    oze_df = (
        df.filter(pl.col('psr_code').is_in(OZE_CODES))
          .group_by('timestamp')
          .agg(pl.col('quantity_MWh').sum().alias('actual_OZE_MWh'))
    )

    oze_df = oze_df.with_columns([
        pl.col('timestamp')
          .str.strip_chars()
          .str.strptime(pl.Datetime)
          .dt.replace_time_zone(None)
    ])
    return oze_df

def load_and_prepare_weather(path: Path) -> pl.DataFrame:
    df = pl.read_csv(path).with_columns([
        pl.col('timestamp')
          .str.strip_chars()
          .str.strptime(pl.Datetime)
          .dt.replace_time_zone(None)
    ])
    return df

def load_and_prepare_forecast(path: Path) -> pl.DataFrame:
    df = pl.read_csv(path).rename({'quantity': 'forecast_total_MWh'}).with_columns([
        pl.col('timestamp')
          .str.strip_chars()
          .str.strptime(pl.Datetime)
          .dt.replace_time_zone(None)
    ])
    return df

def merge_features(weather, forecast, oze) -> pl.DataFrame:
    merged = (
        weather
        .join(forecast, on='timestamp', how='left')
        .join(oze, on='timestamp', how='left')
        .with_columns([
            pl.col('timestamp').dt.hour().alias('hour'),
            pl.col('timestamp').dt.weekday().alias('day_of_week'),
            (pl.col('timestamp').dt.weekday() > 5).alias('is_weekend'),  # TODO add is_holiday from workalendar
        ])
    )
    return merged

def main():
    try:
        actual_generation_data = PROCESSED_DIR / 'entsoe_actual_generation.csv'
        forecast_total_generation = PROCESSED_DIR / 'forecast_generation_total.csv'
        forecast_weather_data = PROCESSED_DIR / 'weather_dk1.csv'

        oze_df = load_and_prepare_generation(actual_generation_data)
        weather_df = load_and_prepare_weather(forecast_weather_data)
        forecast_df = load_and_prepare_forecast(forecast_total_generation)

        merged = merge_features(weather_df, forecast_df, oze_df)

        validate_df(merged, "train_features.json")
        logging.info(f'Merged columns: {merged.columns}')
        logging.info(f'Sample:\n{merged.head()}')

        merged.write_parquet(OUTPUT_FILE_PATH)       # TODO change to write_csv
        logging.info(f'Features set saved as: {OUTPUT_FILE_PATH}')
    except Exception as e:
        logging.error(f'Error in merging features: {e}')
        raise

if __name__ == '__main__':
    main()
