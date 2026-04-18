import sqlite3
import pandas as pd
from process_data import get_all_current, get_all_forecasts

DB_PATH = "weather.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS current_weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT, timestamp TEXT,
            temperature REAL, feels_like REAL,
            humidity REAL, pressure REAL,
            weather_desc TEXT, wind_speed REAL,
            rain_1h REAL, temp_category TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS forecast_weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT, forecast_time TEXT,
            temperature REAL, humidity REAL,
            pressure REAL, rain_3h REAL,
            weather_desc TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_current(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("current_weather", conn, if_exists="append", index=False)
    conn.close()

def save_forecast(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("forecast_weather", conn, if_exists="append", index=False)
    conn.close()

if __name__ == "__main__":
    init_db()
    save_current(get_all_current())
    save_forecast(get_all_forecasts())
    print("Data saved to weather.db successfully!")