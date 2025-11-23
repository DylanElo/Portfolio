# Studio Pierrot BI Analysis

A strategic Business Intelligence project analyzing 10 iconic anime franchises to identify actionable insights for improving production ROI.

## 📊 Data Architecture

This project uses a hybrid data approach to simulate a real-world BI environment:

### 1. Real-Time Metrics (Jikan API)
We fetch live public data from MyAnimeList via the [Jikan API](https://jikan.moe/) for the following metrics:
- **Score:** Critical reception (0-10 scale).
- **Members:** Total audience size/reach.
- **Favorites:** Core fanbase engagement.
- **Popularity:** Relative ranking by member count.

**ETL Process:**
- Script: `etl/fetch_data.js`
- Source: Jikan API (REST)
- Output: `dashboard/data.js` (JSON object used by the frontend)

### 2. Simulated Financial Data
To demonstrate business analysis capabilities without access to private studio financials, we have modeled the following metrics based on industry standards:
- **Revenue:** Estimated earnings from broadcast, streaming, and merchandise.
- **Production Cost:** Estimated budget based on episode count and animation quality.
- **ROI:** Calculated Return on Investment.

## 🗂️ Project Structure

```text
/
├── dashboard/          # Interactive Dashboard
│   ├── index.html      # Dashboard UI
│   ├── dashboard.js    # Chart.js logic & Data binding
│   └── data.js         # Generated data file
├── docs/               # Strategic Documentation
│   ├── executive_requirements.md
│   ├── stakeholder_requirements.md
│   └── strategy_document.md
├── etl/                # Data Pipeline
│   └── fetch_data.js   # Node.js script to fetch Jikan data
└── README.md           # This file
```

## 🚀 How to Run

1. **View the Dashboard:** Open `dashboard/index.html` in your browser.
2. **Run ETL Pipeline:**
   ```bash
   node etl/fetch_data.js
   ```
   *Note: Requires Node.js installed.*
