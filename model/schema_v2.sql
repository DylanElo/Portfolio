-- ============================================================================
-- STUDIO PIERROT BI - STAR SCHEMA V2 (XXL)
-- ============================================================================

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- ============================================================================
-- 1. DIMENSION TABLES
-- ============================================================================

-- DIM_ANIME: Core product dimension
CREATE TABLE IF NOT EXISTS dim_anime (
    anime_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT, -- TV, Movie, OVA
    source TEXT, -- Manga, Novel, Original
    episodes INTEGER,
    status TEXT,
    rating TEXT, -- PG-13, R-17+
    premiered_season TEXT, -- Fall 2002
    premiered_year INTEGER,
    studio TEXT DEFAULT 'Studio Pierrot',
    image_url TEXT,
    filler_percentage DECIMAL(5, 2), -- 0.00 to 100.00
    budget_estimate DECIMAL(12, 2) -- Estimated production budget
);

-- DIM_DATE: Time dimension for time-series analysis
CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY, -- YYYYMMDD format
    full_date DATE NOT NULL,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name TEXT,
    week_of_year INTEGER,
    day_of_week INTEGER,
    day_name TEXT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

-- DIM_PLATFORM: Streaming and broadcast platforms
CREATE TABLE IF NOT EXISTS dim_platform (
    platform_id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform_name TEXT NOT NULL, -- Netflix, Crunchyroll, Hulu, TV Tokyo
    platform_type TEXT, -- SVOD, AVOD, Linear TV
    region_scope TEXT -- Global, Regional, Local
);

-- DIM_REGION: Geographic regions
CREATE TABLE IF NOT EXISTS dim_region (
    region_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_name TEXT NOT NULL, -- North America, Europe, Asia, LATAM
    market_maturity TEXT -- Emerging, Mature
);

-- DIM_CAMPAIGN: Marketing campaigns
CREATE TABLE IF NOT EXISTS dim_campaign (
    campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_name TEXT NOT NULL,
    campaign_type TEXT, -- Launch, Sustain, Revival, Collab
    start_date DATE,
    end_date DATE,
    budget_category TEXT, -- Low, Medium, High
    primary_goal TEXT -- Awareness, Conversion, Retention
);

-- DIM_CHANNEL: Marketing channels
CREATE TABLE IF NOT EXISTS dim_channel (
    channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_name TEXT NOT NULL, -- Social Media, TV Spot, OOH, Digital Ads
    channel_category TEXT -- Digital, Traditional, Experiential
);

-- ============================================================================
-- 2. FACT TABLES
-- ============================================================================

-- FACT_DAILY_PERFORMANCE: Granular daily metrics
CREATE TABLE IF NOT EXISTS fact_daily_performance (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER NOT NULL,
    anime_id INTEGER NOT NULL,
    platform_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    
    -- Metrics
    views INTEGER DEFAULT 0,
    watch_time_minutes INTEGER DEFAULT 0,
    revenue_usd DECIMAL(10, 2) DEFAULT 0.00,
    unique_viewers INTEGER DEFAULT 0,
    
    -- Engagement
    avg_completion_rate DECIMAL(5, 4), -- 0.0 to 1.0
    social_mentions INTEGER DEFAULT 0,
    sentiment_score DECIMAL(3, 2), -- -1.0 to 1.0
    
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (platform_id) REFERENCES dim_platform(platform_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);

-- FACT_CAMPAIGN_PERFORMANCE: Marketing ROI metrics
CREATE TABLE IF NOT EXISTS fact_campaign_performance (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER NOT NULL,
    campaign_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    anime_id INTEGER NOT NULL,
    
    -- Metrics
    spend_usd DECIMAL(10, 2) DEFAULT 0.00,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0, -- e.g., "Add to Watchlist" or "Start Watching"
    
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (campaign_id) REFERENCES dim_campaign(campaign_id),
    FOREIGN KEY (channel_id) REFERENCES dim_channel(channel_id),
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id)
);

-- Create indexes for performance
CREATE INDEX idx_fact_daily_date ON fact_daily_performance(date_id);
CREATE INDEX idx_fact_daily_anime ON fact_daily_performance(anime_id);
CREATE INDEX idx_fact_daily_platform ON fact_daily_performance(platform_id);
