"""Script to merge all datasets to one and save it to parquete"""

from pathlib import Path
import polars as pl

processed_data_dir = Path(__file__).parent.parent.parent / 'data' / 'processed'
processed_data_dir.mkdir(parents=True, exist_ok=True)

output_parquet_dir = Path(__file__).parent.parent.parent / 'data' / 'processed'
output_parquet_dir.mkdir(parents=True, exist_ok=True)
output_parquet = output_parquet_dir / 'train_features.parquet'

actual_generation_data = processed_data_dir / 'entsoe_actual_generation.csv'
benchmark_forecast_total_generation = processed_data_dir / 'forecast_generation_total.csv'
prices = processed_data_dir / 'prices.csv'
forecast_weather_data = processed_data_dir / 'weather_dk1.csv'

df_generation = pl.read_csv(actual_generation_data)
oze_df = (
    df_generation
    .filter(pl.col('psr_code').is_in(['B11', 'B16', 'B17']))
    .group_by('timestamp')
    .agg(pl.col('quantity_MWh').sum().alias('actual_OZE_MWh'))
)
oze_df = oze_df.with_columns([
    pl.col('timestamp')
    .str.strip_chars()
    .str.strptime(pl.Datetime)
    .dt.replace_time_zone(None)
])

df_weather = pl.read_csv(forecast_weather_data).with_columns([
    pl.col('timestamp')
    .str.strip_chars()
    .str.strptime(pl.Datetime)
    .dt.replace_time_zone(None)
])

df_forecast = pl.read_csv(benchmark_forecast_total_generation).rename({'quantity': 'forecast_total_MWh'}).with_columns([
    pl.col('timestamp')
    .str.strip_chars()
    .str.strptime(pl.Datetime)
    .dt.replace_time_zone(None)
])

df_prices = pl.read_csv(prices).with_columns([
    pl.col('timestamp')
    .str.strip_chars()
    .str.strptime(pl.Datetime)
    .dt.replace_time_zone(None)
])

merged = (
    df_weather
    .join(df_forecast, on='timestamp', how='left')
    .join(oze_df, on='timestamp', how='left')
    .join(df_prices, on='timestamp', how='left')
)

merged = merged.with_columns([
    pl.col('timestamp').dt.hour().alias('hour'),
    pl.col('timestamp').dt.weekday().alias('day_of_week'),
    (pl.col('timestamp').dt.weekday() > 5).alias('is_weekend'),    # TODO add is_holiday from workalendar
])

print(merged.columns)
print(merged.head())

merged.write_parquet(output_parquet)
print(f'Features set saved as: {output_parquet}')