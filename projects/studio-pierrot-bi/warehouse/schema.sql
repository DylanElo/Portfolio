-- Studio Pierrot BI Warehouse Schema
-- Star schema design for multi-lens anime analysis
-- SQLite 3 compatible

-- ============================================
-- DIMENSIONAL TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS dim_anime (
    anime_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mal_id INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    title_english TEXT,
    studio TEXT DEFAULT 'Pierrot',
    is_pierrot BOOLEAN DEFAULT 1,
    revenue_profile TEXT, -- LegacyTail, NewHit, RevivalHit, LongRun
    broadcast_status TEXT, -- Finished, Airing, Hiatus
    type TEXT, -- TV, Movie, OVA
    episodes INTEGER,
    status TEXT, -- Finished Airing, Currently Airing
    air_date_start DATE,
    air_date_end DATE,
    source TEXT, -- Manga, Light Novel, Original
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    week_of_year INTEGER,
    day_of_week INTEGER
);

CREATE TABLE IF NOT EXISTS dim_platform (
    platform_id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform_name TEXT NOT NULL UNIQUE, -- Netflix, Crunchyroll, Hulu
    platform_type TEXT, -- SVOD, AVOD, TVOD
    parent_company TEXT,
    primary_region TEXT
);

CREATE TABLE IF NOT EXISTS dim_region (
    region_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_name TEXT NOT NULL UNIQUE, -- North America, Japan, Europe, etc.
    country_group TEXT
);

-- ============================================
-- FACT TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS fact_rating_snapshot (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    anime_id INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    mal_score REAL,
    mal_members INTEGER,
    mal_favorites INTEGER,
    mal_rank INTEGER,
    watching INTEGER,
    completed INTEGER,
    on_hold INTEGER,
    dropped INTEGER,
    plan_to_watch INTEGER,
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    UNIQUE(anime_id, date_id)
);

CREATE TABLE IF NOT EXISTS fact_revenue_stream (
    revenue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    anime_id INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    platform_id INTEGER,
    region_id INTEGER,
    revenue_amount REAL, -- in millions USD or JPY
    revenue_type TEXT, -- streaming, bd_sales, merchandise, licensing
    currency TEXT DEFAULT 'USD',
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (platform_id) REFERENCES dim_platform(platform_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);

CREATE TABLE IF NOT EXISTS fact_production_episode (
    production_id INTEGER PRIMARY KEY AUTOINCREMENT,
    anime_id INTEGER NOT NULL,
    episode_number INTEGER,
    arc_name TEXT,
    is_filler BOOLEAN,
    animation_quality_score REAL, -- 1-10
    budget_tier TEXT, -- low, medium, high
    production_model TEXT, -- seasonal, continuous
    FOREIGN KEY (anime_id) REFERENCES dim_anime(anime_id),
    UNIQUE(anime_id, episode_number)
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX IF NOT EXISTS idx_rating_anime_date ON fact_rating_snapshot(anime_id, date_id);
CREATE INDEX IF NOT EXISTS idx_rating_score ON fact_rating_snapshot(mal_score DESC);
CREATE INDEX IF NOT EXISTS idx_revenue_anime_date ON fact_revenue_stream(anime_id, date_id);
CREATE INDEX IF NOT EXISTS idx_revenue_type ON fact_revenue_stream(revenue_type);
CREATE INDEX IF NOT EXISTS idx_production_anime ON fact_production_episode(anime_id);
CREATE INDEX IF NOT EXISTS idx_production_filler ON fact_production_episode(is_filler);
CREATE INDEX IF NOT EXISTS idx_anime_mal_id ON dim_anime(mal_id);

-- ============================================
-- METADATA TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS etl_metadata (
    etl_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT, -- 'jikan_api', 'manual_load', etc.
    records_processed INTEGER,
    status TEXT, -- 'success', 'failed', 'partial'
    notes TEXT
);
