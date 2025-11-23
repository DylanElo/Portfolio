import sqlite3
import json
import os
from datetime import datetime

# Ensure warehouse directory exists
os.makedirs('warehouse', exist_ok=True)

DB_PATH = 'warehouse/pierrot_bi.db'
SCHEMA_PATH = 'warehouse/schema.sql'
DATA_PATH = 'data/raw_mal_data.json'

def init_database():
    """Initialize database with schema"""
    conn = sqlite3.connect(DB_PATH)
    try:
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        print("✅ Database initialized with schema")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
    finally:
        conn.close()

def load_anime_dimension(anime_data):
    """Load dim_anime from MAL data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for anime in anime_data:
        try:
            # Determine studio (simplified logic)
            studios = [s['name'] for s in anime.get('studios', [])]
            primary_studio = studios[0] if studios else 'Unknown'
            
            cursor.execute('''
                INSERT OR REPLACE INTO dim_anime 
                (mal_id, title, title_english, studio, type, episodes, status, air_date_start, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                anime['mal_id'],
                anime['title'],
                anime.get('title_english'),
                primary_studio,
                anime['type'],
                anime['episodes'],
                anime['status'],
                anime.get('aired', {}).get('from'),
                anime.get('source')
            ))
            count += 1
        except Exception as e:
            print(f"Error loading anime {anime.get('title')}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ Loaded {count} records into dim_anime")

def load_rating_facts(anime_data):
    """Load fact_rating_snapshot from MAL data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    today = datetime.now().date()
    
    # Create date dimension entry
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO dim_date (date, year, quarter, month, week_of_year, day_of_week)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            today, 
            today.year, 
            (today.month-1)//3 + 1, 
            today.month,
            today.isocalendar()[1],
            today.isoweekday()
        ))
        
        # Get date_id
        cursor.execute('SELECT date_id FROM dim_date WHERE date = ?', (today,))
        date_id = cursor.fetchone()[0]
        
        count = 0
        for anime in anime_data:
            # Get anime_id
            cursor.execute('SELECT anime_id FROM dim_anime WHERE mal_id = ?', (anime['mal_id'],))
            result = cursor.fetchone()
            
            if result:
                anime_id = result[0]
                
                cursor.execute('''
                    INSERT OR REPLACE INTO fact_rating_snapshot
                    (anime_id, date_id, mal_score, mal_members, mal_favorites, mal_rank,
                     watching, completed, on_hold, dropped, plan_to_watch)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    anime_id, date_id,
                    anime.get('score'),
                    anime.get('members'),
                    anime.get('favorites'),
                    anime.get('rank'),
                    anime.get('statistics', {}).get('watching', 0) if 'statistics' in anime else 0, # API might not return stats in full view sometimes?
                    anime.get('statistics', {}).get('completed', 0) if 'statistics' in anime else 0,
                    anime.get('statistics', {}).get('on_hold', 0) if 'statistics' in anime else 0,
                    anime.get('statistics', {}).get('dropped', 0) if 'statistics' in anime else 0,
                    anime.get('statistics', {}).get('plan_to_watch', 0) if 'statistics' in anime else 0
                ))
                count += 1
        
        conn.commit()
        print(f"✅ Loaded {count} records into fact_rating_snapshot")
        
    except Exception as e:
        print(f"Error loading facts: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    if not os.path.exists(DATA_PATH):
        print(f"❌ Data file not found: {DATA_PATH}. Run extract_mal.py first.")
    else:
        init_database()
        
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            anime_data = json.load(f)
        
        load_anime_dimension(anime_data)
        load_rating_facts(anime_data)
