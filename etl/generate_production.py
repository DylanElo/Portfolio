"""
Generate simulated production metrics for Studio Pierrot anime.
Creates production quality, stability, and filler data based on realistic assumptions.
"""
import json
import csv
import random
from pathlib import Path
from datetime import datetime

def load_mal_data():
    """Load fetched MAL anime data."""
    data_file = Path(__file__).parent.parent / "data" / "raw" / "mal_anime.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_production_metrics(anime_data):
    """Generate production metrics for each anime."""
    
    # Known filler ratios (from fan wikis and research)
    FILLER_RATIOS = {
        "Naruto": 0.41,  # ~41% filler
        "Naruto: Shippuuden": 0.44,
        "Bleach": 0.45,
        "Boruto": 0.51,  # Higher filler in recent shows
        "Tokyo Ghoul": 0.15,  # Short season, less filler
        "Tokyo Ghoul:re": 0.20,
        "Black Clover": 0.12,  # Different strategy
        "Yuu": 0.10,  # Classic, minimal filler
        "Kingdom": 0.08,
        "Hunter x Hunter": 0.08,  # Known for low filler
        "Monster": 0.02,
        "Shingeki no Kyojin": 0.05,
        "Bleach: Sennen": 0.01,  # New, faithful adaptation
        "Gintama": 0.06,  # Mostly canon
        "Jujutsu Kaisen": 0.00,  # Seasonal, faithful
        "One Piece": 0.09,  # Low filler count but slow pacing
        "Boku no Hero Academia": 0.05,  # Occasional recap/original
        "Chainsaw Man": 0.00,
        "Kimetsu no Yaiba": 0.00,
    }
    
    production_data = []
    season_id = 1
    
    for anime in anime_data:
        mal_id = anime.get("mal_id")
        title = anime.get("title", "")
        episodes = anime.get("episodes", 0)
        studios = anime.get("studios", [])
        year = anime.get("year")
        
        # Determine Studio Pierrot
        is_pierrot = any("Pierrot" in s.get("name", "") for s in studios)
        
        # Determine filler ratio
        filler_ratio = 0.0
        for key in FILLER_RATIOS:
            if key.lower() in title.lower():
                filler_ratio = FILLER_RATIOS[key]
                break
        
        # If not found, estimate based on episode count and year
        if filler_ratio == 0.0:
            if episodes and episodes > 100:
                filler_ratio = random.uniform(0.35, 0.50) if is_pierrot else random.uniform(0.20, 0.35)
            elif episodes and episodes > 50:
                filler_ratio = random.uniform(0.20, 0.35) if is_pierrot else random.uniform(0.10, 0.25)
            else:
                filler_ratio = random.uniform(0.05, 0.15)
        
        # Determine season type
        season_type = "long" if episodes and episodes >= 100 else "short"
        
        # Production stability (older shows had more stable production)
        if year:
            if year < 2010:
                production_stability = random.uniform(0.70, 0.90)
            elif year < 2015:
                production_stability = random.uniform(0.60, 0.80)
            else:
                production_stability = random.uniform(0.50, 0.75) if is_pierrot else random.uniform(0.65, 0.85)
        else:
            production_stability = random.uniform(0.60, 0.80)
        
        # Quality score internal (correlated with MAL score but with variance)
        mal_score = anime.get("score", 7.0)
        if mal_score:
            quality_score_internal = max(0, min(10, mal_score + random.uniform(-0.5, 0.5)))
        else:
            quality_score_internal = random.uniform(6.0, 8.0)
        
        production_data.append({
            "season_id": season_id,
            "mal_id": mal_id,
            "title": title,
            "season_type": season_type,
            "filler_ratio": round(filler_ratio, 3),
            "production_stability": round(production_stability, 3),
            "quality_score_internal": round(quality_score_internal, 2)
        })
        
        season_id += 1
    
    return production_data

def main():
    """Main process to generate production metrics."""
    print("=" * 60)
    print("Studio Pierrot Anime BI - Production Metrics Generator")
    print("=" * 60)
    print()
    
    # Load MAL data
    anime_data = load_mal_data()
    print(f"✓ Loaded {len(anime_data)} anime records")
    
    # Generate production metrics
    production_data = generate_production_metrics(anime_data)
    print(f"✓ Generated production metrics for {len(production_data)} anime")
    
    # Save to CSV
    output_dir = Path(__file__).parent.parent / "data" / "raw"
    output_file = output_dir / "production.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "season_id", "mal_id", "title", "season_type", 
            "filler_ratio", "production_stability", "quality_score_internal"
        ])
        writer.writeheader()
        writer.writerows(production_data)
    
    print(f"✓ Saved to {output_file}")
    print()
    print("=" * 60)
    print("Sample production metrics:")
    print("=" * 60)
    for row in production_data[:5]:
        print(f"{row['title'][:30]:30} | Type: {row['season_type']:5} | Filler: {row['filler_ratio']:.2%} | Stability: {row['production_stability']:.2f} | Quality: {row['quality_score_internal']:.1f}")

if __name__ == "__main__":
    main()
