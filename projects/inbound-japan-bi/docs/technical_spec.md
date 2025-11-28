# Technical Specification
## Japan Inbound Travel Intelligence Hub

### 1. Architecture Overview
*   **ETL**: Python scripts (Requests + Pandas) running sequentially.
*   **Storage**: SQLite Data Warehouse (`inbound_japan.db`).
*   **Presentation**: Web Dashboard (Vite + Chart.js) consuming JSON exports or direct DB connection (via API if needed, initially static/local).

### 2. Data Sources

| Source | Type | Frequency | Usage |
| :--- | :--- | :--- | :--- |
| **JNTO** | CSV/Scraping | Monthly | Visitor Arrivals, Breakdown by Country/Purpose |
| **OpenSky** | API (REST) | Daily | Inbound Flight Volumes (ADS-B) |
| **ExchangeRate** | API | Daily | JPY vs Major Currencies |
| **OpenWeather** | API | Daily | Weather conditions for major tourist hubs |

### 3. Data Model (Star Schema)

#### Dimensions

**`dim_date`**
*   `date_id` (PK, YYYYMMDD)
*   `date`, `year`, `month`, `day`
*   `is_holiday_jp`, `season`

**`dim_month`**
*   `month_id` (PK, YYYYMM)
*   `month_name`, `year`, `season`

**`dim_country`**
*   `country_id` (PK)
*   `country_name_en`, `iso_code`
*   `region_macro` (Asia, Europe, etc.), `region_detail`

**`dim_airport`**
*   `airport_id` (PK)
*   `airport_code` (NRT, HND, etc.), `airport_name`
*   `prefecture`, `region_jp`

**`dim_fx_currency`**
*   `currency_code` (PK)
*   `country_id` (FK)

**`dim_weather_location`**
*   `weather_loc_id` (PK)
*   `city_name`, `prefecture`

#### Facts

**`fact_inbound_arrivals_monthly`**
*   Grain: Month x Country
*   FKs: `month_id`, `country_id`
*   Measures: `visitors_total`, `visitors_leisure`, `visitors_business`

**`fact_flights_daily`**
*   Grain: Day x Airport
*   FKs: `date_id`, `airport_id`
*   Measures: `num_inbound_flights`, `num_unique_origin_countries`

**`fact_fx_rate_daily`**
*   Grain: Day x Currency
*   FKs: `date_id`, `currency_code`
*   Measures: `rate_jpy_per_currency`

**`fact_weather_daily`**
*   Grain: Day x Location
*   FKs: `date_id`, `weather_loc_id`
*   Measures: `temp_avg`, `temp_max`, `temp_min`, `condition_main`

### 4. ETL Pipeline Design
Location: `projects/inbound-japan-bi/etl/`

1.  **`01_fetch_jnto_arrivals.py`**: Download/Parse JNTO CSVs -> `raw_jnto_arrivals`.
2.  **`02_fetch_fx_rates.py`**: Fetch historical/daily rates -> `fact_fx_rate_daily`.
3.  **`03_fetch_weather_daily.py`**: Fetch weather for key cities -> `fact_weather_daily`.
4.  **`04_fetch_opensky_flights.py`**: Fetch inbound flights -> `fact_flights_daily`.
5.  **`10_build_dimensions.py`**: Create/Update Dimension tables.
6.  **`20_build_fact_inbound_arrivals.py`**: Process raw JNTO data into Fact table.

### 5. Dashboard Requirements

**Dashboard 1: Executive Overview**
*   KPIs: YTD Visitors, YoY Growth, Top Markets.
*   Charts: Monthly Trend (Line), Regional Split (Stacked Area).

**Dashboard 2: Markets & Seasonality**
*   Charts: Top 10 Markets (Tree/Bar), Seasonality Heatmap (Country x Month).

**Dashboard 3: FX & Demand**
*   Charts: JPY Rate vs Visitor Volume correlation.

**Dashboard 4: Operations (Capacity)**
*   Charts: Daily Flights vs Monthly Visitors, Risk Heatmap (Flights + Weather).
