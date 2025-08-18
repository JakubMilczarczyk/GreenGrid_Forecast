# GreenGrid Forecast

GreenGrid Forecast is a modular, production-oriented data platform for forecasting energy consumption and renewable generation (PV/Wind).  
It combines **data pipelines, machine learning models, and forecasting tools** to deliver short-term and medium-term energy predictions.  

The project is designed with **scalability, reproducibility, and real-world deployment** in mind.

---

## Architecture Overview

- **Workflow Orchestration:** Apache Airflow (DAGs for ETL, model training, forecasting)
- **Data Processing:** Python (Polars, Pandas)
- **Model Training:** scikit-learn (Linear Regression prototype, expandable to advanced ML/MLops stack)
- **Forecasting Pipeline:** Dedicated DAG producing forecast outputs (benchmarks vs. ENTSO-E)
- **Storage:** Parquet (transition to CSV underway), structured project directories, extendable to S3
- **Visualization:** Streamlit (future web UI)
- **Deployment:** Docker Compose (development), CI/CD ready (cloud-native deployment planned)

---

## Repository Structure

GreenGridForecast/
├── dags/ # Airflow DAG definitions
│ ├── etl_pipeline.py
│ ├── train_model_pipeline.py
│ ├── forecast_pipeline.py
│ └── utils/ # Python scripts for pipelines
│ ├── etl/
│ ├── train/
│ └── forecast/
├── docs/ # Technical documentation
│ ├── architecture.md
│ ├── services.md
│ ├── progress.md
│ ├── readme_dev_setup.md
│ └── notes/ (optional developer notes)
├── shared/ # Shared data directory (mounted in Airflow)
│ ├── data/
│ ├── models/
│ └── forecasts/
├── docker-compose.yml
├── README.md
└── LICENSE

---

## Current Roadmap (MVP Phase)

1. ✅ **Automated ETL** – extraction, cleaning, and saving of historical energy & weather data (Airflow DAG)
2. ✅ **Model training DAG** – linear regression baseline with metrics & benchmarks
3. ✅ **Forecast pipeline** – predictions saved alongside benchmarks (ENTSO-E baseline)
4. 🚧 **Refactor storage format** – transition from Parquet → CSV for portability
5. 🚧 **Documentation** – services, setup, and progress tracking (`docs/`)
6. ⏩ **Visualization (Streamlit UI)** – real-time forecasts and historical trends
7. ⏩ **Cloud deployment** – CI/CD integration and scalable hosting

---

##  Data Sources

- [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/) – energy load & production data
- [Open-Meteo API](https://open-meteo.com/) – weather forecasts (free API)
- [ERA5 (Copernicus CDS)](https://cds.climate.copernicus.eu/) – historical reanalysis (optional, advanced)
- [Renewables.ninja](https://www.renewables.ninja/) – PV/Wind simulation profiles (optional)

---

##  Development Setup

Clone and start with Docker:

```bash
git clone https://github.com/your-username/GreenGridForecast.git
cd GreenGridForecast
docker-compose up --build
```

Airflow UI: http://localhost:8080
Default credentials: airflow / airflow

Detailed setup and service documentation: docs/readme_dev_setup.md

## Documentation
Key technical documentation lives in docs/:

architecture.md – system architecture

services.md – services description & usage

progress.md – project progress log

readme_dev_setup.md – local setup instructions

## License
This project is licensed under a Restricted Private License (see LICENSE).
All rights reserved. Unauthorized use, distribution, or reproduction of code, ideas, or architecture is strictly prohibited.

Contact
Author: Jakub Milczarczyk
LinkedIn: www.linkedin.com/in/jakub-milczarczyk
