# Implementation Plan - Phase 4: Operational Capacity

## Goal
Integrate flight data to monitor inbound capacity and identify operational bottlenecks at major airports.

## Proposed Changes

### ETL Scripts
#### [NEW] `projects/inbound-japan-bi/etl/04_fetch_opensky_flights.py`
- **Function**: Fetch daily inbound flight counts for major airports (NRT, HND, KIX, CTS, FUK).
- **Source**: `OpenSky Network` API (REST) or **Mock Data**.
    - *Note*: OpenSky historical data often requires a paid research license or has strict rate limits for anonymous users. For this portfolio project, I will generate **Mock Flight Data** that realistically reflects the post-COVID recovery curve (2022-2025).
- **Output**: `data/raw/flights_daily.csv`

#### [MODIFY] `projects/inbound-japan-bi/etl/10_build_dimensions.py`
- **Change**: Add `build_dim_airport`.
- **Table**: `dim_airport` (airport_code, airport_name, region).

#### [NEW] `projects/inbound-japan-bi/etl/23_build_fact_flights.py`
- **Function**: Transform raw flight data into `fact_flights_daily`.
- **Logic**: Join with `dim_date` and `dim_airport`.

#### [MODIFY] `projects/inbound-japan-bi/etl/99_export_for_dashboard.py`
- **Change**: Add query for "Airport Capacity" (Daily Flights by Airport).

### Database
#### [UPDATE] `projects/inbound-japan-bi/data/inbound_japan.db`
- Add `dim_airport` and `fact_flights_daily` tables.

### Dashboard
#### [MODIFY] `projects/inbound-japan-bi/dashboard/index.html`
- Add a new section for "Airport Capacity Monitor".
- Add canvas for `flightsChart`.

#### [MODIFY] `projects/inbound-japan-bi/dashboard/app.js`
- Render a Stacked Bar Chart showing daily/monthly flights per airport.

## Verification Plan
### Automated Tests
- Run `04_fetch_opensky_flights.py` and check for CSV output.
- Query SQLite to verify `fact_flights_daily` is populated.

### Manual Verification
- Check Dashboard for the new Flight chart.
- Verify that Haneda (HND) and Narita (NRT) show the highest volume.
