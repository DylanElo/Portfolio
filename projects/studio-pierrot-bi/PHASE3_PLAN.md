# Phase 3 Enhancement Plan - Audit Response

## Overview
Responding to external audit feedback to transform project from "good" to "hire-worthy BI portfolio piece."

## Phase 3a: Documentation Fixes ✅ IN PROGRESS
**Priority: CRITICAL | Time: 30 min**

### Tasks
- [/] Add explicit business context paragraph to README
- [/] Add "Data Sources & Limitations" section to README  
- [/] Update project.html with enhanced strategic framing
- [ ] Add data transparency footer to dashboard
- [ ] Commit and deploy Phase 3a changes

**Goal:** Make business framing and data honesty crystal clear to recruiters.

---

## Phase 3b: Dashboard Narrative Enhancement
**Priority: HIGH | Time: 1-2 hours**

### Tasks
- [ ] Add insight annotations to each tab
  - [ ] Global Fandom: "Bleach TYBW (8.99) matches JJK quality, but Boruto (5.98) significantly underperforms"
  - [ ] Streaming: "JJK dominates at 71.2x demand vs Boruto at 2.3x - quality perception gap"  
  - [ ] Domestic: "Strong MAL score correlation with BD sales (R² > 0.8) - invest in quality"
  - [ ] Production: "High filler % kills scores - shift to seasonal model (JJK/TYBW: <10% filler)"
- [ ] Add "Key Insight" cards to each tab
- [ ] Update chart titles with actionable context

**Goal:** Every chart directly answers a Studio Pierrot strategic question.

---

## Phase 3c: SQL Warehouse Implementation  
**Priority: MEDIUM | Time: 4-6 hours**

### Architecture Decision
**Current:** JavaScript data files + Chart.js  
**Target:** SQLite warehouse + Python ETL + API layer

### Tasks
- [ ] Database Design
  - [ ] Create `schema.sql` with star schema
    - [ ] `dim_anime` (anime_id, title, studio, type, episodes, air_date_start)
    - [ ] `dim_date` (date_id, date, year, quarter, month)
    - [ ] `dim_platform` (platform_id, platform_name, type, region)
    - [ ] `dim_region` (region_id, region_name, country_group)
    - [ ] `fact_rating_snapshot` (anime_id, date_id, score, members, favorites, rank)
    - [ ] `fact_revenue_stream` (anime_id, platform_id, region_id, date_id, revenue, revenue_type)
    - [ ] `fact_production_episode` (anime_id, episode_id, filler_flag, quality_score, budget)
  - [ ] Document grain and relationships in DATA_DICTIONARY.md

- [ ] Python ETL Pipeline
  - [ ] `etl/extract_mal.py` - Fetch data from Jikan API
  - [ ] `etl/transform.py` - Clean and prepare data for warehouse
  - [ ] `etl/load.py` - Populate SQLite tables
  - [ ] `etl/config.yaml` - Pierrot franchise list + API settings
  - [ ] Make ETL idempotent (upsert logic)

- [ ] Data Migration
  - [ ] Convert `data.js` → `fact_rating_snapshot` table
  - [ ] Convert `streaming_data.js` → `fact_revenue_stream` + `dim_platform`
  - [ ] Convert `domestic_data.js` → BD sales + merch revenue facts
  - [ ] Convert `production_data.js` → `fact_production_episode`

- [ ] Backend API Layer
  - [ ] `api/server.py` - Flask/FastAPI endpoint
  - [ ] `/api/fandom` - Return MAL metrics
  - [ ] `/api/streaming` - Return platform + demand data
  - [ ] `/api/domestic` - Return BD + merch data
  - [ ] `/api/production` - Return filler analysis

- [ ] Dashboard Integration
  - [ ] Update `dashboard.js` to fetch from API instead of JS files
  - [ ] Add loading states
  - [ ] Error handling for API failures

**Goal:** Show real BI engineering - dimensional modeling, ETL, SQL queries.

---

## Phase 3d: Case Study Enhancement
**Priority: MEDIUM | Time: 1 hour**

### Tasks
- [ ] Add comparison table to project.html
  - [ ] Pierrot vs MAPPA vs ufotable side-by-side
  - [ ] Metrics: Avg MAL score, Production model, Filler %, Global demand
- [ ] Enhance Key Findings section
  - [ ] Add data points to each finding
  - [ ] Link findings to dashboard tabs
- [ ] Strengthen Recommendations section  
  - [ ] Add "Expected Impact" for each recommendation
  - [ ] Reference specific data evidence
- [ ] Add "Methodology" section
  - [ ] Explain three-lens approach
  - [ ] Show data flow diagram

**Goal:** Case study reads like an actual executive presentation deck.

---

## Success Criteria

When all phases complete, the project should demonstrate:
- ✅ **Strategic Thinking:** Clear business context, competitive analysis
- ✅ **Data Engineering:** Dimensional model, SQL warehouse, Python ETL  
- ✅ **Data Honesty:** Transparent about real vs simulated data
- ✅ **Storytelling:** Every chart answers a specific business question
- ✅ **Technical Depth:** Schema, queries, idempotent ETL, API layer

## Estimated Total Time
- Phase 3a: 30 minutes
- Phase 3b: 1-2 hours  
- Phase 3c: 4-6 hours
- Phase 3d: 1 hour
**Total: 6.5-9.5 hours**
