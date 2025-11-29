# Walkthrough - Phase 4: Operational Capacity

## Accomplishments
I have successfully integrated Flight data into the BI Hub to monitor operational capacity at major airports.

### 1. Flight Data Integration
- **Source**: Mock Data Generator (simulating OpenSky Network).
- **ETL Script**: `etl/04_fetch_opensky_flights.py` generates daily flight counts for 5 major airports (NRT, HND, KIX, FUK, CTS) from 2019 to present.
- **Schema Updates**:
    - `dim_airport`: Stores airport codes, names, and regions.
    - `fact_flights_daily`: Stores daily flight counts per airport.

### 2. Dashboard Enhancements
- **New Chart**: "Airport Capacity: Monthly Inbound Flights".
- **Visualization**: A Stacked Bar Chart showing:
    - Monthly flights for each airport.
    - The chart clearly shows the COVID collapse (2020-2022) and recovery trajectory (2023-2025).
    - Haneda (HND) and Narita (NRT) dominate capacity, as expected.
- **Insight**: This helps Operations teams understand which airports are approaching capacity limits and where bottlenecks might occur during peak seasons.

## Verification Results
- **ETL Execution**: `04_fetch_opensky_flights.py` generated ~12.6k rows of flight data.
- **Data Warehouse**: `fact_flights_daily` is populated and linked to `dim_airport`.
- **Dashboard**: The new chart renders correctly, showing the recovery curve matching the visitor recovery.

## Next Steps
- **Phase 5**: Documentation & Polish. We will finalize the Strategy Document and create a Case Study page.
