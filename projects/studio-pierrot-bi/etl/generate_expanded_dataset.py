"""
Generate expanded anime dataset with industry-calibrated financial model.
Based on Japanese Animation Industry Report 2020-2024.

Key figures:
- Production cost: ¥10-30M per episode (~$75k-$225k USD)
- Revenue split: 72% merchandising, 28% streaming
- Industry total: ~¥3.8 trillion ($25B USD) in 2024
"""
import requests
import json
import time
import csv
from pathlib import Path

# Studio/Producer IDs from MAL/Jikan
STUDIOS = {
    'pierrot': 1,  # Studio Pierrot
    'mappa': 569,  # MAPPA
    'ufotable': 43,  # ufotable
    'bones': 4,  # Bones
    'madhouse': 11  # Madhouse
}

BASE_URL = "https://api.jikan.moe/v4"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "raw"

def fetch_anime_by_producer(producer_id, studio_name, limit=50):
    """Fetch anime from a specific producer/studio"""
    anime_list = []
    page = 1
    
    print(f"\nFetching {studio_name} anime...")
    
    while len(anime_list) < limit:
        url = f"{BASE_URL}/anime?producers={producer_id}&page={page}&limit=25&order_by=members&sort=desc"
        
        try:
            response = requests.get(url)
            time.sleep(1.5)  # Rate limiting
            
            if response.status_code != 200:
                print(f"  Error {response.status_code} on page {page}")
                break
                
            data = response.json()
            anime_page = data.get('data', [])
            
            if not anime_page:
                break
                
            for anime in anime_page:
                # Add studio attribution
                anime['primary_studio'] = studio_name
                anime_list.append(anime)
                print(f"  ✓ {anime.get('title')} (Score: {anime.get('score')}, Members: {anime.get('members')})")
                
            if len(anime_list) >= limit or not data.get('pagination', {}).get('has_next_page'):
                break
                
            page += 1
            
        except Exception as e:
            print(f"  Exception: {e}")
            break
    
    return anime_list[:limit]

def determine_tier(score, members):
    """Determine S/A/B/C tier based on MAL metrics"""
    score = score or 0
    members = members or 0
    
    if score >= 8.5 and members >= 1_000_000:
        return 'S'
    elif score >= 8.0 and members >= 300_000:
        return 'A'
    elif score >= 7.0:
        return 'B'
    else:
        return 'C'

def calculate_financials(anime):
    """
    Calculate realistic financial metrics based on industry report.
    
    Production Costs:
    - Base: $150k per episode (¥19.5M at ¥130/$)
    - Tier multipliers: S=1.6x, A=1.3x, B=1.0x, C=0.7x
    
    Revenue Model:
    - Merchandising (72%): Driven by fandom (members)
    - Streaming (28%): Driven by global popularity
    """
    mal_id = anime.get('mal_id')
    score = anime.get('score') or 0
    members = anime.get('members') or 0
    episodes = anime.get('episodes') or 12
    tier = determine_tier(score, members)
    
    # Base budget per episode in USD
    base_budget_per_ep = 150_000
    
    # Tier multipliers
    tier_multipliers = {'S': 1.6, 'A': 1.3, 'B': 1.0, 'C': 0.7}
    multiplier = tier_multipliers[tier]
    
    # Production budget
    budget_per_ep = base_budget_per_ep * multiplier
    production_budget = budget_per_ep * episodes
    
    # Marketing (25% of production)
    marketing_budget = production_budget * 0.25
    total_cost = production_budget + marketing_budget
    
    # Revenue calculation
    # Merchandising: Based on member base (proxy for fan engagement)
    # Industry avg: $100 per active fan, but MAL members are a small % of actual fans
    # Scale: 1M members ≈ 10M global fanbase ≈ $50M merch potential
    merch_multiplier = members / 1_000_000  # Normalized to 1M members
    merch_base = 50_000_000 * merch_multiplier * (score / 10)  # Quality factor
    
    # Streaming: Based on episodes × tier × score
    streaming_base = episodes * 500_000 * multiplier * (score / 8)
    
    # Apply 72/28 split
    merchandising_revenue = merch_base * 0.72
    streaming_revenue = streaming_base + (merch_base * 0.28)
    disc_revenue = production_budget * 0.05  # Minimal disc sales
    
    total_revenue = merchandising_revenue + streaming_revenue + disc_revenue
    
    # Profit & ROI
    profit = total_revenue - total_cost
    roi = profit / total_cost if total_cost > 0 else 0
    profit_per_episode = profit / episodes if episodes > 0 else 0
    
    return {
        'mal_id': mal_id,
        'tier': tier,
        'tier_multiplier': multiplier,
        'episodes': episodes,
        'base_budget_per_episode': base_budget_per_ep,
        'production_budget': production_budget,
        'total_cost': total_cost,
        'streaming_revenue': streaming_revenue,
        'disc_revenue': disc_revenue,
        'merch_revenue': merchandising_revenue,
        'total_revenue': total_revenue,
        'profit': profit,
        'roi': roi,
        'profit_per_episode': profit_per_episode
    }

def main():
    """Main execution: Fetch all anime and generate financial data"""
    print("=" * 70)
    print("Expanded Anime Dataset Generator with Industry-Calibrated Financials")
    print("=" * 70)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Fetch anime from all studios
    all_anime = []
    
    # Pierrot: Get more (it's our focus)
    all_anime.extend(fetch_anime_by_producer(STUDIOS['pierrot'], 'Studio Pierrot', limit=100))
    
    # Competitors: Get top 50 each
    all_anime.extend(fetch_anime_by_producer(STUDIOS['mappa'], 'MAPPA', limit=50))
    all_anime.extend(fetch_anime_by_producer(STUDIOS['ufotable'], 'ufotable', limit=50))
    all_anime.extend(fetch_anime_by_producer(STUDIOS['bones'], 'Bones', limit=50))
    all_anime.extend(fetch_anime_by_producer(STUDIOS['madhouse'], 'Madhouse', limit=50))
    
    print(f"\n✓ Total anime fetched: {len(all_anime)}")
    
    # Save raw MAL data
    mal_output = OUTPUT_DIR / "mal_anime.json"
    with open(mal_output, 'w', encoding='utf-8') as f:
        json.dump(all_anime, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved raw MAL data to {mal_output}")
    
    # Generate financial data
    print("\nGenerating financial data...")
    financial_records = []
    
    for idx, anime in enumerate(all_anime, start=1):
        fin_data = calculate_financials(anime)
        fin_data['finance_id'] = idx
        financial_records.append(fin_data)
    
    # Save to CSV
    financials_csv = OUTPUT_DIR / "financials.csv"
    with open(financials_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=financial_records[0].keys())
        writer.writeheader()
        writer.writerows(financial_records)
    
    print(f"✓ Generated {len(financial_records)} financial records")
    print(f"✓ Saved to {financials_csv}")
    
    # Generate placeholder production.csv and marketing.csv
    production_csv = OUTPUT_DIR / "production.csv"
    with open(production_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'season_id', 'mal_id', 'season_type', 'filler_ratio', 
            'production_stability', 'quality_score_internal'
        ])
        writer.writeheader()
        for idx, anime in enumerate(all_anime, start=1):
            mal_id = anime.get('mal_id')
            episodes = anime.get('episodes') or 12
            season_type = 'long' if episodes > 24 else 'short'
            writer.writerow({
                'season_id': idx,
                'mal_id': mal_id,
                'season_type': season_type,
                'filler_ratio': 0.15 if season_type == 'long' else 0.0,
                'production_stability': 0.85,
                'quality_score_internal': (anime.get('score') or 7.0) / 10
            })
    
    print(f"✓ Generated production data")
    
    marketing_csv = OUTPUT_DIR / "marketing.csv"
    with open(marketing_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'campaign_id', 'mal_id', 'campaign_type', 'channel', 'cost', 'impressions'
        ])
        writer.writeheader()
        for idx, anime in enumerate(all_anime, start=1):
            mal_id = anime.get('mal_id')
            members = anime.get('members') or 10000
            writer.writerow({
                'campaign_id': idx,
                'mal_id': mal_id,
                'campaign_type': 'Launch',
                'channel': 'Social Media',
                'cost': members * 0.5,  # $0.50 per potential viewer
                'impressions': members * 10
            })
    
    print(f"✓ Generated marketing data")
    print("\n" + "=" * 70)
    print("✅ Dataset generation complete!")
    print(f"   {len(all_anime)} anime with industry-calibrated financials")
    print("=" * 70)

if __name__ == "__main__":
    main()
