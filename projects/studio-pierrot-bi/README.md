# Studio Pierrot BI Analysis

**A Business Intelligence project analyzing the performance of Studio Pierrot's anime franchises.**

This project demonstrates a complete BI workflow, from data extraction (ETL) to strategic analysis and visualization. It focuses on identifying actionable insights to improve production ROI for one of Japan's most legendary animation studios.

## 🚀 Project Status: Phase 1 (Live)

The project is currently in **Phase 1**, focusing on establishing a reliable data pipeline and visualizing core metrics using real-world data.

*   **Data Source:** [Jikan API](https://jikan.moe/) (Unofficial MyAnimeList API).
*   **Data Warehouse:** SQLite (Local) / JSON (Web).
*   **Visualization:** Custom HTML/JS Dashboard (Chart.js).
*   **Key Metrics:** Score, Popularity (Members), Favorites, Airing Status.

## 📂 Project Structure

```
projects/studio-pierrot-bi/
├── dashboard/          # Interactive Web Dashboard
│   ├── index.html      # Dashboard UI
│   ├── dashboard.js    # Visualization Logic
│   └── data.js         # Processed Data (JSON)
├── etl/                # Data Engineering
│   └── fetch_data.js   # Script to fetch real data from Jikan API
├── data/               # Raw Data Storage
│   └── raw_jikan_data.json
└── README.md           # This file
```

## 📊 Dashboard

The interactive dashboard provides a snapshot of franchise performance.

**[Launch Dashboard](./dashboard/index.html)**

### Key Views
1.  **KPI Overview:** Top performing titles by Score, Popularity, and Engagement.
2.  **Comparative Analysis:** Bar charts comparing critical reception (Score) vs. Audience Size (Members).
3.  **Franchise Deep Dive:** Detailed stats for key franchises (Naruto, Bleach, Tokyo Ghoul, etc.).

## 🗺️ Roadmap

### Phase 2: Enhanced Analytics (Planned)
*   **Revenue Modeling:** Integrate estimated revenue data based on box office and disc sales (simulated where actuals are unavailable).
*   **Production Metrics:** Correlate animation quality (filler ratio, staff credits) with audience sentiment.
*   **Regional Analysis:** Break down popularity by region (Domestic vs. International) using Google Trends data.

## 🛠️ Tech Stack
*   **ETL:** Node.js (Axios)
*   **Frontend:** Vanilla JS, Chart.js, TailwindCSS
*   **Version Control:** Git
