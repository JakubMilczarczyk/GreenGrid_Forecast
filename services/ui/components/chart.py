import streamlit as st
import pandas as pd
import altair as alt

def render_chart(df: pd.DataFrame, model_col: str, benchmark_col: str, data_source: str = "Plik Parquet"):
    """
    df must include 'timestamp', 'actual_OZE_MWh' (actual), model_col (model forecasts), benchmark_col (ENTSO-E).
    Renders daily bar chart (hourly) with timestamp on x-axis formatted HH:MM.
    Displays info about current data source above the chart.
    """

    st.info(f"Źródło danych: {data_source}")

    if df is None or df.empty:
        st.warning("No data available to display")
        return

    # Ensure timestamp is datetime and sorted
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # build available days
    df["date"] = df["timestamp"].dt.date
    available_days = sorted(df["date"].unique())
    if not available_days:
        st.warning("No date range available in data")
        return

    selected_day = st.selectbox("Wybierz dzień", available_days, index=0)

    # Filter to selected day and ensure hourly aggregation
    day_mask = df["date"] == selected_day
    df_day = df.loc[day_mask].copy()
    if df_day.empty:
        st.warning("No data for selected day")
        return

    # Check required columns
    missing_cols = []
    for col in ["actual_OZE_MWh", model_col, benchmark_col]:
        if col not in df_day.columns:
            missing_cols.append(col)
    if missing_cols:
        st.error(f"Brak wymaganych kolumn: {', '.join(missing_cols)}")
        return

    # Make sure we have hourly timestamps; if multiple records per hour, aggregate by mean
    df_day["hour"] = df_day["timestamp"].dt.floor("H")
    agg = df_day.groupby("hour").agg({
        "actual_OZE_MWh": "mean",
        model_col: "mean",
        benchmark_col: "mean"
    }).reset_index().rename(columns={"hour":"timestamp"})

    # Melt for Altair
    chart_df = agg.melt(
        id_vars=["timestamp"],
        value_vars=["actual_OZE_MWh", model_col, benchmark_col],
        var_name="Seria",
        value_name="Wartość"
    )

    # Custom colors for clarity
    color_scale = alt.Scale(
        domain=["actual_OZE_MWh", model_col, benchmark_col],
        range=["#2E8B57", "#1E90FF", "#FFD700"],
    )
    legend_labels = {
        "actual_OZE_MWh": "Rzeczywiste",
        model_col: "Model",
        benchmark_col: "ENTSO-E"
    }
    chart_df["Seria"] = chart_df["Seria"].map(legend_labels)

    chart = (
        alt.Chart(chart_df)
        .mark_bar(size=18)
        .encode(
            x=alt.X("timestamp:T", title="Godzina", axis=alt.Axis(format="%H:%M", labelAngle=-45)),
            y=alt.Y("Wartość:Q", title="MWh"),
            color=alt.Color("Seria:N", title="Seria", scale=color_scale),
            xOffset="Seria",
            tooltip=[
                alt.Tooltip("timestamp:T", title="Godzina"),
                alt.Tooltip("Seria:N", title="Seria"),
                alt.Tooltip("Wartość:Q", title="MWh", format=".2f")
            ]
        )
        .properties(width="container", height=450, title=f"Porównanie: Rzeczywiste vs ENTSO-E vs Model ({selected_day})")
    )

    st.altair_chart(chart, use_container_width=True)
