"""
Generate deterministic ROI-ready financial data for Studio Pierrot anime.

This module applies a transparent tiered cost/revenue model using
MyAnimeList (MAL) popularity metrics as the demand signal.
"""
import csv
import json
from pathlib import Path

BASE_BUDGET_PER_EPISODE = 100_000
STREAMING_RATE_PER_INDEX = 150_000
DISC_PRICE = 60
TIER_MULTIPLIERS = {"S": 1.6, "A": 1.3, "B": 1.0, "C": 0.7}
DISC_UNITS_BY_TIER = {"S": 25_000, "A": 10_000, "B": 4_000, "C": 1_500}
MERCH_FACTOR_BY_TIER = {"S": 0.9, "A": 0.6, "B": 0.3, "C": 0.1}


def load_mal_data():
    """Load fetched MAL anime data."""
    data_file = Path(__file__).parent.parent / "data" / "raw" / "mal_anime.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def determine_tier(score: float, members: int) -> str:
    """Return S/A/B/C tier based on MAL score and membership counts."""

    if score >= 8.5 and members >= 1_000_000:
        return "S"
    if score >= 8.0 and members >= 300_000:
        return "A"
    if score >= 7.0:
        return "B"
    return "C"


def calculate_budget(episodes: int, tier: str) -> tuple[float, float]:
    """Calculate production budget and total cost for the series."""

    tier_multiplier = TIER_MULTIPLIERS.get(tier, 1.0)
    production_budget = episodes * BASE_BUDGET_PER_EPISODE * tier_multiplier
    total_cost = production_budget  # marketing could be layered on later
    return production_budget, total_cost


def calculate_revenue(score: float, members: int, tier: str) -> tuple[float, float, float, float]:
    """Calculate revenue components based on the ROI model."""

    global_fandom_index = members / 100_000
    streaming_revenue = global_fandom_index * STREAMING_RATE_PER_INDEX

    disc_units = DISC_UNITS_BY_TIER.get(tier, 1_500)
    if score >= 9.0:
        disc_units *= 1.1  # modest lift for standout hits
    disc_revenue = disc_units * DISC_PRICE

    merch_factor = MERCH_FACTOR_BY_TIER.get(tier, 0.1)
    merch_revenue = streaming_revenue * merch_factor

    total_revenue = streaming_revenue + disc_revenue + merch_revenue
    return streaming_revenue, disc_revenue, merch_revenue, total_revenue


def generate_financial_data(anime_data):
    """Generate finance metrics for each anime using deterministic rules."""

    financial_data = []
    finance_id = 1

    for anime in anime_data:
        mal_id = anime.get("mal_id")
        title = anime.get("title", "")
        episodes = anime.get("episodes") or 12  # default to a single cour when missing
        members = anime.get("members") or 0
        score = anime.get("score") or 0

        tier = determine_tier(score, members)
        production_budget, total_cost = calculate_budget(episodes, tier)
        streaming_revenue, disc_revenue, merch_revenue, total_revenue = calculate_revenue(score, members, tier)

        profit = total_revenue - total_cost
        roi = profit / total_cost if total_cost else 0
        profit_per_episode = profit / episodes if episodes else 0

        financial_data.append({
            "finance_id": finance_id,
            "mal_id": mal_id,
            "title": title,
            "tier": tier,
            "tier_multiplier": TIER_MULTIPLIERS[tier],
            "episodes": episodes,
            "base_budget_per_episode": BASE_BUDGET_PER_EPISODE,
            "production_budget": round(production_budget, 2),
            "total_cost": round(total_cost, 2),
            "streaming_revenue": round(streaming_revenue, 2),
            "disc_revenue": round(disc_revenue, 2),
            "merch_revenue": round(merch_revenue, 2),
            "total_revenue": round(total_revenue, 2),
            "profit": round(profit, 2),
            "roi": round(roi, 4),
            "profit_per_episode": round(profit_per_episode, 2),
        })

        finance_id += 1

    return financial_data

def main():
    """Main process to generate financial data."""
    print("=" * 60)
    print("Studio Pierrot Anime BI - ROI Financial Data Generator")
    print("=" * 60)
    print()

    # Load data
    anime_data = load_mal_data()
    print(f"✓ Loaded {len(anime_data)} anime records")

    # Generate financial data
    financial_data = generate_financial_data(anime_data)
    print(f"✓ Generated financial data for {len(financial_data)} anime")

    # Save to CSV
    output_dir = Path(__file__).parent.parent / "data" / "raw"
    output_file = output_dir / "financials.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "finance_id",
            "mal_id",
            "title",
            "tier",
            "tier_multiplier",
            "episodes",
            "base_budget_per_episode",
            "production_budget",
            "total_cost",
            "streaming_revenue",
            "disc_revenue",
            "merch_revenue",
            "total_revenue",
            "profit",
            "roi",
            "profit_per_episode",
        ])
        writer.writeheader()
        writer.writerows(financial_data)

    print(f"✓ Saved to {output_file}")
    print()

    # Summary stats
    total_production = sum(f["production_budget"] for f in financial_data)
    total_revenue = sum(f["total_revenue"] for f in financial_data)
    total_profit = total_revenue - total_production

    print("=" * 60)
    print("Financial Summary:")
    print("=" * 60)
    print(f"Total production costs:  ${total_production:>15,.2f}")
    print(f"Total estimated revenue: ${total_revenue:>15,.2f}")
    print(f"Estimated profit:        ${total_profit:>15,.2f}")
    roi_pct = (total_profit / total_production * 100) if total_production else 0
    print(f"ROI:                     {roi_pct:>14.1f}%")
    print()
    print("Top 5 anime by estimated profit:")
    sorted_financials = sorted(financial_data, key=lambda x: x["profit"], reverse=True)
    for i, row in enumerate(sorted_financials[:5], 1):
        profit = row["profit"]
        print(f"{i}. {row['title'][:35]:35} | Profit: ${profit:>12,.0f} | ROI: {row['roi']*100:>6.1f}%")

if __name__ == "__main__":
    main()
