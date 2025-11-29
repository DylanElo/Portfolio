import pandas as pd
import sqlite3
import os
from datetime import datetime, timedelta

# Config
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "inbound_japan.db")
RAW_FILE = os.path.join(BASE_DIR, "data", "raw", "jnto_arrivals.csv")

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def build_dim_date(conn):
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    dates = []
    current = start_date
    while current <= end_date:
        dates.append({
            'date_id': int(current.strftime('%Y%m%d')),
            'date': current.strftime('%Y-%m-%d'),
            'year': current.year,
            'month': current.month,
            'day': current.day,
            'quarter': (current.month - 1) // 3 + 1,
            'day_of_week': current.weekday(), # 0=Monday
            'is_weekend': 1 if current.weekday() >= 5 else 0
        })
        current += timedelta(days=1)
        
    df = pd.DataFrame(dates)
    df.to_sql('dim_date', conn, if_exists='replace', index=False)
    print(f"✅ dim_date created: {len(df)} rows")

def build_dim_month(conn):
    # Generate months from 2019 to 2025
    months = []
    for year in range(2019, 2026):
        for month in range(1, 13):
            months.append({
                'month_id': int(f"{year}{month:02d}"),
                'year': year,
                'month': month,
                'month_name': datetime(year, month, 1).strftime('%B'),
                'season': get_season(month)
            })
    
    df = pd.DataFrame(months)
    df.to_sql('dim_month', conn, if_exists='replace', index=False)
    print(f"✅ dim_month created: {len(df)} rows")

def get_season(month):
    if month in [3, 4, 5]: return 'Spring'
    if month in [6, 7, 8]: return 'Summer'
    if month in [9, 10, 11]: return 'Autumn'
    return 'Winter'

def build_dim_country(conn):
    # Read raw data to get unique countries
    if not os.path.exists(RAW_FILE):
        print("⚠️ Raw data not found. Run 01_fetch_jnto_arrivals.py first.")
        return

    df_raw = pd.read_csv(RAW_FILE)
    countries = df_raw['Country'].unique()
    
    country_data = []
    for i, country in enumerate(countries, 1):
        region = 'Other'
        if country in ['China', 'South Korea', 'Taiwan', 'Hong Kong']: region = 'East Asia'
        elif country in ['Thailand', 'Vietnam', 'Philippines', 'Singapore', 'Malaysia', 'Indonesia']: region = 'Southeast Asia'
        elif country in ['United States', 'Canada']: region = 'North America'
        elif country in ['United Kingdom', 'France', 'Germany', 'Italy', 'Spain', 'Russia']: region = 'Europe'
        elif country in ['Australia']: region = 'Oceania'
        elif country in ['India']: region = 'South Asia'
        
        country_data.append({
            'country_id': i,
            'country_name_en': country,
            'region_macro': region
        })
        
    df = pd.DataFrame(country_data)
    df.to_sql('dim_country', conn, if_exists='replace', index=False)
    print(f"✅ dim_country created: {len(df)} rows")

def build_dim_fx_currency(conn):
    currencies = [
        {'currency_code': 'USD', 'currency_name': 'US Dollar'},
        {'currency_code': 'EUR', 'currency_name': 'Euro'},
        {'currency_code': 'KRW', 'currency_name': 'South Korean Won'},
        {'currency_code': 'CNY', 'currency_name': 'Chinese Yuan'},
        {'currency_code': 'AUD', 'currency_name': 'Australian Dollar'},
        {'currency_code': 'THB', 'currency_name': 'Thai Baht'}
    ]
    df = pd.DataFrame(currencies)
    df.to_sql('dim_fx_currency', conn, if_exists='replace', index=False)
    print(f"✅ dim_fx_currency created: {len(df)} rows")

def build_dim_weather_location(conn):
    locations = [
        {'weather_loc_id': 1, 'city_name': 'Tokyo', 'region_jp': 'Kanto'},
        {'weather_loc_id': 2, 'city_name': 'Osaka', 'region_jp': 'Kansai'},
        {'weather_loc_id': 3, 'city_name': 'Sapporo', 'region_jp': 'Hokkaido'},
        {'weather_loc_id': 4, 'city_name': 'Fukuoka', 'region_jp': 'Kyushu'},
        {'weather_loc_id': 5, 'city_name': 'Naha', 'region_jp': 'Okinawa'}
    ]
    df = pd.DataFrame(locations)
    df.to_sql('dim_weather_location', conn, if_exists='replace', index=False)
    print(f"✅ dim_weather_location created: {len(df)} rows")

def build_dim_airport(conn):
    airports = [
        {'airport_id': 1, 'airport_code': 'NRT', 'airport_name': 'Narita International', 'region_jp': 'Kanto'},
        {'airport_id': 2, 'airport_code': 'HND', 'airport_name': 'Haneda International', 'region_jp': 'Kanto'},
        {'airport_id': 3, 'airport_code': 'KIX', 'airport_name': 'Kansai International', 'region_jp': 'Kansai'},
        {'airport_id': 4, 'airport_code': 'FUK', 'airport_name': 'Fukuoka International', 'region_jp': 'Kyushu'},
        {'airport_id': 5, 'airport_code': 'CTS', 'airport_name': 'New Chitose', 'region_jp': 'Hokkaido'}
    ]
    df = pd.DataFrame(airports)
    df.to_sql('dim_airport', conn, if_exists='replace', index=False)
    print(f"✅ dim_airport created: {len(df)} rows")

def main():
    conn = create_connection()
    build_dim_date(conn)
    build_dim_month(conn)
    build_dim_country(conn)
    build_dim_fx_currency(conn)
    build_dim_weather_location(conn)
    build_dim_airport(conn)
    conn.close()

if __name__ == "__main__":
    main()
