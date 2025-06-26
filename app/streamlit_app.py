import streamlit as st
st.title("GreenGrid Forecast")
st.info("Energy and weather data in progress...")

sys.path.append(str(Path(__file__).parent.parent / "src" / "utils"))
from forecast_utils import load_data_and_predictions

st.title("GreenGrid Forecast")
st.info("Compare model and ENTSO-E forecasts")

timestamps, y_true, y_entsoe, y_model = load_data_and_predictions()

# Select a sample for the plot (e.g., 100 points)
sample = slice(0, 100)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(timestamps[sample], y_true[sample], label="Actual OZE production")
ax.plot(timestamps[sample], y_entsoe[sample], label="Forecast ENTSO-E")
ax.plot(timestamps[sample], y_model[sample], label="Forecast model")
ax.set_xlabel("Time")
ax.set_ylabel("MWh")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)