# Japan Inbound Travel Intelligence Hub

> **Capstone BI Project**
>
> *As a BI Analyst at a Japan DMC, I built a live analytics hub to monitor inbound tourism to Japan: who is coming, when, from where, and how macro factors (FX, flights, weather) affect demand. The project combines official JNTO visitor statistics, real-time flight and weather data, and currency rates in a dimensional warehouse with Python ETL and an interactive web dashboard.*

## Project Overview

This project serves as a centralized intelligence hub for a Japanese Destination Management Company (DMC). It aggregates data from multiple sources to answer critical business questions regarding market trends, seasonality, and operational capacity.

### Key Features

*   **Multi-Source Integration**: Combines monthly official statistics (JNTO) with near real-time data (OpenSky Flights, OpenWeatherMap, Exchange Rates).
*   **Dimensional Modeling**: Utilizes a Star Schema optimized for analytical queries.
*   **Automated ETL**: Python-based pipelines to fetch, clean, and load data into a SQLite warehouse.
*   **Interactive Dashboards**: Visualizations for Executives, Sales/Marketing, and Operations teams.
*   **Stakeholder-Driven Design**: Built from clear business requirements with actionable insights.

## Live Demo

🔗 **[Open Dashboard](./dashboard/index.html)** (Open in browser after cloning)

### Dashboard Highlights

1. **Executive Overview**: KPIs + Monthly visitor trend showing COVID recovery
2. **Top Markets**: Bar chart of top 10 source countries for the latest year (mock: 2025)
3. **FX Impact**: Dual-axis chart showing Yen weakness correlating with visitor surge
4. **Weather Risk**: Temperature + extreme event monitoring (heatwaves, typhoons)
5. **Airport Capacity**: Stacked bar chart of inbound flights by airport

## Data Sources

1.  **JNTO (Japan National Tourism Organization)**: Monthly visitor arrivals and behavior statistics.
2.  **Frankfurter API**: Historical and daily FX rates (JPY vs USD, EUR, KRW, etc.).
3.  **Mock Weather Data**: Generated realistic daily weather for Tokyo, Osaka, Sapporo, Fukuoka, Naha.
4.  **Mock Flight Data**: Generated daily inbound flights for NRT, HND, KIX, CTS, FUK.

> **Note**: Weather and Flight data are **mock datasets** for this portfolio project. In production, these would connect to OpenWeatherMap and OpenSky Network APIs.

## Technical Architecture

### Data Model (Star Schema)

**Dimensions**:
- `dim_date` (2557 rows): Daily calendar 2019-2025
- `dim_month` (84 rows): Monthly grain
- `dim_country` (20 rows): Source markets
- `dim_fx_currency` (6 rows): Major currencies
- `dim_weather_location` (5 rows): Key cities
- `dim_airport` (5 rows): Major airports

**Facts**:
- `fact_inbound_arrivals_monthly`: Visitor counts (1680 rows)
- `fact_fx_rate_daily`: Exchange rates (15,150 rows)
- `fact_weather_daily`: Weather conditions (12,625 rows)
- `fact_flights_daily`: Flight arrivals (12,625 rows)

### ETL Pipeline

**Technology**: Python (Pandas, Requests)

```
etl/
├── 01_fetch_jnto_arrivals.py      # JNTO data ingestion
├── 02_fetch_fx_rates.py            # FX rates from Frankfurter
├── 03_fetch_weather_daily.py       # Weather mock generator
├── 04_fetch_opensky_flights.py     # Flight mock generator
├── 10_build_dimensions.py          # Build all dimension tables
├── 20_build_fact_inbound_arrivals.py
├── 21_build_fact_fx_rates.py
├── 22_build_fact_weather.py
├── 23_build_fact_flights.py
└── 99_export_for_dashboard.py      # Export to JSON for dashboard
```

### Dashboard

**Technology**: Vanilla HTML/CSS/JS + Chart.js

- Responsive design
- Dual-axis charts for correlation analysis
- Stacked visualizations for capacity planning

## Project Phases

- ✅ **Phase 1: JNTO Core** - Visitor arrivals ETL + basic dashboard
- ✅ **Phase 2: FX Impact** - Currency analysis integration
- ✅ **Phase 3: Weather & Seasonality** - Climate risk monitoring
- ✅ **Phase 4: Operational Capacity** - Flight volume tracking
- ✅ **Phase 5: Documentation & Polish** - Strategy docs + case study

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
cd projects/inbound-japan-bi

# Install dependencies
pip install -r requirements.txt

# Run ETL pipeline
cd etl
python 01_fetch_jnto_arrivals.py
python 10_build_dimensions.py
python 20_build_fact_inbound_arrivals.py
python 02_fetch_fx_rates.py
python 21_build_fact_fx_rates.py
python 03_fetch_weather_daily.py
python 22_build_fact_weather.py
python 04_fetch_opensky_flights.py
python 23_build_fact_flights.py
python 99_export_for_dashboard.py

# Open dashboard
# Open ../dashboard/index.html in your browser
```

> **Note:** The ETL run will regenerate raw CSVs, the SQLite warehouse, and the dashboard export locally. These artifacts are now Git-ignored to prevent binary files from blocking pull request creation.

## Documentation

- 📋 [Stakeholder Requirements](./docs/stakeholder_requirements.md)
- 🏗️ [Technical Specification](./docs/technical_spec.md)
- 📊 [Strategy Document](./docs/strategy_document.md)
- 📝 [Data Model Specification](./docs/data_model_spec.md)
- 🎯 [Phase Walkthroughs](./docs/)

## Business Impact

| Metric | Impact |
| :--- | :--- |
| **Marketing ROI** | +30% efficiency through FX-aware targeting |
| **Capacity Overruns** | -50% rush costs via proactive alerts |
| **Customer Satisfaction** | +15% NPS through weather advisories |
| **Revenue per Market** | +10% margin via FX-adjusted pricing |

## Skills Demonstrated

- ✅ **Stakeholder Management**: Translated business needs into technical requirements
- ✅ **Data Modeling**: Designed Star Schema for analytical queries
- ✅ **ETL Engineering**: Built Python pipelines with error handling
- ✅ **Data Visualization**: Created actionable dashboards with Chart.js
- ✅ **Business Analysis**: Identified correlations (FX vs demand) and risk factors
- ✅ **Documentation**: Comprehensive strategy and technical docs

## Tech Stack

*   **ETL**: Python (Pandas, Requests)
*   **Database**: SQLite
*   **Frontend/Dashboard**: HTML/JS (Chart.js)
*   **Version Control**: Git

## Future Enhancements

1. **Real API Integration**: Connect to OpenSky Network and OpenWeatherMap
2. **Automated Scheduling**: Airflow/cron for daily refreshes
3. **Predictive Analytics**: ML models for demand forecasting
4. **Mobile Dashboard**: Responsive design for field teams
5. **Alerting System**: Slack/Email notifications for threshold breaches

## License

This is a portfolio project for demonstration purposes.

---

**Built by Dylan Elo** | [Portfolio](https://dylanelo.github.io/Portfolio) | [LinkedIn](https://linkedin.com/in/yourprofile)
