"""
Load data from raw CSVs and JSON into the Studio Pierrot data warehouse.
Transforms and loads data into dimension and fact tables.
"""
import sqlite3
import json
import csv
from pathlib import Path
from datetime import datetime

def load_mal_data():
    """Load MAL anime JSON data."""
    data_file = Path(__file__).parent.parent / "data" / "raw" / "mal_anime.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_csv_data(filename):
    """Load CSV data into a list of dicts."""
    data_file = Path(__file__).parent.parent / "data" / "raw" / filename
    with open(data_file, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def clear_tables(conn):
    """Clear all warehouse tables."""
    cursor = conn.cursor()
    tables = [
        "fact_finance",
        "fact_marketing",
        "fact_anime_metrics",
        "dim_season",
        "dim_anime"
    ]

    for table in tables:
        cursor.execute(f"DELETE FROM {table}")

    conn.commit()
    print("✓ Cleared all warehouse tables")


def determine_tier(score: float, members: int) -> str:
    """Return S/A/B/C tier based on MAL score and membership counts."""

    if score >= 8.5 and members >= 1_000_000:
        return "S"
    if score >= 8.0 and members >= 300_000:
        return "A"
    if score >= 7.0:
        return "B"
    return "C"

def load_dim_anime(conn, anime_data):
    """Load dimension table: dim_anime."""
    cursor = conn.cursor()
    
    anime_records = []
    for idx, anime in enumerate(anime_data, start=1):
        mal_id = anime.get("mal_id")
        title = anime.get("title", "")
        score = anime.get("score") or 0
        members = anime.get("members") or 0
        tier = determine_tier(score, members)
        
        # Extract studio names
        studios = anime.get("studios", [])
        studio = ", ".join([s.get("name", "") for s in studios]) if studios else "Unknown"
        
        episodes = anime.get("episodes") or 12  # default to a single cour when missing
        
        # Extract dates
        aired = anime.get("aired", {})
        start_date = aired.get("from", "")[:10] if aired.get("from") else None
        end_date = aired.get("to", "")[:10] if aired.get("to") else None
        
        # Extract genres
        genres = anime.get("genres", [])
        genre = ", ".join([g.get("name", "") for g in genres]) if genres else None
        
        # Extract demographic
        demographics = anime.get("demographics", [])
        demographic = demographics[0].get("name", "") if demographics else None
        
        anime_records.append((
            idx,  # anime_id is our surrogate key
            mal_id,
            title,
            score,
            members,
            tier,
            studio,
            episodes,
            start_date,
            end_date,
            genre,
            demographic
        ))

    cursor.executemany("""
        INSERT INTO dim_anime (anime_id, mal_id, title, mal_score, mal_members, tier, studio, episodes, start_date, end_date, genre, demographic)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, anime_records)
    
    conn.commit()
    print(f"✓ Loaded {len(anime_records)} records into dim_anime")
    return {anime[1]: anime[0] for anime in anime_records}  # mal_id -> anime_id mapping

def load_dim_season(conn, production_data, mal_to_anime_id):
    """Load dimension table: dim_season."""
    cursor = conn.cursor()
    
    season_records = []
    for row in production_data:
        mal_id = int(row["mal_id"])
        anime_id = mal_to_anime_id.get(mal_id)
        
        if anime_id:
            season_records.append((
                int(row["season_id"]),
                anime_id,
                row["season_type"],
                float(row["filler_ratio"]),
                float(row["production_stability"]),
                float(row["quality_score_internal"])
            ))
    
    cursor.executemany("""
        INSERT INTO dim_season (season_id, anime_id, season_type, filler_ratio, production_stability, quality_score_internal)
        VALUES (?, ?, ?, ?, ?, ?)
    """, season_records)
   
    conn.commit()
    print(f"✓ Loaded {len(season_records)} records into dim_season")

def load_fact_anime_metrics(conn, anime_data, mal_to_anime_id):
    """Load fact table: fact_anime_metrics."""
    cursor = conn.cursor()
    
    metric_records = []
    record_date = datetime.now().isoformat()
    
    for idx, anime in enumerate(anime_data, start=1):
        mal_id = anime.get("mal_id")
        anime_id = mal_to_anime_id.get(mal_id)
        
        if anime_id:
            statistics = anime.get("statistics", {})
            
            metric_records.append((
                idx,  # metric_id
                anime_id,
                anime.get("score"),
                anime.get("scored_by"),
                anime.get("popularity"),
                anime.get("rank"),
                anime.get("members"),
                anime.get("favorites"),
                statistics.get("watching"),
                statistics.get("completed"),
                statistics.get("dropped"),
                statistics.get("plan_to_watch"),
                record_date
            ))
    
    cursor.executemany("""
        INSERT INTO fact_anime_metrics 
        (metric_id, anime_id, score, scored_by, popularity, rank, members, favorites, 
         watching, completed, dropped, plan_to_watch, record_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, metric_records)
    
    conn.commit()
    print(f"✓ Loaded {len(metric_records)} records into fact_anime_metrics")

def load_fact_marketing(conn, marketing_data, mal_to_anime_id):
    """Load fact table: fact_marketing."""
    cursor = conn.cursor()
    
    marketing_records = []
    record_date = datetime.now().isoformat()
    
    for row in marketing_data:
        mal_id = int(row["mal_id"])
        anime_id = mal_to_anime_id.get(mal_id)
        
        if anime_id:
            marketing_records.append((
                int(row["campaign_id"]),
                anime_id,
                row["campaign_type"],
                row["channel"],
                float(row["cost"]),
                int(row["impressions"]),
                record_date
            ))
    
    cursor.executemany("""
        INSERT INTO fact_marketing (campaign_id, anime_id, campaign_type, channel, cost, impressions, record_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, marketing_records)
    
    conn.commit()
    print(f"✓ Loaded {len(marketing_records)} records into fact_marketing")

def load_fact_finance(conn, financial_data, mal_to_anime_id):
    """Load fact table: fact_finance."""
    cursor = conn.cursor()

    financial_records = []
    record_date = datetime.now().isoformat()

    for row in financial_data:
        mal_id = int(row["mal_id"])
        anime_id = mal_to_anime_id.get(mal_id)

        if anime_id:
            financial_records.append((
                int(row["finance_id"]),
                anime_id,
                row["tier"],
                float(row["tier_multiplier"]),
                int(float(row["episodes"])),
                float(row["base_budget_per_episode"]),
                float(row["production_budget"]),
                float(row["total_cost"]),
                float(row["streaming_revenue"]),
                float(row["disc_revenue"]),
                float(row["merch_revenue"]),
                float(row["total_revenue"]),
                float(row["profit"]),
                float(row["roi"]),
                float(row["profit_per_episode"]),
                record_date
            ))

    cursor.executemany("""
        INSERT INTO fact_finance (
            finance_id, anime_id, tier, tier_multiplier, episodes, base_budget_per_episode,
            production_budget, total_cost, streaming_revenue, disc_revenue, merch_revenue,
            total_revenue, profit, roi, profit_per_episode, record_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, financial_records)

    conn.commit()
    print(f"✓ Loaded {len(financial_records)} records into fact_finance")

def main():
    """Main ETL process."""
    print("=" * 70)
    print("Studio Pierrot Anime BI - Warehouse Data Loader")
    print("=" * 70)
    print()
    
    # Connect to database
    db_path = Path(__file__).parent.parent / "studio_pierrot.db"
    conn = sqlite3.connect(db_path)
    
    try:
        # Clear existing data
        clear_tables(conn)
        print()
        
        # Load raw data
        print("Loading raw data files...")
        anime_data = load_mal_data()
        production_data = load_csv_data("production.csv")
        marketing_data = load_csv_data("marketing.csv")
        financial_data = load_csv_data("financials.csv")
        print(f"✓ Loaded all raw data files")
        print()
        
        # Load dimensions first
        print("Loading dimension tables...")
        mal_to_anime_id = load_dim_anime(conn, anime_data)
        load_dim_season(conn, production_data, mal_to_anime_id)
        print()
        
        # Load facts
        print("Loading fact tables...")
        load_fact_anime_metrics(conn, anime_data, mal_to_anime_id)
        load_fact_marketing(conn, marketing_data, mal_to_anime_id)
        load_fact_finance(conn, financial_data, mal_to_anime_id)
        print()
        
        # Verification
        print("=" * 70)
        print("Data Warehouse Load Summary")
        print("=" * 70)
        
        cursor = conn.cursor()
        tables = [
            ("dim_anime", "Anime titles"),
            ("dim_season", "Season/production records"),
            ("fact_anime_metrics", "MAL performance metrics"),
            ("fact_marketing", "Marketing campaigns"),
            ("fact_finance", "Financial records")
        ]
        
        for table_name, description in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"{table_name:25} | {count:>6} {description}")
        
        print("=" * 70)
        print("✓ Data warehouse load complete!")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
