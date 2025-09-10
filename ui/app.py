import streamlit as st
from components.header import render_header
from components.selectors import render_selectors
from components.chart import render_chart
from services.data_service import load_merged_dataframe

def main():
    st.set_page_config(page_title="GreenGrid Forecast", layout="wide")
    render_header()

    # Pobierz dane oraz informację o źródle
    df, data_source = load_merged_dataframe(return_source=True)

    # Przygotuj dostępne serie
    available_models = [c for c in df.columns if c.lower().startswith("model")]
    available_benchmarks = [c for c in df.columns if c.lower().startswith("entsoe") or c.lower().startswith("forecast") and c != "model_forecast"]

    # Fallback defaults
    if not available_models and "model_forecast" in df.columns:
        available_models = ["model_forecast"]
    if not available_benchmarks and "entsoe_benchmark_MWh" in df.columns:
        available_benchmarks = ["entsoe_benchmark_MWh"]
    elif not available_benchmarks and "forecast_total_MWh" in df.columns:
        available_benchmarks = ["forecast_total_MWh"]

    selected_model, selected_benchmark = render_selectors(available_models, available_benchmarks)

    # Jeśli brak wyboru, pokaż komunikat
    if not selected_model and not selected_benchmark:
        st.warning("No model/benchmark series available in data.")
        st.stop()

    # Upewnij się, że jest kolumna rzeczywista
    if "actual_OZE_MWh" not in df.columns:
        st.warning("Actual values column 'actual_OZE_MWh' not found in data. Chart may not be meaningful.")

    # Przekaż źródło danych do wykresu
    render_chart(
        df,
        model_col=selected_model or "model_forecast",
        benchmark_col=selected_benchmark or "entsoe_benchmark_MWh",
        data_source=data_source
    )

if __name__ == "__main__":
    main()
