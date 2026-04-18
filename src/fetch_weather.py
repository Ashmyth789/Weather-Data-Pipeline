import requests
import json
from datetime import datetime

API_KEY = "e916ae7c1affc77dec1900697dac0818"
CITIES = ["Chennai", "Mumbai", "Delhi", "Bangalore"]

def fetch_current_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(url, params=params)
    return response.json()

def fetch_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric", "cnt": 40}
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    for city in CITIES:
        data = fetch_current_weather(city)
        print(f"{city}: {data['main']['temp']}°C")
        