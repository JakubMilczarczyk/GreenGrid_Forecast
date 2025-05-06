import requests
from datetime import datetime, timedelta
from pathlib import Path
import polars as pl
import json

# Lokalizacja (Kopenhaga, Dania)
LAT = 55.6761
LON = 12.5683

# Czas: ostatnia doba
now = datetime.now()
start = (now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
end = now.strftime("%Y-%m-%dT%H:%M")

# Parametry
params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": start.split("T")[0],
    "end_date": end.split("T")[0],
    "hourly": ",".join([
        "wind_speed_10m",
        "cloud_cover",
        "wave_height",
        "shortwave_radiation",
        "temperature_2m"
    ]),
    "timezone": "UTC"
}

url = "https://api.open-meteo.com/v1/marine"

response = requests.get(url, params=params)
response.raise_for_status()
weather_json = response.json()

# Zapis JSON (opcjonalnie)
# Path("data/raw").mkdir(parents=True, exist_ok=True)
# with open("data/raw/weather_dk1.json", "w") as f:
#     json.dump(weather_json, f, indent=2)

# Konwersja do CSV
hourly = weather_json["hourly"]
df = pl.DataFrame({
    "timestamp": hourly["time"],
    "wind_speed": hourly["wind_speed_10m"],
    "cloud_cover": hourly["cloud_cover"],
    "wave_height": hourly.get("wave_height", [None] * len(hourly["time"])),
    "solar_radiation": hourly.get("shortwave_radiation", [None] * len(hourly["time"])),
    "temperature": hourly["temperature_2m"]
})

# Zapis CSV
Path("data/processed").mkdir(parents=True, exist_ok=True)
df.write_csv("data/processed/weather_dk1.csv")

print("✔️ Dane pogodowe zapisane: data/processed/weather_dk1.csv")
