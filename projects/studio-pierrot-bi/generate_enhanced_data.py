"""
Enhanced Dashboard Data Generator
Generates realistic anime performance data for Studio Pierrot and competitors
Based on real anime titles, MAL scores, air dates, and known platform deals
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict

# Set seed for reproducibility
random.seed(42)

# ============================================================================
# REAL STUDIO PIERROT ANIME DATA (50+ titles from 2000-2024)
# ============================================================================

STUDIO_PIERROT_ANIME = [
    # LEGACY ERA (2000-2015)
    {"title": "Naruto", "start_year": 2002, "end_year": 2007, "episodes": 220, "mal_score": 7.99, "genre": "Shonen", "category": "legacy", "tier": "S"},
    {"title": "Naruto: Shippuuden", "start_year": 2007, "end_year": 2017, "episodes": 500, "mal_score": 8.26, "genre": "Shonen", "category": "legacy", "tier": "S"},
    {"title": "Bleach", "start_year": 2004, "end_year": 2012, "episodes": 366, "mal_score": 7.92, "genre": "Shonen", "category": "legacy", "tier": "S"},
    {"title": "Yu Yu Hakusho", "start_year": 1992, "end_year": 1995, "episodes": 112, "mal_score": 8.46, "genre": "Shonen", "category": "legacy", "tier": "S"},
    {"title": "Tokyo Ghoul", "start_year": 2014, "end_year": 2014, "episodes": 12, "mal_score": 7.79, "genre": "Seinen", "category": "legacy", "tier": "A"},
    {"title": "Tokyo Ghoul √A", "start_year": 2015, "end_year": 2015, "episodes": 12, "mal_score": 7.02, "genre": "Seinen", "category": "legacy", "tier": "B"},
    {"title": "Beelzebub", "start_year": 2011, "end_year": 2012, "episodes": 60, "mal_score": 7.88, "genre": "Comedy", "category": "legacy", "tier": "B"},
    {"title": "Great Teacher Onizuka", "start_year": 1999, "end_year": 2000, "episodes": 43, "mal_score": 8.58, "genre": "Comedy", "category": "legacy", "tier": "A"},
    {"title": "Hikaru no Go", "start_year": 2001, "end_year": 2003, "episodes": 75, "mal_score": 8.18, "genre": "Sports", "category": "legacy", "tier": "A"},
    {"title": "Yona of the Dawn", "start_year": 2014, "end_year": 2015, "episodes": 24, "mal_score": 8.03, "genre": "Adventure", "category": "legacy", "tier": "A"},
    
    # MODERN ERA (2016-2024) - Bleach TYBW is HERE now
    {"title": "Bleach: Thousand-Year Blood War", "start_year": 2022, "end_year": 2024, "episodes": 52, "mal_score": 9.11, "genre": "Shonen", "category": "modern", "tier": "S"},
    {"title": "Black Clover", "start_year": 2017, "end_year": 2021, "episodes": 170, "mal_score": 8.13, "genre": "Shonen", "category": "modern", "tier": "A"},
    {"title": "Boruto: Naruto Next Generations", "start_year": 2017, "end_year": 2024, "episodes": 293, "mal_score": 5.91,  "genre": "Shonen", "category": "modern", "tier": "C"},
    {"title": "Tokyo Ghoul:re", "start_year": 2018, "end_year": 2018, "episodes": 12, "mal_score": 6.45, "genre": "Seinen", "category": "modern", "tier": "C"},
    {"title": "Akudama Drive", "start_year": 2020, "end_year": 2020, "episodes": 12, "mal_score": 7.63, "genre": "Sci-Fi", "category": "modern", "tier": "B"},
    {"title": "Kingdom Season 3", "start_year": 2020, "end_year": 2021, "episodes": 26, "mal_score": 8.51, "genre": "Historical", "category": "modern", "tier": "A"},
    {"title": "Kingdom Season 4", "start_year": 2022, "end_year": 2022, "episodes": 26, "mal_score": 8.69, "genre": "Historical", "category": "modern", "tier": "A"},
    {"title": "Kingdom Season 5", "start_year": 2024, "end_year": 2024, "episodes": 13, "mal_score": 8.75, "genre": "Historical", "category": "modern", "tier": "A"},
    {"title": "Twin Star Exorcists", "start_year": 2016, "end_year": 2017, "episodes": 50, "mal_score": 7.31, "genre": "Shonen", "category": "modern", "tier": "B"},
    {"title": "The Legend of Korra", "start_year": 2012, "end_year": 2014, "episodes": 52, "mal_score": 8.25, "genre": "Adventure", "category": "modern", "tier": "A"},
    
    # Additional Modern Titles
    {"title": "Baby Steps", "start_year": 2014, "end_year": 2015, "episodes": 50, "mal_score": 7.89, "genre": "Sports", "category": "modern", "tier": "B"},
    {"title": "Osomatsu-san", "start_year": 2015, "end_year": 2018, "episodes": 51, "mal_score": 7.97, "genre": "Comedy", "category": "modern", "tier": "B"},
    {"title": "Saiki K Season 2", "start_year": 2018, "end_year": 2018, "episodes": 24, "mal_score": 8.42, "genre": "Comedy", "category": "modern", "tier": "A"},
    {"title": "Radiant Season 2", "start_year": 2019, "end_year": 2020, "episodes": 21, "mal_score": 7.01, "genre": "Fantasy", "category": "modern", "tier": "C"},
    {"title": "Cardfight!! Vanguard (2018)", "start_year": 2018, "end_year": 2019, "episodes": 52, "mal_score": 6.82, "genre": "Card Game", "category": "modern", "tier": "C"},
]

# ============================================================================
# COMPETITOR STUDIOS DATA
# ============================================================================

COMPETITOR_STUDIOS = {
    "MAPPA": [
        {"title": "Jujutsu Kaisen", "start_year": 2020, "end_year": 2021, "episodes": 24, "mal_score": 8.63, "tier": "S"},
        {"title": "Jujutsu Kaisen 2nd Season", "start_year": 2023, "end_year": 2023, "episodes": 23, "mal_score": 8.80, "tier": "S"},
        {"title": "Attack on Titan Final Season", "start_year": 2020, "end_year": 2021, "episodes": 16, "mal_score": 8.80, "tier": "S"},
        {"title": "Attack on Titan Final Season Part 2", "start_year": 2022, "end_year": 2022, "episodes": 12, "mal_score": 9.05, "tier": "S"},
        {"title": "Chainsaw Man", "start_year": 2022, "end_year": 2022, "episodes": 12, "mal_score": 8.55, "tier": "S"},
        {"title": "Vinland Saga Season 2", "start_year": 2023, "end_year": 2023, "episodes": 24, "mal_score": 8.81, "tier": "S"},
        {"title": "Hell's Paradise", "start_year": 2023, "end_year": 2023, "episodes": 13, "mal_score": 8.15, "tier": "A"},
        {"title": "Dororo", "start_year": 2019, "end_year": 2019, "episodes": 24, "mal_score": 8.25, "tier": "A"},
        {"title": "Banana Fish", "start_year": 2018, "end_year": 2018, "episodes": 24, "mal_score": 8.50, "tier": "A"},
        {"title": "Zombieland Saga", "start_year": 2018, "end_year": 2018, "episodes": 12, "mal_score": 7.50, "tier": "B"},
        {"title": "Yuri!!! on Ice", "start_year": 2016, "end_year": 2016, "episodes": 12, "mal_score": 7.90, "tier": "A"},
        {"title": "Kakegurui", "start_year": 2017, "end_year": 2017, "episodes": 12, "mal_score": 7.25, "tier": "B"},
        {"title": "Inuyashiki", "start_year": 2017, "end_year": 2017, "episodes": 11, "mal_score": 7.65, "tier": "B"},
        {"title": "The God of High School", "start_year": 2020, "end_year": 2020, "episodes": 13, "mal_score": 7.05, "tier": "C"},
        {"title": "Takt Op. Destiny", "start_year": 2021, "end_year": 2021, "episodes": 12, "mal_score": 7.15, "tier": "C"},
        {"title": "Campfire Cooking in Another World", "start_year": 2023, "end_year": 2023, "episodes": 12, "mal_score": 7.70, "tier": "B"},
        {"title": "Dance Dance Danseur", "start_year": 2022, "end_year": 2022, "episodes": 11, "mal_score": 7.95, "tier": "B"},
        {"title": "Dorohedoro", "start_year": 2020, "end_year": 2020, "episodes": 12, "mal_score": 8.05, "tier": "A"},
        {"title": "Terror in Resonance", "start_year": 2014, "end_year": 2014, "episodes": 11, "mal_score": 8.10, "tier": "A"},
        {"title": "Kids on the Slope", "start_year": 2012, "end_year": 2012, "episodes": 12, "mal_score": 8.30, "tier": "A"},
    ],
    "Bones": [
        {"title": "Fullmetal Alchemist: Brotherhood", "start_year": 2009, "end_year": 2010, "episodes": 64, "mal_score": 9.10, "tier": "S"},
        {"title": "My Hero Academia", "start_year": 2016, "end_year": 2016, "episodes": 13, "mal_score": 7.90, "tier": "A"},
        {"title": "My Hero Academia 2", "start_year": 2017, "end_year": 2017, "episodes": 25, "mal_score": 8.15, "tier": "S"},
        {"title": "My Hero Academia 3", "start_year": 2018, "end_year": 2018, "episodes": 25, "mal_score": 8.05, "tier": "S"},
        {"title": "Mob Psycho 100", "start_year": 2016, "end_year": 2016, "episodes": 12, "mal_score": 8.48, "tier": "S"},
        {"title": "Mob Psycho 100 II", "start_year": 2019, "end_year": 2019, "episodes": 13, "mal_score": 8.80, "tier": "S"},
        {"title": "Bungo Stray Dogs", "start_year": 2016, "end_year": 2016, "episodes": 12, "mal_score": 7.80, "tier": "A"},
        {"title": "Noragami", "start_year": 2014, "end_year": 2014, "episodes": 12, "mal_score": 7.95, "tier": "A"},
        {"title": "Soul Eater", "start_year": 2008, "end_year": 2009, "episodes": 51, "mal_score": 7.85, "tier": "A"},
        {"title": "Ouran High School Host Club", "start_year": 2006, "end_year": 2006, "episodes": 26, "mal_score": 8.15, "tier": "A"},
        {"title": "Space Dandy", "start_year": 2014, "end_year": 2014, "episodes": 13, "mal_score": 7.90, "tier": "B"},
        {"title": "The Case Study of Vanitas", "start_year": 2021, "end_year": 2021, "episodes": 12, "mal_score": 7.90, "tier": "B"},
        {"title": "SK8 the Infinity", "start_year": 2021, "end_year": 2021, "episodes": 12, "mal_score": 8.00, "tier": "B"},
        {"title": "Blood Blockade Battlefront", "start_year": 2015, "end_year": 2015, "episodes": 12, "mal_score": 7.60, "tier": "B"},
        {"title": "Eureka Seven", "start_year": 2005, "end_year": 2006, "episodes": 50, "mal_score": 8.05, "tier": "A"},
        {"title": "Darker than Black", "start_year": 2007, "end_year": 2007, "episodes": 25, "mal_score": 8.10, "tier": "A"},
        {"title": "Wolf's Rain", "start_year": 2003, "end_year": 2003, "episodes": 26, "mal_score": 7.80, "tier": "B"},
        {"title": "Gosick", "start_year": 2011, "end_year": 2011, "episodes": 24, "mal_score": 8.05, "tier": "B"},
        {"title": "Snow White with the Red Hair", "start_year": 2015, "end_year": 2015, "episodes": 12, "mal_score": 7.75, "tier": "B"},
        {"title": "Carole & Tuesday", "start_year": 2019, "end_year": 2019, "episodes": 24, "mal_score": 7.90, "tier": "B"},
    ],
    "Ufotable": [
        {"title": "Demon Slayer", "start_year": 2019, "end_year": 2019, "episodes": 26, "mal_score": 8.50, "tier": "S"},
        {"title": "Demon Slayer: Mugen Train Arc", "start_year": 2021, "end_year": 2021, "episodes": 7, "mal_score": 8.35, "tier": "S"},
        {"title": "Demon Slayer: Entertainment District", "start_year": 2021, "end_year": 2022, "episodes": 11, "mal_score": 8.80, "tier": "S"},
        {"title": "Demon Slayer: Swordsmith Village", "start_year": 2023, "end_year": 2023, "episodes": 11, "mal_score": 8.30, "tier": "S"},
        {"title": "Fate/Zero", "start_year": 2011, "end_year": 2011, "episodes": 13, "mal_score": 8.30, "tier": "A"},
        {"title": "Fate/Zero 2nd Season", "start_year": 2012, "end_year": 2012, "episodes": 12, "mal_score": 8.55, "tier": "A"},
        {"title": "Fate/stay night: UBW", "start_year": 2014, "end_year": 2014, "episodes": 12, "mal_score": 8.20, "tier": "A"},
        {"title": "Fate/stay night: UBW 2nd Season", "start_year": 2015, "end_year": 2015, "episodes": 13, "mal_score": 8.30, "tier": "A"},
        {"title": "The Garden of Sinners (Movie Series)", "start_year": 2007, "end_year": 2009, "episodes": 8, "mal_score": 8.00, "tier": "B"},
        {"title": "God Eater", "start_year": 2015, "end_year": 2016, "episodes": 13, "mal_score": 7.30, "tier": "C"},
        {"title": "Tales of Zestiria the X", "start_year": 2016, "end_year": 2016, "episodes": 12, "mal_score": 7.20, "tier": "C"},
        {"title": "Katsugeki/Touken Ranbu", "start_year": 2017, "end_year": 2017, "episodes": 13, "mal_score": 7.00, "tier": "C"},
        {"title": "Today's Menu for the Emiya Family", "start_year": 2018, "end_year": 2019, "episodes": 13, "mal_score": 7.80, "tier": "B"},
    ],
    "Wit Studio": [
        {"title": "Attack on Titan", "start_year": 2013, "end_year": 2013, "episodes": 25, "mal_score": 8.54, "tier": "S"},
        {"title": "Attack on Titan Season 2", "start_year": 2017, "end_year": 2017, "episodes": 12, "mal_score": 8.50, "tier": "S"},
        {"title": "Attack on Titan Season 3", "start_year": 2018, "end_year": 2018, "episodes": 12, "mal_score": 8.65, "tier": "S"},
        {"title": "Attack on Titan Season 3 Part 2", "start_year": 2019, "end_year": 2019, "episodes": 10, "mal_score": 9.05, "tier": "S"},
        {"title": "Spy x Family", "start_year": 2022, "end_year": 2022, "episodes": 12, "mal_score": 8.50, "tier": "S"},
        {"title": "Vinland Saga", "start_year": 2019, "end_year": 2019, "episodes": 24, "mal_score": 8.75, "tier": "S"},
        {"title": "Ranking of Kings", "start_year": 2021, "end_year": 2022, "episodes": 23, "mal_score": 8.55, "tier": "A"},
        {"title": "Great Pretender", "start_year": 2020, "end_year": 2020, "episodes": 23, "mal_score": 8.25, "tier": "A"},
        {"title": "Vivy: Fluorite Eye's Song", "start_year": 2021, "end_year": 2021, "episodes": 13, "mal_score": 8.45, "tier": "A"},
        {"title": "Seraph of the End", "start_year": 2015, "end_year": 2015, "episodes": 12, "mal_score": 7.50, "tier": "B"},
        {"title": "The Ancient Magus' Bride", "start_year": 2017, "end_year": 2018, "episodes": 24, "mal_score": 8.05, "tier": "B"},
        {"title": "Kabaneri of the Iron Fortress", "start_year": 2016, "end_year": 2016, "episodes": 12, "mal_score": 7.25, "tier": "C"},
        {"title": "After the Rain", "start_year": 2018, "end_year": 2018, "episodes": 12, "mal_score": 7.50, "tier": "B"},
    ],
    "CloverWorks": [
        {"title": "Spy x Family (Part 2)", "start_year": 2022, "end_year": 2022, "episodes": 13, "mal_score": 8.40, "tier": "S"},
        {"title": "Bocchi the Rock!", "start_year": 2022, "end_year": 2022, "episodes": 12, "mal_score": 8.80, "tier": "S"},
        {"title": "My Dress-Up Darling", "start_year": 2022, "end_year": 2022, "episodes": 12, "mal_score": 8.30, "tier": "A"},
        {"title": "The Promised Neverland", "start_year": 2019, "end_year": 2019, "episodes": 12, "mal_score": 8.50, "tier": "S"},
        {"title": "Horimiya", "start_year": 2021, "end_year": 2021, "episodes": 13, "mal_score": 8.20, "tier": "A"},
        {"title": "Rascal Does Not Dream of Bunny Girl Senpai", "start_year": 2018, "end_year": 2018, "episodes": 13, "mal_score": 8.25, "tier": "A"},
        {"title": "Wind Breaker", "start_year": 2024, "end_year": 2024, "episodes": 13, "mal_score": 7.80, "tier": "B"},
        {"title": "Wonder Egg Priority", "start_year": 2021, "end_year": 2021, "episodes": 12, "mal_score": 7.60, "tier": "B"},
        {"title": "Darling in the FranXX", "start_year": 2018, "end_year": 2018, "episodes": 24, "mal_score": 7.20, "tier": "B"},
        {"title": "Fate/Grand Order: Babylonia", "start_year": 2019, "end_year": 2020, "episodes": 21, "mal_score": 7.90, "tier": "B"},
        {"title": "Shadows House", "start_year": 2021, "end_year": 2021, "episodes": 13, "mal_score": 7.70, "tier": "B"},
        {"title": "Fugou Keiji: Balance:UNLIMITED", "start_year": 2020, "end_year": 2020, "episodes": 11, "mal_score": 7.50, "tier": "C"},
        {"title": "Akebi's Sailor Uniform", "start_year": 2022, "end_year": 2022, "episodes": 12, "mal_score": 7.60, "tier": "C"},
    ]
}

# ============================================================================
# PLATFORM DISTRIBUTION WEIGHTS (Based on known deals)
# ============================================================================

PLATFORM_WEIGHTS = {
    # Platform: (base_weight, variance)
    "Crunchyroll": (0.35, 0.10),
    "Netflix": (0.25, 0.08),
    "Hulu": (0.20, 0.07),
    "Funimation": (0.15, 0.05),
    "Disney+": (0.05, 0.03),
}

# Known exclusive deals
PLATFORM_EXCLUSIVES = {
    "Bleach: Thousand-Year Blood War": {"Hulu": 0.45, "Disney+": 0.35, "Crunchyroll": 0.20},
    "Jujutsu Kaisen": {"Crunchyroll": 0.70, "Netflix": 0.20, "Hulu": 0.10},
    "Demon Slayer": {"Crunchyroll": 0.60, "Netflix": 0.25, "Hulu": 0.15},
}

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def get_generation(start_year):
    if start_year < 2016:
        return "Legacy (Pre-2016)"
    elif 2016 <= start_year <= 2019:
        return "Gen 1 (2016-2019)"
    elif 2020 <= start_year <= 2022:
        return "Gen 2 (2020-2022)"
    else:
        return "Gen 3 (2023-Present)"

def calculate_realistic_views(anime: Dict, platform_split: Dict) -> int:
    """Calculate realistic view counts based on MAL score, episodes, tier"""
    base_views = {
        "S": 800_000_000,  # Mega hits
        "A": 400_000_000,  # Strong performers
        "B": 150_000_000,  # Mid-tier
        "C": 50_000_000,   # Underperformers
    }
    
    tier = anime.get("tier", "B")
    episodes = anime["episodes"]
    mal_score = anime["mal_score"]
    
    # Base calculation
    views = base_views[tier]
    
    # Episode multiplier (longer series get more total views)
    episode_multiplier = min(2.0, 0.5 + (episodes / 100))
    views *= episode_multiplier
    
    # MAL score bonus (higher rated = more views)
    score_multiplier = 0.7 + (mal_score / 10) * 0.6
    views *= score_multiplier
    
    # Modern anime get platform boost
    if anime.get("start_year", 2000) >= 2016:
        views *= 1.3
    
    # Add realistic variance
    views *= random.uniform(0.85, 1.15)
    
    return int(views)

def calculate_revenue(views: int, tier: str, platform_split: Dict) -> int:
    """Calculate revenue based on views and platform deal quality"""
    # CPM (cost per mille) varies by platform
    platform_cpms = {
        "Crunchyroll": 2.50,
        "Netflix": 4.00,
        "Hulu": 3.50,
        "Funimation": 2.80,
        "Disney+": 4.50,
    }
    
    total_revenue = 0
    for platform, percentage in platform_split.items():
        platform_views = views * (percentage / 100)
        cpm = platform_cpms.get(platform, 3.00)
        revenue = (platform_views / 1000) * cpm
        total_revenue += revenue
    
    # Tier bonus (premium content gets better deals)
    tier_multipliers = {"S": 1.5, "A": 1.2, "B": 1.0, "C": 0.8}
    total_revenue *= tier_multipliers.get(tier, 1.0)
    
    return int(total_revenue)

def generate_platform_split(anime_title: str) -> Dict[str, float]:
    """Generate realistic platform distribution"""
    if anime_title in PLATFORM_EXCLUSIVES:
        return PLATFORM_EXCLUSIVES[anime_title]
    
    split = {}
    remaining = 100.0
    
    for platform, (base_weight, variance) in PLATFORM_WEIGHTS.items():
        if remaining <= 0:
            break
        
        # Add variance
        weight = base_weight + random.uniform(-variance, variance)
        weight = max(0.05, min(0.50, weight))  # Clamp between 5% and 50%
        
        percentage = weight * 100
        if percentage > remaining:
            percentage = remaining
        
        split[platform] = round(percentage, 2)
        remaining -= percentage
    
    # Normalize to exactly 100%
    total = sum(split.values())
    if total > 0:
        split = {k: round((v / total) * 100, 2) for k, v in split.items()}
    
    return split

def generate_daily_trend_data(anime: Dict, views: int, start_date: str, end_date: str) -> List[Dict]:
    """Generate daily trend data with realistic patterns"""
    from datetime import datetime, timedelta
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    days = (end - start).days + 1
    daily_data = []
    
    # Calculate average daily views
    avg_daily_views = views / days if days > 0 else views
    
    for i in range(days):
        current_date = start + timedelta(days=i)
        
        # Seasonal pattern (weekends get more views)
        weekday_multiplier = 1.3 if current_date.weekday() in [5, 6] else 1.0
        
        # Release pattern (premiere and finale get spikes)
        position_in_series = i / max(days, 1)
        if position_in_series < 0.05 or position_in_series > 0.95:
            event_multiplier = 1.5
        else:
            event_multiplier = 1.0
        
        # Random daily variance
        variance = random.uniform(0.7, 1.3)
        
        daily_views = int(avg_daily_views * weekday_multiplier * event_multiplier * variance)
        daily_revenue = int(daily_views * 0.003)  # Rough CPM estimate
        
        daily_data.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "title": anime["title"],
            "views": daily_views,
            "revenue": daily_revenue
        })
    
    return daily_data

# ============================================================================
# MAIN DATA GENERATION
# ============================================================================

def generate_cohort_matrix(competitor_data):
    """Generate cohort performance matrix for heatmap visualization"""
    generations = ["Legacy (Pre-2016)", "Gen 1 (2016-2019)", "Gen 2 (2020-2022)", "Gen 3 (2023-Present)"]
    studios = sorted(set(d["studio"] for d in competitor_data))
    
    matrix = []
    for studio in studios:
        for gen in generations:
            # Filter data for this studio and generation
            filtered = [d for d in competitor_data if d["studio"] == studio and d["generation"] == gen]
            if filtered:
                avg_revenue = sum(d["revenue"] for d in filtered) / len(filtered)
                matrix.append({
                    "studio": studio,
                    "generation": gen,
                    "value": int(avg_revenue)
                })
    
    return matrix

def generate_platform_generation_data(competitor_data):
    """Generate platform market share by generation for stacked area chart"""
    from collections import defaultdict
    
    generations = ["Legacy (Pre-2016)", "Gen 1 (2016-2019)", "Gen 2 (2020-2022)", "Gen 3 (2023-Present)"]
    gen_platform_data = defaultdict(lambda: defaultdict(int))
    
    # Estimate platform share for each anime based on generation
    platform_weights_by_gen = {
        "Legacy (Pre-2016)": {"TV Tokyo": 0.60, "Crunchyroll": 0.20, "Funimation": 0.15, "Netflix": 0.05},
        "Gen 1 (2016-2019)": {"Crunchyroll": 0.45, "Funimation": 0.25, "Netflix": 0.20, "Hulu": 0.10},
        "Gen 2 (2020-2022)": {"Crunchyroll": 0.40, "Netflix": 0.30, "Hulu": 0.20, "Disney+": 0.10},
        "Gen 3 (2023-Present)": {"Crunchyroll": 0.35, "Netflix": 0.30, "Disney+": 0.20, "Hulu": 0.15}
    }
    
    for item in competitor_data:
        gen = item["generation"]
        revenue = item["revenue"]
        
        if gen in platform_weights_by_gen:
            for platform, weight in platform_weights_by_gen[gen].items():
                gen_platform_data[gen][platform] += revenue * weight
    
    # Format for stacked area chart
    result = []
    for gen in generations:
        gen_data = {"generation": gen}
        for platform in set(p for weights in platform_weights_by_gen.values() for p in weights.keys()):
            gen_data[platform] = int(gen_platform_data[gen].get(platform, 0))
        result.append(gen_data)
    
    return result

def generate_platform_matrix(platform_aggregates):
    """Generate platform performance matrix for heatmap"""
    metrics = ["Revenue", "Views", "Engagement"]
    matrix = []
    
    for platform, data in platform_aggregates.items():
        matrix.append({
            "platform": platform,
            "metric": "Revenue",
            "value": int(data["revenue"])
        })
        matrix.append({
            "platform": platform,
            "metric": "Views",
            "value": int(data["views"])
        })
        # Engagement = views/revenue ratio(normalized)
        engagement = (data["views"] / data["revenue"]) if data["revenue"] > 0 else 0
        matrix.append({
            "platform": platform,
            "metric": "Engagement",
            "value": int(engagement)
        })
    
    return matrix

def generate_enhanced_dataset():
    """Generate complete enhanced dataset"""
    
    print("🎬 Generating Enhanced Anime BI Dataset...")
    print(f"📊 Studio Pierrot Titles: {len(STUDIO_PIERROT_ANIME)}")
    
    # Storage
    all_anime_performance = []
    all_daily_trends = []
    platform_aggregates = {p: {"revenue": 0, "views": 0} for p in PLATFORM_WEIGHTS.keys()}
    region_data = {}
    studio_comparison = []
    
    # Process Studio Pierrot Anime
    print("\n🔵 Processing Studio Pierrot anime...")
    for anime in STUDIO_PIERROT_ANIME:
        platform_split = generate_platform_split(anime["title"])
        views = calculate_realistic_views(anime, platform_split)
        revenue = calculate_revenue(views, anime["tier"], platform_split)
        
        # Anime performance
        performance = {
            "title": anime["title"],
            "views": views,
            "revenue": revenue,
            "sentiment": min(1.0, anime["mal_score"] / 10),
            "completion_rate": random.uniform(0.65, 0.95) if anime["tier"] in ["S", "A"] else random.uniform(0.45, 0.70),
            "roi": random.uniform(250, 450) if anime["tier"] == "S" else random.uniform(150, 300),
            "category": anime["category"],
            "generation": get_generation(anime["start_year"]),
            "tier": anime["tier"],
        }
        all_anime_performance.append(performance)
        
        # Daily trend (last 30 days)
        end_date = "2024-11-22"
        start_date = "2024-10-23"
        daily_trends = generate_daily_trend_data(anime, views // 365, start_date, end_date)
        all_daily_trends.extend(daily_trends)
        
        # Platform aggregates
        for platform, percentage in platform_split.items():
            platform_revenue = revenue * (percentage / 100)
            platform_views = views * (percentage / 100)
            platform_aggregates[platform]["revenue"] += platform_revenue
            platform_aggregates[platform]["views"] += platform_views
        
        print(f"  ✓ {anime['title'][:40]:40} | Tier {anime['tier']} | {views:,} views")
    
    # Process Competitor Studios
    print("\n🏢 Processing Competitor Studios...")
    competitor_raw_data = []

    for studio_name, anime_list in COMPETITOR_STUDIOS.items():
        studio_total_revenue = 0
        studio_total_views = 0
        
        for anime in anime_list:
            platform_split = generate_platform_split(anime["title"])
            views = calculate_realistic_views({**anime, "category": "modern"}, platform_split)
            revenue = calculate_revenue(views, anime["tier"], platform_split)
            
            studio_total_revenue += revenue
            studio_total_views += views
            
            # Add to raw list for frontend filtering
            competitor_raw_data.append({
                "title": anime["title"],
                "studio": studio_name,
                "start_year": anime["start_year"],
                "end_year": anime["end_year"],
                "generation": get_generation(anime["start_year"]),
                "views": views,
                "revenue": revenue,
                "sentiment": anime["mal_score"] / 10,
                "tier": anime["tier"]
            })
        
        studio_comparison.append({
            "studio": studio_name,
            "total_revenue": studio_total_revenue,
            "total_views": studio_total_views,
            "avg_sentiment": sum(a["mal_score"] for a in anime_list) / len(anime_list) / 10,
            "title_count": len(anime_list)
        })
        
        print(f"  ✓ {studio_name:15} | {len(anime_list)} titles | {studio_total_views:,} views")
    
    # Add Studio Pierrot to comparison
    pierrot_total = {
        "studio": "Studio Pierrot",
        "total_revenue": sum(p["revenue"] for p in all_anime_performance),
        "total_views": sum(p["views"] for p in all_anime_performance),
        "avg_sentiment": sum(p["sentiment"] for p in all_anime_performance) / len(all_anime_performance),
        "title_count": len(STUDIO_PIERROT_ANIME)
    }
    studio_comparison.insert(0, pierrot_total)

    # Add Pierrot data to raw list
    for p in all_anime_performance:
        # Find original metadata for year
        meta = next((a for a in STUDIO_PIERROT_ANIME if a["title"] == p["title"]), None)
        start_year = meta["start_year"] if meta else 2000
        competitor_raw_data.append({
            "title": p["title"],
            "studio": "Studio Pierrot",
            "start_year": start_year,
            "end_year": meta["end_year"] if meta else 2024,
            "generation": get_generation(start_year),
            "views": p["views"],
            "revenue": p["revenue"],
            "sentiment": p["sentiment"],
            "tier": p["tier"]
        })
    
    # Generate Sankey Data (Studio -> Platform -> Region)
    print("  Generating Sankey flows...")
    sankey_flows = {}
    
    # 1. Studio -> Platform
    for entry in competitor_raw_data:
        studio = entry["studio"]
        # Re-estimate platform split for this entry since we didn't save it
        # This is a simplification, ideally we'd save it.
        # But for aggregate flow it's okay to re-generate based on title/tier
        platforms = generate_platform_split(entry["title"])
        
        for plat, share in platforms.items():
            flow = int(entry["views"] * share)
            key = f"{studio}|{plat}"
            sankey_flows[key] = sankey_flows.get(key, 0) + flow

    sankey_data = []
    platform_totals = {}
    
    for key, flow in sankey_flows.items():
        studio, plat = key.split("|")
        sankey_data.append({"from": studio, "to": plat, "flow": flow})
        platform_totals[plat] = platform_totals.get(plat, 0) + flow

    # 2. Platform -> Region (Estimated)
    # Define regional affinity for platforms
    platform_regions = {
        "Crunchyroll": {"North America": 0.45, "Europe": 0.30, "Japan": 0.05, "Asia (Other)": 0.10, "Other": 0.10},
        "Netflix": {"North America": 0.30, "Europe": 0.25, "Japan": 0.15, "Asia (Other)": 0.20, "Other": 0.10},
        "Hulu": {"North America": 0.95, "Japan": 0.05, "Europe": 0.0, "Asia (Other)": 0.0, "Other": 0.0},
        "Disney+": {"North America": 0.35, "Europe": 0.30, "Japan": 0.15, "Asia (Other)": 0.15, "Other": 0.05},
        "Funimation": {"North America": 0.80, "Europe": 0.15, "Japan": 0.0, "Asia (Other)": 0.0, "Other": 0.05},
        "Amazon Prime": {"North America": 0.30, "Europe": 0.30, "Japan": 0.20, "Asia (Other)": 0.15, "Other": 0.05},
    }

    # Aggregate platform totals into regions
    for plat, total_flow in platform_totals.items():
        regions = platform_regions.get(plat, platform_regions["Netflix"])  # Default to Netflix distribution
        for region, share in regions.items():
            flow = int(total_flow * share)
            if flow > 0:
                sankey_data.append({"from": plat, "to": region, "flow": flow})

    # Build final dataset
    dataset = {
        "kpis": {
            "total_revenue": sum(p["revenue"] for p in all_anime_performance),
            "total_views": sum(p["views"] for p in all_anime_performance),
            "total_watch_time": sum(p["views"] for p in all_anime_performance) * 20 // 60,
            "avg_sentiment": sum(p["sentiment"] for p in all_anime_performance) / len(all_anime_performance),
        },
        "anime_list": [{"title": a["title"]} for a in STUDIO_PIERROT_ANIME],
        "anime_performance": all_anime_performance,
        "daily_anime_trend": all_daily_trends,
        "daily_trend": [],  # will be filled later
        "platform_split": [
            {"platform_name": platform, "revenue": int(data["revenue"]), "views": int(data["views"])}
            for platform, data in platform_aggregates.items()
        ],
        "scatter_plot": [
            {
                "title": p["title"],
                "filler_percentage": random.uniform(5, 45) if "Boruto" in p["title"] or "Black Clover" in p["title"] else random.uniform(0, 15),
                "roi_percentage": p["roi"],
                "total_views": p["views"]
            }
            for p in all_anime_performance
        ],
        "heatmap": [
            {"day_name": day, "views": random.randint(50_000_000, 150_000_000)}
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        ],
        "region_split": [
            {"region_name": "Japan", "views": sum(p["views"] for p in all_anime_performance) * 0.25, "revenue": sum(p["revenue"] for p in all_anime_performance) * 0.30},
            {"region_name": "North America", "views": sum(p["views"] for p in all_anime_performance) * 0.35, "revenue": sum(p["revenue"] for p in all_anime_performance) * 0.40},
            {"region_name": "Europe", "views": sum(p["views"] for p in all_anime_performance) * 0.20, "revenue": sum(p["revenue"] for p in all_anime_performance) * 0.18},
            {"region_name": "Asia (Other)", "views": sum(p["views"] for p in all_anime_performance) * 0.15, "revenue": sum(p["revenue"] for p in all_anime_performance) * 0.10},
            {"region_name": "Other", "views": sum(p["views"] for p in all_anime_performance) * 0.05, "revenue": sum(p["revenue"] for p in all_anime_performance) * 0.02}
        ],
        "cohort_performance_matrix": generate_cohort_matrix(competitor_raw_data),
        "platform_by_generation": generate_platform_generation_data(competitor_raw_data),
        "platform_performance_matrix": generate_platform_matrix(platform_aggregates),
        "studio_comparison": studio_comparison,
        "competitor_raw_data": competitor_raw_data,
        "sankey_data": sankey_data
    }

    # Aggregate daily trend by date
    daily_agg = {}
    for entry in all_daily_trends:
        date = entry["date"]
        if date not in daily_agg:
            daily_agg[date] = {"date": date, "views": 0, "revenue": 0}
        daily_agg[date]["views"] += entry["views"]
        daily_agg[date]["revenue"] += entry["revenue"]
    dataset["daily_trend"] = sorted(daily_agg.values(), key=lambda x: x["date"])

    return dataset

if __name__ == "__main__":
    dataset = generate_enhanced_dataset()
    
    output_file = "Portfolio-vite/public/data.json"
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"\n✅ Dataset generated successfully!")
    print(f"📁 Saved to: {output_file}")
    print(f"📊 Total Studios Pierrot titles: {len(dataset['anime_performance'])}")
    print(f"🏢 Competitor studios: {len(dataset['studio_comparison']) - 1}")
    print(f"💰 Total Revenue: ${dataset['kpis']['total_revenue']:,}")
    print(f"👁️  Total Views: {dataset['kpis']['total_views']:,}")





