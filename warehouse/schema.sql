-- Studio Pierrot Anime Performance Analytics Warehouse
-- Schema: Star Schema (Dimensions & Facts)
-- Dialect: SQLite / PostgreSQL Compatible

-- ==========================================
-- 🧱 DIMENSIONS
-- ==========================================

-- 1. dim_anime
CREATE TABLE dim_anime (
    anime_id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    title_english VARCHAR(255),
    title_romaji VARCHAR(255),
    franchise_group VARCHAR(100), -- e.g. Naruto, Bleach
    studio_name VARCHAR(100) DEFAULT 'Studio Pierrot',
    type VARCHAR(50), -- TV, OVA, Movie
    release_date_start DATE,
    release_date_end DATE,
    release_year_start INTEGER,
    release_year_end INTEGER,
    total_episodes INTEGER,
    format_type VARCHAR(50), -- Long-running / Short-season
    main_genre VARCHAR(50),
    sub_genres TEXT, -- Semicolon separated
    target_demographic VARCHAR(50), -- Shonen, Seinen
    original_source VARCHAR(50), -- Manga, Novel
    is_flagship BOOLEAN,
    is_recent BOOLEAN,
    status VARCHAR(50), -- Announced, Airing, Completed
    avg_episode_duration_min INTEGER
);

-- 2. dim_season
CREATE TABLE dim_season (
    season_id INTEGER PRIMARY KEY,
    anime_id INTEGER,
    season_number INTEGER,
    season_name VARCHAR(255),
    release_date_start DATE,
    release_date_end DATE,
    num_episodes INTEGER,
    is_canon_only BOOLEAN,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id)
);

-- 3. dim_date
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY, -- YYYYMMDD
    date DATE,
    day INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    year INTEGER,
    quarter INTEGER,
    week_of_year INTEGER,
    day_of_week INTEGER,
    day_name VARCHAR(20),
    is_weekend BOOLEAN,
    is_jp_holiday BOOLEAN
);

-- 4. dim_episode
CREATE TABLE dim_episode (
    episode_id INTEGER PRIMARY KEY,
    anime_id INTEGER,
    season_id INTEGER,
    episode_number INTEGER, -- Absolute
    episode_code VARCHAR(20), -- S01E01
    episode_title VARCHAR(255),
    air_date_id INTEGER,
    is_filler BOOLEAN,
    is_recap BOOLEAN,
    is_double_length BOOLEAN,
    is_key_episode BOOLEAN,
    runtime_minutes INTEGER,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (season_id) REFERENCES dim_season(season_id),
    FOREIGN KEY (air_date_id) REFERENCES dim_date(date_id)
);

-- 5. dim_platform
CREATE TABLE dim_platform (
    platform_id INTEGER PRIMARY KEY,
    platform_name VARCHAR(100), -- Netflix, Crunchyroll
    platform_type VARCHAR(50), -- streaming, broadcast, social
    default_region_id INTEGER,
    website_url VARCHAR(255)
    -- FK to region added later or handled logically
);

-- 6. dim_region
CREATE TABLE dim_region (
    region_id INTEGER PRIMARY KEY,
    region_name VARCHAR(100), -- Japan, NA
    country_code VARCHAR(10),
    region_group VARCHAR(50) -- APAC, EMEA
);

-- 7. dim_channel
CREATE TABLE dim_channel (
    channel_id INTEGER PRIMARY KEY,
    channel_name VARCHAR(100),
    channel_type VARCHAR(50),
    owner_company VARCHAR(100),
    region_id INTEGER,
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);

-- 8. dim_timeslot
CREATE TABLE dim_timeslot (
    timeslot_id INTEGER PRIMARY KEY,
    start_time TIME,
    end_time TIME,
    timeslot_label VARCHAR(100)
);

-- 9. dim_campaign
CREATE TABLE dim_campaign (
    campaign_id INTEGER PRIMARY KEY,
    anime_id INTEGER,
    campaign_name VARCHAR(255),
    campaign_type VARCHAR(50),
    objective VARCHAR(100),
    start_date_id INTEGER,
    end_date_id INTEGER,
    primary_channel_id INTEGER,
    budget_estimated NUMERIC,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (start_date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (end_date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (primary_channel_id) REFERENCES dim_channel(channel_id)
);

-- 10. dim_staff
CREATE TABLE dim_staff (
    staff_id INTEGER PRIMARY KEY,
    full_name VARCHAR(255),
    primary_role VARCHAR(100),
    is_in_house BOOLEAN,
    experience_years INTEGER,
    notes TEXT
);

-- Bridge Table: Staff x Episode
CREATE TABLE bridge_episode_staff (
    episode_id INTEGER,
    staff_id INTEGER,
    role_on_episode VARCHAR(100),
    PRIMARY KEY (episode_id, staff_id),
    FOREIGN KEY (episode_id) REFERENCES dim_episode(episode_id),
    FOREIGN KEY (staff_id) REFERENCES dim_staff(staff_id)
);

-- 11. dim_revenue_type
CREATE TABLE dim_revenue_type (
    revenue_type_id INTEGER PRIMARY KEY,
    revenue_type_name VARCHAR(100),
    category VARCHAR(50)
);

-- 12. dim_cost_type
CREATE TABLE dim_cost_type (
    cost_type_id INTEGER PRIMARY KEY,
    cost_type_name VARCHAR(100),
    is_fixed BOOLEAN,
    is_variable BOOLEAN
);

-- 13. dim_user_segment
CREATE TABLE dim_user_segment (
    segment_id INTEGER PRIMARY KEY,
    segment_name VARCHAR(100),
    age_band VARCHAR(50),
    gender VARCHAR(20),
    region_id INTEGER,
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);


-- ==========================================
-- 📊 FACTS
-- ==========================================

-- 1. fact_rating_snapshot
CREATE TABLE fact_rating_snapshot (
    anime_id INTEGER,
    platform_id INTEGER,
    date_id INTEGER,
    avg_rating NUMERIC,
    num_votes INTEGER,
    members_count INTEGER,
    favorites_count INTEGER,
    rank_global INTEGER,
    popularity_index INTEGER,
    PRIMARY KEY (anime_id, platform_id, date_id),
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (platform_id) REFERENCES dim_platform(platform_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- 2. fact_mal_stats_snapshot
CREATE TABLE fact_mal_stats_snapshot (
    anime_id INTEGER,
    platform_id INTEGER,
    date_id INTEGER,
    watching_count INTEGER,
    completed_count INTEGER,
    on_hold_count INTEGER,
    dropped_count INTEGER,
    plan_to_watch_count INTEGER,
    total_users INTEGER,
    completion_rate NUMERIC, -- Derived
    drop_rate NUMERIC, -- Derived
    PRIMARY KEY (anime_id, platform_id, date_id),
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (platform_id) REFERENCES dim_platform(platform_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- 3. fact_audience_episode
CREATE TABLE fact_audience_episode (
    anime_id INTEGER,
    episode_id INTEGER,
    platform_id INTEGER,
    date_id INTEGER,
    region_id INTEGER,
    segment_id INTEGER,
    views INTEGER,
    unique_viewers INTEGER,
    avg_watch_time_minutes NUMERIC,
    completion_rate_episode NUMERIC,
    drop_from_prev_episode NUMERIC,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (episode_id) REFERENCES dim_episode(episode_id),
    FOREIGN KEY (platform_id) REFERENCES dim_platform(platform_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (segment_id) REFERENCES dim_user_segment(segment_id)
);

-- 4. fact_audience_timeslot
CREATE TABLE fact_audience_timeslot (
    anime_id INTEGER,
    episode_id INTEGER,
    channel_id INTEGER,
    date_id INTEGER,
    timeslot_id INTEGER,
    tv_rating NUMERIC,
    households_reached INTEGER,
    share_vs_competition NUMERIC,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (episode_id) REFERENCES dim_episode(episode_id),
    FOREIGN KEY (channel_id) REFERENCES dim_channel(channel_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (timeslot_id) REFERENCES dim_timeslot(timeslot_id)
);

-- 5. fact_production_episode
CREATE TABLE fact_production_episode (
    anime_id INTEGER,
    episode_id INTEGER,
    season_id INTEGER,
    production_days INTEGER,
    overtime_hours INTEGER,
    outsourced_flag BOOLEAN,
    production_stability_idx INTEGER,
    quality_score_internal INTEGER,
    budget_episode_estimated NUMERIC,
    revisions_count INTEGER,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (episode_id) REFERENCES dim_episode(episode_id),
    FOREIGN KEY (season_id) REFERENCES dim_season(season_id)
);

-- 6. fact_sentiment_daily
CREATE TABLE fact_sentiment_daily (
    anime_id INTEGER,
    platform_id INTEGER,
    date_id INTEGER,
    sentiment_score_avg NUMERIC,
    num_mentions INTEGER,
    num_positive INTEGER,
    num_negative INTEGER,
    num_neutral INTEGER,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (platform_id) REFERENCES dim_platform(platform_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- 7. fact_review
CREATE TABLE fact_review (
    review_id INTEGER PRIMARY KEY,
    anime_id INTEGER,
    platform_id INTEGER,
    date_id INTEGER,
    user_id_external VARCHAR(255),
    review_score NUMERIC,
    sentiment_score NUMERIC,
    review_length_words INTEGER,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (platform_id) REFERENCES dim_platform(platform_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- 8. fact_engagement_social
CREATE TABLE fact_engagement_social (
    anime_id INTEGER,
    platform_id INTEGER,
    date_id INTEGER,
    posts_count INTEGER,
    likes INTEGER,
    shares INTEGER,
    comments INTEGER,
    followers_gained INTEGER,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (platform_id) REFERENCES dim_platform(platform_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- 9. fact_campaign_performance
CREATE TABLE fact_campaign_performance (
    campaign_id INTEGER,
    anime_id INTEGER,
    channel_id INTEGER,
    date_id INTEGER,
    impressions INTEGER,
    clicks INTEGER,
    click_through_rate NUMERIC,
    cost NUMERIC,
    conversions INTEGER,
    estimated_viewers_gained INTEGER,
    FOREIGN KEY (campaign_id) REFERENCES dim_campaign(campaign_id),
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (channel_id) REFERENCES dim_channel(channel_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- 10. fact_revenue_stream
CREATE TABLE fact_revenue_stream (
    anime_id INTEGER,
    region_id INTEGER,
    date_id INTEGER,
    revenue_type_id INTEGER,
    revenue_amount NUMERIC,
    units_sold INTEGER,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (revenue_type_id) REFERENCES dim_revenue_type(revenue_type_id)
);

-- 11. fact_costs
CREATE TABLE fact_costs (
    anime_id INTEGER,
    date_id INTEGER,
    cost_type_id INTEGER,
    cost_amount NUMERIC,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (cost_type_id) REFERENCES dim_cost_type(cost_type_id)
);
