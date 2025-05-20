import xml.etree.cElementTree as ET
from pathlib import Path
import polars as pl
from datetime import datetime, timedelta

xml_files = [
    "installed_capacity_a01",
    ]

ns = {"ns":"urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"}

def parse_xml_file(root: ET.Element, ns: dict):
    for ts in root.findall("ns:TimeSeries", ns):
        business_type = ts.find("ns:businessType", ns).text
        currency = ts.find("ns:currency_Unit.name", ns).text
        price_unit = ts.find("ns:price_Measure_Unit.name", ns).text
        curve_type = ts.find("ns:curveType", ns).text

        period = ts.find("ns:Period", ns)
        start = period.find("ns:timeInterval/ns:start", ns).text
        start_time = datetime.fromisoformat(start)
        resolution_minutes = 60  # PT60M

        for pt in period.findall("ns:Point", ns):
            pos = int(pt.find("ns:position", ns).text)
            price = float(pt.find("ns:price.amount", ns).text)
            timestamp = (start_time + timedelta(minutes=(pos - 1) * resolution_minutes)).isoformat()

            data.append({
                "timestamp": timestamp,
                "price": price,
                "business_type": business_type,
                "currency": currency,
                "price_unit": price_unit,
                "curve_type": curve_type
            })

if __name__=="__main__":
    # path to XML files
    xml_file_path = Path(__file__).parent.parent.parent / "data" / "raw"
    xml_file_path.mkdir(parents=True, exist_ok=True)
    output_dir_path = Path(__file__).parent.parent.parent / "data" / "processed"
    output_dir_path.mkdir(parents=True, exist_ok=True)

    data = []

    for file in xml_files:
        tree = ET.parse(xml_file_path / (file + ".xml"))
        root = tree.getroot()
        
        parse_xml_file(root, ns)

    output_file_path = output_dir_path / "prices.csv"

    df = pl.DataFrame(data)
    df.write_csv(output_file_path)

    print(f"Zapisano dane do {output_file_path}")
