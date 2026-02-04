"""
Step 3: Build fact table from staged bookings + dimension lookups.

Creates:
  - fact_bookings: One row per booking with foreign keys to all dimensions
                   Measures: pax, nights, revenue, cost, margin
"""

import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "bookings.db"


def main():
    print("=== Building Fact Table ===\n")

    conn = sqlite3.connect(DB_PATH)

    # Load staged bookings
    df = pd.read_sql("SELECT * FROM stg_bookings", conn)
    print(f"  Staged bookings: {len(df)} rows")

    # Load dimension lookups
    df_status = pd.read_sql("SELECT status_id, status_name FROM dim_status", conn)

    # --- Build foreign keys ---

    # date_id from booking_date (YYYYMMDD integer)
    df["booking_date"] = pd.to_datetime(df["booking_date"], errors="coerce")
    df["checkin_date"] = pd.to_datetime(df["checkin_date"], errors="coerce")
    df["checkout_date"] = pd.to_datetime(df["checkout_date"], errors="coerce")

    df["booking_date_id"] = df["booking_date"].dt.strftime("%Y%m%d").astype(int)
    df["checkin_date_id"] = df["checkin_date"].dt.strftime("%Y%m%d").astype(int)
    df["checkout_date_id"] = df["checkout_date"].dt.strftime("%Y%m%d").astype(int)

    # month_id from booking_date
    df["month_id"] = (
        df["booking_date"].dt.year.astype(str)
        + df["booking_date"].dt.month.apply(lambda x: f"{x:02d}")
    ).astype(int)

    # status_id lookup
    status_map = dict(zip(df_status["status_name"], df_status["status_id"]))
    df["status_id"] = df["status"].map(status_map)

    # Calculate margin
    df["margin"] = df["revenue"] - df["cost"]
    df["margin_pct"] = ((df["margin"] / df["revenue"]) * 100).round(1)

    # Select final columns for fact table
    fact_cols = [
        "booking_id",
        "booking_date_id",
        "checkin_date_id",
        "checkout_date_id",
        "month_id",
        "client_id",
        "service_id",
        "agent_id",
        "status_id",
        "pax",
        "nights",
        "revenue",
        "cost",
        "margin",
        "margin_pct",
        "currency",
    ]

    fact = df[fact_cols].copy()

    fact.to_sql("fact_bookings", conn, if_exists="replace", index=False)
    print(f"  fact_bookings: {len(fact)} rows")

    # Print quick validation
    print("\n  Validation:")
    total_rev = fact["revenue"].sum()
    total_margin = fact["margin"].sum()
    avg_margin = fact["margin_pct"].mean()
    print(f"    Total revenue: {total_rev:,.2f} EUR")
    print(f"    Total margin:  {total_margin:,.2f} EUR")
    print(f"    Avg margin %:  {avg_margin:.1f}%")

    conn.close()
    print("\nFact table built.")


if __name__ == "__main__":
    main()
