# Booking Calendar BI

End-to-end BI pipeline that solves the Excel/Sheets reporting problem:
**VBA-exported CSVs → SQLite star schema → Web dashboard + Looker Studio export**

## The Problem

- Company uses Google Workspace but reports are generated in Excel via VPN
- Can't access the database directly from Sheets connectors
- VBA script extracts raw booking data into multiple CSVs (split due to size)
- No way to consolidate and query across years of booking data

## The Solution

```
VBA Export (CSV files)          SQLite Star Schema           Output
┌──────────────────┐     ┌───────────────────────┐     ┌─────────────────┐
│ bookings_2020.csv│     │                       │     │ Web Dashboard   │
│ bookings_2021.csv│────>│  fact_bookings        │────>│ (Chart.js)      │
│ bookings_2022.csv│     │    │                  │     │                 │
│ bookings_2023.csv│     │    ├── dim_date        │     │ Looker Studio   │
│ bookings_2024.csv│     │    ├── dim_client      │     │ (CSV export)    │
│ bookings_2025.csv│     │    ├── dim_service     │     │                 │
│ clients.csv      │     │    ├── dim_agent       │     │ Direct SQL      │
│ services.csv     │     │    └── dim_status      │     │ queries         │
│ agents.csv       │     │                       │     │                 │
└──────────────────┘     └───────────────────────┘     └─────────────────┘
```

## Data Model (Star Schema)

```
                    ┌──────────────┐
                    │  dim_date    │
                    │──────────────│
                    │ date_id (PK) │
                    │ date         │
                    │ year, month  │
                    │ quarter      │
                    │ day_of_week  │
                    │ season       │
                    │ is_weekend   │
                    └──────┬───────┘
                           │
┌──────────────┐   ┌──────┴────────────┐   ┌──────────────┐
│ dim_client   │   │  fact_bookings    │   │ dim_service   │
│──────────────│   │───────────────────│   │──────────────│
│ client_id(PK)│───│ booking_id        │───│ service_id(PK)│
│ client_name  │   │ booking_date_id   │   │ service_name │
│ client_type  │   │ checkin_date_id   │   │ category     │
│ client_region│   │ checkout_date_id  │   │ destination  │
│ client_country   │ month_id          │   └──────────────┘
└──────────────┘   │ client_id (FK)    │
                   │ service_id (FK)   │   ┌──────────────┐
┌──────────────┐   │ agent_id (FK)     │   │ dim_status   │
│ dim_agent    │   │ status_id (FK)    │   │──────────────│
│──────────────│   │ pax               │───│ status_id(PK)│
│ agent_id(PK) │───│ nights            │   │ status_name  │
│ agent_name   │   │ revenue           │   │ is_active    │
│ team         │   │ cost              │   └──────────────┘
└──────────────┘   │ margin            │
                   │ margin_pct        │
                   │ currency          │
                   └───────────────────┘
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full pipeline (uses sample data)
python run_pipeline.py

# 3. Open the dashboard
open dashboard/index.html
```

## Using Your Real Data

### Step 1: Export CSVs from your VBA script

Your VBA script should produce CSVs with these columns (or similar):

| Column | Type | Description |
|--------|------|-------------|
| booking_id | string | Unique booking reference |
| booking_date | date | When the booking was made |
| checkin_date | date | Service start date |
| checkout_date | date | Service end date |
| client_id | int | Client identifier |
| client_name | string | Client/agency name |
| service_id | int | Service identifier |
| service_name | string | Service description |
| service_category | string | Tour/Transfer/Accommodation |
| destination | string | Service location |
| agent_id | int | Booking agent identifier |
| agent_name | string | Agent name |
| status | string | Confirmed/Pending/Cancelled/Completed |
| pax | int | Number of passengers |
| nights | int | Number of nights (0 for day services) |
| revenue | float | Booking revenue |
| cost | float | Booking cost |
| currency | string | Currency code (EUR, USD, etc.) |

### Step 2: Place CSVs in data/raw/

```
data/raw/
├── bookings_2020.csv    # (or however your VBA splits them)
├── bookings_2021.csv
├── bookings_2022.csv
├── ...
├── clients.csv          # Optional: client reference table
├── services.csv         # Optional: service catalog
└── agents.csv           # Optional: agent list
```

### Step 3: Update column mapping (if needed)

Edit `etl/01_ingest_csvs.py` and update:
1. `DATA_SOURCE = "raw"` (change from "sample")
2. `COLUMN_MAP` dictionary if your CSV headers differ

### Step 4: Run the pipeline

```bash
python run_pipeline.py
```

## Pipeline Steps

| Script | Description |
|--------|-------------|
| `etl/01_ingest_csvs.py` | Merges multiple CSVs → SQLite staging |
| `etl/10_build_dimensions.py` | Builds star schema dimensions |
| `etl/20_build_fact_bookings.py` | Builds fact table with FK lookups |
| `etl/99_export_for_dashboard.py` | Exports JSON (dashboard) + CSV (Looker) |

## Outputs

| Output | Path | Use Case |
|--------|------|----------|
| SQLite database | `data/bookings.db` | Direct SQL queries |
| Dashboard JSON | `dashboard/data/dashboard_data.json` | Web dashboard |
| Flat CSV | `data/looker_export/bookings_flat.csv` | Looker Studio import |
| Web dashboard | `dashboard/index.html` | Browser-based reports |

## Looker Studio Integration

The pipeline exports a denormalized `bookings_flat.csv` that you can upload directly to Looker Studio as a data source. It includes all dimension attributes joined in, so you can immediately build charts without any SQL.

## Tech Stack

- **ETL**: Python 3.9+, pandas, sqlite3
- **Data Warehouse**: SQLite (star schema)
- **Dashboard**: HTML5, Chart.js, vanilla JS
- **Reporting**: Looker Studio (via CSV export)
