# Studio Pierrot Anime BI Capstone

<parameter name="portfolio-grade Business Intelligence project analyzing Studio Pierrot anime performance using a complete BI workflow: dimensional modeling, ETL/ELT, data warehousing, SQL analysis, and dashboard visualization.

## 🎯 Project Goals

Analyze why recent Studio Pierrot anime (Boruto, Tokyo Ghoul:re) underperform compared to historical hits (Naruto, Bleach) by examining:
- Rating and popularity trends from MyAnimeList
- Production metrics (filler ratio, quality, stability)
- Marketing campaign effectiveness (simulated)
- Financial performance (simulated)

## 📊 Architecture

```
Studio Pierrot BI Project
├── data/           # Raw CSV/JSON dumps from MAL API
├── etl/            # Python ETL scripts
│   └── init_db.py  # Database initialization
├── model/          # Star schema definition
│   ├── schema.sql  # DDL for all tables
│   └── model.md    # ER diagram & documentation
├── sql/            # Analytical queries
├── dashboard/      # Tableau/Power BI files
└── studio_pierrot.db  # SQLite data warehouse
```

## 🗄️ Data Model

**Star Schema** with 2 dimensions and 3 fact tables:

### Dimensions
- `dim_anime` – Core anime attributes (title, studio, episodes, dates, genre)
- `dim_season` – Production metadata (season type, filler ratio, quality scores)

### Facts
- `fact_anime_metrics` – MAL performance (ratings, popularity, member counts)
- `fact_marketing` – Campaign data (type, channel, cost, impressions)
- `fact_financials` – Cost and revenue estimates

See [`model/model.md`](model/model.md) for full documentation.

## 🚀 Quick Start

### 1. Initialize the Database
```bash
python etl/init_db.py
```

This creates all tables in `studio_pierrot.db`.

### 2. Verify Tables
```bash
sqlite3 studio_pierrot.db "SELECT name FROM sqlite_master WHERE type='table';"
```

Expected output:
```
dim_anime
dim_season
fact_anime_metrics
fact_financials
fact_marketing
```

## 📋 Roadmap

### ✅ Phase 1: Project Setup (Completed)
- [x] Folder structure
- [x] Star schema design
- [x] SQLite database
- [x] Model documentation

### ✅ Phase 2: Data Acquisition (Completed)
- [x] Fetched 20 anime from MyAnimeList via Jikan API (incl. Gintama, JJK, One Piece, etc.)
- [x] Generated simulated production metrics
- [x] Generated marketing campaigns
- [x] Generated financial data
- [x] Loaded all data into warehouse

### ✅ Phase 3: SQL Analysis (Completed)
- [x] Created 10 comprehensive analytical queries
- [x] Tested and validated all queries
- [x] Derived key business insights

### ✅ Phase 4: Dashboard (Completed)
- [x] Created web-based dashboard with Chart.js
- [x] Exported warehouse data to JSON
- [x] Visualized KPIs, Score vs Filler, and ROI

### ✅ Phase 5: Portfolio Integration (Completed)
- [x] Added project showcase page (`project_studio_pierrot.html`)
- [x] Embedded interactive dashboard
- [x] Linked from main portfolio page (`index.html`)
- [ ] Add project showcase page
- [ ] Embed screenshots and findings
- [ ] Link to GitHub repository
- [ ] Write analytical queries
- [ ] Answer business questions

### 🔜 Phase 5: Dashboard
- [ ] Create visualizations
- [ ] Build executive dashboard

## 🎨 Portfolio Integration

This project will be showcased on my portfolio website with:
- Interactive demo
- Key findings and insights
- Dashboard screenshots
- Link to GitHub repository

## 📝 Business Context

**Scenario**: Studio Pierrot notices recent shows underperform compared to classics. They need to understand:
1. Performance gaps (ratings, engagement)
2. Structural issues (filler, pacing, production quality)
3. Risk factors for current projects
4. Recommendations for future productions

## 🛠️ Tech Stack

- **Database**: SQLite (easily portable)
- **ETL**: Python (pandas, requests)
- **Analysis**: SQL
- **Visualization**: Tableau / Power BI / Looker Studio
- **Version Control**: Git

## 📄 License

This is a portfolio project for demonstration purposes.

---

**Status**: Phase 1 Complete ✓ | Next: Data Acquisition
