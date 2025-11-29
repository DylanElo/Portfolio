import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import time

# Config
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_FILE = os.path.join(RAW_DIR, "fx_rates.csv")
BASE_CURRENCY = "JPY" # Frankfurter gives rates FROM Base. We want JPY per USD, so we might need to invert if we use USD as base. 
# Actually, standard is usually "How many JPY for 1 USD". 
# Frankfurter: /history?from=USD&to=JPY gives JPY per 1 USD.
# We want rates for multiple currencies.
# Strategy: Fetch from=USD, to=JPY -> JPY/USD
# Fetch from=EUR, to=JPY -> JPY/EUR
# etc.

CURRENCIES_TO_FETCH = ['USD', 'EUR', 'KRW', 'CNY', 'AUD', 'THB']
START_DATE = "2019-01-01"
# END_DATE = datetime.now().strftime("%Y-%m-%d")

def ensure_directories():
    if not os.path.exists(RAW_DIR):
        os.makedirs(RAW_DIR)

def fetch_rates():
    print("⏳ Fetching FX rates from Frankfurter API...")
    
    all_data = []
    
    for currency in CURRENCIES_TO_FETCH:
        try:
            # We want: How much JPY is 1 Unit of Currency? (e.g. 150 JPY = 1 USD)
            # API: https://api.frankfurter.app/2019-01-01..?from=USD&to=JPY
            url = f"https://api.frankfurter.app/{START_DATE}..?from={currency}&to=JPY"
            print(f"   Fetching {currency} -> JPY...")
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                
                for date_str, rate_dict in rates.items():
                    val = rate_dict.get('JPY')
                    if val:
                        all_data.append({
                            'date': date_str,
                            'base_currency': currency,
                            'target_currency': 'JPY',
                            'rate': val
                        })
            else:
                print(f"❌ Failed to fetch {currency}: {response.status_code}")
            
            time.sleep(0.5) # Be nice to API
            
        except Exception as e:
            print(f"❌ Error fetching {currency}: {e}")

    if not all_data:
        print("⚠️ No data fetched. Generating mock data instead.")
        generate_mock_fx_data()
        return

    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ FX rates saved to: {OUTPUT_FILE} ({len(df)} rows)")

def generate_mock_fx_data():
    # Fallback if API fails
    print("⚠️ Generating mock FX data...")
    dates = pd.date_range(start=START_DATE, end=datetime.now())
    records = []
    
    # Base rates approx
    bases = {'USD': 110, 'EUR': 120, 'KRW': 0.09, 'CNY': 15, 'AUD': 80, 'THB': 3.5}
    
    for d in dates:
        date_str = d.strftime("%Y-%m-%d")
        # Trend: Yen gets weaker (rate goes UP) over time, esp 2022-2024
        trend_factor = 1.0
        if d.year >= 2022:
            trend_factor = 1.0 + (0.0005 * (d - datetime(2022,1,1)).days) # Linear weakening
            
        for curr, base_rate in bases.items():
            rate = base_rate * trend_factor * (1 + (hash(date_str + curr) % 100 / 1000.0)) # Noise
            records.append({
                'date': date_str,
                'base_currency': curr,
                'target_currency': 'JPY',
                'rate': rate
            })
            
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Mock FX rates saved to: {OUTPUT_FILE}")

def main():
    ensure_directories()
    fetch_rates()

if __name__ == "__main__":
    main()
