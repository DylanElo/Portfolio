-- Star Schema for Studio Pierrot Anime BI

-- Dimension: Anime
CREATE TABLE dim_anime (
    anime_id INTEGER PRIMARY KEY,
    mal_id INTEGER UNIQUE,
    title TEXT NOT NULL,
    studio TEXT,
    episodes INTEGER,
    start_date TEXT,
    end_date TEXT,
    genre TEXT,
    demographic TEXT
);

-- Dimension: Season (long vs short)
CREATE TABLE dim_season (
    season_id INTEGER PRIMARY KEY,
    anime_id INTEGER REFERENCES dim_anime(anime_id),
    season_type TEXT, -- e.g., "long", "short"
    filler_ratio REAL,
    production_stability REAL,
    quality_score_internal REAL
);

-- Fact: Anime Performance Metrics (from MAL)
CREATE TABLE fact_anime_metrics (
    metric_id INTEGER PRIMARY KEY,
    anime_id INTEGER REFERENCES dim_anime(anime_id),
    score REAL,
    scored_by INTEGER,
    popularity INTEGER,
    rank INTEGER,
    members INTEGER,
    favorites INTEGER,
    watching INTEGER,
    completed INTEGER,
    dropped INTEGER,
    plan_to_watch INTEGER,
    record_date TEXT DEFAULT (datetime('now'))
);

-- Fact: Marketing Campaigns (simulated)
CREATE TABLE fact_marketing (
    campaign_id INTEGER PRIMARY KEY,
    anime_id INTEGER REFERENCES dim_anime(anime_id),
    campaign_type TEXT,
    channel TEXT,
    cost REAL,
    impressions INTEGER,
    record_date TEXT DEFAULT (datetime('now'))
);

-- Fact: Financials (simulated)
CREATE TABLE fact_financials (
    financial_id INTEGER PRIMARY KEY,
    anime_id INTEGER REFERENCES dim_anime(anime_id),
    production_cost REAL,
    marketing_cost REAL,
    estimated_revenue REAL,
    record_date TEXT DEFAULT (datetime('now'))
);
