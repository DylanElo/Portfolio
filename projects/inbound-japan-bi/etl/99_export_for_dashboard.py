import pandas as pd
import sqlite3
import json
from pathlib import Path

# Config - cross-platform path resolution
DB_PATH = Path(__file__).parent.parent / "data" / "inbound_japan.db"
OUTPUT_DIR = Path(__file__).parent.parent / "dashboard" / "data"
OUTPUT_FILE = OUTPUT_DIR / "dashboard_data.json"

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
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

    # ==== NEW: PRESCRIPTIVE ANALYTICS ====
    
    # Query 7: Marketing Recommendations (Growth + FX Scoring)
    query_marketing_priority = """
    WITH country_growth AS (
        SELECT 
            c.country_name_en,
            SUM(CASE WHEN m.year = 2024 THEN f.visitors_total ELSE 0 END) as visitors_2024,
            SUM(CASE WHEN m.year = 2023 THEN f.visitors_total ELSE 0 END) as visitors_2023
        FROM fact_inbound_arrivals_monthly f
        JOIN dim_country c ON f.country_id = c.country_id
        JOIN dim_month m ON f.month_id = m.month_id
        WHERE m.year IN (2023, 2024)
        GROUP BY c.country_name_en
    )
    SELECT 
        country_name_en,
        visitors_2024,
        ROUND((visitors_2024 * 1.0 / NULLIF(visitors_2023, 0) - 1) * 100, 1) as growth_rate,
        CASE 
            WHEN (visitors_2024 * 1.0 / NULLIF(visitors_2023, 0) - 1) >= 0.15 THEN 'High Priority'
            WHEN (visitors_2024 * 1.0 / NULLIF(visitors_2023, 0) - 1) >= 0.05 THEN 'Medium Priority'
            ELSE 'Maintain'
        END as recommendation
    FROM country_growth
    WHERE visitors_2023 > 0
    ORDER BY growth_rate DESC
    LIMIT 8
    """
    df_marketing = pd.read_sql(query_marketing_priority, conn)
    
    # Query 8: Staffing Forecast (Next 6 Months Based on Seasonal Average)
    # Using 2019-2024 averages to project demand
    query_staffing = """
    WITH seasonal_avg AS (
        SELECT 
            m.month,
            AVG(f.visitors_total) as avg_monthly_visitors
        FROM fact_inbound_arrivals_monthly f
        JOIN dim_month m ON f.month_id = m.month_id
        WHERE m.year >= 2019 AND m.year <= 2024
        GROUP BY m.month
    )
    SELECT 
        month,
        ROUND(avg_monthly_visitors) as projected_visitors,
        CASE 
            WHEN month IN (3, 4, 10, 11) THEN ROUND(avg_monthly_visitors / 80)  -- Peak months: 1 guide per 80 visitors
            ELSE ROUND(avg_monthly_visitors / 120)  -- Off-peak: 1 guide per 120
        END as recommended_staff
    FROM seasonal_avg
    ORDER BY month
    """
    df_staffing = pd.read_sql(query_staffing, conn)
    
    # Query 9: Capacity Health (Airport Utilization)
    query_capacity = """
    WITH recent_flights AS (
        SELECT 
            a.airport_code,
            a.airport_name,
            AVG(f.total_flights) as avg_monthly_flights
        FROM (
            SELECT 
                airport_id,
                strftime('%Y', d.date) as year,
                strftime('%m', d.date) as month,
                SUM(flights_count) as total_flights
            FROM fact_flights_daily
            JOIN dim_date d ON fact_flights_daily.date_id = d.date_id
            WHERE d.year = 2024
            GROUP BY airport_id, year, month
        ) f
        JOIN dim_airport a ON f.airport_id = a.airport_id
        GROUP BY a.airport_code, a.airport_name
    ),
    capacity_limits AS (
        SELECT 'NRT' as code, 8000 as capacity UNION
        SELECT 'HND', 7500 UNION
        SELECT 'KIX', 5000 UNION
        SELECT 'FUK', 3000 UNION
        SELECT 'CTS', 2500
    )
    SELECT 
        r.airport_code,
        r.airport_name,
        ROUND(r.avg_monthly_flights) as current_flights,
        c.capacity as max_capacity,
        ROUND((r.avg_monthly_flights * 100.0 / c.capacity), 1) as utilization_pct,
        CASE 
            WHEN (r.avg_monthly_flights / c.capacity) >= 0.85 THEN 'Critical'
            WHEN (r.avg_monthly_flights / c.capacity) >= 0.70 THEN 'Warning'
            ELSE 'Healthy'
        END as status
    FROM recent_flights r
    JOIN capacity_limits c ON r.airport_code = c.code
    ORDER BY utilization_pct DESC
    """
    df_capacity = pd.read_sql(query_capacity, conn)

    data = {
        "monthly_trend": df_monthly.to_dict(orient="records"),
        "top_countries_2024": df_countries.to_dict(orient="records"),
        "seasonality": df_seasonality.to_dict(orient="records"),
        "fx_impact": df_fx_impact.to_dict(orient="records"),
        "weather_risk": df_weather.to_dict(orient="records"),
        "airport_capacity": df_flights.to_dict(orient="records"),
        # NEW: Prescriptive insights
        "marketing_recommendations": df_marketing.to_dict(orient="records"),
        "staffing_forecast": df_staffing.to_dict(orient="records"),
        "capacity_health": df_capacity.to_dict(orient="records")
    }
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f)
        
    print(f"✅ Dashboard data exported to: {OUTPUT_FILE}")
    conn.close()

if __name__ == "__main__":
    main()
