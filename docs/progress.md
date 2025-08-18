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

