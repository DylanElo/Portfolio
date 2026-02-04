"""
Step 1: Merge all raw_Bookings_*.csv files into SQLite staging.

Handles:
  - 21 CSV files (VBA export hit Excel's 1M row limit)
  - Excel serial date conversion to ISO dates
  - BOM-encoded UTF-8 from Excel
  - Multiline text fields in REMARKS, PICKUP, DROPOFF
"""

import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

# Config
PROJECT_DIR = Path(__file__).parent.parent
DB_PATH = PROJECT_DIR / "data" / "bookings.db"
RAW_DIR = Path(__file__).parent.parent.parent.parent / "public"

# Excel serial date epoch
EXCEL_EPOCH = datetime(1899, 12, 30)


def excel_serial_to_date(serial):
    """Convert Excel serial number to YYYY-MM-DD string."""
    if pd.isna(serial):
        return None
    try:
        serial = float(serial)
        dt = EXCEL_EPOCH + timedelta(days=int(serial))
        if 2010 <= dt.year <= 2030:
            return dt.strftime("%Y-%m-%d")
        return None
    except (ValueError, OverflowError):
        return None


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(RAW_DIR.glob("raw_Bookings_*.csv"))
    if not csv_files:
        print(f"No raw_Bookings_*.csv files found in {RAW_DIR}")
        return

    print(f"=== CSV Ingestion ===")
    print(f"Source: {RAW_DIR}\n")

    frames = []
    for f in csv_files:
        df = pd.read_csv(f, encoding="utf-8-sig", low_memory=False)
        frames.append(df)
        print(f"  {f.name}: {len(df):,} rows")

    df = pd.concat(frames, ignore_index=True)
    print(f"\n  Merged: {len(df):,} rows, {len(df.columns)} columns")

    # Convert Excel serial dates to ISO format
    date_cols = [
        "PICKUP_DATE", "DROPOFF_DATE", "BOOKING_TRAVEL_DATE",
        "BOOKING_ENTERED_DATE", "SERVICE_DATE", "DATE OUT"
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").apply(excel_serial_to_date)

    # Clean up time columns (strip decimal time artifacts)
    for col in ["PICKUP_TIME", "DROPOFF_TIME"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Standardize column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]

    # Load into SQLite
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("stg_bookings", conn, if_exists="replace", index=False)
    conn.close()

    print(f"\n  Staged to: {DB_PATH}")
    print(f"  Table: stg_bookings ({len(df):,} rows)")


if __name__ == "__main__":
    main()
