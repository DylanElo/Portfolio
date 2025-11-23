# Phase 2 Roadmap: Full 3-Lens BI Integration

## Vision

Transform the current **Global Fandom Lens** (MAL) into a comprehensive BI platform that integrates:
1. 🇯🇵 **Domestic (Japan) Lens** - TV ratings, local platforms, merchandise
2. 🌏 **International Streaming Lens** - Netflix/Crunchyroll analytics, regional growth
3. 🌐 **Global Fandom Lens** - MAL, Parrot Analytics, social media sentiment (current phase)

This will enable Studio Pierrot leadership to answer strategic questions like:
> "Should we invest in a seasonal high-quality arc (JJK-style) or continue long-running formats (Boruto-style)?"

---

## Phase 1 (Current) ✅

**Status:** Live and functional

**What We Have:**
- Real-time MAL data for 12 Pierrot titles
- KPI dashboard with critical reception and engagement metrics
- Clear disclaimer about data sources and limitations

**What We've Proven:**
- Legacy IP (Naruto, Bleach) still scores highly globally
- New IP (Boruto, Tokyo Ghoul:re) underperforms compared to MAPPA/ufotable titles
- MAL provides valuable fandom sentiment but is Western-biased

---

## Phase 2: Domestic (Japan) Integration 🇯🇵

### Data Sources

| Source | Metric | Availability | Plan |
|--------|--------|--------------|------|
| **TV Tokyo Ratings** | Weekly viewership, timeslot performance | Private | Simulate based on known patterns (late-night vs prime-time) |
| **Oricon Charts** | Blu-ray/DVD sales rankings | Public (aggregated) | Scrape historical Oricon data or use known benchmarks |
| **dAnime Store** | Streaming rank (Japan-specific) | Limited API | Model based on MAL + domestic popularity proxies |
| **Merchandise Revenue** | Licensing, events, collaborations | Private | Simulate using industry estimates (~40% of anime revenue) |

### New Data Model Tables

```sql
-- Domestic TV Performance
CREATE TABLE fact_tv_rating_weekly (
    anime_id INT,
    broadcast_date DATE,
    timeslot VARCHAR(50), -- 'late_night', 'prime_time', etc.
    viewership_rating DECIMAL(5,2), -- % of households
    rank_in_slot INT,
    PRIMARY KEY (anime_id, broadcast_date)
);

-- Physical Media Sales (Oricon)
CREATE TABLE fact_bd_sales (
    anime_id INT,
    volume_number INT,
    release_date DATE,
    units_sold INT,
    oricon_rank INT,
    PRIMARY KEY (anime_id, volume_number)
);

-- Merchandise & Licensing
CREATE TABLE fact_revenue_merch (
    anime_id INT,
    year INT,
    quarter INT,
    merch_revenue_jpy BIGINT,
    licensing_revenue_jpy BIGINT,
    event_revenue_jpy BIGINT,
    PRIMARY KEY (anime_id, year, quarter)
);
```

### Dashboard: "Domestic Performance" Tab

**Visualizations:**
1. **TV Ratings Trend** - Weekly viewership for each title
2. **BD Sales Comparison** - Oricon rankings vs MAL score (does quality = sales?)
3. **Merchandise ROI** - Revenue from merch vs production budget

**Key Insight:**
> "Domestic revenue still represents ~60% of Pierrot's income, but international streaming is growing 15% YoY."

---

## Phase 3: International Streaming Integration 🌏

### Data Sources

| Platform | Data Available | Integration Strategy |
|----------|----------------|----------------------|
| **Netflix** | Public reports (top 10, hours viewed) | Scrape Netflix Top 10 API + official reports |
| **Crunchyroll** | Limited (no public API) | Model based on MAL popularity + known market share (~40%) |
| **Parrot Analytics** | Global demand ratings (paid service) | Use free reports + simulate demand index |
| **Social Media** | Twitter/X mentions, TikTok trends | Twitter API v2 (academic access) or manual sampling |

### New Data Model Tables

```sql
-- Platform Market Share
CREATE TABLE fact_platform_share_region (
    platform_id INT, -- Netflix, Crunchyroll, Disney+
    region_id INT,   -- North America, Europe, Asia-Pacific
    year INT,
    quarter INT,
    subscriber_count BIGINT,
    anime_viewer_share DECIMAL(5,2), -- % of subscribers watching anime
    PRIMARY KEY (platform_id, region_id, year, quarter)
);

-- Global Demand Index (Parrot-style)
CREATE TABLE fact_global_demand (
    anime_id INT,
    week_start_date DATE,
    global_demand_index DECIMAL(10,2), -- 1.0 = average series
    rank_global INT,
    rank_anime_category INT,
    PRIMARY KEY (anime_id, week_start_date)
);

-- Streaming Revenue (Estimated)
CREATE TABLE fact_revenue_streaming (
    anime_id INT,
    platform_id INT,
    region_id INT,
    year INT,
    quarter INT,
    estimated_revenue_usd BIGINT, -- Based on licensing deals + viewership
    PRIMARY KEY (anime_id, platform_id, region_id, year, quarter)
);
```

### Dashboard: "Global Streaming" Tab

**Visualizations:**
1. **Pierrot vs MAPPA/ufotable** - Global demand index comparison (JJK, Demon Slayer vs Naruto, Boruto)
2. **Regional Growth** - Streaming revenue by region (highlight: North America = fastest growing)
3. **Platform Dominance** - Netflix vs Crunchyroll market share for Pierrot titles

**Key Insight:**
> "Naruto Shippuden dominates Netflix (40M views in H1 2025), but Boruto struggles to retain that audience. Meanwhile, JJK (MAPPA) commands 71x average demand globally."

**Strategic Recommendation:**
- Leverage legacy IP on Netflix for licensing revenue
- Develop 1-2 new "premium quality" IPs to compete with MAPPA/ufotable
- Shift from long-running formats to seasonal arcs (higher quality, less filler)

---

## Phase 4: Production Quality Metrics 🎬

### New Data Model Tables

```sql
-- Episode-Level Production Tracking
CREATE TABLE fact_production_episode (
    anime_id INT,
    episode_number INT,
    air_date DATE,
    is_filler BOOLEAN,
    animation_budget_tier VARCHAR(20), -- 'low', 'medium', 'high', 'sakuga'
    key_animators TEXT[], -- Array of notable staff
    production_delay_days INT,
    PRIMARY KEY (anime_id, episode_number)
);

-- Arc Quality vs Reception
CREATE TABLE fact_arc_analysis (
    anime_id INT,
    arc_name VARCHAR(100),
    start_episode INT,
    end_episode INT,
    filler_percentage DECIMAL(5,2),
    avg_mal_score DECIMAL(4,2), -- User ratings for this arc
    production_quality_score DECIMAL(3,1), -- Internal rating (1-10)
    PRIMARY KEY (anime_id, arc_name)
);
```

### Dashboard: "Production Insights" Tab

**Visualizations:**
1. **Filler Impact** - Scatter plot: Filler % vs MAL Score (hypothesis: high filler = lower scores)
2. **Budget Efficiency** - Production cost vs viewer retention
3. **Arc Comparison** - Best-performing arcs (Naruto Pain Arc, Bleach TYBW) vs worst (Boruto filler arcs)

**Key Insight:**
> "Episodes with 'high' or 'sakuga' budget tiers correlate with 0.5-1.0 point higher MAL scores. Filler-heavy arcs (>30% filler) see 20-30% drop in viewership."

**Strategic Recommendation:**
- Cap filler at 10% max (vs current 40%+ in Boruto)
- Invest in seasonal production breaks (JJK/Demon Slayer model)
- Allocate budget to key episodes (finales, climactic battles)

---

## Implementation Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| **Phase 1** | ✅ Complete | MAL dashboard, strategic docs, ETL pipeline |
| **Phase 2** | 4-6 weeks | Domestic data integration, TV ratings + BD sales |
| **Phase 3** | 6-8 weeks | Streaming analytics, Parrot demand index, regional revenue |
| **Phase 4** | 4-6 weeks | Production quality metrics, filler analysis |
| **Phase 5** | 2-4 weeks | Multi-lens executive dashboard, final recommendations |

**Total Time:** ~4-6 months for full implementation

---

## Success Metrics

By the end of Phase 5, the BI platform should enable leadership to:

1. ✅ **Compare Pierrot vs Competitors** across all three lenses (domestic, international, fandom)
2. ✅ **Predict ROI** for different production strategies (long-running vs seasonal)
3. ✅ **Identify Growth Opportunities** (e.g., "Double down on Netflix for legacy IP, focus Crunchyroll for new IP")
4. ✅ **Optimize Production** (data-driven decisions on budget allocation, filler reduction)

---

## Technical Stack (Phase 2+)

- **ETL:** Python (Pandas, BeautifulSoup for Oricon scraping)
- **Database:** PostgreSQL (star schema for OLAP queries)
- **BI Tools:** 
  - Custom dashboards (React + Chart.js) for flexibility
  - OR Power BI for stakeholder-facing reports
- **Data Sources:**
  - Jikan API (MAL)
  - Netflix Top 10 API
  - Twitter API v2 (social sentiment)
  - Manual Oricon data entry (quarterly updates)

---

## Why This Matters

This project demonstrates:
1. **End-to-End BI Skills** - From ETL to executive dashboards
2. **Strategic Thinking** - Understanding industry dynamics (not just data wrangling)
3. **Data Source Integration** - Combining public APIs, simulated data, and market research
4. **Stakeholder Communication** - Tailoring insights for Production, Marketing, and Finance teams

**For Recruiters:** This showcases my ability to build BI systems in ambiguous, data-scarce environments—a common challenge in real-world analytics projects.
