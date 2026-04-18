import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

DB = "weather.db"

def load_data(query):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("Live Weather Dashboard")
st.caption("Auto-refreshes every 60 seconds")

auto_refresh = st.empty()

import time
refresh_interval = 60

col1, col2, col3, col4 = st.columns(4)

current = load_data("SELECT * FROM current_weather ORDER BY timestamp DESC LIMIT 4")

for i, row in current.iterrows():
    col = [col1, col2, col3, col4][i % 4]
    with col:
        st.metric(
            label=row["city"],
            value=f"{row['temperature']}°C",
            delta=f"Humidity: {row['humidity']}%"
        )

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Temperature trend")
    trend = load_data("""
        SELECT city, timestamp, temperature
        FROM current_weather
        ORDER BY timestamp
    """)
    if not trend.empty:
        fig = px.line(trend, x="timestamp", y="temperature",
                      color="city", markers=True)
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Humidity by city")
    humidity = load_data("""
        SELECT city, AVG(humidity) as avg_humidity
        FROM current_weather
        GROUP BY city
    """)
    if not humidity.empty:
        fig2 = px.bar(humidity, x="city", y="avg_humidity",
                      color="city")
        st.plotly_chart(fig2, use_container_width=True)

st.divider()

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Rain chance from forecast")
    rain = load_data("""
        SELECT city,
        ROUND(100.0 * SUM(CASE WHEN rain_3h > 0 THEN 1 ELSE 0 END) / COUNT(*), 1)
        AS rain_chance_pct
        FROM forecast_weather
        GROUP BY city
    """)
    if not rain.empty:
        fig3 = px.bar(rain, x="city", y="rain_chance_pct",
                      color="city", title="Rain probability %")
        st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.subheader("City comparison")
    compare = load_data("""
        SELECT city,
        ROUND(AVG(temperature), 2) as avg_temp,
        ROUND(AVG(humidity), 2) as avg_humidity,
        ROUND(AVG(pressure), 2) as avg_pressure
        FROM current_weather
        GROUP BY city
    """)
    if not compare.empty:
        st.dataframe(compare, use_container_width=True)

st.divider()
st.subheader("Raw data")
raw = load_data("SELECT * FROM current_weather ORDER BY timestamp DESC LIMIT 20")
st.dataframe(raw, use_container_width=True)

time.sleep(refresh_interval)
st.rerun()