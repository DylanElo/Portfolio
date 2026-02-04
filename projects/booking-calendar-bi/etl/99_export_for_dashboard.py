"""
Step 4: Export aggregated data from SQLite to JSON for the web dashboard.

This replaces the need for Sheets/Excel reporting entirely.
The JSON output feeds the Chart.js dashboard directly.

Also exports a Looker Studio-compatible CSV if you want to use that instead.
"""

import pandas as pd
import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "bookings.db"
DASHBOARD_DIR = Path(__file__).parent.parent / "dashboard" / "data"
LOOKER_DIR = Path(__file__).parent.parent / "data" / "looker_export"


def main():
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    LOOKER_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    print("=== Exporting Dashboard Data ===\n")

    # --- Query 1: Monthly Booking Trend ---
    q_monthly = """
    SELECT
        m.year, m.month, m.month_name,
        COUNT(*) as total_bookings,
        SUM(f.pax) as total_pax,
        ROUND(SUM(f.revenue), 2) as total_revenue,
        ROUND(SUM(f.margin), 2) as total_margin,
        ROUND(AVG(f.margin_pct), 1) as avg_margin_pct
    FROM fact_bookings f
    JOIN dim_month m ON f.month_id = m.month_id
    GROUP BY m.year, m.month
    ORDER BY m.year, m.month
    """
    df_monthly = pd.read_sql(q_monthly, conn)

    # --- Query 2: Revenue by Service Category ---
    q_service = """
    SELECT
        s.service_category,
        COUNT(*) as booking_count,
        SUM(f.pax) as total_pax,
        ROUND(SUM(f.revenue), 2) as total_revenue,
        ROUND(AVG(f.margin_pct), 1) as avg_margin_pct
    FROM fact_bookings f
    JOIN dim_service s ON f.service_id = s.service_id
    GROUP BY s.service_category
    ORDER BY total_revenue DESC
    """
    df_service = pd.read_sql(q_service, conn)

    # --- Query 3: Top Clients by Revenue ---
    q_clients = """
    SELECT
        c.client_name,
        c.client_type,
        c.client_region,
        COUNT(*) as booking_count,
        ROUND(SUM(f.revenue), 2) as total_revenue,
        ROUND(AVG(f.margin_pct), 1) as avg_margin_pct
    FROM fact_bookings f
    JOIN dim_client c ON f.client_id = c.client_id
    GROUP BY c.client_id
    ORDER BY total_revenue DESC
    LIMIT 15
    """
    df_clients = pd.read_sql(q_clients, conn)

    # --- Query 4: Booking Status Breakdown ---
    q_status = """
    SELECT
        st.status_name,
        COUNT(*) as count,
        ROUND(SUM(f.revenue), 2) as revenue
    FROM fact_bookings f
    JOIN dim_status st ON f.status_id = st.status_id
    GROUP BY st.status_name
    ORDER BY count DESC
    """
    df_status = pd.read_sql(q_status, conn)

    # --- Query 5: Agent Performance ---
    q_agents = """
    SELECT
        a.agent_name,
        a.team,
        COUNT(*) as booking_count,
        SUM(f.pax) as total_pax,
        ROUND(SUM(f.revenue), 2) as total_revenue,
        ROUND(AVG(f.margin_pct), 1) as avg_margin_pct
    FROM fact_bookings f
    JOIN dim_agent a ON f.agent_id = a.agent_id
    GROUP BY a.agent_id
    ORDER BY total_revenue DESC
    """
    df_agents = pd.read_sql(q_agents, conn)

    # --- Query 6: Destination Performance ---
    q_dest = """
    SELECT
        s.destination,
        COUNT(*) as booking_count,
        SUM(f.pax) as total_pax,
        ROUND(SUM(f.revenue), 2) as total_revenue
    FROM fact_bookings f
    JOIN dim_service s ON f.service_id = s.service_id
    GROUP BY s.destination
    ORDER BY total_revenue DESC
    """
    df_dest = pd.read_sql(q_dest, conn)

    # --- Query 7: Seasonality Heatmap (month x client_region) ---
    q_season = """
    SELECT
        c.client_region,
        m.month,
        COUNT(*) as booking_count,
        ROUND(SUM(f.revenue), 2) as revenue
    FROM fact_bookings f
    JOIN dim_client c ON f.client_id = c.client_id
    JOIN dim_month m ON f.month_id = m.month_id
    GROUP BY c.client_region, m.month
    """
    df_season = pd.read_sql(q_season, conn)

    # --- Query 8: Year-over-Year Growth ---
    q_yoy = """
    SELECT
        m.year,
        COUNT(*) as total_bookings,
        SUM(f.pax) as total_pax,
        ROUND(SUM(f.revenue), 2) as total_revenue,
        ROUND(SUM(f.margin), 2) as total_margin
    FROM fact_bookings f
    JOIN dim_month m ON f.month_id = m.month_id
    GROUP BY m.year
    ORDER BY m.year
    """
    df_yoy = pd.read_sql(q_yoy, conn)

    # --- Query 9: Booking Lead Time Distribution ---
    q_leadtime = """
    SELECT
        CASE
            WHEN (f.checkin_date_id - f.booking_date_id) <= 7 THEN '0-7 days'
            WHEN (f.checkin_date_id - f.booking_date_id) <= 30 THEN '8-30 days'
            WHEN (f.checkin_date_id - f.booking_date_id) <= 60 THEN '31-60 days'
            ELSE '60+ days'
        END as lead_time_bucket,
        COUNT(*) as booking_count,
        ROUND(AVG(f.revenue), 2) as avg_revenue
    FROM fact_bookings f
    GROUP BY lead_time_bucket
    ORDER BY MIN(f.checkin_date_id - f.booking_date_id)
    """
    df_leadtime = pd.read_sql(q_leadtime, conn)

    # --- Query 10: KPIs (latest year) ---
    q_kpis = """
    SELECT
        COUNT(*) as total_bookings,
        SUM(f.pax) as total_pax,
        ROUND(SUM(f.revenue), 2) as total_revenue,
        ROUND(SUM(f.margin), 2) as total_margin,
        ROUND(AVG(f.margin_pct), 1) as avg_margin_pct,
        ROUND(SUM(f.revenue) / COUNT(*), 2) as avg_booking_value
    FROM fact_bookings f
    JOIN dim_month m ON f.month_id = m.month_id
    WHERE m.year = (SELECT MAX(year) FROM dim_month dm
                    JOIN fact_bookings fb ON dm.month_id = fb.month_id)
    """
    df_kpis = pd.read_sql(q_kpis, conn)

    # --- Assemble JSON ---
    dashboard_data = {
        "kpis": df_kpis.to_dict(orient="records")[0] if len(df_kpis) > 0 else {},
        "monthly_trend": df_monthly.to_dict(orient="records"),
        "service_breakdown": df_service.to_dict(orient="records"),
        "top_clients": df_clients.to_dict(orient="records"),
        "status_breakdown": df_status.to_dict(orient="records"),
        "agent_performance": df_agents.to_dict(orient="records"),
        "destination_performance": df_dest.to_dict(orient="records"),
        "seasonality": df_season.to_dict(orient="records"),
        "yearly_summary": df_yoy.to_dict(orient="records"),
        "lead_time": df_leadtime.to_dict(orient="records"),
    }

    output_file = DASHBOARD_DIR / "dashboard_data.json"
    with open(output_file, "w") as f:
        json.dump(dashboard_data, f, indent=2)
    print(f"  Dashboard JSON: {output_file}")

    # --- Export Looker Studio CSV ---
    # Flat denormalized table for easy Looker import
    q_flat = """
    SELECT
        f.booking_id,
        d.date as booking_date,
        d.year as booking_year,
        d.month as booking_month,
        d.month_name,
        d.quarter,
        d.season,
        d.day_name,
        d.is_weekend,
        c.client_name,
        c.client_type,
        c.client_region,
        c.client_country,
        s.service_name,
        s.service_category,
        s.destination,
        a.agent_name,
        a.team as agent_team,
        st.status_name as booking_status,
        f.pax,
        f.nights,
        f.revenue,
        f.cost,
        f.margin,
        f.margin_pct,
        f.currency
    FROM fact_bookings f
    JOIN dim_date d ON f.booking_date_id = d.date_id
    JOIN dim_client c ON f.client_id = c.client_id
    JOIN dim_service s ON f.service_id = s.service_id
    JOIN dim_agent a ON f.agent_id = a.agent_id
    JOIN dim_status st ON f.status_id = st.status_id
    ORDER BY d.date
    """
    df_flat = pd.read_sql(q_flat, conn)
    looker_file = LOOKER_DIR / "bookings_flat.csv"
    df_flat.to_csv(looker_file, index=False)
    print(f"  Looker CSV:     {looker_file} ({len(df_flat)} rows)")

    conn.close()
    print("\nExport complete.")


if __name__ == "__main__":
    main()
