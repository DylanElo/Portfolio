"""
Generate simulated financial data for Studio Pierrot anime.
Creates production costs, marketing costs, and estimated revenue.
"""
import json
import csv
import random
from pathlib import Path

def load_mal_data():
    """Load fetched MAL anime data."""
    data_file = Path(__file__).parent.parent / "data" / "raw" / "mal_anime.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_marketing_data():
    """Load marketing campaign data to calculate total marketing costs."""
    marketing_file = Path(__file__).parent.parent / "data" / "raw" / "marketing.csv"
    marketing_costs = {}
    
    with open(marketing_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mal_id = int(row["mal_id"])
            cost = float(row["cost"])
            if mal_id not in marketing_costs:
                marketing_costs[mal_id] = 0
            marketing_costs[mal_id] += cost
    
    return marketing_costs

def generate_financial_data(anime_data, marketing_costs):
    """Generate financial data for each anime."""
    
    financial_data = []
    financial_id = 1
    
    for anime in anime_data:
        mal_id = anime.get("mal_id")
        title = anime.get("title", "")
        episodes = anime.get("episodes", 0)
        members = anime.get("members", 0)
        score = anime.get("score", 0)
        year = anime.get("year")
        studios = anime.get("studios", [])
        
        # Determine if Studio Pierrot
        is_pierrot = any("Pierrot" in s.get("name", "") for s in studios)
        
        # Production cost estimation
        if episodes and episodes > 0:
            # Cost per episode varies by era and series type
            if year:
                if year < 2005:
                    cost_per_ep = random.uniform(80000, 120000)  # Older, cheaper
                elif year < 2015:
                    cost_per_ep = random.uniform(100000, 150000)
                else:
                    cost_per_ep = random.uniform(150000, 300000)  # Modern, expensive
            else:
                cost_per_ep = random.uniform(100000, 200000)
            
            # Long-running shows have economies of scale
            if episodes >= 100:
                cost_per_ep *= random.uniform(0.7, 0.9)
            
            production_cost = episodes * cost_per_ep
        else:
            production_cost = random.uniform(1000000, 5000000)
        
        # Marketing cost from generated data
        marketing_cost = marketing_costs.get(mal_id, 0)
        
        # Revenue estimation (multiple streams)
        # Based on members (proxy for viewership), score (merchandising potential), episodes
        
        # Streaming rights revenue
        if members > 1000000:
            streaming_revenue = random.uniform(5000000, 15000000)
        elif members > 500000:
            streaming_revenue = random.uniform(2000000, 7000000)
        elif members > 100000:
            streaming_revenue = random.uniform(500000, 3000000)
        else:
            streaming_revenue = random.uniform(100000, 800000)
        
        # Merchandise revenue (higher for popular, high-scoring shows)
        if score and score >= 8.5 and members > 1000000:
            merch_revenue = random.uniform(10000000, 50000000)  # Huge hits like Naruto
        elif score and score >= 8.0 and members > 500000:
            merch_revenue = random.uniform(3000000, 15000000)
        elif score and score >= 7.5:
            merch_revenue = random.uniform(500000, 5000000)
        else:
            merch_revenue = random.uniform(100000, 2000000)
        
        # Licensing and international rights
        licensing_revenue = streaming_revenue * random.uniform(0.3, 0.7)
        
        # Home video / DVD/Blu-ray (declining over time)
        if year and year < 2010:
            home_video_revenue = random.uniform(1000000, 5000000)
        elif year and year < 2015:
            home_video_revenue = random.uniform(500000, 2000000)
        else:
            home_video_revenue = random.uniform(100000, 800000)
        
        # Total estimated revenue
        estimated_revenue = (
            streaming_revenue +
            merch_revenue +
            licensing_revenue +
            home_video_revenue
        )
        
        # Add some variance
        estimated_revenue *= random.uniform(0.9, 1.1)
        
        financial_data.append({
            "financial_id": financial_id,
            "mal_id": mal_id,
            "title": title,
            "production_cost": round(production_cost, 2),
            "marketing_cost": round(marketing_cost, 2),
            "estimated_revenue": round(estimated_revenue, 2)
        })
        
        financial_id += 1
    
    return financial_data

def main():
    """Main process to generate financial data."""
    print("=" * 60)
    print("Studio Pierrot Anime BI - Financial Data Generator")
    print("=" * 60)
    print()
    
    # Load data
    anime_data = load_mal_data()
    print(f"✓ Loaded {len(anime_data)} anime records")
    
    marketing_costs = load_marketing_data()
    print(f"✓ Loaded marketing costs for {len(marketing_costs)} anime")
    
    # Generate financial data
    financial_data = generate_financial_data(anime_data, marketing_costs)
    print(f"✓ Generated financial data for {len(financial_data)} anime")
    
    # Save to CSV
    output_dir = Path(__file__).parent.parent / "data" / "raw"
    output_file = output_dir / "financials.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "financial_id", "mal_id", "title", "production_cost",
            "marketing_cost", "estimated_revenue"
        ])
        writer.writeheader()
        writer.writerows(financial_data)
    
    print(f"✓ Saved to {output_file}")
    print()
    
    # Summary stats
    total_production = sum(f["production_cost"] for f in financial_data)
    total_marketing = sum(f["marketing_cost"] for f in financial_data)
    total_revenue = sum(f["estimated_revenue"] for f in financial_data)
    total_profit = total_revenue - total_production - total_marketing
    
    print("=" * 60)
    print("Financial Summary:")
    print("=" * 60)
    print(f"Total production costs:  ${total_production:>15,.2f}")
    print(f"Total marketing costs:   ${total_marketing:>15,.2f}")
    print(f"Total estimated revenue: ${total_revenue:>15,.2f}")
    print(f"Estimated profit:        ${total_profit:>15,.2f}")
    print(f"ROI:                     {(total_profit/( total_production+total_marketing)*100):>14.1f}%")
    print()
    print("Top 5 anime by estimated profit:")
    sorted_financials = sorted(financial_data, key=lambda x: x["estimated_revenue"] - x["production_cost"] - x["marketing_cost"], reverse=True)
    for i, row in enumerate(sorted_financials[:5], 1):
        profit = row["estimated_revenue"] - row["production_cost"] - row["marketing_cost"]
        print(f"{i}. {row['title'][:35]:35} | Profit: ${profit:>12,.0f}")

if __name__ == "__main__":
    main()
