"""
Generate simulated marketing campaign data for Studio Pierrot anime.
Creates realistic marketing campaigns across different channels and types.
"""
import json
import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

def load_mal_data():
    """Load fetched MAL anime data."""
    data_file = Path(__file__).parent.parent / "data" / "raw" / "mal_anime.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_marketing_campaigns(anime_data):
    """Generate marketing campaigns for each anime."""
    
    CAMPAIGN_TYPES = [
        "TV Commercial",
        "Social Media",
        "Digital Display",
        "Convention/Event",
        "Influencer Partnership",
        "Streaming Platform",
        "Print Media"
    ]
    
    CHANNELS = {
        "TV Commercial": ["Fuji TV", "TV Tokyo", "Nippon TV", "TBS"],
       "Social Media": ["Twitter/X", "Instagram", "TikTok", "YouTube", "Facebook"],
        "Digital Display": ["Google Display Network", "Crunchyroll", "AnimePlanet", "MyAnimeList"],
        "Convention/Event": ["Anime Expo", "Comic-Con", "AnimeJapan", "Comiket"],
        "Influencer Partnership": ["YouTube Creators", "Twitch Streamers", "Instagram Influencers"],
        "Streaming Platform": ["Crunchyroll", "Funimation", "Hulu", "Netflix"],
        "Print Media": ["Shonen Jump", "Newtype", "Animedia", "Anime magazines"]
    }
    
    marketing_data = []
    campaign_id = 1
    
    for anime in anime_data:
        mal_id = anime.get("mal_id")
        title = anime.get("title", "")
        members = anime.get("members", 0)
        year = anime.get("year")
        episodes = anime.get("episodes", 0)
        
        # Number of campaigns based on popularity and recency
        if members > 1000000:
            num_campaigns = random.randint(8, 15)  # Big titles
        elif members > 500000:
            num_campaigns = random.randint(5, 10)
        else:
            num_campaigns = random.randint(3, 7)
        
        # Budget multiplier based on year and popularity
        if year and year >= 2015:
            budget_multiplier = random.uniform(1.5, 2.5)  # Modern campaigns cost more
        else:
            budget_multiplier = random.uniform(0.8, 1.5)
        
        for _ in range(num_campaigns):
            campaign_type = random.choice(CAMPAIGN_TYPES)
            channel = random.choice(CHANNELS.get(campaign_type, ["Generic"]))
            
            # Campaign cost based on type and anime popularity
            base_costs = {
                "TV Commercial": (50000, 500000),
                "Social Media": (5000, 50000),
                "Digital Display": (10000, 100000),
                "Convention/Event": (20000, 150000),
                "Influencer Partnership": (15000, 80000),
                "Streaming Platform": (30000, 200000),
                "Print Media": (10000, 75000)
            }
            
            min_cost, max_cost = base_costs.get(campaign_type, (5000, 50000))
            cost = random.uniform(min_cost, max_cost) * budget_multiplier
            
            # Impressions based on cost and type
            impressions_per_dollar = {
                "TV Commercial": random.uniform(15, 25),
                "Social Media": random.uniform(50, 150),
                "Digital Display": random.uniform(30, 80),
                "Convention/Event": random.uniform(5, 15),
                "Influencer Partnership": random.uniform(40, 120),
                "Streaming Platform": random.uniform(20, 60),
                "Print Media": random.uniform(10, 30)
            }
            
            multiplier = impressions_per_dollar.get(campaign_type, 30)
            impressions = int(cost * multiplier * random.uniform(0.8, 1.2))
            
            marketing_data.append({
                "campaign_id": campaign_id,
                "mal_id": mal_id,
                "title": title,
                "campaign_type": campaign_type,
                "channel": channel,
                "cost": round(cost, 2),
                "impressions": impressions
            })
            
            campaign_id += 1
    
    return marketing_data

def main():
    """Main process to generate marketing campaigns."""
    print("=" * 60)
    print("Studio Pierrot Anime BI - Marketing Campaign Generator")
    print("=" * 60)
    print()
    
    # Load MAL data
    anime_data = load_mal_data()
    print(f"✓ Loaded {len(anime_data)} anime records")
    
    # Generate marketing data
    marketing_data = generate_marketing_campaigns(anime_data)
    print(f"✓ Generated {len(marketing_data)} marketing campaigns")
    
    # Save to CSV
    output_dir = Path(__file__).parent.parent / "data" / "raw"
    output_file = output_dir / "marketing.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "campaign_id", "mal_id", "title", "campaign_type",
            "channel", "cost", "impressions"
        ])
        writer.writeheader()
        writer.writerows(marketing_data)
    
    print(f"✓ Saved to {output_file}")
    print()
    
    # Summary stats
    total_cost = sum(c["cost"] for c in marketing_data)
    total_impressions = sum(c["impressions"] for c in marketing_data)
    
    print("=" * 60)
    print("Marketing Summary:")
    print("=" * 60)
    print(f"Total campaigns: {len(marketing_data)}")
    print(f"Total cost: ${total_cost:,.2f}")
    print(f"Total impressions: {total_impressions:,}")
    print(f"Avg cost per campaign: ${total_cost/len(marketing_data):,.2f}")
    print()
    print("Sample campaigns:")
    for row in marketing_data[:5]:
        print(f"{row['title'][:25]:25} | {row['campaign_type']:20} | ${row['cost']:>10,.0f} | {row['impressions']:>12,} impressions")

if __name__ == "__main__":
    main()
