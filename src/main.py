import schedule
import time
from store_data import init_db, save_current, save_forecast
from process_data import get_all_current, get_all_forecasts

def collect():
    print("Collecting weather data...")
    save_current(get_all_current())
    save_forecast(get_all_forecasts())
    print("Done!")

init_db()
collect()                          # run once immediately
schedule.every(1).hours.do(collect)

while True:
    schedule.run_pending()
    time.sleep(60)