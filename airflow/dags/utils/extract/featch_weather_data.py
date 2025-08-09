import requests
from datetime import datetime, timedelta
import polars as pl
import json
import logging
import os

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_DIR = os.getenv("DATA_DIR", "/opt/shared/data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

if __name__=="__main__":

    # Localization – Copenhagen (DK1)
    LAT = 55.6761
    LON = 12.5683

    # Time range
    now = datetime.now()
    start = (now - timedelta(days=30)).strftime("%Y-%m-%d")
    end = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    # Weather parameters
    # https://open-meteo.com/en/docs
    HOURLY_PARAMS = ",".join([
        "temperature_2m",
        "cloud_cover",
        "shortwave_radiation",
        "wind_speed_10m",
        "wind_speed_100m",
        "wind_direction_10m"
    ])

    params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": start,
        "end_date": end,
        "hourly": HOURLY_PARAMS,
        "timezone": "UTC",
        "interval": 15
    }

    url = "https://api.open-meteo.com/v1/forecast"

    # Extracting weather data
    response = requests.get(url, params=params)
    response.raise_for_status()
    weather_json = response.json()

    # Saving raw data    
    with open(RAW_DATA_DIR / "weather_dk1.json", "w") as f:
        json.dump(weather_json, f, indent=2)
        logging.info(f'Weather data saved as {RAW_DATA_DIR / "weather_dk1.json"}')

    # Converting to DataFrame
    hourly = weather_json["hourly"]
    df = pl.DataFrame({
        "timestamp": hourly["time"],
        "temperature_2m": hourly["temperature_2m"],
        "cloud_cover": hourly["cloud_cover"],
        "shortwave_radiation": hourly["shortwave_radiation"],
        "wind_speed_10m": hourly["wind_speed_10m"],
        "wind_speed_100m": hourly["wind_speed_100m"],
        "wind_direction_10m": hourly["wind_direction_10m"]
    })

    # Saving processed data
    df.write_csv(PROCESSED_DATA_DIR / "weather_dk1.csv")

    logging.info(f'Weather for DK1 saved as: {PROCESSED_DATA_DIR / "weather_dk1.csv"}')
