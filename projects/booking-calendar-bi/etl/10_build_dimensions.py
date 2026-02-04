"""
Step 2: Build dimension tables from staged data.

Creates a star schema with:
  - dim_date      : Calendar dimension (daily grain)
  - dim_month     : Monthly calendar (for aggregations)
  - dim_client    : Client/agency profiles
  - dim_service   : Service catalog (tours, transfers, hotels)
  - dim_agent     : Sales/booking agents
  - dim_status    : Booking statuses
"""

import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "bookings.db"


def create_connection():
    return sqlite3.connect(DB_PATH)


def build_dim_date(conn):
    """Calendar dimension covering 2019-2027 for historical + forecasting."""
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2027, 12, 31)

    dates = []
    current = start_date
    while current <= end_date:
        month = current.month
        dates.append({
            "date_id": int(current.strftime("%Y%m%d")),
            "date": current.strftime("%Y-%m-%d"),
            "year": current.year,
            "month": month,
            "day": current.day,
            "quarter": (month - 1) // 3 + 1,
            "day_of_week": current.weekday(),  # 0=Monday
            "day_name": current.strftime("%A"),
            "month_name": current.strftime("%B"),
            "is_weekend": 1 if current.weekday() >= 5 else 0,
            "season": get_season(month),
            "fiscal_year": current.year if month >= 4 else current.year - 1,
        })
        current += timedelta(days=1)

    df = pd.DataFrame(dates)
    df.to_sql("dim_date", conn, if_exists="replace", index=False)
    print(f"  dim_date: {len(df)} rows (2019-2027)")


def get_season(month):
    if month in [3, 4, 5]:
        return "Spring"
    if month in [6, 7, 8]:
        return "Summer"
    if month in [9, 10, 11]:
        return "Autumn"
    return "Winter"


def build_dim_month(conn):
    """Monthly grain dimension for aggregated reporting."""
    months = []
    for year in range(2019, 2028):
        for month in range(1, 13):
            months.append({
                "month_id": int(f"{year}{month:02d}"),
                "year": year,
                "month": month,
                "month_name": datetime(year, month, 1).strftime("%B"),
                "quarter": (month - 1) // 3 + 1,
                "season": get_season(month),
            })

    df = pd.DataFrame(months)
    df.to_sql("dim_month", conn, if_exists="replace", index=False)
    print(f"  dim_month: {len(df)} rows")


def build_dim_client(conn):
    """Build client dimension from staged data."""
    try:
        df = pd.read_sql("SELECT * FROM stg_clients", conn)
        df = df.rename(columns={
            "id": "client_id",
            "name": "client_name",
            "type": "client_type",
            "region": "client_region",
            "country": "client_country",
        })
    except Exception:
        # Fallback: extract from booking data if no client reference table
        df_bookings = pd.read_sql(
            "SELECT DISTINCT client_id, client_name FROM stg_bookings", conn
        )
        df = df_bookings.copy()
        df["client_type"] = "Unknown"
        df["client_region"] = "Unknown"
        df["client_country"] = "Unknown"

    df.to_sql("dim_client", conn, if_exists="replace", index=False)
    print(f"  dim_client: {len(df)} rows")


def build_dim_service(conn):
    """Build service dimension from staged data."""
    try:
        df = pd.read_sql("SELECT * FROM stg_services", conn)
        df = df.rename(columns={
            "id": "service_id",
            "name": "service_name",
            "category": "service_category",
        })
    except Exception:
        df_bookings = pd.read_sql(
            "SELECT DISTINCT service_id, service_name, service_category, destination FROM stg_bookings",
            conn,
        )
        df = df_bookings.copy()

    df.to_sql("dim_service", conn, if_exists="replace", index=False)
    print(f"  dim_service: {len(df)} rows")


def build_dim_agent(conn):
    """Build agent dimension from staged data."""
    try:
        df = pd.read_sql("SELECT * FROM stg_agents", conn)
        df = df.rename(columns={
            "id": "agent_id",
            "name": "agent_name",
        })
    except Exception:
        df_bookings = pd.read_sql(
            "SELECT DISTINCT agent_id, agent_name FROM stg_bookings", conn
        )
        df = df_bookings.copy()
        df["team"] = "Unknown"

    df.to_sql("dim_agent", conn, if_exists="replace", index=False)
    print(f"  dim_agent: {len(df)} rows")


def build_dim_status(conn):
    """Booking status dimension."""
    statuses = [
        {"status_id": 1, "status_name": "Confirmed", "is_active": 1},
        {"status_id": 2, "status_name": "Pending", "is_active": 1},
        {"status_id": 3, "status_name": "Cancelled", "is_active": 0},
        {"status_id": 4, "status_name": "Completed", "is_active": 0},
    ]
    df = pd.DataFrame(statuses)
    df.to_sql("dim_status", conn, if_exists="replace", index=False)
    print(f"  dim_status: {len(df)} rows")


def main():
    print("=== Building Dimensions ===\n")
    conn = create_connection()

    build_dim_date(conn)
    build_dim_month(conn)
    build_dim_client(conn)
    build_dim_service(conn)
    build_dim_agent(conn)
    build_dim_status(conn)

    conn.close()
    print("\nDimensions built.")


if __name__ == "__main__":
    main()
