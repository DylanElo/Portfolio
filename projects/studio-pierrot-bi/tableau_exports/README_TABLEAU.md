# Tableau Data Exports

## Overview
This directory contains CSV files formatted for Tableau import. All data is simulated for portfolio demonstration purposes, calibrated to industry benchmarks.

## Files

### 1. `anime_scores.csv`
**Purpose:** MAL scores and fandom metrics  
**Key Fields:**
- `title`, `studio`, `is_pierrot` (boolean)
- `mal_score`, `members`
- `revenue_profile` (LegacyEvergreen, RecentHit, RevivalHit, LongRun)

**Suggested Tableau Visualizations:**
- **Horizontal bar chart**: MAL Score by Title, colored by `is_pierrot`
- **Scatter plot**: Members (X) vs MAL Score (Y), sized by episodes
- **Treemap**: Member base distribution, colored by revenue profile

### 2. `revenue_timeline.csv`
**Purpose:** Revenue evolution 2020-2024  
**Key Fields:**
- `year`, `title`, `studio`
- `revenue_millions`, `revenue_profile`

**Suggested Tableau Visualizations:**
- **Line chart**: Revenue by Year, colored by Title
- **Area chart**: Stacked revenue showing Pierrot vs competitors
- **Slope graph**: 2020 vs 2024 revenue comparison

### 3. `streaming_metrics.csv`
**Purpose:** Streaming demand and platform data  
**Key Fields:**
- `demand_index` (Parrot Analytics benchmark)
- `platform_netflix`, `platform_crunchyroll` (availability scores 0-100)
- `global_reach_score` (1-10 scale)

**Suggested Tableau Visualizations:**
- **Bar chart**: Demand Index comparison
- **Dual-axis chart**: Platform availability (Netflix vs Crunchyroll)
- **Bullet chart**: Global reach scores vs targets

### 4. `production_metrics.csv`
**Purpose:** Production costs and quality metrics  
**Key Fields:**
- `budget_per_episode_thousands`
- `filler_percentage`, `production_model`
- `avg_score`

**Suggested Tableau Visualizations:**
- **Scatter plot**: Budget vs Avg Score, colored by production model
- **Box plot**: Filler % distribution by model (Seasonal vs Continuous)
- **Heatmap**: Budget + Filler correlation with scores

## Importing to Tableau

### Option 1: Tableau Desktop
1. Open Tableau Desktop
2. Connect to Data → Text File
3. Navigate to `tableau_exports/` folder
4. Select CSV files
5. Join files as needed:
   - Join `anime_scores` with `revenue_timeline` on `title`
   - Join with `streaming_metrics` on `title`

### Option 2: Tableau Public
1. Upload CSVs to Tableau Public
2. Create workbook with multiple data sources
3. Build dashboards combining views

## Recommended Dashboards

### Dashboard 1: "Pierrot Competitive Position"
- **Top**: MAL Score comparison (bar chart)
- **Middle**: Revenue timeline (line chart)
- **Bottom**: Streaming demand (bar chart)
- **Filter**: Revenue profile

### Dashboard 2: "Production Quality Analysis"
- **Left**: Budget vs Score scatter
- **Right**: Filler impact (box plot by model)
- **Bottom**: Production model distribution

### Dashboard 3: "Market Evolution 2020-2024"
- **Main**: Revenue timeline with forecasting
- **Side**: Revenue profile breakdown (pie/donut)
- **Bottom**: Growth rate table

## Data Dictionary

### Revenue Profiles
- **LegacyEvergreen**: Finished airing, strong long-tail monetization
- **RecentHit**: Currently airing or recent, high momentum
- **RevivalHit**: Returning franchise with renewed production
- **LongRun**: Ongoing continuous production

### Production Models
- **Seasonal**: 12-26 episodes per season, breaks between cours
- **Continuous**: Year-round production, 50+ episodes
- **Mixed**: Hybrid approach

## Notes
- All revenue figures are in millions USD
- Budgets are per-episode in thousands USD
- MAL scores are on 1-10 scale
- Demand indices are relative to average anime (1.0x)
- Simulated data is calibrated to:
  - Parrot Analytics 2023 report (JJK 71.2x demand)
  - Industry budget ranges ($100K-$450K per episode)
  - Known filler percentages from anime databases

## Contact
For questions about this data, see `DATA_DICTIONARY.md` in the parent directory.
