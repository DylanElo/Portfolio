"""
Fetch Studio Pierrot anime data from MyAnimeList via Jikan API.
Saves raw JSON responses to data/raw/mal_anime.json
"""
import requests
import json
import time
from pathlib import Path
from typing import List, Dict

# Jikan API base URL
JIKAN_BASE = "https://api.jikan.moe/v4"

# Studio Pierrot MAL ID
STUDIO_PIERROT_ID = 1  # Will search by name instead

# Target Studio Pierrot anime (curated list)
TARGET_ANIME = [
    {"mal_id": 20, "title": "Naruto"},
    {"mal_id": 1735, "title": "Naruto: Shippuuden"},
    {"mal_id": 269, "title": "Bleach"},
    {"mal_id": 22319, "title": "Tokyo Ghoul"},
    {"mal_id": 36511, "title": "Tokyo Ghoul:re"},
    {"mal_id": 34566, "title": "Boruto: Naruto Next Generations"},
    {"mal_id": 34572, "title": "Black Clover"},
    {"mal_id": 392, "title": "Yuu☆Yuu☆Hakusho"},
    {"mal_id": 12031, "title": "Kingdom"},
    {"mal_id": 37510, "title": "Tokyo Ghoul:re 2nd Season"},
    {"mal_id": 113415, "title": "Bleach: Sennen Kessen-hen"},
    {"mal_id": 11061, "title": "Hunter x Hunter (2011)"},
    {"mal_id": 19, "title": "Monster"},
    {"mal_id": 16498, "title": "Shingeki no Kyojin"},
    # New additions
    {"mal_id": 918, "title": "Gintama"},
    {"mal_id": 40748, "title": "Jujutsu Kaisen"},
    {"mal_id": 21, "title": "One Piece"},
    {"mal_id": 31964, "title": "Boku no Hero Academia"},
    {"mal_id": 44511, "title": "Chainsaw Man"},
    {"mal_id": 38000, "title": "Kimetsu no Yaiba"},
]

def fetch_anime_details(mal_id: int) -> Dict:
    """Fetch detailed anime information from Jikan API."""
    url = f"{JIKAN_BASE}/anime/{mal_id}/full"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data:
            anime = data["data"]
            print(f"✓ Fetched: {anime.get('title', 'Unknown')} (ID: {mal_id})")
            return anime
        else:
            print(f"✗ No data for MAL ID {mal_id}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching MAL ID {mal_id}: {e}")
        return None

def fetch_anime_statistics(mal_id: int) -> Dict:
    """Fetch anime statistics (watching, completed, dropped, etc.)."""
    url = f"{JIKAN_BASE}/anime/{mal_id}/statistics"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data:
            return data["data"]
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching statistics for MAL ID {mal_id}: {e}")
        return None

def main():
    """Main ETL process to fetch MAL data."""
    print("=" * 60)
    print("Studio Pierrot Anime BI - MAL Data Fetcher")
    print("=" * 60)
    print()
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_anime_data = []
    
    # Fetch data for each anime
    for anime_info in TARGET_ANIME:
        mal_id = anime_info["mal_id"]
        expected_title = anime_info["title"]
        
        print(f"Fetching {expected_title} (MAL ID: {mal_id})...")
        
        # Fetch main details
        anime_data = fetch_anime_details(mal_id)
        
        if anime_data:
            # Fetch statistics
            time.sleep(1)  # Rate limiting (Jikan allows 3 req/sec, being conservative)
            stats = fetch_anime_statistics(mal_id)
            
            if stats:
                anime_data["statistics"] = stats
            
            all_anime_data.append(anime_data)
        
        # Rate limiting
        time.sleep(1)
        print()
    
    # Save to JSON
    output_file = output_dir / "mal_anime.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_anime_data, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print(f"✓ Saved {len(all_anime_data)} anime records to {output_file}")
    print("=" * 60)
    
    # Summary
    print("\nFetched anime:")
    for anime in all_anime_data:
        title = anime.get("title", "Unknown")
        score = anime.get("score", 0)
        members = anime.get("members", 0)
        studios = ", ".join([s["name"] for s in anime.get("studios", [])])
        print(f"  - {title} | Score: {score} | Members: {members:,} | Studio: {studios}")

if __name__ == "__main__":
    main()
