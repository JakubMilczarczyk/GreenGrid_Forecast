import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Dodaj src/ do sys.path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from utils.forecast_utils import load_data_and_predictions

# ---- Tytuł i opis ----
st.title("GreenGrid Forecast")
st.info("Compare model forecast with ENTSO-E benchmark and actual OZE production")

# ---- Wczytanie danych ----
timestamps, y_true, y_entsoe, y_model = load_data_and_predictions()
timestamps = pd.to_datetime(timestamps)

# ---- Ramka danych ----
df = pd.DataFrame({
    "timestamp": timestamps,
    "true": y_true,
    "entsoe": y_entsoe,
    "model": y_model
})

# ---- Metryki ----
st.subheader("Forecast Metrics Comparison")

mse_model = mean_squared_error(df["true"], df["model"])
mae_model = mean_absolute_error(df["true"], df["model"])
r2_model = r2_score(df["true"], df["model"])

mse_entsoe = mean_squared_error(df["true"], df["entsoe"])
mae_entsoe = mean_absolute_error(df["true"], df["entsoe"])

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Model Forecast")
    st.metric("MSE", f"{mse_model:.2f}")
    st.metric("MAE", f"{mae_model:.2f}")
    st.metric("R²", f"{r2_model:.2f}")

with col2:
    st.markdown("### ENTSO-E Benchmark")
    st.metric("MSE", f"{mse_entsoe:.2f}")
    st.metric("MAE", f"{mae_entsoe:.2f}")

# ---- Wykres interaktywny dla wybranego dnia ----
st.subheader("Forecast Comparison Chart")

# Wybór dnia z dostępnych timestampów
available_days = sorted(df['timestamp'].dt.date.unique())
selected_day = st.selectbox("Select a date to display", available_days)

# Filtrowanie danych tylko z wybranego dnia
mask = df['timestamp'].dt.date == selected_day
df_day = df[mask]

# Wykres interaktywny (Plotly)
fig = go.Figure()
fig.add_trace(go.Bar(x=df_day["timestamp"], y=df_day["true"], name='Actual OZE'))
fig.add_trace(go.Bar(x=df_day["timestamp"], y=df_day["entsoe"], name='ENTSO-E Forecast'))
fig.add_trace(go.Bar(x=df_day["timestamp"], y=df_day["model"], name='Model Forecast'))

fig.update_layout(
    xaxis_title='Hour',
    yaxis_title='MWh',
    xaxis=dict(
        tickformat="%H:%M",
        nticks=12
    ),
    barmode='group',
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)
