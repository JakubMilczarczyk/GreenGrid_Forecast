import os
import requests
import logging
from datetime import datetime
from typing import Optional
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

logger = logging.getLogger("entsoe_api")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Mapowanie documentType -> domyślny processType
DOCUMENT_PROCESS_MAP = {
    "A65": "A01",  # Load Forecast -> Day-ahead
    "A75": "A16",  # Actual Generation per Type -> Realised
    "A71": "A01",  # Generation Forecast -> Day-ahead
    "A69": "A16",  # Load Unavailability -> Realised
}

# Typy dokumentów wymagające out_Domain
REQUIRES_OUT_DOMAIN = {"A65", "A75"}

class EntsoeAPI:
    def __init__(self, api_key: str, country_code: str):
        self.api_key = api_key
        self.country_code = country_code
        self.base_url = "https://web-api.tp.entsoe.eu/api"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def _format_datetime(self, date_str: str) -> str:
        dt = datetime.strptime(date_str, "%Y.%m.%d")
        return dt.strftime("%Y%m%d%H%M")

    def fetch_data(
        self,
        document_type: str,
        process_type: Optional[str] = None,
        start_date: str = "2025.04.01",
        end_date: str = "2025.04.30",
        out_domain: Optional[str] = None,
        output_path: Optional[str] = None,
        output_format: str = "csv"
    ):
        logger.info(f"Pobieranie danych: documentType={document_type}, processType={process_type or 'auto'}")

        if not process_type:
            process_type = DOCUMENT_PROCESS_MAP.get(document_type)
            if not process_type:
                raise ValueError(f"Brak domyślnego processType dla documentType={document_type}")
            logger.debug(f"Użyto domyślnego processType: {process_type}")

        params = {
            "documentType": document_type,
            "processType": process_type,
            "in_Domain": self.country_code,
            "periodStart": self._format_datetime(start_date),
            "periodEnd": self._format_datetime(end_date),
            "securityToken": self.api_key,
        }

        if document_type in REQUIRES_OUT_DOMAIN:
            if not out_domain:
                logger.warning("out_Domain nie podany, ale wymagany - użycie in_Domain jako fallback")
                out_domain = self.country_code
            params["out_Domain"] = out_domain
            logger.debug(f"Użyto out_Domain: {out_domain}")

        logger.debug(f"Parametry żądania: {params}")

        response = requests.get(self.base_url, headers=self.headers, params=params)

        if response.status_code != 200:
            logger.error(f"Błąd pobierania: {response.status_code} - {response.text}")
            raise Exception(f"Zapytanie nie powiodło się: {response.status_code}")

        logger.info("Dane pobrane poprawnie. Przetwarzanie odpowiedzi...")

        try:
            df = pd.read_xml(StringIO(response.text))
            logger.debug(f"Wczytano dane do DataFrame Polars: {df.shape}")
        except Exception as e:
            logger.error(f"Błąd przetwarzania XML: {e}")
            raise

        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            if output_format == "csv":
                df.to_csv(output_path)
                logger.info(f"Dane zapisane do CSV: {output_path}")
            elif output_format == "parquet":
                df.to_parquet(output_path)
                logger.info(f"Dane zapisane do Parquet: {output_path}")
            else:
                raise ValueError(f"Nieobsługiwany format wyjściowy: {output_format}")

        return df

# Przykładowe użycie:
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("ENTSOE_API_KEY")
    client = EntsoeAPI(api_key=api_key, country_code="10YDK-1--------W")
    df = client.fetch_data(
        document_type="A75",
        start_date="2025.04.01",
        end_date="2025.04.30",
        output_path="data/raw/dk1_generation_actual_2025_04.csv"
    )
