# GreenGrid Forecast

GreenGrid Forecast is a lightweight, modular data pipeline designed to forecast energy consumption and renewable energy (PV/Wind) production based on historical and weather data.  
The project focuses on providing accurate short-term and medium-term predictions for the energy sector, with an emphasis on scalability and real-world applications.

> **⚠️ Project Status: Under Construction / Migration**
> This project is currently transitioning from a monolithic script to a modular architecture.
> While the core data extraction logic is functional, the orchestration (Airflow) and visualization layers are being refactored.

##  Architecture Overview

* **Data Ingestion:** Automated scrapers/API clients for PSE and ENTSO-E.
* **Processing:** Python (**Polars/Pandas**) for high-performance time-series manipulation.
* **Forecasting:** Prophet / ARIMA implemented for price & generation trends.
* **Storage:** Parquet (Silver Layer) for analytical queries.
* **Infrastructure:** Dockerized environment (Development phase).

##  Data Sources
This pipeline integrates complex domain-specific data sources:
1.  **PSE (Polskie Sieci Elektroenergetyczne):** Real-time system imbalance, CRO (Operational Reserve), and generation data.
2.  **TGE (Towarowa Giełda Energii):** Day-Ahead Market (Rdn) prices.
3.  **ENTSO-E Transparency Platform:** Cross-border flows and European load data.
4.  **Open-Meteo API:** Weather parameters affecting RES generation.

##  Roadmap & Current Focus
- [x] **Core:** Automated extraction of PSE & ENTSO-E datasets.
- [x] **Logic:** Basic forecasting model for imbalance prices.
- [ ] **Architecture:** Migrating ETL pipelines to Apache Airflow.
- [ ] **Visualization:** Building a Streamlit dashboard for traders.

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
