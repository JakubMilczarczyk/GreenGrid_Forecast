# Services Overview

## Airflow
- **Cel:** Orkiestracja procesów ETL i trenowania modeli.
- **Kontenery:** `airflow-webserver`, `airflow-scheduler`, `airflow-worker`, `airflow-init`.
- **Kluczowe ścieżki i volumes:**
  ```yaml
  volumes:
    - ./airflow/dags:/opt/airflow/dags
    - ./airflow/logs:/opt/airflow/logs
    - ./airflow/plugins:/opt/airflow/plugins
    - ./shared/data:/opt/airflow/shared/data
    - ./shared/models:/opt/airflow/shared/models

## Shared Structure
shared/
├── data/
│   ├── raw/          # Dane surowe z API/ETL
│   ├── processed/    # Dane po transformacjach
│   └── splits/       # Dane podzielone na train/test
└── models/
    ├── saved_models/ # Modele zapisane po treningu
    ├── metrics/      # Wyniki ewaluacji modeli
    └── versions/     # Archiwalne wersje modeli