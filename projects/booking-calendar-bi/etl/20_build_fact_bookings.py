"""
Step 3: Build fact tables from staged data + dimension lookups.

Creates two fact tables at different grains:
  - fact_services   : One row per service line item (1M+ rows) - operational detail
  - fact_bookings   : One row per booking (39K rows) - booking-level summary
"""

import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "bookings.db"


def build_fact_services(conn):
    """Service-level fact table: one row per service line in a booking."""
    print("  Building fact_services...")

    # Load dimension lookups
    agents = pd.read_sql("SELECT agent_id, agent_name, agent_country FROM dim_agent", conn)
    agent_map = {}
    for _, r in agents.iterrows():
        agent_map[(r["agent_name"], r["agent_country"])] = r["agent_id"]

    svc_types = pd.read_sql("SELECT service_type_id, service_type FROM dim_service_type", conn)
    svc_map = dict(zip(svc_types["service_type"], svc_types["service_type_id"]))

    locations = pd.read_sql("SELECT location_id, location_name, region FROM dim_location", conn)
    loc_map = {}
    for _, r in locations.iterrows():
        loc_map[(r["location_name"], r["region"])] = r["location_id"]

    suppliers = pd.read_sql("SELECT supplier_id, supplier_name FROM dim_supplier", conn)
    sup_map = dict(zip(suppliers["supplier_name"], suppliers["supplier_id"]))

    bk_statuses = pd.read_sql("SELECT booking_status_id, status_code FROM dim_booking_status", conn)
    bk_stat_map = dict(zip(bk_statuses["status_code"], bk_statuses["booking_status_id"]))

    svc_statuses = pd.read_sql("SELECT service_status_id, status_code FROM dim_service_status", conn)
    svc_stat_map = dict(zip(svc_statuses["status_code"], svc_statuses["service_status_id"]))

    # Load staging in chunks to manage memory
    df = pd.read_sql("SELECT * FROM stg_bookings", conn)
    print(f"    Staged rows: {len(df):,}")

    # Build FK columns
    df["agent_id"] = df.apply(
        lambda r: agent_map.get((r["AGENT_NAME"], r["AGENT_ANALYSIS1_NAME"])), axis=1
    )
    df["service_type_id"] = df["PRODUCT_SERVICE_NAME"].map(svc_map)
    df["location_id"] = df.apply(
        lambda r: loc_map.get((r["PRODUCT_LOCATION_NAME"], r["REGION"])), axis=1
    )
    df["supplier_id"] = df["SUPPLIER_NAME"].map(sup_map)
    df["booking_status_id"] = df["BOOKING_STATUS"].map(bk_stat_map)
    df["service_status_id"] = df["SERVICE_STATUS"].map(svc_stat_map)

    # Build date FKs (YYYYMMDD integers)
    for src, dst in [
        ("SERVICE_DATE", "service_date_id"),
        ("BOOKING_TRAVEL_DATE", "travel_date_id"),
        ("BOOKING_ENTERED_DATE", "entered_date_id"),
    ]:
        df[dst] = pd.to_datetime(df[src], errors="coerce").dt.strftime("%Y%m%d")
        df[dst] = pd.to_numeric(df[dst], errors="coerce").astype("Int64")

    # Month ID from service date
    svc_dt = pd.to_datetime(df["SERVICE_DATE"], errors="coerce")
    df["month_id"] = (svc_dt.dt.year.astype(str) + svc_dt.dt.month.apply(lambda x: f"{x:02d}")).astype("Int64")

    # Select fact columns
    fact = df[[
        "BOOKING_REFERENCE", "service_date_id", "travel_date_id", "entered_date_id",
        "month_id", "agent_id", "service_type_id", "location_id", "supplier_id",
        "booking_status_id", "service_status_id",
        "PAX", "CHILDREN", "DAY_NUMBER", "SEQUENCE_NUMBER",
        "PRODUCT_OPTION_NAME", "PRODUCT_OPTION_COMMENT",
        "BOOKING_NAME", "BOOKING_DEPARTMENT",
    ]].copy()

    fact.columns = [
        "booking_ref", "service_date_id", "travel_date_id", "entered_date_id",
        "month_id", "agent_id", "service_type_id", "location_id", "supplier_id",
        "booking_status_id", "service_status_id",
        "pax", "children", "day_number", "sequence_number",
        "product_option", "product_comment",
        "booking_name", "department",
    ]

    fact.to_sql("fact_services", conn, if_exists="replace", index=False)
    print(f"    fact_services: {len(fact):,} rows")
    return fact


def build_fact_bookings(conn):
    """Booking-level fact table: one row per booking (aggregated)."""
    print("\n  Building fact_bookings...")

    query = """
    SELECT
        fs.booking_ref,
        fs.travel_date_id,
        fs.entered_date_id,
        fs.agent_id,
        fs.booking_status_id,
        fs.booking_name,
        fs.department,
        MIN(fs.service_date_id) as first_service_date_id,
        MAX(fs.service_date_id) as last_service_date_id,
        MAX(fs.pax) as pax,
        MAX(fs.children) as children,
        COUNT(*) as total_services,
        COUNT(DISTINCT fs.service_type_id) as service_types_count,
        COUNT(DISTINCT fs.location_id) as locations_count,
        COUNT(DISTINCT fs.supplier_id) as suppliers_count,
        MAX(fs.day_number) as trip_days,
        SUM(CASE WHEN st.service_type = 'Accommodation' THEN 1 ELSE 0 END) as accommodation_nights,
        SUM(CASE WHEN st.service_type = 'Activities' THEN 1 ELSE 0 END) as activity_count,
        SUM(CASE WHEN st.service_type = 'Guide' THEN 1 ELSE 0 END) as guide_count,
        SUM(CASE WHEN st.service_type = 'Ground Transport' THEN 1 ELSE 0 END) as transport_count,
        SUM(CASE WHEN st.service_type = 'Flight Ticket' THEN 1 ELSE 0 END) as flight_count
    FROM fact_services fs
    LEFT JOIN dim_service_type st ON fs.service_type_id = st.service_type_id
    GROUP BY fs.booking_ref
    """

    df = pd.read_sql(query, conn)

    # Month ID from travel date
    travel_dt = pd.to_datetime(df["travel_date_id"].astype(str), format="%Y%m%d", errors="coerce")
    df["month_id"] = (travel_dt.dt.year.astype(str) + travel_dt.dt.month.apply(lambda x: f"{x:02d}")).astype("Int64")

    df.to_sql("fact_bookings", conn, if_exists="replace", index=False)
    print(f"    fact_bookings: {len(df):,} rows")


def main():
    print("=== Building Fact Tables ===\n")
    conn = sqlite3.connect(DB_PATH)

    build_fact_services(conn)
    build_fact_bookings(conn)

    # Quick validation
    print("\n  Validation:")
    for table in ["fact_services", "fact_bookings"]:
        count = pd.read_sql(f"SELECT COUNT(*) as n FROM {table}", conn).iloc[0, 0]
        print(f"    {table}: {count:,} rows")

    conn.close()
    print("\nFact tables complete.")


if __name__ == "__main__":
    main()
