# Development Environment Setup – GGF Energy Demand Project

## Cel
Ten dokument opisuje, jak skonfigurować i uruchomić środowisko deweloperskie projektu **GGF Energy Demand Prediction** od zera, korzystając z Docker Compose.

---

## 1. Wymagania wstępne

Przed rozpoczęciem upewnij się, że masz zainstalowane:
- **Docker** ≥ 24.x
- **Docker Compose** (wbudowany w Docker CLI)
- **Git**
- **curl** (do testów API i pobierania plików)
- **Python** ≥ 3.11 (opcjonalnie, jeśli chcesz uruchamiać skrypty lokalnie)

---

## 2. Klonowanie repozytorium

```bash
git clone git@github.com:twoje/repo.git
cd repo
3. Plik .env
Utwórz plik .env w katalogu głównym projektu na podstawie szablonu .env.example:

```bash

cp .env.example .env
```
W pliku `.env` skonfiguruj:

Ścieżki dla volumes (`DATA_DIR`, `MODELS_DIR`, `CONFIG_DIR`)

Uwierzytelnienia (np. `API keys`)

Parametry Airflow (opcjonalnie)

## Struktura katalogów
Twoje lokalne drzewo projektu powinno wyglądać tak:

```arduino

.
├── airflow/
│   ├── dags/
│   ├── logs/
│   ├── plugins/
│   └── Dockerfile.airflow
├── shared/
│   ├── data/
│   ├── models/
│   └── config/
├── docs/
│   ├── services.md
│   ├── readme_dev_setup.md
│   └── ...
├── pyproject.toml
├── poetry.lock
├── docker-compose.yml
└── .env
```
Uwaga: katalog shared/ jest montowany do kontenerów i współdzielony między usługami.

## Budowanie obrazów
```bash

docker compose build
```

## Inicjalizacja bazy Airflow
Wykonaj jednorazowo po pierwszym uruchomieniu:

```bash

docker compose up airflow-init
```

## Uruchamianie środowiska
Po zainicjalizowaniu bazy uruchom wszystkie usługi:

```bash

docker compose up -d
```

## Usługi i porty
- **Airflow Webserver:** http://localhost:8080
    Login: admin, Hasło: admin (domyślne w docker-compose.yml)

- **Postgres:** port `5432`

- **Redis:** port `6379`

- **(w przyszłości) Streamlit:** port `8501`

## Debugowanie
- **Logi konkretnej usługi:**

```bash

docker compose logs airflow-scheduler
docker compose logs airflow-worker
```

- **Wejście do kontenera Airflow:**

``bash

docker compose exec airflow-webserver
```

## Zatrzymywanie i czyszczenie
- **Zatrzymanie środowiska:**

```bash

docker compose down
```

**Zatrzymanie i usunięcie danych (pełny reset):**

```bash

docker compose down -v
```

## Dalszy rozwój
Nowe DAG-i umieszczaj w `airflow/dags/`

Dane wejściowe wrzucaj do `shared/data/`

Wyniki modeli i pipeline’ów zapisuj w `shared/models/`

Pliki konfiguracyjne przechowuj w `shared/config/`

📌 Tip: Jeżeli zmieniasz pliki `.env` lub konfigurację `docker-compose.yml`, wykonaj:

```bash

docker compose down && docker compose up -d --build
```