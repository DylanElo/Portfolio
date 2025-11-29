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
