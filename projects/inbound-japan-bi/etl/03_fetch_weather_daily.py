import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Config
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_FILE = os.path.join(RAW_DIR, "weather_daily.csv")
START_DATE = "2019-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")

CITIES = {
    'Tokyo': {'base_temp': 16, 'amp': 12, 'rain_prob': 0.3},
    'Osaka': {'base_temp': 17, 'amp': 13, 'rain_prob': 0.3},
    'Sapporo': {'base_temp': 9, 'amp': 14, 'rain_prob': 0.4}, # Colder
    'Fukuoka': {'base_temp': 17, 'amp': 11, 'rain_prob': 0.35},
    'Naha': {'base_temp': 23, 'amp': 6, 'rain_prob': 0.4} # Tropical
}

def ensure_directories():
    if not os.path.exists(RAW_DIR):
        os.makedirs(RAW_DIR)

def generate_weather_data():
    print("🌦️ Generating mock Weather data...")
    
    dates = pd.date_range(start=START_DATE, end=END_DATE)
    records = []
    
    for d in dates:
        day_of_year = d.dayofyear
        
        for city, params in CITIES.items():
            # Sinusoidal temperature curve
            # Peak in summer (approx day 200)
            temp_seasonality = -np.cos((day_of_year - 20) * 2 * np.pi / 365)
            avg_temp = params['base_temp'] + (params['amp'] * temp_seasonality)
            
            # Random daily variation
            daily_var = np.random.normal(0, 2)
            temp_avg = avg_temp + daily_var
            temp_max = temp_avg + np.random.uniform(3, 8)
            temp_min = temp_avg - np.random.uniform(3, 8)
            
            # Conditions
            is_rainy = np.random.random() < params['rain_prob']
            condition = 'Clear'
            precipitation = 0.0
            
            if is_rainy:
                condition = 'Rain'
                precipitation = np.random.exponential(5) # mm
                temp_max -= 2 # Cooler when raining
            
            # Extreme events
            if temp_max > 35:
                condition = 'Heatwave'
            elif temp_max < 0 and city == 'Sapporo':
                condition = 'Snow'
            
            # Typhoon season (Aug-Sep)
            if d.month in [8, 9] and np.random.random() < 0.05:
                condition = 'Typhoon'
                precipitation = np.random.uniform(50, 200)
            
            records.append({
                'date': d.strftime("%Y-%m-%d"),
                'city_name': city,
                'temp_avg': round(temp_avg, 1),
                'temp_max': round(temp_max, 1),
                'temp_min': round(temp_min, 1),
                'condition': condition,
                'precipitation_mm': round(precipitation, 1)
            })
            
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Weather data saved to: {OUTPUT_FILE} ({len(df)} rows)")

def main():
    ensure_directories()
    generate_weather_data()

if __name__ == "__main__":
    main()
