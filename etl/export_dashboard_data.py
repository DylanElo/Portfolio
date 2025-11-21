import sqlite3
import json
import os

DB_PATH = 'studio_pierrot.db'
OUTPUT_PATH = 'dashboard/data.json'

def export_data():
    print("Exporting Dashboard Data (V2)...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    data = {}

    # 1. Global KPIs
    print("  - Calculating Global KPIs...")
    kpis = cursor.execute('''
        SELECT 
            SUM(views) as total_views,
            SUM(revenue_usd) as total_revenue,
            SUM(watch_time_minutes) as total_watch_time,
            AVG(sentiment_score) as avg_sentiment
        FROM fact_daily_performance
    ''').fetchone()
    data['kpis'] = dict(kpis)

    # 2. Daily Trend (Time Series)
    print("  - Aggregating Daily Trends...")
    daily_trend = cursor.execute('''
        SELECT 
            d.full_date as date,
            SUM(f.views) as views,
            SUM(f.revenue_usd) as revenue
        FROM fact_daily_performance f
        JOIN dim_date d ON f.date_id = d.date_id
        GROUP BY d.full_date
        ORDER BY d.full_date
    ''').fetchall()
    data['daily_trend'] = [dict(row) for row in daily_trend]

    # 3. Platform Split
    print("  - Aggregating Platform Data...")
    platform_split = cursor.execute('''
        SELECT 
            p.platform_name,
            SUM(f.views) as views,
            SUM(f.revenue_usd) as revenue
        FROM fact_daily_performance f
        JOIN dim_platform p ON f.platform_id = p.platform_id
        GROUP BY p.platform_name
        ORDER BY revenue DESC
    ''').fetchall()
    data['platform_split'] = [dict(row) for row in platform_split]

    # 4. Region Split
    print("  - Aggregating Region Data...")
    region_split = cursor.execute('''
        SELECT 
            r.region_name,
            SUM(f.views) as views,
            SUM(f.revenue_usd) as revenue
        FROM fact_daily_performance f
        JOIN dim_region r ON f.region_id = r.region_id
        GROUP BY r.region_name
        ORDER BY revenue DESC
    ''').fetchall()
    data['region_split'] = [dict(row) for row in region_split]

    # 5. Anime Performance (Top Lists)
    print("  - Aggregating Anime Performance...")
    anime_perf = cursor.execute('''
        SELECT 
            a.title,
            a.image_url,
            SUM(f.views) as views,
            SUM(f.revenue_usd) as revenue,
            AVG(f.sentiment_score) as sentiment,
            AVG(f.avg_completion_rate) as completion_rate
        FROM fact_daily_performance f
        JOIN dim_anime a ON f.anime_id = a.anime_id
        GROUP BY a.title
        ORDER BY revenue DESC
    ''').fetchall()
    data['anime_performance'] = [dict(row) for row in anime_perf]

    # 6. Heatmap Data (Day of Week)
    print("  - Aggregating Heatmap Data...")
    heatmap = cursor.execute('''
        SELECT 
            d.day_name,
            SUM(f.views) as views
        FROM fact_daily_performance f
        JOIN dim_date d ON f.date_id = d.date_id
        GROUP BY d.day_name
        ORDER BY 
            CASE d.day_name 
                WHEN 'Monday' THEN 1 
                WHEN 'Tuesday' THEN 2 
                WHEN 'Wednesday' THEN 3 
                WHEN 'Thursday' THEN 4 
                WHEN 'Friday' THEN 5 
                WHEN 'Saturday' THEN 6 
                WHEN 'Sunday' THEN 7 
            END
    ''').fetchall()
    data['heatmap'] = [dict(row) for row in heatmap]

    conn.close()

    # Write to JSON
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data exported to {OUTPUT_PATH}")

if __name__ == '__main__':
    export_data()
