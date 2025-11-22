import sqlite3
from datetime import datetime, timedelta
import random
import os

# Configuration
DB_PATH = 'studio_pierrot.db'
SCHEMA_PATH = 'model/schema_v2.sql'
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

def init_db():
    print("Initializing V2 Database...")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Removed existing database.")
    
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    conn.close()
    print("Database initialized.")

def populate_dimensions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Populating Dimensions...")

    # 1. DIM_PLATFORM
    platforms = [
        ('Netflix', 'SVOD', 'Global'),
        ('Crunchyroll', 'SVOD', 'Global'),
        ('Hulu', 'SVOD', 'North America'),
        ('TV Tokyo', 'Linear TV', 'Japan'),
        ('Amazon Prime', 'SVOD', 'Global')
    ]
    cursor.executemany('INSERT INTO dim_platform (platform_name, platform_type, region_scope) VALUES (?, ?, ?)', platforms)

    # 2. DIM_REGION
    regions = [
        ('North America', 'Mature'),
        ('Europe', 'Mature'),
        ('Asia', 'Emerging'),
        ('LATAM', 'Emerging'),
        ('Japan', 'Mature')
    ]
    cursor.executemany('INSERT INTO dim_region (region_name, market_maturity) VALUES (?, ?)', regions)

    # 3. DIM_CHANNEL
    channels = [
        ('Social Media', 'Digital'),
        ('TV Spot', 'Traditional'),
        ('YouTube Ads', 'Digital'),
        ('Influencer', 'Digital'),
        ('OOH (Billboards)', 'Traditional')
    ]
    cursor.executemany('INSERT INTO dim_channel (channel_name, channel_category) VALUES (?, ?)', channels)

    # 4. DIM_DATE
    current_date = START_DATE
    dates = []
    while current_date <= END_DATE:
        date_id = int(current_date.strftime('%Y%m%d'))
        is_weekend = current_date.weekday() >= 5
        dates.append((
            date_id,
            current_date.strftime('%Y-%m-%d'),
            current_date.year,
            (current_date.month - 1) // 3 + 1,
            current_date.month,
            current_date.strftime('%B'),
            current_date.isocalendar()[1],
            current_date.weekday(),
            current_date.strftime('%A'),
            is_weekend,
            False # Simplify holidays for now
        ))
        current_date += timedelta(days=1)
    
    cursor.executemany('''
        INSERT OR IGNORE INTO dim_date 
        (date_id, full_date, year, quarter, month, month_name, week_of_year, day_of_week, day_name, is_weekend, is_holiday) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dates)

    # 5. DIM_ANIME (Migrate from existing raw data or hardcode list for V2)
    # Added Filler % and Budget Estimate for analysis
    anime_list = [
        (1, 'Naruto', 'TV', 'Manga', 220, 'Finished', 'PG-13', 'Fall 2002', 2002, 41.0, 15000000), # High filler
        (2, 'Naruto: Shippuuden', 'TV', 'Manga', 500, 'Finished', 'PG-13', 'Winter 2007', 2007, 40.0, 45000000), # High filler
        (3, 'Bleach', 'TV', 'Manga', 366, 'Finished', 'PG-13', 'Fall 2004', 2004, 45.0, 30000000), # Very high filler
        (4, 'Bleach: Sennen Kessen-hen', 'TV', 'Manga', 13, 'Finished', 'R-17+', 'Fall 2022', 2022, 0.0, 5000000), # No filler, high budget
        (5, 'Tokyo Ghoul', 'TV', 'Manga', 12, 'Finished', 'R-17+', 'Summer 2014', 2014, 0.0, 3000000),
        (6, 'Black Clover', 'TV', 'Manga', 170, 'Finished', 'PG-13', 'Fall 2017', 2017, 10.0, 18000000),
        (7, 'Boruto: Naruto Next Generations', 'TV', 'Manga', 293, 'Finished', 'PG-13', 'Spring 2017', 2017, 75.0, 25000000), # Extreme filler
        (8, 'Great Teacher Onizuka', 'TV', 'Manga', 43, 'Finished', 'R-17+', 'Summer 1999', 1999, 5.0, 4000000),
        (9, 'Yu Yu Hakusho', 'TV', 'Manga', 112, 'Finished', 'PG-13', 'Fall 1992', 1992, 3.0, 8000000),
        (10, 'Kingdom', 'TV', 'Manga', 38, 'Finished', 'PG-13', 'Summer 2012', 2012, 0.0, 4500000)
    ]
    cursor.executemany('''
        INSERT OR REPLACE INTO dim_anime (anime_id, title, type, source, episodes, status, rating, premiered_season, premiered_year, filler_percentage, budget_estimate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', anime_list)

    conn.commit()
    conn.close()
    print("Dimensions populated.")

def generate_facts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("Generating Facts (this may take a moment)...")

    # Get IDs
    date_ids = [row[0] for row in cursor.execute('SELECT date_id FROM dim_date').fetchall()]
    anime_ids = [row[0] for row in cursor.execute('SELECT anime_id FROM dim_anime').fetchall()]
    platform_ids = [row[0] for row in cursor.execute('SELECT platform_id FROM dim_platform').fetchall()]
    region_ids = [row[0] for row in cursor.execute('SELECT region_id FROM dim_region').fetchall()]

    fact_rows = []
    
    # Simulation Parameters
    base_views = 5000
    
    for date_id in date_ids:
        # Parse date to check for seasonality
        date_str = str(date_id)
        month = int(date_str[4:6])
        is_weekend = datetime.strptime(date_str, '%Y%m%d').weekday() >= 5
        
        seasonality = 1.2 if is_weekend else 1.0
        if month in [7, 8, 12]: seasonality *= 1.1 # Summer/Winter break boost

        for anime_id in anime_ids:
            # Anime popularity factor (Naruto/Bleach are huge)
            popularity = 5.0 if anime_id in [1, 2, 3, 4] else (3.0 if anime_id in [6, 7] else 1.0)
            
            for platform_id in platform_ids:
                for region_id in region_ids:
                    # Random noise
                    noise = random.gauss(1.0, 0.2)
                    
                    # Calculate Metrics
                    views = int(base_views * popularity * seasonality * noise)
                    if platform_id == 4 and region_id != 5: views = 0 # TV Tokyo only in Japan
                    
                    if views > 0:
                        watch_time = views * 22 # Approx 22 mins per ep
                        revenue = views * 0.02 # Approx $0.02 per view (ads/sub share)
                        unique_viewers = int(views * 0.8)
                        completion_rate = min(0.98, max(0.4, random.gauss(0.75, 0.1)))
                        sentiment = min(1.0, max(-1.0, random.gauss(0.6, 0.3)))
                        
                        fact_rows.append((
                            date_id, anime_id, platform_id, region_id,
                            views, watch_time, revenue, unique_viewers,
                            completion_rate, 0, sentiment
                        ))

    print(f"Generated {len(fact_rows)} daily fact rows.")
    
    # Batch insert
    cursor.executemany('''
        INSERT INTO fact_daily_performance 
        (date_id, anime_id, platform_id, region_id, views, watch_time_minutes, revenue_usd, unique_viewers, avg_completion_rate, social_mentions, sentiment_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', fact_rows)

    conn.commit()
    conn.close()
    print("Facts populated.")

if __name__ == '__main__':
    init_db()
    populate_dimensions()
    generate_facts()
