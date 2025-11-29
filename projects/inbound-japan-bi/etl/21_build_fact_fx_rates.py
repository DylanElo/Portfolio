import pandas as pd
import sqlite3
from pathlib import Path

# Config - cross-platform path resolution
DB_PATH = Path(__file__).parent.parent / "data" / "inbound_japan.db"
RAW_FILE = Path(__file__).parent.parent / "data" / "raw" / "fx_rates.csv"

def main():
    conn = sqlite3.connect(DB_PATH)
    
    if not RAW_FILE.exists():
        print("⚠️ Raw FX data not found. Run 02_fetch_fx_rates.py first.")
        return

    # Load Raw
    df_raw = pd.read_csv(RAW_FILE)
    
    # Transform
    # We need date_id (YYYYMMDD)
    df_raw['date_obj'] = pd.to_datetime(df_raw['date'])
    df_raw['date_id'] = df_raw['date_obj'].dt.strftime('%Y%m%d').astype(int)
    
    # Select columns for Fact Table
    # Grain: Day x Currency
    fact_table = df_raw[['date_id', 'base_currency', 'rate']].copy()
    fact_table.rename(columns={'base_currency': 'currency_code', 'rate': 'rate_jpy_per_currency'}, inplace=True)
    
    # Save
    fact_table.to_sql('fact_fx_rate_daily', conn, if_exists='replace', index=False)
    print(f"✅ fact_fx_rate_daily created: {len(fact_table)} rows")
    
    conn.close()

if __name__ == "__main__":
    main()
