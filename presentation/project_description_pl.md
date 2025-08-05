# 🌍 GreenGrid Forecast – Inteligentna prognoza energii z wykorzystaniem danych pogodowych i historycznych
GreenGrid Forecast to system wspierający podejmowanie decyzji w sektorze energetycznym. Umożliwia prognozowanie zużycia oraz produkcji energii z odnawialnych źródeł (np. fotowoltaika, wiatr), na podstawie danych pogodowych i historycznych.

System został zaprojektowany z myślą o:

operatorach sieci elektroenergetycznych,

firmach zajmujących się OZE,

odbiorcach przemysłowych.

## 🔁 Jak działa GreenGrid Forecast?

1. Pobieranie danych (ETL)
Codziennie automatycznie pobierane są dane:

pogodowe (temperatura, nasłonecznienie, wiatr),

energetyczne (rzeczywiste zużycie i produkcja z ENTSO-E),

opcjonalnie: dane cenowe z rynku energii.

🔧 Technologie: Python, Airflow, API, Docker
🗂 Dane surowe są czyszczone i zapisywane w formacie analitycznym (CSV/Parquet).

## 2. Przetwarzanie danych i tworzenie cech (feature engineering)
Z danych wejściowych tworzony jest zestaw zmiennych (cech), które mają wpływ na prognozy:

średnia temperatura, różnice godzinowe,

zmienne pogodowe z przesunięciem czasowym (np. opóźnione słońce),

efektywne użycie kodów ENTSO-E (np. A01 = Total Load).

🧠 Efekt: Zestaw danych gotowy do uczenia modeli ML.

## 3. Trenowanie i ewaluacja modeli
Na podstawie przetworzonych danych system automatycznie:

uczy model predykcyjny (np. regresja),

porównuje wyniki z benchmarkiem (np. średnia historyczna),

zapisuje metryki skuteczności (MSE, MAE, R²).

🔍 Technologie: scikit-learn, MLFlow-ready pipeline
📈 Możliwe rozszerzenie na modele szeregów czasowych (np. Prophet, XGBoost, LSTM).

## 4. Interaktywny frontend (Streamlit)
Użytkownik może:

uruchomić proces ETL i trenowania jednym kliknięciem,

zobaczyć wykresy porównujące prognozę vs. dane rzeczywiste,

pobrać gotowe wyniki do dalszej analizy.

🖥️ Technologie: Streamlit, wykresy Matplotlib/Plotly
💡 Tryb demo: gotowe wyniki bez potrzeby uruchamiania całego pipeline.

## 5. Architektura systemu
Całość działa w lekkim środowisku kontenerowym (Docker), co ułatwia:

lokalne testowanie,

uruchomienie w chmurze (np. AWS, GCP),

integrację z innymi systemami (np. dashboard, SCADA).

## 📦 Stack technologiczny:

Docker – uruchamianie całości jako zestawu kontenerów

Apache Airflow – automatyzacja zadań (ETL, trenowanie)

Streamlit – prosty interfejs użytkownika

Python – silnik przetwarzania danych i ML

Polars/Pandas – szybkie operacje na danych

CSV/Parquet – formaty danych

## 🎯 Co zyskuje użytkownik?
Codzienna prognoza energii na podstawie danych pogodowych

Usprawnione planowanie produkcji i zakupów energii

Intuicyjny interfejs i transparentność danych

Możliwość integracji z istniejącymi narzędziami i systemami