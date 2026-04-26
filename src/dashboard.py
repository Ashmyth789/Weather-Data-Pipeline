import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("Live Weather Dashboard")
st.caption("Data updated daily from OpenWeatherMap API")

@st.cache_data(ttl=3600)
def load_data():
    current = pd.read_csv("data/current.csv")
    forecast = pd.read_csv("data/forecast.csv")
    return current, forecast

current, forecast = load_data()

st.divider()

col1, col2, col3, col4 = st.columns(4)
latest = current.drop_duplicates(subset="city", keep="last")

for i, (_, row) in enumerate(latest.iterrows()):
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
    fig = px.line(current, x="timestamp", y="temperature",
                  color="city", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Humidity by city")
    humidity = current.groupby("city")["humidity"].mean().reset_index()
    fig2 = px.bar(humidity, x="city", y="humidity", color="city")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Rain chance from forecast")
    forecast["has_rain"] = forecast["rain_3h"] > 0
    rain = forecast.groupby("city")["has_rain"].mean().reset_index()
    rain["rain_chance_pct"] = (rain["has_rain"] * 100).round(1)
    fig3 = px.bar(rain, x="city", y="rain_chance_pct", color="city")
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.subheader("City comparison")
    compare = current.groupby("city").agg(
        avg_temp=("temperature", "mean"),
        avg_humidity=("humidity", "mean"),
        avg_pressure=("pressure", "mean")
    ).round(2).reset_index()
    st.dataframe(compare, use_container_width=True)

st.divider()
st.subheader("Raw data")
st.dataframe(current.sort_values("timestamp", ascending=False).head(20), use_container_width=True)
