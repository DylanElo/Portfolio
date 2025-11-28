# Walkthrough - Phase 2: FX Impact

## Accomplishments
I have successfully integrated Foreign Exchange (FX) data into the BI Hub to analyze the correlation between the Yen's value and visitor demand.

### 1. FX Data Integration
- **Source**: `frankfurter.app` API (Historical daily rates).
- **ETL Script**: `etl/02_fetch_fx_rates.py` fetches daily rates for JPY against USD, EUR, KRW, CNY, AUD, THB from 2019 to present.
- **Schema Updates**:
    - `dim_fx_currency`: Stores currency codes and names.
    - `fact_fx_rate_daily`: Stores daily exchange rates.

### 2. Dashboard Enhancements
- **New Chart**: "FX Impact: JPY/USD Rate vs Visitor Volume".
- **Visualization**: A dual-axis line chart showing:
    - **Left Axis (Blue)**: Total Monthly Visitors.
    - **Right Axis (Red Dashed)**: JPY per USD Rate.
- **Insight**: This allows stakeholders to visually confirm if a weaker Yen (higher JPY/USD rate) correlates with increased visitor numbers.

## Verification Results
- **ETL Execution**: `02_fetch_fx_rates.py` successfully fetched ~2000 days of data for 6 currencies.
- **Data Warehouse**: `fact_fx_rate_daily` is populated and linked to `dim_date`.
- **Dashboard**: The new chart renders correctly, showing the inverse relationship (or lack thereof) clearly.

## Next Steps
- **Phase 3**: Weather & Seasonality. We will add weather data to identify climate risks (heatwaves, typhoons).
