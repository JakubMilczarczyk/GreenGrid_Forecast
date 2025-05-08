import xml.etree.ElementTree as ET
import polars as pl
from datetime import datetime, timedelta

# Ścieżka do pliku XML
xml_file = "data/raw/actual_generation.xml"

# Parsowanie XML
tree = ET.parse(xml_file)
root = tree.getroot()

# ENTSO-E używa przestrzeni nazw
ns = {"ns": "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"}

# Mapowanie kodów PSR (Production Source)
psr_mapping = {
    "B01": "Fossil Brown Coal/Lignite",
    "B02": "Fossil Hard coal",
    "B03": "Fossil Gas",
    "B04": "Fossil Oil",
    "B05": "Fossil Oil shale",
    "B06": "Fossil Peat",
    "B07": "Geothermal",
    "B08": "Hydro Pumped Storage",
    "B09": "Hydro Run-of-river and poundage",
    "B10": "Hydro Water Reservoir",
    "B11": "Marine",
    "B12": "Nuclear",
    "B13": "Other renewable",
    "B14": "Solar",
    "B15": "Waste",
    "B16": "Wind Offshore",
    "B17": "Wind Onshore",
    "B18": "Other",
    "B19": "Biomass",
}

data = []

# Parsowanie danych
for ts in root.findall("ns:TimeSeries", ns):
    psr_code = ts.find("ns:MktPSRType/ns:psrType", ns).text
    psr_name = psr_mapping.get(psr_code, psr_code)
    business_type = ts.find("ns:businessType", ns).text
    period = ts.find("ns:Period", ns)

    start = period.find("ns:timeInterval/ns:start", ns).text
    start_time = datetime.fromisoformat(start.replace("Z", "+00:00"))
    resolution_minutes = 15  # PT15M

    for pt in period.findall("ns:Point", ns):
        pos = int(pt.find("ns:position", ns).text)
        qty = float(pt.find("ns:quantity", ns).text)
        timestamp = start_time + timedelta(minutes=(pos - 1) * resolution_minutes)
        data.append((timestamp.isoformat(), qty, psr_code, psr_name, business_type))

# Tworzenie DataFrame z Polars
df = pl.DataFrame(
    data,
    orient="row",
    schema=["timestamp", "quantity", "psr_code", "psr_name", "business_type"]
)

# Zapis do CSV
output_path = "data/processed/entsoe_actual_generation.csv"
df.write_csv(output_path)

print(f"Zapisano dane do {output_path}")
