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
