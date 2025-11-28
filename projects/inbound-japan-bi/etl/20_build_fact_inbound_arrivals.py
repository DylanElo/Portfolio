import pandas as pd
import sqlite3
import os

DB_PATH = r"..\data\inbound_japan.db"
RAW_FILE = r"..\data\raw\jnto_arrivals.csv"

def main():
    conn = sqlite3.connect(DB_PATH)
    
    if not os.path.exists(RAW_FILE):
        print("⚠️ Raw data not found. Run 01_fetch_jnto_arrivals.py first.")
        return

    # Load Raw
    df_raw = pd.read_csv(RAW_FILE)
    
    # Load Dimensions for lookup
    df_country = pd.read_sql("SELECT country_id, country_name_en FROM dim_country", conn)
    
    # Merge Country ID
    df_merged = df_raw.merge(df_country, left_on='Country', right_on='country_name_en', how='left')
    
    # Create Month ID in raw data to match dim_month
    df_merged['month_id'] = df_merged['Year'].astype(str) + df_merged['Month'].apply(lambda x: f"{x:02d}")
    df_merged['month_id'] = df_merged['month_id'].astype(int)
    
    # Select and Rename
    fact_table = df_merged[['month_id', 'country_id', 'Visitor Arrivals']].copy()
    fact_table.rename(columns={'Visitor Arrivals': 'visitors_total'}, inplace=True)
    
    # Add other columns as null for now (leisure/business not in mock)
    fact_table['visitors_leisure'] = None
    fact_table['visitors_business'] = None
    
    # Save
    fact_table.to_sql('fact_inbound_arrivals_monthly', conn, if_exists='replace', index=False)
    print(f"✅ fact_inbound_arrivals_monthly created: {len(fact_table)} rows")
    
    conn.close()

if __name__ == "__main__":
    main()
