import sqlite3
import pandas as pd

DB = "weather.db"

def run(sql):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

# Average temperature by city
avg_temp = run("""
    SELECT city, ROUND(AVG(temperature), 2) AS avg_temp,
           ROUND(AVG(humidity), 2) AS avg_humidity
    FROM current_weather
    GROUP BY city ORDER BY avg_temp DESC
""")

# Hottest recorded moment
hottest = run("""
    SELECT city, temperature, timestamp
    FROM current_weather
    ORDER BY temperature DESC LIMIT 5
""")

# Rain probability from forecast (% of slots with rain > 0)
rain_chance = run("""
    SELECT city,
        ROUND(100.0 * SUM(CASE WHEN rain_3h > 0 THEN 1 ELSE 0 END) / COUNT(*), 1)
        AS rain_chance_pct
    FROM forecast_weather
    GROUP BY city
""")

# Temperature trend over time for one city
trend = run("""
    SELECT timestamp, temperature FROM current_weather
    WHERE city = 'Chennai'
    ORDER BY timestamp
""")

print(avg_temp)
print(rain_chance)

# Add to queries.py
import pandas as pd, sqlite3
conn = sqlite3.connect("weather.db")
pd.read_sql("SELECT * FROM current_weather", conn).to_csv("current.csv", index=False)
pd.read_sql("SELECT * FROM forecast_weather", conn).to_csv("forecast.csv", index=False)