import requests
import json
import time
import os
from datetime import datetime

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

JIKAN_BASE_URL = "https://api.jikan.moe/v4"

# List of Studio Pierrot titles to track
PIERROT_TITLES = [
    {"mal_id": 1735, "title": "Naruto: Shippuden"},
    {"mal_id": 269, "title": "Bleach"},
    {"mal_id": 41467, "title": "Bleach: Thousand-Year Blood War"},
    {"mal_id": 34572, "title": "Black Clover"},
    {"mal_id": 22319, "title": "Tokyo Ghoul"},
    {"mal_id": 27899, "title": "Tokyo Ghoul √A"},
    {"mal_id": 34566, "title": "Boruto: Naruto Next Generations"},
    {"mal_id": 12, "title": "One Piece (Early Episodes)"}, # Note: Toei, but often compared
    {"mal_id": 20, "title": "Naruto"},
    {"mal_id": 223, "title": "Dragon Ball (Early)"}, # Note: Toei
    {"mal_id": 136, "title": "Hunter x Hunter (1999)"}, # Nippon Animation, but Pierrot did 2011? No, Madhouse. 
    # Correcting Pierrot list based on known works
    {"mal_id": 26, "title": "Texhnolyze"}, # Madhouse
    {"mal_id": 121, "title": "Fullmetal Alchemist"}, # Bones
    # Let's stick to confirmed Pierrot hits
    {"mal_id": 11061, "title": "Hunter x Hunter (2011)"}, # Madhouse - wait, let's verify Pierrot list
    {"mal_id": 1604, "title": "Katekyo Hitman Reborn!"}, # Artland
    {"mal_id": 1575, "title": "Code Geass"}, # Sunrise
    
    # CONFIRMED PIERROT LIST
    {"mal_id": 1735, "title": "Naruto: Shippuden"},
    {"mal_id": 20, "title": "Naruto"},
    {"mal_id": 269, "title": "Bleach"},
    {"mal_id": 41467, "title": "Bleach: TYBW"},
    {"mal_id": 34572, "title": "Black Clover"},
    {"mal_id": 22319, "title": "Tokyo Ghoul"},
    {"mal_id": 27899, "title": "Tokyo Ghoul √A"},
    {"mal_id": 34566, "title": "Boruto"},
    {"mal_id": 127, "title": "Gate Keepers"},
    {"mal_id": 2904, "title": "Code Geass (Wait, Sunrise)"}, 
    {"mal_id": 101, "title": "Air"}, # KyoAni
    {"mal_id": 19, "title": "Monster"}, # Madhouse
    {"mal_id": 2476, "title": "School Days"}, # TNK
    {"mal_id": 235, "title": "Detective Conan"}, # TMS
    {"mal_id": 813, "title": "Dragon Ball Z"}, # Toei
    {"mal_id": 50602, "title": "Bleach: TYBW Part 2"},
    {"mal_id": 40356, "title": "Akudama Drive"},
    {"mal_id": 37430, "title": "Tensei shitara Slime Datta Ken"}, # 8bit
    {"mal_id": 38000, "title": "Demon Slayer"}, # ufotable (Competitor)
    {"mal_id": 40748, "title": "Jujutsu Kaisen"}, # MAPPA (Competitor)
]

# Refined list for the portfolio
TARGET_IDS = [
    1735, # Naruto Shippuden
    20,   # Naruto
    269,  # Bleach
    41467, # Bleach TYBW
    34572, # Black Clover
    22319, # Tokyo Ghoul
    27899, # Tokyo Ghoul Root A
    34566, # Boruto
    40356, # Akudama Drive
    129,  # Gensoumaden Saiyuki
    226,  # Elfen Lied (Arms, not Pierrot? Wait, checking)
    # Adding Competitors for comparison
    40748, # JJK (MAPPA)
    38000, # Demon Slayer (ufotable)
]

def fetch_anime_data(mal_id):
    """Fetch anime data from Jikan API"""
    url = f"{JIKAN_BASE_URL}/anime/{mal_id}/full"
    try:
        response = requests.get(url)
        time.sleep(1.5)  # Rate limiting (Jikan is strict)
        
        if response.status_code == 200:
            return response.json()['data']
        else:
            print(f"Error fetching {mal_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception fetching {mal_id}: {e}")
        return None

def extract_all():
    """Extract data for all target titles"""
    results = []
    print(f"Starting extraction for {len(TARGET_IDS)} titles...")
    
    for mal_id in TARGET_IDS:
        print(f"Fetching MAL ID {mal_id}...")
        data = fetch_anime_data(mal_id)
        if data:
            results.append(data)
            print(f"✅ Fetched: {data.get('title')}")
    
    # Save raw data
    os.makedirs('data/raw', exist_ok=True)
    output_file = 'data/raw/mal_anime.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Extracted {len(results)} anime records to {output_file}")
    return results

if __name__ == '__main__':
    extract_all()
