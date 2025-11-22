# Studio Pierrot BI - Data Model Specification

This document defines the target dimensional model (Star Schema) for the Studio Pierrot Business Intelligence Data Warehouse.

## 1. Dimensions

### Core Dimensions
*   **dim_anime**: `anime_id` (PK), title, genre, studio, source_material, release_year, etc.
*   **dim_season**: `season_id` (PK), anime_id (FK), season_number, year, season_name (e.g., "Fall 2023").
*   **dim_episode**: `episode_id` (PK), season_id (FK), episode_number, title, air_date, duration, is_filler (boolean).
*   **dim_date**: `date_id` (PK - YYYYMMDD), year, month, day, day_of_week, is_holiday, fiscal_quarter.
*   **dim_platform**: `platform_id` (PK), platform_name (Crunchyroll, Netflix, Hulu, etc.), region_availability.

### Extended Dimensions
*   **dim_region**: `region_id` (PK), country, region_name (NA, EU, APAC, LATAM), language.
*   **dim_channel**: `channel_id` (PK), channel_name (TV Tokyo, etc.), type (Broadcast, Streaming, Social).
*   **dim_timeslot**: `timeslot_id` (PK), start_time, end_time, day_part (Prime Time, Late Night).
*   **dim_campaign**: `campaign_id` (PK), campaign_name, start_date, end_date, budget, type (Social, Display, TV).
*   **dim_staff**: `staff_id` (PK), name, role (Director, Animator, VA), primary_discipline.
*   **dim_revenue_type**: `revenue_type_id` (PK), category (Streaming, Merchandise, Licensing, Box Office), sub_category.
*   **dim_cost_type**: `cost_type_id` (PK), category (Production, Marketing, Distribution), sub_category.
*   **dim_user_segment**: `segment_id` (PK), segment_name (Core Fan, Casual, Churn Risk), criteria.

### Bridge Tables
*   **bridge_episode_staff**: `episode_id` (FK), `staff_id` (FK), specific_role.

## 2. Fact Tables

### Performance & Engagement
*   **fact_rating_snapshot**:
    *   Keys: `rating_id` (PK), `anime_id` (FK), `date_id` (FK).
    *   Metrics: `score` (MAL score), `scored_by` (user count), `rank`, `popularity`.
    *   Grain: Daily snapshot per anime.

*   **fact_mal_stats_snapshot**:
    *   Keys: `stat_id` (PK), `anime_id` (FK), `date_id` (FK).
    *   Metrics: `watching`, `completed`, `on_hold`, `dropped`, `plan_to_watch`, `total_members`.
    *   Grain: Daily snapshot per anime.

*   **fact_sentiment_daily**:
    *   Keys: `sentiment_id` (PK), `anime_id` (FK), `date_id` (FK), `platform_id` (FK).
    *   Metrics: `positive_mentions`, `negative_mentions`, `neutral_mentions`, `sentiment_score` (-1 to 1).
    *   Grain: Daily per anime per platform.

*   **fact_review**:
    *   Keys: `review_id` (PK), `anime_id` (FK), `date_id` (FK), `user_id` (if available).
    *   Metrics: `score`, `helpful_count`.
    *   Attributes: `review_text` (raw or processed).
    *   Grain: Individual review.

*   **fact_engagement_social**:
    *   Keys: `engagement_id` (PK), `anime_id` (FK), `date_id` (FK), `platform_id` (FK).
    *   Metrics: `likes`, `shares`, `comments`, `views` (for video content).
    *   Grain: Daily per anime per platform.

### Production & Audience
*   **fact_production_episode**:
    *   Keys: `production_id` (PK), `episode_id` (FK).
    *   Metrics: `production_cost`, `animation_cuts`, `correction_count`, `production_days`.
    *   Grain: Per episode.

*   **fact_audience_episode**:
    *   Keys: `audience_id` (PK), `episode_id` (FK), `platform_id` (FK), `region_id` (FK), `date_id` (FK).
    *   Metrics: `views`, `unique_viewers`, `avg_watch_time_seconds`, `completion_rate`.
    *   Grain: Daily per episode per platform/region.

*   **fact_audience_timeslot** (Broadcast):
    *   Keys: `broadcast_id` (PK), `episode_id` (FK), `channel_id` (FK), `timeslot_id` (FK), `date_id` (FK).
    *   Metrics: `viewership_rating` (TV rating), `share`.
    *   Grain: Per broadcast.

### Financials
*   **fact_revenue_stream**:
    *   Keys: `revenue_id` (PK), `anime_id` (FK), `revenue_type_id` (FK), `region_id` (FK), `date_id` (FK).
    *   Metrics: `gross_revenue`, `net_revenue`.
    *   Grain: Daily/Monthly per revenue stream.

*   **fact_costs**:
    *   Keys: `cost_id` (PK), `anime_id` (FK), `cost_type_id` (FK), `date_id` (FK).
    *   Metrics: `amount`.
    *   Grain: Transaction or aggregated daily cost.

*   **fact_campaign_performance**:
    *   Keys: `performance_id` (PK), `campaign_id` (FK), `date_id` (FK).
    *   Metrics: `spend`, `impressions`, `clicks`, `conversions`, `roi`.
    *   Grain: Daily per campaign.

## 3. Implementation Notes
*   **Database**: SQLite (for current phase), scalable to PostgreSQL/Snowflake.
*   **ETL**: Python scripts to populate these tables from Jikan API (public data) and simulated internal CSVs (for private metrics like revenue/production).
