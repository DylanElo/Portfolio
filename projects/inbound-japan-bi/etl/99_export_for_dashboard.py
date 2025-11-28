import pandas as pd
import sqlite3
import json
import os

DB_PATH = r"..\data\inbound_japan.db"
OUTPUT_DIR = r"..\dashboard\data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "dashboard_data.json")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    
    # Query 1: Total Monthly Visitors
    query_monthly = """
    SELECT 
        m.year, m.month, m.month_name,
        SUM(f.visitors_total) as total_visitors
    FROM fact_inbound_arrivals_monthly f
    JOIN dim_month m ON f.month_id = m.month_id
    GROUP BY m.year, m.month
    ORDER BY m.year, m.month
    """
    df_monthly = pd.read_sql(query_monthly, conn)
    
    # Query 2: Top Countries (Latest Year)
    query_countries = """
    SELECT 
        c.country_name_en,
        SUM(f.visitors_total) as total_visitors
    FROM fact_inbound_arrivals_monthly f
    JOIN dim_country c ON f.country_id = c.country_id
    JOIN dim_month m ON f.month_id = m.month_id
    WHERE m.year = 2024
    GROUP BY c.country_name_en
    ORDER BY total_visitors DESC
    LIMIT 10
    """
    df_countries = pd.read_sql(query_countries, conn)
    
    # Query 3: Seasonality Heatmap Data (Avg visitors per month per country)
    query_seasonality = """
    SELECT 
        c.country_name_en,
        m.month,
        AVG(f.visitors_total) as avg_visitors
    FROM fact_inbound_arrivals_monthly f
    JOIN dim_country c ON f.country_id = c.country_id
    JOIN dim_month m ON f.month_id = m.month_id
    WHERE m.year >= 2019
    GROUP BY c.country_name_en, m.month
    """
    df_seasonality = pd.read_sql(query_seasonality, conn)
    
    # Query 4: FX Rates vs Total Visitors (Monthly Avg)
    # We aggregate daily rates to monthly avg to match visitor grain
    query_fx_impact = """
    WITH monthly_fx AS (
        SELECT 
            strftime('%Y', d.date) as year,
            strftime('%m', d.date) as month,
            f.currency_code,
            AVG(f.rate_jpy_per_currency) as avg_rate
        FROM fact_fx_rate_daily f
        JOIN dim_date d ON f.date_id = d.date_id
        WHERE f.currency_code = 'USD' -- Focus on USD for main chart
        GROUP BY 1, 2, 3
    ),
    monthly_visitors AS (
        SELECT 
            m.year, m.month,
            SUM(v.visitors_total) as total_visitors
        FROM fact_inbound_arrivals_monthly v
        JOIN dim_month m ON v.month_id = m.month_id
        GROUP BY 1, 2
    )
    SELECT 
        v.year, v.month,
        v.total_visitors,
        fx.avg_rate as usd_rate
    FROM monthly_visitors v
    JOIN monthly_fx fx ON v.year = fx.year AND v.month = fx.month
    ORDER BY v.year, v.month
    """
    df_fx_impact = pd.read_sql(query_fx_impact, conn)

    # Query 5: Weather Risk (Tokyo Heatwaves/Rain)
    # Aggregated by Month for simple visualization
    query_weather = """
    SELECT 
        strftime('%Y', d.date) as year,
        strftime('%m', d.date) as month,
        AVG(w.temp_max) as avg_max_temp,
        SUM(CASE WHEN w.condition = 'Heatwave' THEN 1 ELSE 0 END) as heatwave_days,
        SUM(CASE WHEN w.condition IN ('Rain', 'Typhoon') THEN 1 ELSE 0 END) as rainy_days
    FROM fact_weather_daily w
    JOIN dim_date d ON w.date_id = d.date_id
    JOIN dim_weather_location l ON w.weather_loc_id = l.weather_loc_id
    WHERE l.city_name = 'Tokyo' -- Focus on Tokyo for summary
    GROUP BY 1, 2
    ORDER BY 1, 2
    """
    df_weather = pd.read_sql(query_weather, conn)

    # Query 6: Airport Capacity (Monthly Flights by Airport)
    query_flights = """
    SELECT 
        strftime('%Y', d.date) as year,
        strftime('%m', d.date) as month,
        a.airport_code,
        SUM(f.flights_count) as total_flights
    FROM fact_flights_daily f
    JOIN dim_date d ON f.date_id = d.date_id
    JOIN dim_airport a ON f.airport_id = a.airport_id
    WHERE d.year >= 2023
    GROUP BY 1, 2, 3
    ORDER BY 1, 2, 3
    """
    df_flights = pd.read_sql(query_flights, conn)

    data = {
        "monthly_trend": df_monthly.to_dict(orient="records"),
        "top_countries_2024": df_countries.to_dict(orient="records"),
        "seasonality": df_seasonality.to_dict(orient="records"),
        "fx_impact": df_fx_impact.to_dict(orient="records"),
        "weather_risk": df_weather.to_dict(orient="records"),
        "airport_capacity": df_flights.to_dict(orient="records")
    }
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f)
        
    print(f"✅ Dashboard data exported to: {OUTPUT_FILE}")
    conn.close()

if __name__ == "__main__":
    main()
