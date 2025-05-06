import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path

# Załaduj klucz API z pliku .env
load_dotenv()
api_key = os.getenv("ENTSOE_API_KEY")

if not api_key:
    raise ValueError("Brak klucza ENTSOE_API_KEY w pliku .env")

# Parametry zapytania
area = "10YDK-1--------W"  # DK1
document_type = "A75"      # Actual generation per type
process_type = "A16"       # Realised

# Zakres czasowy – 2 dni wstecz do dziś
end = datetime.now().replace(hour=0, minute=0)  # dziś 00:00
start = end - timedelta(days=1)                   # wczoraj 00:00

start_str = start.strftime("%Y%m%d%H%M")
end_str = end.strftime("%Y%m%d%H%M")

# Budowa URL
url = "https://web-api.tp.entsoe.eu/api"
params = {
    "securityToken": api_key,
    "documentType": document_type,
    "processType": process_type,
    "in_Domain": area,
    "out_Domain": area,
    "periodStart": start_str,
    "periodEnd": end_str
}

# Wysyłanie zapytania
print("Wysyłam zapytanie do ENTSO-E...")
response = requests.get(url, params=params)

if response.status_code == 200:
    output_path = Path("data/raw/entsoe_actual_generation.xml")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"✅ Dane zapisane do {output_path}")
else:
    print(f"❌ Błąd {response.status_code}: {response.text}")
