"""Script to merge all datasets to one and save it to parquete"""

import logging
from pathlib import Path
import polars as pl

logging.basicConfig(level=logging.INFO)


PROCESSED_DIR = Path(__file__).parent.parent.parent / 'data' / 'processed'
OUTPUT_FILE = PROCESSED_DIR / 'train_features.parquet'

def load_and_prepare_generation(path: Path) -> pl.DataFrame:
    df = pl.read_csv(path)
    gen_df = (
        df.group_by('timestamp')
          .agg(pl.col('quantity_MWh').sum().alias('actual_OZE_MWh'))
    )
    gen_df = gen_df.with_columns([
        pl.col('timestamp')
          .str.strip_chars()
          .str.strptime(pl.Datetime)
          .dt.replace_time_zone(None)
    ])
    return gen_df

def load_and_prepare_weather(path: Path) -> pl.DataFrame:
    df = pl.read_csv(path).with_columns([
        pl.col('timestamp')
          .str.strip_chars()
          .str.strptime(pl.Datetime)
          .dt.replace_time_zone(None)
    ])
    return df

def load_and_prepare_forecast(path: Path) -> pl.DataFrame:
    df = pl.read_csv(path).rename({'quantity': 'forecast_total_Mwh'}).with_columns([
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
        logging.info(f'Merged columns: {merged.columns}')
        logging.info(f'Sample:\n{merged.head()}')

        merged.write_parquet(OUTPUT_FILE)
        logging.info(f'Features set saved as: {OUTPUT_FILE}')
    except Exception as e:
        logging.error(f'Error in merging features: {e}')
        raise

if __name__ == '__main__':
    main()
