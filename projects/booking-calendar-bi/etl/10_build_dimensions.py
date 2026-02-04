"""
Step 2: Build dimension tables from staged booking data.

Star schema dimensions:
  - dim_date          : Calendar (daily, 2013-2028)
  - dim_month         : Monthly grain
  - dim_agent         : Travel agents / tour operators
  - dim_service_type  : Service categories (Accommodation, Guide, etc.)
  - dim_location      : Japan locations + regions
  - dim_supplier      : Service suppliers
  - dim_consultant    : Booking + operations consultants
  - dim_booking_status: Booking status codes
  - dim_service_status: Service-level status codes
"""

import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "bookings.db"


def build_dim_date(conn):
    """Calendar dimension: 2013-01-01 to 2028-12-31."""
    start = datetime(2013, 1, 1)
    end = datetime(2028, 12, 31)
    dates = []
    current = start
    while current <= end:
        m = current.month
        dates.append({
            "date_id": int(current.strftime("%Y%m%d")),
            "date": current.strftime("%Y-%m-%d"),
            "year": current.year,
            "month": m,
            "day": current.day,
            "quarter": (m - 1) // 3 + 1,
            "day_of_week": current.weekday(),
            "day_name": current.strftime("%A"),
            "month_name": current.strftime("%B"),
            "is_weekend": 1 if current.weekday() >= 5 else 0,
            "season": _season(m),
            "fiscal_year": current.year if m >= 4 else current.year - 1,
        })
        current += timedelta(days=1)

    df = pd.DataFrame(dates)
    df.to_sql("dim_date", conn, if_exists="replace", index=False)
    print(f"  dim_date: {len(df):,} rows")


def _season(m):
    if m in [3, 4, 5]:
        return "Spring"
    if m in [6, 7, 8]:
        return "Summer"
    if m in [9, 10, 11]:
        return "Autumn"
    return "Winter"


def build_dim_month(conn):
    months = []
    for year in range(2013, 2029):
        for month in range(1, 13):
            months.append({
                "month_id": int(f"{year}{month:02d}"),
                "year": year,
                "month": month,
                "month_name": datetime(year, month, 1).strftime("%B"),
                "quarter": (month - 1) // 3 + 1,
                "season": _season(month),
            })
    df = pd.DataFrame(months)
    df.to_sql("dim_month", conn, if_exists="replace", index=False)
    print(f"  dim_month: {len(df):,} rows")


def build_dim_agent(conn):
    """Agent dimension from booking data (agent = tour operator / travel agency)."""
    df = pd.read_sql("""
        SELECT DISTINCT
            AGENT_NAME as agent_name,
            AGENT_ANALYSIS1_NAME as agent_country
        FROM stg_bookings
        WHERE AGENT_NAME IS NOT NULL
    """, conn)
    df = df.reset_index(drop=True)
    df["agent_id"] = df.index + 1
    df.to_sql("dim_agent", conn, if_exists="replace", index=False)
    print(f"  dim_agent: {len(df):,} rows")


def build_dim_service_type(conn):
    """Service type dimension (Accommodation, Guide, Activities, etc.)."""
    df = pd.read_sql("""
        SELECT DISTINCT PRODUCT_SERVICE_NAME as service_type
        FROM stg_bookings
        WHERE PRODUCT_SERVICE_NAME IS NOT NULL
    """, conn)
    df = df.reset_index(drop=True)
    df["service_type_id"] = df.index + 1
    df.to_sql("dim_service_type", conn, if_exists="replace", index=False)
    print(f"  dim_service_type: {len(df):,} rows")


def build_dim_location(conn):
    """Location dimension (city + region in Japan)."""
    df = pd.read_sql("""
        SELECT DISTINCT
            PRODUCT_LOCATION_NAME as location_name,
            REGION as region
        FROM stg_bookings
        WHERE PRODUCT_LOCATION_NAME IS NOT NULL
    """, conn)
    df = df.reset_index(drop=True)
    df["location_id"] = df.index + 1
    df.to_sql("dim_location", conn, if_exists="replace", index=False)
    print(f"  dim_location: {len(df):,} rows")


def build_dim_supplier(conn):
    """Supplier dimension (hotels, tour companies, transport providers)."""
    df = pd.read_sql("""
        SELECT DISTINCT SUPPLIER_NAME as supplier_name
        FROM stg_bookings
        WHERE SUPPLIER_NAME IS NOT NULL
    """, conn)
    df = df.reset_index(drop=True)
    df["supplier_id"] = df.index + 1
    df.to_sql("dim_supplier", conn, if_exists="replace", index=False)
    print(f"  dim_supplier: {len(df):,} rows")


def build_dim_consultant(conn):
    """Consultant dimension (booking + ops consultants)."""
    booking_consultants = pd.read_sql("""
        SELECT DISTINCT BOOKING_CONSULTANT_NAME as consultant_name
        FROM stg_bookings WHERE BOOKING_CONSULTANT_NAME IS NOT NULL
    """, conn)
    booking_consultants["role"] = "Booking"

    ops_consultants = pd.read_sql("""
        SELECT DISTINCT "OP CONSULTANT" as consultant_name
        FROM stg_bookings WHERE "OP CONSULTANT" IS NOT NULL
    """, conn)
    ops_consultants["role"] = "Operations"

    df = pd.concat([booking_consultants, ops_consultants]).drop_duplicates(
        subset=["consultant_name", "role"]
    ).reset_index(drop=True)
    df["consultant_id"] = df.index + 1
    df.to_sql("dim_consultant", conn, if_exists="replace", index=False)
    print(f"  dim_consultant: {len(df):,} rows")


def build_dim_booking_status(conn):
    """Booking status codes."""
    statuses = pd.read_sql("""
        SELECT DISTINCT BOOKING_STATUS as status_code
        FROM stg_bookings
    """, conn)

    status_labels = {
        "IV": "Invoice", "CF": "Confirmed", "CX": "Cancelled",
        "CP": "Completed", "CC": "Credit Card", "IX": "Index",
        "FC": "Final Confirmed",
    }
    statuses["status_name"] = statuses["status_code"].map(status_labels).fillna("Unknown")
    statuses = statuses.reset_index(drop=True)
    statuses["booking_status_id"] = statuses.index + 1
    statuses.to_sql("dim_booking_status", conn, if_exists="replace", index=False)
    print(f"  dim_booking_status: {len(statuses):,} rows")


def build_dim_service_status(conn):
    """Service-level status codes."""
    statuses = pd.read_sql("""
        SELECT DISTINCT SERVICE_STATUS as status_code
        FROM stg_bookings
        WHERE SERVICE_STATUS IS NOT NULL
    """, conn)

    status_labels = {
        "OK": "Confirmed", "CX": "Cancelled", "AG": "Agent Hold",
        "RQ": "Requested", "FB": "Fallback", "CA": "Cancel Requested",
        "CC": "Credit Card", "EK": "E-Ticket", "OI": "On Invoice",
        "CR": "Credit", "OL": "Online", "WL": "Waitlist",
    }
    statuses["status_name"] = statuses["status_code"].map(status_labels).fillna("Other")
    statuses = statuses.reset_index(drop=True)
    statuses["service_status_id"] = statuses.index + 1
    statuses.to_sql("dim_service_status", conn, if_exists="replace", index=False)
    print(f"  dim_service_status: {len(statuses):,} rows")


def main():
    print("=== Building Dimensions ===\n")
    conn = sqlite3.connect(DB_PATH)

    build_dim_date(conn)
    build_dim_month(conn)
    build_dim_agent(conn)
    build_dim_service_type(conn)
    build_dim_location(conn)
    build_dim_supplier(conn)
    build_dim_consultant(conn)
    build_dim_booking_status(conn)
    build_dim_service_status(conn)

    conn.close()
    print("\nDimensions complete.")


if __name__ == "__main__":
    main()
