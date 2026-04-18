# Weather Data Pipeline

An end-to-end data engineering project that collects, processes, stores, and visualizes real-time weather data using Python and Streamlit.

## Live Dashboard
Run locally using the steps below.

## Tech Stack
- Python — core programming
- Requests — API calls
- Pandas — data cleaning and processing
- SQLite — local database storage
- SQL — analytics queries
- Streamlit — live interactive dashboard
- Plotly — charts and visualizations

## What it does
- Fetches live weather data every hour from 4 Indian cities — Chennai, Mumbai, Delhi, Bangalore
- Cleans and processes raw API data using Pandas
- Stores data in a local SQLite database that grows over time
- Analyzes trends like temperature, humidity, pressure, and rain probability
- Displays everything in a live auto-refreshing Streamlit dashboard

## Dashboard Features
- Live temperature display for all 4 cities
- Temperature trend chart over time
- Humidity comparison bar chart
- Rain probability from forecast data
- City comparison table
- Raw data view

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/Ashmyth789/Weather-Data-Pipeline.git
cd Weather-Data-Pipeline
```

### 2. Install dependencies
```bash
pip install requests pandas streamlit plotly schedule
```

### 3. Add your API key
Get a free API key from [openweathermap.org](https://openweathermap.org)

Open `fetch_weather.py` and replace:
```python
API_KEY = "your_api_key_here"
```

### 4. Run the data pipeline
```bash
python main.py
```

### 5. Launch the dashboard
```bash
streamlit run dashboard.py
```

Open your browser at `http://localhost:8501`

## Screenshots
Coming soon