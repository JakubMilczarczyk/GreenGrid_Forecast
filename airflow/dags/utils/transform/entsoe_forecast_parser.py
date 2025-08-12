import xml.etree.ElementTree as ET
import os
from pathlib import Path
import polars as pl
from datetime import datetime, timedelta
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths for XML input and CSV output
DATA_DIR = Path(os.getenv("DATA_DIR", "/opt/airflow/shared/data"))
XML_DIR = DATA_DIR / "raw"
XML_DIR.mkdir(parents=True, exist_ok=True)
XML_FILE_PATH = XML_DIR / "generation_forecast.xml"

OUTPUT_DIR = DATA_DIR / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE_PATH = OUTPUT_DIR / "forecast_generation_total.csv"

ns = {"ns": "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"}

if __name__=="__main__":

    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()

    data = []

    for ts in root.findall("ns:TimeSeries", ns):
        business_type = ts.find("ns:businessType", ns).text
        period = ts.find("ns:Period", ns)
        start = period.find("ns:timeInterval/ns:start", ns).text

        start_time = datetime.fromisoformat(start)
        resolution = period.find("ns:resolution", ns).text  # PT60M → 60 minut
        interval_minutes = int(resolution[2:-1])

        for pt in period.findall("ns:Point", ns):
            pos = int(pt.find("ns:position", ns).text)
            qty = float(pt.find("ns:quantity", ns).text)
            timestamp = start_time + timedelta(minutes=(pos - 1) * interval_minutes)
            data.append((timestamp.isoformat(), qty, business_type))

    # Save CSV
    df = pl.DataFrame(data, orient="row", schema=["timestamp", "quantity", "business_type"])
    df.write_csv(OUTPUT_FILE_PATH)

    logging.info(f"Agregated forecast data saved as: {OUTPUT_FILE_PATH}")
