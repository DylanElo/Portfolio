"""
Step 1: Merge multiple CSV files into a single staging table in SQLite.

This handles the core problem: your VBA script exports booking data into
multiple CSVs (split by year or by sheet) because of Excel's row limits.
This script merges them all into one unified staging table.

Usage:
  - Place your VBA-exported CSVs in data/raw/ (or data/sample/ for demo)
  - The script auto-detects all bookings_*.csv files and merges them
  - Reference tables (clients.csv, services.csv, agents.csv) are loaded separately

To use your real data:
  1. Copy your VBA-exported CSVs into data/raw/
  2. Update COLUMN_MAP below if your column names differ
  3. Run: python etl/01_ingest_csvs.py
"""

import pandas as pd
import sqlite3
import glob
from pathlib import Path

# Config
PROJECT_DIR = Path(__file__).parent.parent
DB_PATH = PROJECT_DIR / "data" / "bookings.db"

# Change this to "raw" when using real data
DATA_SOURCE = "sample"
RAW_DIR = PROJECT_DIR / "data" / DATA_SOURCE

# Column mapping: YOUR CSV column name -> our standard name
# Update the left side to match your VBA export headers
COLUMN_MAP = {
    "booking_id": "booking_id",
    "booking_date": "booking_date",
    "checkin_date": "checkin_date",
    "checkout_date": "checkout_date",
    "client_id": "client_id",
    "client_name": "client_name",
    "service_id": "service_id",
    "service_name": "service_name",
    "service_category": "service_category",
    "destination": "destination",
    "agent_id": "agent_id",
    "agent_name": "agent_name",
    "status": "status",
    "pax": "pax",
    "nights": "nights",
    "revenue": "revenue",
    "cost": "cost",
    "currency": "currency",
}


def merge_booking_csvs():
    """Find all bookings_*.csv files and merge into one DataFrame."""
    csv_files = sorted(RAW_DIR.glob("bookings_*.csv"))

    if not csv_files:
        print(f"No bookings_*.csv files found in {RAW_DIR}")
        print("Place your VBA-exported CSVs there first.")
        return None

    frames = []
    for f in csv_files:
        df = pd.read_csv(f, encoding="utf-8")
        # Apply column mapping (rename if needed)
        df = df.rename(columns=COLUMN_MAP)
        frames.append(df)
        print(f"  Loaded {f.name}: {len(df)} rows")

    merged = pd.concat(frames, ignore_index=True)
    print(f"\n  Merged total: {len(merged)} rows")
    return merged


def load_reference_table(filename, table_name, conn):
    """Load a reference CSV (clients, services, agents) into SQLite."""
    filepath = RAW_DIR / filename
    if not filepath.exists():
        print(f"  {filename} not found, skipping")
        return

    df = pd.read_csv(filepath, encoding="utf-8")
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"  {table_name}: {len(df)} rows loaded")


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"=== CSV Ingestion ===")
    print(f"Source: {RAW_DIR}\n")

    # Merge all booking CSVs
    df_bookings = merge_booking_csvs()
    if df_bookings is None:
        return

    # Parse dates
    for col in ["booking_date", "checkin_date", "checkout_date"]:
        df_bookings[col] = pd.to_datetime(df_bookings[col], errors="coerce")

    # Load into SQLite staging
    conn = sqlite3.connect(DB_PATH)

    df_bookings.to_sql("stg_bookings", conn, if_exists="replace", index=False)
    print(f"\n  stg_bookings staged in SQLite")

    # Load reference tables
    print("\nLoading reference tables...")
    load_reference_table("clients.csv", "stg_clients", conn)
    load_reference_table("services.csv", "stg_services", conn)
    load_reference_table("agents.csv", "stg_agents", conn)

    conn.close()
    print(f"\nDatabase: {DB_PATH}")


if __name__ == "__main__":
    main()
