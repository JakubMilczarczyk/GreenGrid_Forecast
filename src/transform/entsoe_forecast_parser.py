import xml.etree.ElementTree as ET
from pathlib import Path
import polars as pl
from datetime import datetime, timedelta

# Pliki
# xml_path = "data/raw/generation_forecast.xml"
# output_csv = "data/processed/entsoe_generation_forecast_total.csv"
xml_dir_path = Path(__file__).parent.parent.parent / "data" / "raw"
xml_dir_path.mkdir(parents=True, exist_ok=True)
xml_path = xml_dir_path / "generation_forecast.xml"

output_csv_dir = Path(__file__).parent.parent.parent / "data" / "processed"
output_csv_dir.mkdir(parents=True, exist_ok=True)
output_csv = output_csv_dir / "entsoe_generation_forecast_total.csv"

ns = {"ns": "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"}

if __name__=="__main__":

    tree = ET.parse(xml_path)
    root = tree.getroot()

    data = []

    for ts in root.findall("ns:TimeSeries", ns):
        business_type = ts.find("ns:businessType", ns).text
        period = ts.find("ns:Period", ns)

        start_time = datetime.fromisoformat(
            period.find("ns:timeInterval/ns:start", ns).text.replace("Z", "+00:00")
        )
        resolution = period.find("ns:resolution", ns).text  # PT60M → 60 minut
        interval_minutes = int(resolution[2:-1])

        for pt in period.findall("ns:Point", ns):
            pos = int(pt.find("ns:position", ns).text)
            qty = float(pt.find("ns:quantity", ns).text)
            timestamp = start_time + timedelta(minutes=(pos - 1) * interval_minutes)
            data.append((timestamp.isoformat(), qty, business_type))

    # Zapis CSV
    df = pl.DataFrame(data, orient="row", schema=["timestamp", "quantity", "business_type"])
    df.write_csv(output_csv)

    print(f"✔️ Forecast agregowany zapisany: {output_csv}")
