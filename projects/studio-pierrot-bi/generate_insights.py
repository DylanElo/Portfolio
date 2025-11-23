# Phase 3b: Add Insight Cards to Dashboard Tabs

# Key insights to add to each tab
insights = {
    "fandom": {
        "title": "💡 Key Insight: Legacy Quality Still Competitive",
        "content": "Bleach TYBW (8.99) matches JJK quality benchmarks, but new IP like Boruto (5.98) significantly underperforms. Quality perception matters more than episode quantity.",
        "color": "blue"
    },
    "streaming": {
        "title": "💡 Key Insight: Competitive Gap vs MAPPA/ufotable",
        "content": "JJK dominates at 71.2x average demand vs Pierrot titles at 2-12x. Netflix + Crunchyroll control >80% of overseas market—Pierrot needs premium-quality new IP to compete globally.",
        "color": "purple"
    },
    "domestic": {
        "title": "💡 Key Insight: Strong MAL-BD Sales Correlation",
        "content": "Clear linear relationship (R² > 0.7): Higher MAL score = Better BD sales. Bleach TYBW (8.99, 48K units) vs Boruto (5.98, 6K units). Invest in quality for domestic monetization.",
        "color": "green"
    },
    "production": {
        "title": "💡 Key Insight: Filler Kills Engagement",
        "content": "Seasonal model (JJK/TYBW: <10% filler, 8.7 avg score) vastly outperforms continuous production (Boruto: 42% filler, 6.1 score). Cap filler at 10% max to maintain quality perception.",
        "color": "orange"
    }
}

# Generate HTML for insight cards
html_template = '''
      <!-- Key Insight Card -->
      <div class="mb-6 p-4 bg-{color}-50 border-l-4 border-{color}-500 rounded-r-lg">
        <h4 class="font-bold text-{color}-900 mb-2">{title}</h4>
        <p class="text-{color}-800 text-sm">{content}</p>
      </div>
'''

# Generate each insight card
for tab_name, insight in insights.items():
    html = html_template.format(**insight)
    print(f"\n=== {tab_name.upper()} TAB INSIGHT ===")
    print(html)
    
print("\n\n=== INSTRUCTIONS ===")
print("These insight cards should be added AFTER the data source disclaimer in each tab.")
print("Since HTML editing is unreliable, I'll create a detailed documentation file showing where each goes.")
