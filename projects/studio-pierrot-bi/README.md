# Studio Pierrot – Turnaround Strategy (BI Capstone)

A complete Business‑Intelligence pipeline that extracts data from the MyAnimeList (Jikan) API, stores it in a normalized SQLite warehouse, and visualises key performance metrics on a web dashboard.

## 📚 Overview
- **ETL** – Python scripts under `etl/` pull anime metadata, ratings, and episode data.
- **Warehouse** – SQLite DB (`warehouse/studio_pierrot.db`) implements a **full dimensional model**:
  - **Dimensions**: `dim_anime`, `dim_season`, `dim_episode`, `dim_date`, `dim_platform`, `dim_region`, `dim_campaign`, `dim_staff`, `dim_user_segment`, …
  - **Bridge tables**: `bridge_episode_staff`, `bridge_episode_revenue_type`, …
  - **Facts**: `fact_rating_snapshot`, `fact_mal_stats_snapshot`, `fact_production_episode`, `fact_sentiment_daily`, `fact_audience_episode`, `fact_revenue_stream`, `fact_costs`, `fact_campaign_performance`, …
- **Dashboard** – `dashboard.html` (Tailwind‑CDN + Chart.js) visualises:
  - Revenue & view trends
  - Sentiment heat‑maps (matrix chart)
  - Episode‑level performance
  - Campaign ROI

## 📂 Folder structure
```
studio-pierrot-bi/
├─ README.md                # This file
├─ etl/                     # Python ETL scripts
├─ data/                    # Raw JSON dumps (cached API responses)
├─ model/                   # Data‑model spec (SQL DDL)
├─ sql/                     # Helper queries & view definitions
├─ warehouse/               # SQLite DB (studio_pierrot.db)
├─ dashboard/               # Front‑end assets (HTML, CSS, JS)
│   ├─ dashboard.html
│   ├─ dashboard.js
│   └─ dashboard-style.css
└─ docs/                    # Optional design docs, diagrams
```

## 🚀 How to run locally
```bash
# 1️⃣ Install Python deps (inside the repo root)
pip install -r requirements.txt   # includes requests, pandas, etc.

# 2️⃣ Run the ETL (creates/updates the SQLite DB)
python etl/run_all.py

# 3️⃣ Serve the dashboard (simple HTTP server)
cd dashboard
python -m http.server 8000   # then open http://localhost:8000/dashboard.html
```

## 📈 Future work
- Add **campaign** dimension & cost‑tracking facts.
- Replace the static CSV/JSON data with a scheduled CI job that refreshes nightly.
- Migrate the dashboard to a Vite‑based SPA for a better dev experience.

---
*Feel free to open an issue or PR if you’d like to contribute or suggest improvements!*
