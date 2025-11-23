# Data Dictionary - Studio Pierrot BI Analysis

## Overview
This document describes all data tables used in the Studio Pierrot BI Analysis project, including both Phase 1 (live MAL data) and Phase 2 (simulated domestic, streaming, and production data).

---

## Phase 1: Global Fandom Data (Live)

### `animeData` (from `dashboard/data.js`)
**Source:** Jikan API (MyAnimeList)  
**Update Frequency:** Manual ETL via `etl/fetch_data.js`  
**Purpose:** International fan sentiment and engagement metrics

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `mal_id` | Integer | MyAnimeList unique identifier | `20` |
| `title` | String | Official English title | `"Naruto"` |
| `type` | String | Format type | `"TV"`, `"Movie"` |
| `episodes` | Integer | Total episode count | `220` |
| `status` | String | Production status | `"Finished Airing"`, `"Currently Airing"` |
| `score` | Float | Average user rating (0-10) | `8.28` |
| `scored_by` | Integer | Number of users who rated | `1847234` |
| `members` | Integer | Total MAL members tracking | `2657890` |
| `favorites` | Integer | Users who favorited | `98543` |
| `popularity` | Integer | Global popularity rank | `45` |

**Business Use Cases:**
- Critical reception benchmarking
- Fan engagement analysis
- International audience reach measurement

**Known Limitations:**
- Western/international bias (MAL user base skews non-Japanese)
- Does not reflect domestic (Japan) preferences
- No financial metrics

---

## Phase 2: Domestic (Japan) Data (Simulated)

### `tvRatings` (from `dashboard/domestic_data.js`)
**Source:** Simulated (based on TV Tokyo patterns)  
**Purpose:** Japanese broadcast viewership performance

| Column | Type | Description | Example | Calibration Source |
|--------|------|-------------|---------|-------------------|
| `anime_id` | String | Anime identifier | `"naruto-shippuden"` | - |
| `week` | String | ISO week format | `"2015-W10"` | - |
| `timeslot` | String | Broadcast timeslot | `"prime_time"`, `"late_night"` | Industry standard |
| `viewership_rating` | Float | TV rating percentage | `3.4` | Prime-time: 2-4%, Late-night: 0.5-1.5% |
| `rank_in_slot` | Integer | Ranking within timeslot | `1` | - |

**Calibration Notes:**
- Prime-time shows (Naruto era): 2-4% typical ratings
- Late-night shows (Boruto current): 0.5-1.5% typical ratings
- Based on known TV Tokyo performance patterns

**Business Use Cases:**
- Domestic audience measurement
- Timeslot optimization analysis
- Broadcast contract negotiation

---

### `bdSales` (from `dashboard/domestic_data.js`)
**Source:** Simulated (based on Oricon rankings)  
**Purpose:** Physical media sales performance (Blu-ray/DVD)

| Column | Type | Description | Example | Calibration Source |
|--------|------|-------------|---------|-------------------|
| `anime_id` | String | Anime identifier | `"bleach-tybw"` | - |
| `volume` | Integer | Volume/box set number | `1` | - |
| `release_date` | String | Release date (YYYY-MM-DD) | `"2023-04-15"` | - |
| `units_sold` | Integer | Units sold (first week) | `48500` | Oricon chart patterns |
| `oricon_rank` | Integer | Oricon top 50 rank | `1` | - |

**Calibration Notes:**
- **Correlation with MAL scores:**
  - MAL 8.5+ → 30K+ units per volume
  - MAL 7.0-8.5 → 10K-30K units
  - MAL <7.0 → <10K units
- Based on Oricon chart patterns for anime releases

**Business Use Cases:**
- Revenue forecasting
- Physical distribution strategy
- Production quality ROI analysis

---

### `merchRevenue` (from `dashboard/domestic_data.js`)
**Source:** Simulated (based on industry benchmarks)  
**Purpose:** Merchandise and licensing revenue tracking

| Column | Type | Description | Example | Calibration Source |
|--------|------|-------------|---------|-------------------|
| `anime_id` | String | Anime identifier | `"naruto"` | - |
| `year` | Integer | Fiscal year | `2023` | - |
| `quarter` | Integer | Fiscal quarter (1-4) |  `1` | - |
| `merch_revenue_jpy` | Integer | Merchandise revenue (¥) | `1200000000` | Industry benchmarks |
| `licensing_revenue_jpy` | Integer | Licensing revenue (¥) | `450000000` | Industry benchmarks |
| `event_revenue_jpy` | Integer | Event revenue (¥) | `80000000` | Industry benchmarks |

**Calibration Notes:**
- **Legacy IP advantage:**
  - Naruto generates ~¥1.2-1.5B/quarter in merchandise
  - Boruto generates ~¥90-120M/quarter (10x gap)
- Based on ~$34B global anime market estimates (2024)
- Event revenue includes cafe collaborations, pop-up shops, exhibitions

**Business Use Cases:**
- IP value assessment
- Licensing deal negotiations
- Long-term franchise planning

---

## Phase 2: International Streaming Data (Simulated)

### `platformShare` (from `dashboard/streaming_data.js`)
**Source:** Simulated (based on public subscriber data)  
**Purpose:** Streaming platform market share analysis

| Column | Type | Description | Example | Calibration Source |
|--------|------|-------------|---------|-------------------|
| `platform` | String | Streaming platform | `"Netflix"` | - |
| `region` | String | Geographic region | `"North America"` | - |
| `year` | Integer | Year | `2024` | - |
| `quarter` | Integer | Quarter (1-4) | `1` | - |
| `subscriber_count` | Integer | Total platform subscribers | `75000000` | Netflix public reports |
| `anime_viewer_share` | Integer | % who watch anime | `52` | Industry reports |

**Calibration Notes:**
- **Netflix:** ~40M anime viewers globally, ~75M North America subscribers
- **Crunchyroll:** ~15M total subscribers, 85% anime-focused
- Based on public subscriber reports and anime consumption surveys

**Business Use Cases:**
- Platform prioritization strategy
- Regional expansion planning
- Licensing deal terms negotiation

---

### `globalDemand` (from `dashboard/streaming_data.js`)
**Source:** Simulated (based on Parrot Analytics methodology)  
**Purpose:** Global demand measurement (Parrot Analytics-style)

| Column | Type | Description | Example | Calibration Source |
|--------|------|-------------|---------|-------------------|
| `anime_id` | String | Anime identifier | `"jujutsu-kaisen"` | - |
| `week` | String | ISO week format | `"2024-W10"` | - |
| `global_demand_index` | Float | Demand vs average (multiplier) | `71.2` | Parrot Analytics report |
| `rank_global` | Integer | Global TV series rank | `1` | - |
| `rank_anime` | Integer | Rank among anime titles | `1` | - |

**Calibration Notes:**
- **JJK = 71.2x average demand** (known Parrot Analytics benchmark from 2023)
- Pierrot titles scaled realistically:
  - Naruto Shippuden: 12.5x (strong legacy)
  - Bleach TYBW: 9.8x (resurgence)
  - Boruto: 2.3x (struggling)
- Reflects "Most in-demand TV series globally" methodology

**Business Use Cases:**
- Competitive positioning analysis
- Marketing investment prioritization
- Licensing revenue forecasting

---

### `streamingRevenue` (from `dashboard/streaming_data.js`)
**Source:** Simulated (based on industry deal structures)  
**Purpose:** Estimated platform licensing revenue

| Column | Type | Description | Example | Calibration Source |
|--------|------|-------------|---------|-------------------|
| `anime_id` | String | Anime identifier | `"naruto-shippuden"` | - |
| `platform` | String | Streaming platform | `"Netflix"` | - |
| `region` | String | Geographic region | `"North America"` | - |
| `year` | Integer | Year | `2024` | - |
| `quarter` | Integer | Quarter (1-4) | `1` | - |
| `estimated_revenue_usd` | Integer | Revenue estimate (USD) | `3200000` | Industry standard deals |

**Calibration Notes:**
- **Typical licensing deals:** $1-3M per title per platform per quarter for popular shows
- **Naruto Shippuden on Netflix:** $3.2M/quarter (flagship title, #1 anime globally)
- **Boruto:** $320K/quarter (10x gap reflects demand difference)
- Based on industry-standard licensing agreements

**Business Use Cases:**
- Revenue forecasting
- Platform deal negotiations
- Regional market prioritization

---

## Phase 2: Production Quality Data (Simulated)

### `arcAnalysis` (from `dashboard/production_data.js`)
**Source:** Simulated (based on fan wikis and episode ratings)  
**Purpose:** Story arc quality and filler impact analysis

| Column | Type | Description | Example | Calibration Source |
|--------|------|-------------|---------|-------------------|
| `anime_id` | String | Anime identifier | `"naruto-shippuden"` | - |
| `arc_name` | String | Story arc name | `"Pain Arc"` | - |
| `start_ep` | Integer | Starting episode number | `152` | Fan wikis |
| `end_ep` | Integer | Ending episode number | `175` | Fan wikis |
| `filler_percentage` | Integer | % filler content | `8` | Fan-documented |
| `avg_mal_score` | Float | Average arc rating | `9.2` | Episode ratings |
| `production_quality_score` | Float | Production quality (0-10) | `9.5` | Sakuga analysis |
| `notes` | String | Additional context | `"Iconic arc..."` | - |

**Calibration Notes:**
- **Filler percentages:** Known from fan databases
  - Naruto Shippuden overall: 41% filler
  - Boruto overall: ~40% filler
  - Bleach TYBW: 0% filler (seasonal model)
- **MAL arc scores:** Approximated from episode-level ratings
- **Production quality:** Inferred from sakuga analysis and animation tier

**Business Use Cases:**
- Production strategy optimization
- Filler impact analysis
- Quality investment ROI assessment

---

### `productionBudgets` (from `dashboard/production_data.js`)
**Source:** Simulated (based on industry budget ranges)  
**Purpose:** Production cost analysis

| Column | Type | Description | Example | Calibration Source |
|--------|------|-------------|---------|-------------------|
| `anime_id` | String | Anime identifier | `"bleach-tybw"` | - |
| `avg_budget_per_episode_usd` | Integer | Average cost per episode (USD) | `380000` | Industry standards |
| `tier` | String | Budget tier classification | `"sakuga"` | - |
| `notes` | String | Additional context | `"Seasonal production..."` | - |

**Calibration Notes:**
- **Industry budget ranges for TV anime:**
  - Low: ~$100K per episode
  - Medium: $150-200K per episode
  - High: $250-300K per episode
  - Sakuga (premium): $400K+ per episode
- Bleach TYBW: $380K/episode (seasonal, high-quality production)
- Boruto: $140K/episode (cost-cutting vs Naruto era evident)

**Business Use Cases:**
- Production budget planning
- Quality vs cost trade-off analysis
- Seasonal vs long-running model comparison

---

### `fillerImpact` (from `dashboard/production_data.js`)
**Source:** Simulated (statistical aggregation)  
**Purpose:** Quantify filler content impact on performance

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `filler_range` | String | Filler percentage range | `"0-10%"` |
| `avg_mal_score` | Float | Average MAL score in range | `8.9` |
| `avg_bd_sales` | Integer | Average BD units sold | `42000` |
| `sample_size` | Integer | Number of arcs analyzed | `5` |

**Calibration Notes:**
- Shows clear negative correlation:
  - 0-10% filler → 8.9 avg score
  - 60-100% filler → 5.8 avg score
- Supports strategic recommendation to cap filler at 10% max

**Business Use Cases:**
- Production strategy decisions
- Seasonal vs continuous model evaluation
- Quality investment justification

---

## Data Governance

### Data Quality
- **Phase 1 (MAL):** Real-time data, refreshed manually via ETL
- **Phase 2:** Simulated data calibrated against known benchmarks
- All simulated data transparently disclosed in dashboard

### Update Frequency
- **MAL data:** Manual refresh (run `node etl/fetch_data.js`)
- **Phase 2 data:** Static mock data for demonstration

### Known Limitations
1. **MAL data:**
   - Western/international bias
   - No financial metrics
   - Doesn't reflect Japanese domestic preferences

2. **Simulated data:**
   - Not actual studio financials
   - Estimates based on industry reports
   - Intended for demonstration of BI methodology

### Data Privacy
- All data is from public sources or simulated
- No proprietary studio financials included
- Transparent disclosure in all documentation

---

## References

**Real Data Sources:**
- Jikan API: https://jikan.moe/
- MyAnimeList: https://myanimelist.net/

**Calibration Sources:**
- Netflix Anime Statistics: https://www.gamesradar.com/entertainment/anime-shows/
- Parrot Analytics (JJK 71.2x): https://www.parrotanalytics.com/
- Anime Market Reports: https://www.grandviewresearch.com/industry-analysis/anime-market
- Industry production budgets: Standard TV anime ranges ($100K-$400K per episode)
- Filler percentages: Fan wikis (Anime Filler List, etc.)
