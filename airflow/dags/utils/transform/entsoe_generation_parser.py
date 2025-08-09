import xml.etree.ElementTree as ET
from pathlib import Path
import polars as pl
from datetime import datetime, timedelta
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Filepath to XML
xml_file_path = Path(__file__).parent.parent.parent / "data" / "raw"
xml_file_path.mkdir(parents=True, exist_ok=True)
xml_file = xml_file_path / "actual_generation.xml"

# Pharsing XML
tree = ET.parse(xml_file)
root = tree.getroot()

# ENTSO-E uses namespaces, so we need to define it
# ns = {"ns": "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"}
ns = {"ns": root.tag.split("}")[0].strip("{")}

# Mapping psr codes (Production Source)
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

if __name__=="__main__":

    # Pharsing XML and extracting data
    for ts in root.findall("ns:TimeSeries", ns):
        psr_code = ts.find("ns:MktPSRType/ns:psrType", ns)
        psr_code = psr_code.text if psr_code is not None else "UNKNOWN"

        psr_name = psr_mapping.get(psr_code, psr_code)
        business_type = ts.find("ns:businessType", ns).text
        period = ts.find("ns:Period", ns)

        start = period.find("ns:timeInterval/ns:start", ns).text
        start_time = datetime.fromisoformat(start.replace("Z", "+00:00"))
        
        resolution = period.find("ns:resolution", ns).text
        if resolution == "PT15M":
            res_minutes = 15
        elif resolution == "PT30M":
            res_minutes = 30
        elif resolution == "PT60M":
            res_minutes = 60
        else:
            raise VaueError(f"Unnown rosolution: {resolution}")

        for pt in period.findall("ns:Point", ns):
            pos = int(pt.find("ns:position", ns).text)
            qty = float(pt.find("ns:quantity", ns).text)
            timestamp = (start_time + timedelta(minutes=(pos - 1) * res_minutes)).isoformat()
            data.append((timestamp, qty, psr_code, psr_name, business_type))

    # Converting to DataFrame
    df = pl.DataFrame(
        data,
        orient="row",
        schema=["timestamp", "quantity", "psr_code", "psr_name", "business_type"]
    )

    # Aggregating data to hourly
    df = df.with_columns(pl.col("timestamp").cast(pl.Datetime))
    df_hourly = (
        df.group_by_dynamic("timestamp", every="1h", period="1h", group_by=["psr_code", "psr_name", "business_type"])
        .agg(pl.col("quantity").mean().alias("quantity_MWh"))
        .sort("timestamp")
    )

    # Saveing as CSV
    output_dir_path = Path(__file__).parent.parent.parent / "data" / "processed"
    output_dir_path.mkdir(parents=True, exist_ok=True)

    output_file_path = output_dir_path / "entsoe_actual_generation.csv"
    df_hourly.write_csv(output_file_path)

    logging.info(f"Data saved as: {output_file_path}")
