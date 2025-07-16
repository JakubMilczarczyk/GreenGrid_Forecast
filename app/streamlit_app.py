import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

sys.path.append(str(Path(__file__).parent.parent / "src"))
from utils.forecast_utils import load_data_and_predictions

st.title("GreenGrid Forecast")
st.info("Compare model forecast with ENTSO-E benchmark and actual OZE production")

timestamps, y_true, y_entsoe, y_model = load_data_and_predictions()

# ---- METRICS ----
st.subheader("Forecast Metrics Comparison")

mse_model = mean_squared_error(y_true, y_model)
mae_model = mean_absolute_error(y_true, y_model)
r2_model = r2_score(y_true, y_model)

mse_entsoe = mean_squared_error(y_true, y_entsoe)
mae_entsoe = mean_absolute_error(y_true, y_entsoe)

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

# ---- PLOT ----
st.subheader("Forecast Comparison Chart")

start = st.slider("Start index", min_value=0, max_value=len(y_true) - 100, value=0, step=10)
sample = slice(start, start + 100)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(timestamps[sample], y_true[sample], label="Actual OZE production")
ax.plot(timestamps[sample], y_entsoe[sample], label="Forecast ENTSO-E")
ax.plot(timestamps[sample], y_model[sample], label="Forecast model")
ax.set_xlabel("Time")
ax.set_ylabel("MWh")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)
