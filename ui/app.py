"""Streamlit, który odpyta endpoint /predict z Prediction Service."""

#TODO: przenieść część obecnego UI 1:1, tylko zmienić źródło danych z lokalnego pliku na API.
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import requests
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

AIRFLOW_API_BASE_URL = "http://localhost:8080/api/v1"
AIRFLOW_USERNAME = "airflow"
AIRFLOW_PASSWORD = "airflow"

def trigger_dag(dag_id: str):
    """Trigger an Airflow DAG."""
    from requests.auth import HTTPBasicAuth

    url = f"{AIRFLOW_API_BASE_URL}/dags/{dag_id}/dagRuns"
    response = requests.post(
        url,
        auth=HTTPBasicAuth(AIRFLOW_USERNAME, AIRFLOW_PASSWORD),
        json={"conf": {}}
        )
    return response
    
# Add src/ to sys.path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from utils.forecast_utils import load_data_and_predictions

# Title and info
st.title("GreenGrid Forecast - Pipeline Comparison")
st.info("Compare model forecast with ENTSO-E benchmark and actual OZE production")

# Trigger ETL Pipeline
if st.button("Download Data (ETL)"):
    with st.spinner("Triggering ETL Pipeline..."):
        response = trigger_dag("etl_pipeline")
        st.success(f"Download started! {response.status_code}")
        st.json(response.json())

if st.button("Train Model"):
    with st.spinner("Training model..."):
        response = trigger_dag("train_model_pipeline")
        st.success(f"Model training started! {response.status_code}")
        st.json(response.json())


# Load Data 
timestamps, y_true, y_entsoe, y_model = load_data_and_predictions()
timestamps = pd.to_datetime(timestamps)

# Data Frame 
df = pd.DataFrame({
    "timestamp": timestamps,
    "true": y_true,
    "entsoe": y_entsoe,
    "model": y_model
})

if len(df) == 0:
    st.warning("Brak danych do wyświetlenia. Najpierw uruchom ETL i trening modelu.")
    st.stop()

# Metrics
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

# Interactiv chart for chosen day
st.subheader("Forecast Comparison Chart")

# Choice of date
available_days = sorted(df['timestamp'].dt.date.unique())
selected_day = st.selectbox("Select a date to display", available_days)

# Filter data for the selected day
mask = df['timestamp'].dt.date == selected_day
df_day = df[mask]

# Interactive chart (Plotly)
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
