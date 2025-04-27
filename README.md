# GreenGrid Forecast

GreenGrid Forecast is a lightweight, modular data pipeline designed to forecast energy consumption and renewable energy (PV/Wind) production based on historical and weather data.  
The project focuses on providing accurate short-term and medium-term predictions for the energy sector, with an emphasis on scalability and real-world applications.

## Architecture Overview
- **Data Extraction:** Airflow (scheduled ETL pipelines)
- **Data Processing:** Python (Polars, Pandas)
- **Forecasting Models:** Prophet / ARIMA (expandable to ML models)
- **Storage:** Parquet/CSV (local; S3 planned for later phases)
- **Visualization:** Streamlit Web App
- **Deployment:** Docker Compose (development), scalable cloud hosting (future)

## Project Roadmap
1. Automated extraction and cleaning of historical energy and weather datasets
2. Modular ETL pipelines managed by Apache Airflow
3. Forecasting model development and evaluation
4. Web-based dashboard displaying real-time forecasts and historical trends
5. Public demo deployment and documentation

## Data Sources
- [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/) – energy load, production data by country
- [Open-Meteo API](https://open-meteo.com/) – free and simple weather API
- [ERA5 (Copernicus Climate Data Store)](https://cds.climate.copernicus.eu/) – historical weather reanalysis (optional advanced version)
- [Renewables.ninja](https://www.renewables.ninja/) – simulated PV/Wind production profiles (optional)

## Installation (Development Version)

```bash
git clone https://github.com/your-username/GreenGridForecast.git
cd GreenGridForecast
docker-compose up --build
```

The project uses Docker containers for easy reproducibility and environment management.

## License
This project is licensed under a Restricted Private License (see LICENSE file for full terms).
All rights reserved. Unauthorized use, distribution, or reproduction of code, ideas, or architecture is strictly prohibited.

Contact
Author: Jakub Milczarczyk
LinkedIn: www.linkedin.com/in/jakub-milczarczyk
