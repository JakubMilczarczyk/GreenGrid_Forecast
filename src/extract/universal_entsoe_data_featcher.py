import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import json

# Wczytaj klucz API z pliku .env
load_dotenv()
API_KEY = os.getenv("ENTSOE_API_KEY")

# Stałe
BASE_URL = "https://web-api.tp.entsoe.eu/api"
DOMAIN = "10YDK-1--------W"
RAW_DATA_DIR = Path("data/raw")
CONFIG_FILE = Path(__file__).parent.parent.parent / "config" / "entsoe_requests.json"
# CONFIG_FILE = Path("config/entsoe_requests.json")

# Utwórz folder na dane, jeśli nie istnieje
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch_entsoe_data(document_type: str, process_type: str) -> str:
    now = datetime.now()
    start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    params = {
        "securityToken": API_KEY,
        "documentType": document_type,
        "processType": process_type,
        "in_Domain": DOMAIN,
        "out_Domain": DOMAIN,
        "periodStart": start.strftime("%Y%m%d%H%M"),
        "periodEnd": end.strftime("%Y%m%d%H%M"),
    }


    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.text


def main():
    # Wczytaj konfigurację zapytań
    with open(CONFIG_FILE, "r") as f:
        queries = json.load(f)

    for query in queries:
        name = query["name"]
        document_type = query["documentType"]
        process_type = query["processType"]

        filename = RAW_DATA_DIR / f"{name}.xml"
        if filename.exists():
            print(f"[SKIP] {name} już istnieje.")
            continue

        print(f"[INFO] Pobieranie danych: {name}")
        try:
            xml_data = fetch_entsoe_data(document_type, process_type)
            with open(filename, "w") as f:
                f.write(xml_data)
            print(f"[OK] Zapisano do {filename}")
        except requests.HTTPError as e:
            print(f"[ERROR] Nie udało się pobrać danych dla {name}: {e}")


if __name__ == "__main__":
    main()
