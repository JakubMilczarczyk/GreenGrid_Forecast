# Postęp prac nad projektem

## Data: 2025-08-18

### Wykonane działania
- Stworzono nowy DAG `forecast_pipeline` w Airflow.
- DAG uruchamia pipeline predykcji poprzez `run_forecast`.
- Dodano weryfikację istnienia wymaganych danych i modelu w kodzie (prace trwają).
- Część skryptów została zmodyfikowana, aby poprawnie obsługiwać ścieżki plików.

### Aktualny status
- DAG `forecast_pipeline` nie wykonuje się poprawnie z powodu problemów ze ścieżkami do danych.
- Konieczne jest sprawdzenie konfiguracji ścieżek w kodzie i/lub plikach docker-compose.

### Kolejne kroki
1. Naprawić obsługę ścieżek do danych i modeli (w kodzie lub docker volumes).
2. Zweryfikować poprawność działania DAGa po poprawkach.
3. Utrzymać dokumentację postępu w pliku `docs/progress.md`.

## 2025-08-23

### Wykonane działania

- Naprawiono skrypt transformujący dane `actual_generation.xml -> Parquet`, dodając `if __name__ == "__main__"`.
- Zweryfikowano działanie ETL w `etl_pipeline` i `train_model_pipeline`.
- Zaktualizowano skrypt treningowy modelu:
  - Dane treningowe i testowe (`x_train.parquet`, `x_test.parquet`) wczytywane poprawnie.
  - Model LinearRegression zapisuje plik `.joblib`.
  - Metryki i benchmarki zapisane w JSON i CSV.
- Stworzono nowy DAG `forecast_pipeline`:
  - Funkcja `run_forecast` przepuszcza dane `x_test.parquet` przez wytrenowany model.
  - Prognozy zapisywane w `forecasts/latest_forecast.parquet`.
  - Dodano walidację istnienia modelu i danych (`check_model`, `check_data`).
- Zidentyfikowano problem ze ścieżkami w Dockerze, potwierdzono poprawne montowanie katalogów `shared/data/splits`.

### Kolejne kroki
1. UI Streamlit – MVP + wczytywanie danych i wykres.
2. Kolejne 1–2 dni: Integracja z Airflow API → przycisk triggerowania prognozy.
3. Następnie: Mapa architektury + diagram przepływu danych.
4. Na koniec: Prezentacja w PowerPoint / Google Slides.

## Data: 2025-08-24

### Wykonane działania
- Uruchomiono nowy serwis Prediction Service w kontenerze Docker.
- Dockerfile został zmodyfikowany pod kątem instalacji zależności i zgodności z `.env`.
- Stworzono szablony plików `main.py`, `config.py` i struktury aplikacji zgodnie z zasadami clean code i SOLID.
- Serwis jest przygotowany do komunikacji REST, z logowaniem i możliwością podłączenia do UI Streamlit.

### Aktualny status
- Serwis Prediction Service startuje, ale pada z powodu problemu z brakującą lub niepoprawną zależnością FastAPI w `main.py`.
- Zależności Python/Poetry wymagają weryfikacji i poprawnej instalacji w kontenerze.
- Ścieżki montowanych folderów są prawidłowe i kontener widzi pliki z shared **SPRAWDZIĆ**

### Kolejne kroki
1. Naprawić problem z zależnością FastAPI w serwisie Prediction Service (sprawdzenie `requirements.txt` lub instalacja poprzez Poetry).
2. Zweryfikować instalację wszystkich zależności w Dockerfile (poetry/native lub generowanie `requirements.txt`).
3. Przetestować działanie endpointów REST (`/predict`, `/health`) po poprawnej instalacji zależności.
4. Po stabilizacji serwisu uruchomić UI Streamlit, które będzie odpytywało Prediction Service i prezentowało prognozy.
