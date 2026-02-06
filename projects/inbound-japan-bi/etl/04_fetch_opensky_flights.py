import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path

# Config - cross-platform path resolution
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT_FILE = RAW_DIR / "flights_daily.csv"
START_DATE = "2019-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")

AIRPORTS = {
    'NRT': {'name': 'Narita', 'base_flights': 400, 'recovery_speed': 0.8},
    'HND': {'name': 'Haneda', 'base_flights': 300, 'recovery_speed': 0.95}, # Faster recovery
    'KIX': {'name': 'Kansai', 'base_flights': 200, 'recovery_speed': 0.7},
    'FUK': {'name': 'Fukuoka', 'base_flights': 100, 'recovery_speed': 0.85}, # Asia connection
    'CTS': {'name': 'New Chitose', 'base_flights': 50, 'recovery_speed': 0.6}
}

def ensure_directories():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

def generate_flight_data():
    print("Generating mock Flight data...")
    
    dates = pd.date_range(start=START_DATE, end=END_DATE)
    records = []
    
    for d in dates:
        year = d.year
        month = d.month
        
        # COVID Impact Factor
        covid_factor = 1.0
        if 2020 <= year <= 2022:
            if year == 2020 and month < 3: covid_factor = 1.0
            elif year == 2022 and month > 9: covid_factor = 0.4
            else: covid_factor = 0.05 # Almost grounded
        elif year >= 2023:
            # Recovery curve
            days_since_opening = (d - datetime(2022, 10, 11)).days
            covid_factor = min(1.0, 0.4 + (days_since_opening / 600))
            
        for code, params in AIRPORTS.items():
            # Seasonality (more flights in holidays)
            seasonality = 1.0
            if month in [4, 8, 12]: seasonality = 1.15
            
            # Daily variation
            day_factor = 1.0
            if d.weekday() >= 5: day_factor = 1.1 # Weekend
            
            base = params['base_flights'] * params['recovery_speed']
            flights = int(base * covid_factor * seasonality * day_factor * np.random.uniform(0.9, 1.1))
            
            records.append({
                'date': d.strftime("%Y-%m-%d"),
                'airport_code': code,
                'flights_count': flights
            })
            
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Flight data saved to: {OUTPUT_FILE} ({len(df)} rows)")

def main():
    ensure_directories()
    generate_flight_data()

if __name__ == "__main__":
    main()
