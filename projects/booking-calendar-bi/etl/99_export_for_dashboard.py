"""
Step 4: Export aggregated data from SQLite to JSON for the web dashboard
and a flat CSV for Looker Studio.
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

    # --- KPIs (all time + latest full year) ---
    q_kpis = """
    SELECT
        (SELECT COUNT(DISTINCT booking_ref) FROM fact_bookings) as total_bookings,
        (SELECT SUM(pax) FROM fact_bookings) as total_pax,
        (SELECT SUM(total_services) FROM fact_bookings) as total_services,
        (SELECT ROUND(AVG(trip_days), 1) FROM fact_bookings WHERE trip_days > 0) as avg_trip_days,
        (SELECT ROUND(AVG(total_services), 1) FROM fact_bookings) as avg_services_per_booking,
        (SELECT COUNT(DISTINCT booking_ref) FROM fact_bookings
         WHERE month_id BETWEEN 202401 AND 202412) as bookings_2024,
        (SELECT COUNT(DISTINCT booking_ref) FROM fact_bookings
         WHERE month_id BETWEEN 202501 AND 202512) as bookings_2025
    """
    df_kpis = pd.read_sql(q_kpis, conn)

    # --- Monthly booking trend ---
    q_monthly = """
    SELECT
        m.year, m.month, m.month_name,
        COUNT(DISTINCT fb.booking_ref) as total_bookings,
        SUM(fb.pax) as total_pax,
        SUM(fb.total_services) as total_services
    FROM fact_bookings fb
    JOIN dim_month m ON fb.month_id = m.month_id
    WHERE m.year BETWEEN 2015 AND 2027
    GROUP BY m.year, m.month
    ORDER BY m.year, m.month
    """
    df_monthly = pd.read_sql(q_monthly, conn)

    # --- Year-over-Year ---
    q_yoy = """
    SELECT
        m.year,
        COUNT(DISTINCT fb.booking_ref) as total_bookings,
        SUM(fb.pax) as total_pax,
        SUM(fb.total_services) as total_services,
        ROUND(AVG(fb.trip_days), 1) as avg_trip_days,
        COUNT(DISTINCT fb.agent_id) as active_agents
    FROM fact_bookings fb
    JOIN dim_month m ON fb.month_id = m.month_id
    WHERE m.year BETWEEN 2015 AND 2027
    GROUP BY m.year
    ORDER BY m.year
    """
    df_yoy = pd.read_sql(q_yoy, conn)

    # --- Top Agents by Bookings ---
    q_agents = """
    SELECT
        a.agent_name,
        a.agent_country,
        COUNT(DISTINCT fb.booking_ref) as booking_count,
        SUM(fb.pax) as total_pax,
        ROUND(AVG(fb.trip_days), 1) as avg_trip_days
    FROM fact_bookings fb
    JOIN dim_agent a ON fb.agent_id = a.agent_id
    GROUP BY a.agent_id
    ORDER BY booking_count DESC
    LIMIT 20
    """
    df_agents = pd.read_sql(q_agents, conn)

    # --- Agent Country Distribution ---
    q_countries = """
    SELECT
        a.agent_country,
        COUNT(DISTINCT fb.booking_ref) as booking_count,
        SUM(fb.pax) as total_pax
    FROM fact_bookings fb
    JOIN dim_agent a ON fb.agent_id = a.agent_id
    GROUP BY a.agent_country
    ORDER BY booking_count DESC
    LIMIT 15
    """
    df_countries = pd.read_sql(q_countries, conn)

    # --- Service Type Breakdown ---
    q_services = """
    SELECT
        st.service_type,
        COUNT(*) as service_count,
        COUNT(DISTINCT fs.booking_ref) as booking_count
    FROM fact_services fs
    JOIN dim_service_type st ON fs.service_type_id = st.service_type_id
    GROUP BY st.service_type
    ORDER BY service_count DESC
    """
    df_services = pd.read_sql(q_services, conn)

    # --- Top Locations ---
    q_locations = """
    SELECT
        l.location_name,
        l.region,
        COUNT(*) as service_count,
        COUNT(DISTINCT fs.booking_ref) as booking_count
    FROM fact_services fs
    JOIN dim_location l ON fs.location_id = l.location_id
    GROUP BY l.location_id
    ORDER BY service_count DESC
    LIMIT 20
    """
    df_locations = pd.read_sql(q_locations, conn)

    # --- Booking Status Distribution ---
    q_status = """
    SELECT
        bs.status_code,
        bs.status_name,
        COUNT(*) as booking_count
    FROM fact_bookings fb
    JOIN dim_booking_status bs ON fb.booking_status_id = bs.booking_status_id
    GROUP BY bs.booking_status_id
    ORDER BY booking_count DESC
    """
    df_status = pd.read_sql(q_status, conn)

    # --- Region Distribution ---
    q_regions = """
    SELECT
        l.region,
        COUNT(*) as service_count,
        COUNT(DISTINCT fs.booking_ref) as booking_count
    FROM fact_services fs
    JOIN dim_location l ON fs.location_id = l.location_id
    WHERE l.region IS NOT NULL AND l.region != ''
    GROUP BY l.region
    ORDER BY service_count DESC
    """
    df_regions = pd.read_sql(q_regions, conn)

    # --- Seasonality: bookings by month x source country ---
    q_season = """
    SELECT
        a.agent_country,
        m.month,
        COUNT(DISTINCT fb.booking_ref) as booking_count
    FROM fact_bookings fb
    JOIN dim_agent a ON fb.agent_id = a.agent_id
    JOIN dim_month m ON fb.month_id = m.month_id
    WHERE a.agent_country IN (
        SELECT a2.agent_country
        FROM fact_bookings fb2 JOIN dim_agent a2 ON fb2.agent_id = a2.agent_id
        GROUP BY a2.agent_country ORDER BY COUNT(*) DESC LIMIT 8
    )
    GROUP BY a.agent_country, m.month
    """
    df_season = pd.read_sql(q_season, conn)

    # --- Top Suppliers ---
    q_suppliers = """
    SELECT
        s.supplier_name,
        COUNT(*) as service_count,
        COUNT(DISTINCT fs.booking_ref) as booking_count
    FROM fact_services fs
    JOIN dim_supplier s ON fs.supplier_id = s.supplier_id
    GROUP BY s.supplier_id
    ORDER BY service_count DESC
    LIMIT 15
    """
    df_suppliers = pd.read_sql(q_suppliers, conn)

    # --- Lead Time (days between entered and travel) ---
    q_leadtime = """
    SELECT
        CASE
            WHEN (fb.travel_date_id - fb.entered_date_id) <= 30 THEN '0-30 days'
            WHEN (fb.travel_date_id - fb.entered_date_id) <= 90 THEN '31-90 days'
            WHEN (fb.travel_date_id - fb.entered_date_id) <= 180 THEN '91-180 days'
            WHEN (fb.travel_date_id - fb.entered_date_id) <= 365 THEN '181-365 days'
            ELSE '365+ days'
        END as lead_time_bucket,
        COUNT(*) as booking_count,
        ROUND(AVG(fb.trip_days), 1) as avg_trip_days
    FROM fact_bookings fb
    WHERE fb.travel_date_id > fb.entered_date_id
    GROUP BY lead_time_bucket
    ORDER BY MIN(fb.travel_date_id - fb.entered_date_id)
    """
    df_leadtime = pd.read_sql(q_leadtime, conn)

    # --- Department distribution ---
    q_dept = """
    SELECT
        department,
        COUNT(DISTINCT booking_ref) as booking_count,
        SUM(pax) as total_pax
    FROM fact_bookings
    GROUP BY department
    ORDER BY booking_count DESC
    """
    df_dept = pd.read_sql(q_dept, conn)

    # --- Assemble JSON ---
    dashboard_data = {
        "kpis": df_kpis.to_dict(orient="records")[0] if len(df_kpis) > 0 else {},
        "monthly_trend": df_monthly.to_dict(orient="records"),
        "yearly_summary": df_yoy.to_dict(orient="records"),
        "top_agents": df_agents.to_dict(orient="records"),
        "agent_countries": df_countries.to_dict(orient="records"),
        "service_breakdown": df_services.to_dict(orient="records"),
        "top_locations": df_locations.to_dict(orient="records"),
        "status_breakdown": df_status.to_dict(orient="records"),
        "region_distribution": df_regions.to_dict(orient="records"),
        "seasonality": df_season.to_dict(orient="records"),
        "top_suppliers": df_suppliers.to_dict(orient="records"),
        "lead_time": df_leadtime.to_dict(orient="records"),
        "department_breakdown": df_dept.to_dict(orient="records"),
    }

    output = DASHBOARD_DIR / "dashboard_data.json"
    with open(output, "w") as f:
        json.dump(dashboard_data, f, indent=2)
    print(f"  Dashboard JSON: {output}")

    # --- Looker Studio flat CSV ---
    q_flat = """
    SELECT
        fs.booking_ref,
        d.date as service_date,
        d.year, d.month, d.month_name, d.quarter, d.season, d.day_name, d.is_weekend,
        a.agent_name, a.agent_country,
        st.service_type,
        l.location_name, l.region,
        s.supplier_name,
        bs.status_code as booking_status, bs.status_name as booking_status_name,
        ss.status_code as service_status, ss.status_name as service_status_name,
        fs.pax, fs.children, fs.day_number, fs.sequence_number,
        fs.product_option, fs.department
    FROM fact_services fs
    LEFT JOIN dim_date d ON fs.service_date_id = d.date_id
    LEFT JOIN dim_agent a ON fs.agent_id = a.agent_id
    LEFT JOIN dim_service_type st ON fs.service_type_id = st.service_type_id
    LEFT JOIN dim_location l ON fs.location_id = l.location_id
    LEFT JOIN dim_supplier s ON fs.supplier_id = s.supplier_id
    LEFT JOIN dim_booking_status bs ON fs.booking_status_id = bs.booking_status_id
    LEFT JOIN dim_service_status ss ON fs.service_status_id = ss.service_status_id
    ORDER BY d.date, fs.booking_ref, fs.day_number, fs.sequence_number
    """
    df_flat = pd.read_sql(q_flat, conn)
    looker_file = LOOKER_DIR / "bookings_flat.csv"
    df_flat.to_csv(looker_file, index=False)
    print(f"  Looker CSV: {looker_file} ({len(df_flat):,} rows)")

    conn.close()
    print("\nExport complete.")


if __name__ == "__main__":
    main()
