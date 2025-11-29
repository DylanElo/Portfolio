import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

# Configuration
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_FILE = os.path.join(RAW_DIR, "jnto_arrivals.csv")

def ensure_directories():
    if not os.path.exists(RAW_DIR):
        os.makedirs(RAW_DIR)

def generate_mock_data():
    """
    Generates a realistic mock dataset for JNTO visitor arrivals
    if the official CSV is not present (since JNTO requires form submission).
    """
    print("⚠️  Official JNTO CSV not found. Generating realistic mock data...")
    
    countries = [
        'South Korea', 'China', 'Taiwan', 'Hong Kong', 'Thailand', 
        'United States', 'Australia', 'United Kingdom', 'France', 'Germany',
        'Vietnam', 'Philippines', 'Singapore', 'Malaysia', 'Indonesia',
        'Canada', 'Italy', 'Spain', 'Russia', 'India'
    ]
    
    # Generate monthly data from Jan 2019 to Dec 2025
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2025, 12, 1)
    
    records = []
    current_date = start_date
    
    while current_date <= end_date:
        month_str = current_date.strftime("%Y-%m")
        year = current_date.year
        month = current_date.month
        
        for country in countries:
            # Base volume depending on country size (approximate)
            if country in ['South Korea', 'China', 'Taiwan']:
                base = 500000
            elif country in ['United States', 'Hong Kong', 'Thailand']:
                base = 150000
            else:
                base = 50000
            
            # Seasonality factor (simplified)
            seasonality = 1.0
            if month in [4, 11]: # Cherry blossom / Autumn
                seasonality = 1.3
            elif month in [8]: # Summer
                seasonality = 1.1
            elif month in [1, 2]: # Winter (ski)
                seasonality = 0.9
            
            # COVID impact (simplified)
            covid_factor = 1.0
            if 2020 <= year <= 2022:
                if year == 2020 and month < 3:
                    covid_factor = 1.0
                elif year == 2022 and month > 9:
                    covid_factor = 0.3 # Reopening
                else:
                    covid_factor = 0.01 # Borders closed
            elif year >= 2023:
                covid_factor = 0.8 + (0.05 * (year - 2023)) # Recovery
            
            # Random variation
            variation = np.random.uniform(0.9, 1.1)
            
            visitors = int(base * seasonality * covid_factor * variation)
            
            records.append({
                'Year': year,
                'Month': month,
                'Country': country,
                'Visitor Arrivals': visitors
            })
        
        # Move to next month
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)
            
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Mock data generated at: {OUTPUT_FILE}")
    print("ℹ️  To use real data, download 'Visitor Arrivals' CSV from JNTO website and overwrite this file.")

def main():
    ensure_directories()
    
    if os.path.exists(OUTPUT_FILE):
        print(f"✅ Found existing data at: {OUTPUT_FILE}")
    else:
        generate_mock_data()

if __name__ == "__main__":
    main()
