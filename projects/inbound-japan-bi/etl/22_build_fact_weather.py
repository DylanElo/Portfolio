import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "inbound_japan.db")
RAW_FILE = os.path.join(BASE_DIR, "data", "raw", "weather_daily.csv")

def main():
    conn = sqlite3.connect(DB_PATH)
    
    if not os.path.exists(RAW_FILE):
        print("⚠️ Raw Weather data not found. Run 03_fetch_weather_daily.py first.")
        return

    # Load Raw
    df_raw = pd.read_csv(RAW_FILE)
    
    # Load Dimensions
    df_loc = pd.read_sql("SELECT weather_loc_id, city_name FROM dim_weather_location", conn)
    
    # Merge Location ID
    df_merged = df_raw.merge(df_loc, on='city_name', how='left')
    
    # Date ID
    df_merged['date_obj'] = pd.to_datetime(df_merged['date'])
    df_merged['date_id'] = df_merged['date_obj'].dt.strftime('%Y%m%d').astype(int)
    
    # Select columns
    fact_table = df_merged[[
        'date_id', 'weather_loc_id', 
        'temp_avg', 'temp_max', 'temp_min', 
        'condition', 'precipitation_mm'
    ]].copy()
    
    # Save
    fact_table.to_sql('fact_weather_daily', conn, if_exists='replace', index=False)
    print(f"✅ fact_weather_daily created: {len(fact_table)} rows")
    
    conn.close()

if __name__ == "__main__":
    main()
