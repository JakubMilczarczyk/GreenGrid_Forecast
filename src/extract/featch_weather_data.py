import requests
from datetime import datetime, timedelta
from pathlib import Path
import polars as pl
import json

# 📍 Lokalizacja – Kopenhaga (DK1)
LAT = 55.6761
LON = 12.5683

# 🕒 Zakres czasowy
now = datetime.now()
start = (now - timedelta(days=3)).strftime("%Y-%m-%d")
end = (now + timedelta(days=1)).strftime("%Y-%m-%d")

# 🌦️ Parametry pogodowe
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
    "interval": 15  # co 15 minut
}

url = "https://api.open-meteo.com/v1/forecast"

# 📡 Pobranie danych
response = requests.get(url, params=params)
response.raise_for_status()
weather_json = response.json()

# 📁 Zapis JSON (opcjonalnie)
Path("data/raw").mkdir(parents=True, exist_ok=True)
with open("data/raw/weather_dk1.json", "w") as f:
    json.dump(weather_json, f, indent=2)

# 📄 Konwersja do Polars DataFrame
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

# 💾 Zapis CSV
Path("data/processed").mkdir(parents=True, exist_ok=True)
df.write_csv("data/processed/weather_dk1.csv")

print("✔️ Pogoda DK1 zapisana: data/processed/weather_dk1.csv")
