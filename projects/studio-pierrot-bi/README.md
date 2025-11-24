# Studio Pierrot BI Analysis

## 📋 Project Context

**Role:** BI Analyst at Studio Pierrot (Tokyo, Japan)

**Business Question:** *Why are our flagship IPs (Naruto, Bleach, Tokyo Ghoul, Black Clover) struggling to capture the same global momentum as newer titles like Jujutsu Kaisen (MAPPA) and Demon Slayer (ufotable)—and what should we do about it?*

This project simulates a real-world Business Intelligence environment where I combine **domestic (Japan), international streaming, and global fandom data** to provide actionable recommendations to studio leadership.

**Strategic Context:**
- Global anime market: $34B (2024) → projected $60B+ by 2030
- International streaming revenue: $3.7B → $12.5B by 2030
- Jujutsu Kaisen (MAPPA) was named "Most in-demand TV series in the world" in 2023 at 71.2x average demand
- Netflix + Crunchyroll control >80% of overseas anime streaming market
- Pierrot's legacy IPs dominate Netflix, but new titles fail to match MAPPA/ufotable quality perception

---

## 📊 Data Sources & Limitations

### Real Data (Phase 1: Global Fandom Lens)
**Source:** MyAnimeList via [Jikan API](https://jikan.moe/)
- Live scores, members, favorites, popularity rankings for 12 Studio Pierrot titles
- **Limitation:** MAL has a Western/international bias; Japanese domestic fans rarely use it
- **Use Case:** Proxy for global online anime fandom sentiment

**Curation for readability:** the working dataset is intentionally scoped to **the full Studio Pierrot catalog** (Naruto, Bleach, Tokyo Ghoul, Black Clover, Boruto, etc.) **plus 15 récents blockbusters** (Jujutsu Kaisen, Demon Slayer, Spy x Family, Blue Lock, Tokyo Revengers, Oshi no Ko, Solo Leveling, Kaiju No. 8, Frieren, etc.). This keeps the dashboards legible while still contrasting Pierrot IPs against today’s market leaders.

### Market Context (Public Reports)
**Sources:** Parrot Analytics, Netflix reports, industry publications
- Platform market share (Netflix ~52% anime watchers, Crunchyroll ~85% anime-focused)
- Global demand indices (JJK 71.2x benchmark)
- Streaming revenue projections and regional growth rates
- **Use Case:** Calibrate simulated data against real industry trends

### Simulated Data (Phase 2: Domestic & Streaming Lenses)
**Note:** Production costs, TV ratings, BD sales, merchandise revenue are **modeled for this project**
- Calibrated against known market sizes (e.g., Oricon BD sales rankings, standard production budgets)
- **Not actual Studio Pierrot financials**
- **Transparency:** All Phase 2 data clearly marked as "simulated" in dashboard and documentation

---

## 🎯 Business Objective

Studio Pierrot has dominated anime for decades with legendary franchises. However, the industry landscape has shifted:
- **Netflix reports 4.4 billion hours of anime watched in H1 2025 alone**, with over 50% of subscribers watching anime
- **Jujutsu Kaisen (MAPPA)** was named the "Most in-demand TV series in the world" in 2023, at **71.2x** the average demand
- **Streaming is projected to grow from $3.7B (2023) to $12.5B (2030)**, with Netflix + Crunchyroll controlling ~80% of the market

Meanwhile, Pierrot's newer titles (Boruto, Tokyo Ghoul:re) face criticism for:
- Long-running formats with high filler percentages
- Inconsistent production quality
- Lower engagement compared to "new wave" anime

**The Question:** How do we compete in this new era?

---

## 📊 Data Architecture

This project uses a **three-lens approach** to simulate a comprehensive BI environment:

### 1️⃣ Global Fandom Lens (Real Data)
**Source:** [Jikan API](https://jikan.moe/) (MyAnimeList public data)

Live metrics for understanding international fan sentiment:
- **Score:** Critical reception (0-10 scale)
- **Members:** Total audience reach
- **Favorites:** Core fanbase engagement
- **Popularity Rank:** Relative demand

**Limitation:** MAL has a Western/international bias and doesn't fully represent Japanese domestic audience preferences.

**ETL Process:**
- Script: `etl/fetch_data.js`
- Output: `dashboard/data.js`

### 2️⃣ International Streaming Lens (Modeled)
**Simulated based on industry reports:**
- Netflix viewership patterns (e.g., Naruto Shippuden = #1 anime in 2025)
- Crunchyroll/HBO Max demand analytics
- Regional streaming revenue breakdown (North America, Europe, Asia-Pacific)

**Key Insight:** Legacy Pierrot IPs (Naruto, Bleach) still dominate Netflix, but new titles struggle to compete with MAPPA/ufotable quality perception.

### 3️⃣ Domestic (Japan) Lens (Modeled)
**Simulated based on industry standards:**
- TV Tokyo broadcast ratings
All Phase 2 data is **calibrated against real benchmarks** (Netflix reports, Parrot Analytics, industry standards) and ready for dashboard integration.

**What's Acknowledged:**
- ⚠️ MAL data alone is insufficient for strategic decisions (Phase 2 expands this)
- ⚠️ Financial metrics referenced in case study are **simulated** for demonstration
- ⚠️ Phase 2 multi-tab dashboard UI is planned (data layer complete)

**Dashboard Disclaimer:**
The live dashboard clearly states: *"Public metrics (Score, Members, Favorites) are fetched live from the Jikan API. Financial data (Revenue, ROI) referenced in the case study is simulated for demonstration purposes."*

---

## 🚀 Key Findings (Phase 1 - Global Fandom Lens)

Based on MAL data analysis:

1. **Legacy Dominance:** Naruto Shippuden (8.28) and Bleach: TYBW (8.99) score highest, showing enduring quality
2. **New Title Struggles:** Boruto (5.98) and Tokyo Ghoul √A (7.03) significantly underperform
3. **Engagement Gaps:** Top legacy titles have 2.6M+ members, while newer titles plateau at <1M

**Strategic Implication:** Pierrot's legacy IP remains strong, but new IP development is failing to match competitor standards (JJK = 8.6+, Demon Slayer = 8.7+).

---

## 🏗️ Data Engineering (Phase 3: SQL Warehouse)

To support scalable analysis, I implemented a **dimensional data warehouse** using SQLite and Python ETL.

### Schema Design (Star Schema)
- **Fact Tables:** `fact_rating_snapshot`, `fact_revenue_stream`, `fact_production_episode`
- **Dimension Tables:** `dim_anime`, `dim_date`, `dim_platform`, `dim_region`

### ETL Pipeline
1. **Extract:** Python script (`etl/extract_mal.py`) fetches raw JSON from Jikan API
2. **Transform:** Data cleaning and standardization (handling missing values, date parsing)
3. **Load:** Python script (`etl/load.py`) populates the SQLite warehouse (`warehouse/pierrot_bi.db`) with upsert logic

### Example SQL Analysis

**1. Top 5 Highest Rated Pierrot Titles**
```sql
SELECT 
    a.title,
    r.mal_score,
    r.mal_members
FROM fact_rating_snapshot r
JOIN dim_anime a ON r.anime_id = a.anime_id
WHERE r.date_id = (SELECT MAX(date_id) FROM dim_date)
ORDER BY r.mal_score DESC
LIMIT 5;
```

**2. Revenue by Stream Type (Simulated)**
```sql
SELECT 
    revenue_type,
    SUM(revenue_amount) as total_revenue,
    COUNT(DISTINCT anime_id) as num_titles
FROM fact_revenue_stream
GROUP BY revenue_type
ORDER BY total_revenue DESC;
```

---

## 🛠️ How to Run

1. **View the Dashboard:** Open `dashboard/index.html` or visit the [live deployment](https://dylanelo.github.io/Portfolio/projects/studio-pierrot-bi/dashboard/index.html)

2. **Run Python ETL Pipeline (Phase 3):**
   ```bash
   # 1. Extract fresh data from MAL
   python etl/extract_mal.py
   
   # 2. Load into SQL Warehouse
   python etl/load.py
   ```
   *Requires Python 3.x and `requests` library*

3. **Run Legacy JS ETL (Phase 1):**
   ```bash
   node etl/fetch_data.js
   ```

---

## 🗺️ Next Steps (Phase 2)

See [ROADMAP_PHASE_2.md](./ROADMAP_PHASE_2.md) for the full vision of integrating:
- Streaming platform analytics (Netflix, Crunchyroll market share)
- Domestic TV ratings and merchandise data
- Production quality metrics (filler %, animation budget tiers)
- Multi-lens dashboards for holistic decision-making

---

## 📚 References

- [Netflix Anime Statistics (2025)](https://www.gamesradar.com/entertainment/anime-shows/)
- [Jujutsu Kaisen Global Demand Analysis](https://www.parrotanalytics.com/announcements/)
- [Anime Streaming Market Projections](https://www.parrotanalytics.com/press/)
- [Grand View Research: Anime Market Report (2030)](https://www.grandviewresearch.com/industry-analysis/anime-market)
