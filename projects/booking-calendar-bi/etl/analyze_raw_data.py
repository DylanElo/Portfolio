"""
Analyze the raw booking CSV files to understand structure,
data quality, and key dimensions before building the ETL.
"""
import pandas as pd
import os
from pathlib import Path
from datetime import datetime, timedelta

RAW_DIR = Path("/home/user/Portfolio/public")

def excel_serial_to_date(serial):
    """Convert Excel serial date number to Python date."""
    if pd.isna(serial):
        return None
    try:
        serial = float(serial)
        # Excel epoch: Dec 30, 1899
        return datetime(1899, 12, 30) + timedelta(days=int(serial))
    except (ValueError, OverflowError):
        return None

def main():
    # Load all CSVs
    csv_files = sorted(RAW_DIR.glob("raw_Bookings_*.csv"))
    print(f"Found {len(csv_files)} CSV files\n")

    frames = []
    for f in csv_files:
        df = pd.read_csv(f, encoding="utf-8-sig", low_memory=False)
        frames.append(df)
        print(f"  {f.name}: {len(df):,} rows")

    df = pd.concat(frames, ignore_index=True)
    print(f"\n  TOTAL: {len(df):,} rows")
    print(f"  Columns: {len(df.columns)}")

    # --- Column listing ---
    print("\n" + "="*60)
    print("COLUMNS")
    print("="*60)
    for i, col in enumerate(df.columns):
        dtype = df[col].dtype
        nulls = df[col].isna().sum()
        pct = (nulls / len(df)) * 100
        print(f"  {i+1:2d}. {col:<40} {str(dtype):<10} nulls: {nulls:,} ({pct:.1f}%)")

    # --- Date analysis ---
    print("\n" + "="*60)
    print("DATE RANGES (Excel serial → actual dates)")
    print("="*60)
    date_cols = ["PICKUP_DATE", "DROPOFF_DATE", "BOOKING_TRAVEL_DATE",
                 "BOOKING_ENTERED_DATE", "SERVICE_DATE", "DATE OUT"]
    for col in date_cols:
        if col in df.columns:
            valid = pd.to_numeric(df[col], errors="coerce").dropna()
            if len(valid) > 0:
                min_serial = valid.min()
                max_serial = valid.max()
                min_date = excel_serial_to_date(min_serial)
                max_date = excel_serial_to_date(max_serial)
                print(f"  {col:<30} {min_date.strftime('%Y-%m-%d') if min_date else 'N/A'} → {max_date.strftime('%Y-%m-%d') if max_date else 'N/A'}")

    # --- Key dimensions ---
    print("\n" + "="*60)
    print("KEY DIMENSIONS")
    print("="*60)

    dims = {
        "AGENT_NAME": "Agents (tour operators)",
        "AGENT_ANALYSIS1_NAME": "Agent countries",
        "PRODUCT_SERVICE_NAME": "Service types",
        "PRODUCT_LOCATION_NAME": "Locations",
        "BOOKING_STATUS": "Booking statuses",
        "SERVICE_STATUS": "Service statuses",
        "BOOKING_BRANCH": "Branches",
        "BOOKING_DEPARTMENT": "Departments",
        "REGION": "Regions",
        "BOOKING_CONSULTANT_NAME": "Booking consultants",
        "OP CONSULTANT": "Operations consultants",
        "BOOKING_ANALYSIS1_NAME": "Analysis 1",
        "BOOKING_ANALYSIS2_NAME": "Analysis 2",
    }

    for col, label in dims.items():
        if col in df.columns:
            uniques = df[col].nunique()
            top = df[col].value_counts().head(10)
            print(f"\n  {label} ({col}): {uniques} unique values")
            for val, cnt in top.items():
                print(f"    {val}: {cnt:,}")

    # --- Booking-level stats ---
    print("\n" + "="*60)
    print("BOOKING-LEVEL ANALYSIS")
    print("="*60)

    n_bookings = df["BOOKING_REFERENCE"].nunique()
    print(f"  Unique bookings: {n_bookings:,}")
    print(f"  Unique booking names: {df['BOOKING_NAME'].nunique():,}")

    # Services per booking
    services_per = df.groupby("BOOKING_REFERENCE").size()
    print(f"\n  Services per booking:")
    print(f"    Mean:   {services_per.mean():.1f}")
    print(f"    Median: {services_per.median():.0f}")
    print(f"    Max:    {services_per.max()}")

    # PAX stats
    print(f"\n  PAX distribution:")
    pax = pd.to_numeric(df["PAX"], errors="coerce")
    print(f"    Mean:   {pax.mean():.1f}")
    print(f"    Median: {pax.median():.0f}")
    print(f"    Max:    {pax.max():.0f}")

    # --- Supplier analysis ---
    print("\n" + "="*60)
    print("SUPPLIER ANALYSIS")
    print("="*60)
    n_suppliers = df["SUPPLIER_NAME"].nunique()
    print(f"  Total unique suppliers: {n_suppliers:,}")
    top_suppliers = df["SUPPLIER_NAME"].value_counts().head(15)
    for s, c in top_suppliers.items():
        print(f"    {s}: {c:,}")

    # --- Yearly distribution ---
    print("\n" + "="*60)
    print("YEARLY DISTRIBUTION (by SERVICE_DATE)")
    print("="*60)
    df["_service_serial"] = pd.to_numeric(df["SERVICE_DATE"], errors="coerce")
    df["_service_year"] = df["_service_serial"].apply(
        lambda x: excel_serial_to_date(x).year if excel_serial_to_date(x) else None
    )
    yearly = df.groupby("_service_year").agg(
        rows=("_service_year", "size"),
        unique_bookings=("BOOKING_REFERENCE", "nunique")
    )
    for year, row in yearly.iterrows():
        if year and 2015 <= year <= 2030:
            print(f"  {int(year)}: {row['rows']:>8,} services, {row['unique_bookings']:>6,} bookings")


if __name__ == "__main__":
    main()
