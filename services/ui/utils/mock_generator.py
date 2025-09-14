import pandas as pd
import numpy as np
import datetime

def generate_mock_merged_df(days: int = 3) -> pd.DataFrame:
    """
    Generate mock dataset matching expected merged structure:
    - timestamp (hourly)
    - forecast_total_MWh (ENTSO-E benchmark)
    - actual_OZE_MWh (actual)
    - model_forecast (model predictions)
    """
    end = pd.Timestamp.now().floor("H")
    start = end - pd.Timedelta(days=days)
    timestamps = pd.date_range(start=start, end=end, freq="H")

    n = len(timestamps)
    base = 1000 + 200 * np.sin(np.linspace(0, 3.14 * 2, n))
    actual = base + np.random.normal(scale=50, size=n)
    benchmark = base + np.random.normal(scale=60, size=n)  # ENTSO-E
    model = base + np.random.normal(scale=40, size=n)      # your model output

    df = pd.DataFrame({
        "timestamp": timestamps,
        "forecast_total_MWh": benchmark,
        "actual_OZE_MWh": actual,
        "model_forecast": model,
    })
    return df
