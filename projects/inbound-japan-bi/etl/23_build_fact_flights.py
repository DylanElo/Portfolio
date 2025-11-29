        return

    # Load Raw
    df_raw = pd.read_csv(RAW_FILE)
    
    # Load Dimensions
    df_airport = pd.read_sql("SELECT airport_id, airport_code FROM dim_airport", conn)
    
    # Merge Airport ID
    df_merged = df_raw.merge(df_airport, on='airport_code', how='left')
    
    # Date ID
    df_merged['date_obj'] = pd.to_datetime(df_merged['date'])
    df_merged['date_id'] = df_merged['date_obj'].dt.strftime('%Y%m%d').astype(int)
    
    # Select columns
    fact_table = df_merged[[
        'date_id', 'airport_id', 'flights_count'
    ]].copy()
    
    # Save
    fact_table.to_sql('fact_flights_daily', conn, if_exists='replace', index=False)
    print(f"✅ fact_flights_daily created: {len(fact_table)} rows")
    
    conn.close()

if __name__ == "__main__":
    main()
