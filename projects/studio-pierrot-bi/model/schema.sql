-- Star Schema for Studio Pierrot Anime BI

-- Dimension: Anime
CREATE TABLE dim_anime (
    anime_id INTEGER PRIMARY KEY,
    mal_id INTEGER UNIQUE,
    title TEXT NOT NULL,
    mal_score REAL,
    mal_members INTEGER,
    tier TEXT,
    studio TEXT,
    episodes INTEGER,
    start_date TEXT,
    end_date TEXT,
    genre TEXT,
    demographic TEXT,
    type TEXT,
    status TEXT
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
CREATE TABLE fact_finance (
    finance_id INTEGER PRIMARY KEY,
    anime_id INTEGER REFERENCES dim_anime(anime_id),
    tier TEXT,
    tier_multiplier REAL,
    episodes INTEGER,
    base_budget_per_episode REAL,
    production_budget REAL,
    total_cost REAL,
    streaming_revenue REAL,
    disc_revenue REAL,
    merch_revenue REAL,
    total_revenue REAL,
    profit REAL,
    roi REAL,
    profit_per_episode REAL,
    record_date TEXT DEFAULT (datetime('now'))
);
