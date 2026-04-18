import pandas as pd
from fetch_weather import fetch_current_weather, fetch_forecast, CITIES
from datetime import datetime

def parse_current(city):
    raw = fetch_current_weather(city)
    return {
        "city": city,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": raw["main"]["temp"],
        "feels_like": raw["main"]["feels_like"],
        "humidity": raw["main"]["humidity"],
        "pressure": raw["main"]["pressure"],
        "weather_desc": raw["weather"][0]["description"],
        "wind_speed": raw["wind"]["speed"],
        "rain_1h": raw.get("rain", {}).get("1h", 0),  # 0 if no rain
    }

def parse_forecast(city):
    raw = fetch_forecast(city)
    rows = []
    for item in raw["list"]:
        rows.append({
            "city": city,
            "forecast_time": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "pressure": item["main"]["pressure"],
            "rain_3h": item.get("rain", {}).get("3h", 0),
            "weather_desc": item["weather"][0]["description"],
        })
    return rows

def get_all_current():
    records = [parse_current(city) for city in CITIES]
    df = pd.DataFrame(records)
    df.dropna(inplace=True)                        # remove nulls
    df["temp_category"] = pd.cut(                  # feature: temp bucket
        df["temperature"],
        bins=[-10, 15, 25, 35, 60],
        labels=["Cold", "Mild", "Warm", "Hot"]
    )
    return df

def get_all_forecasts():
    all_rows = []
    for city in CITIES:
        all_rows.extend(parse_forecast(city))
    return pd.DataFrame(all_rows)

if __name__ == "__main__":
    df = get_all_current()
    print(df)
    print("\nForecast data:")
    df2 = get_all_forecasts()
    print(df2)