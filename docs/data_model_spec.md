# Data Model Specification

## Overview
This document outlines the data model used in the Studio Pierrot BI Analysis project. The model is designed to support the analytical requirements defined in the [Stakeholder Requirements](./stakeholder_requirements.md).

## Phase 1: Core Metrics (Current)

In Phase 1, the data model focuses on "Snapshot" metrics—current values retrieved from the MyAnimeList database via Jikan API.

### `dim_anime`
The central dimension table containing static metadata for each anime title.

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `anime_id` | INT | Unique MyAnimeList ID | Jikan API (`mal_id`) |
| `title` | TEXT | Official English or Romaji title | Jikan API (`title`) |
| `type` | TEXT | TV, Movie, OVA, etc. | Jikan API (`type`) |
| `episodes` | INT | Total episode count | Jikan API (`episodes`) |
| `status` | TEXT | Finished Airing, Currently Airing | Jikan API (`status`) |
| `rating` | TEXT | Age rating (e.g., PG-13, R-17+) | Jikan API (`rating`) |
| `aired_from` | DATE | Start date of airing | Jikan API (`aired.from`) |
| `aired_to` | DATE | End date of airing | Jikan API (`aired.to`) |

### `fact_performance_snapshot`
A fact table storing the current performance metrics for each anime. In Phase 1, this is a snapshot of the "current state".

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `anime_id` | INT | Foreign Key to `dim_anime` | Jikan API |
| `score` | FLOAT | Weighted score (0-10) | Jikan API (`score`) |
| `scored_by` | INT | Number of users who scored the anime | Jikan API (`scored_by`) |
| `rank` | INT | Overall rank on MyAnimeList | Jikan API (`rank`) |
| `popularity` | INT | Popularity rank (based on members) | Jikan API (`popularity`) |
| `members` | INT | Total members (watching, completed, etc.) | Jikan API (`members`) |
| `favorites` | INT | Number of users who favorited the anime | Jikan API (`favorites`) |
| `snapshot_date` | DATE | Date when data was fetched | System Date |

## Phase 2: Enhanced Metrics (Planned)

Future phases will introduce simulated or scraped data to support deeper analysis.

### `fact_revenue_est` (Planned)
*   `revenue_domestic`: Estimated revenue in Japan (Yen).
*   `revenue_international`: Estimated revenue global (USD).
*   `source`: Financial reports / Box Office Mojo (Simulated).

### `fact_production` (Planned)
*   `filler_count`: Number of filler episodes.
*   `filler_ratio`: Percentage of filler content.
*   `studio_primary`: Main studio responsible (if co-produced).

## Phase 3: Finance ROI Layer (New)

The latest ETL adds a deterministic finance model to keep ROI assumptions transparent and reproducible.

### `dim_anime` additions
*   `mal_score` – MAL score used for tiering.
*   `mal_members` – MAL members used as demand proxy.
*   `tier` – S/A/B/C band derived from score + members thresholds.

### `fact_finance`
*   `base_budget_per_episode` – Starting production budget.
*   `tier_multiplier` – Cost multiplier based on tier (S=1.6, A=1.3, B=1.0, C=0.7).
*   `production_budget` / `total_cost` – Modeled cost using episode count and tier multiplier.
*   `streaming_revenue` – (MAL members / 100k) × 150k constant.
*   `disc_revenue` – Tier-based disc units × 60 price (with 10% bonus for 9.0+ scores).
*   `merch_revenue` – Streaming revenue × tier-specific merch factor.
*   `total_revenue`, `profit`, `roi`, `profit_per_episode` – Derived finance KPIs for dashboard use.
