# Environment Snapshot – 2024-08-13

Purpose: Airflow environment for processing energy demand and weather data.

## 1. Active Services

airflow-scheduler

airflow-webserver

airflow-worker

postgres (Airflow metadata)

redis (task queue)

shared (data & logs volume)

## 2. Key Paths

Project root: /GreenGridForecast

shared volume:

Local: ./shared

In container: /opt/airflow/shared

**Note:** `shared/` directory is uses locally now. In future it will be installed as a volume in containers (np. Airflow, UI, prediction_service).

Structure:

shared/
  data/      # raw & processed data  
  models/    # models, metrics & old model's versions
  config/    # JSON/YAML configs  

## 3. Configuration

.env at /GreenGridForecast/.env

Includes ENTSOE_API_KEY & other env vars

Mounted via docker-compose.yml

## 4. Dockerfile Mods

Base: apache/airflow:2.9.2-python3.11

Copied requirements.txt → /tmp/

Installed deps with virtualenvs.create false

## 5. Running
docker compose up -d


    Airfow UI: http://localhost:8080

    Default creds: airflow / airflow (change for prod)

## 6. Debug

**Airflow logs**:

    docker compose logs airflow-scheduler
    docker compose logs airflow-worker


Task logs → Airflow UI (**Logs** tab)

## 7. Last DAG Test

    DAG 'etl_pipeline': ✅ success

    DAG 'train_mode_pipeline': ✅ success

**Note**: Update after any change in shared, .env, docker-compose.yml, or Dockerfile.