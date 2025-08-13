# Services Overview – GGF Energy Demand Project

**Cel dokumentu:**  
Opis wszystkich usług wchodzących w skład środowiska, sposób ich uruchamiania, debugowania oraz zależności między nimi.


## Airflow
- **Cel:** Orkiestracja procesów ETL i trenowania modeli.
- **Obraz bazowy:** `apache/airflow:2.9.2-python3.11`
- **Dodatki:** 
  - Install dependencies from `requirements.txt`
  - Install volume `shared` for data nad logs
- **Kontenery:** `airflow-webserver`, `airflow-scheduler`, `airflow-worker`, `airflow-init`.
- **Ports:**
  - Webserver: `8080`
- **Kluczowe ścieżki i volumes:**
  ```yaml
  volumes:
    - ./airflow/dags:/opt/airflow/dags
    - ./airflow/logs:/opt/airflow/logs
    - ./airflow/plugins:/opt/airflow/plugins
    - ./shared/data:/opt/airflow/shared/data
    - ./shared/models:/opt/airflow/shared/models
  ```

- **Running:**
```bash
docker compose up -d
```

- **Debuggung:**
```bash
docker compose logs airflow-scheduler
docker compose logs airflow-worker
```
  
  UI: http://localhost:8080 – login: airflow / airflow
  

## Postgres (Airflow Metadata DB)
- **Cel:** Przechowywanie metadanych Airflow (DAG's status, task's history, veriabes).

- **Obraz:** `postgres:14`

- **Port:** `5432`

- **Ścieżka w kontenerze:** `/var/lib/postgresql/data` (trwały volume)

- **Running:** automatycznie przez docker compose

- **Debuging:**
```bash
docker compose logs postgres
```


## Redis
- **Opis:** Broker kolejek dla Airflow Celery Executor.

- **Obraz:** `redis:latest`

- **Port:** `6379`

- **Uruchamianie:** automaticly via docker compose

- **Debugowanie:**
```bash
docker compose logs redis
```


## Shared Volume

- **Opis:** Przestrzeń współdzielona między usługami na dane, logi i pliki konfiguracyjne.

- **Ścieżki:**

  - Lokalnie: `./shared`

  - W kontenerze Airflow: `/opt/airflow/shared`

- **Struktura:**
```bash
shared/
  data/           # Dane źródłowe i przetworzone
  config/         # Konfiguracje
  logs/           # Logi DAG-ów i aplikacji
```


## Streamlit (w przygotowaniu)

- **Opis:** Interaktywny dashboard do wizualizacji wyników przetwarzania.

- **Port:** `8501`

- **Ścieżki w kontenerze:** `/app` – kod aplikacji Streamlit.

- **Uruchamianie (docelowo):**
```bash
docker compose up -d streamlit
```

- **Debugowanie:**
```bash

docker compose logs streamlit
```


**Notatka:** Wszystkie usługi są uruchamiane i kontrolowane przez docker compose.
Zmiana konfiguracji w .env wymaga restartu usług:
```bash

docker compose down && docker compose up -d
```
