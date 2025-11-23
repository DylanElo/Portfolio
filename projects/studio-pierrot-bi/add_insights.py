"""
Phase 3b: Add Insight Cards to Dashboard
Injects the insight card function into dashboard.js safely
"""

def add_insights_to_dashboard():
    dashboard_js_path = 'dashboard/dashboard.js'
    
    # Read the current file
    with open(dashboard_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The function to add
    insights_function = '''
// Add insight cards to dashboard tabs (Phase 3b)
function addInsightCards() {
    const insights = {
        'content-fandom': {
            title: '💡 Key Insight: Legacy Quality Still Competitive',
            content: 'Bleach TYBW (8.99) matches JJK quality benchmarks, but new IP like Boruto (5.98) significantly underperforms. Quality perception matters more than episode quantity.',
            color: 'blue'
        },
        'content-streaming': {
            title: '💡 Key Insight: Competitive Gap vs MAPPA/ufotable',
            content: 'JJK dominates at 71.2x average demand vs Pierrot titles at 2-12x. Netflix + Crunchyroll control >80% of overseas market—Pierrot needs premium-quality new IP to compete globally.',
            color: 'purple'
        },
        'content-domestic': {
            title: '💡 Key Insight: Strong MAL-BD Sales Correlation',
            content: 'Clear linear relationship (R² > 0.7): Higher MAL score = Better BD sales. Bleach TYBW (8.99, 48K units) vs Boruto (5.98, 6K units). Invest in quality for domestic monetization.',
            color: 'green'
        },
        'content-production': {
            title: '💡 Key Insight: Filler Kills Engagement',
            content: 'Seasonal model (JJK/TYBW: <10% filler, 8.7 avg score) vastly outperforms continuous production (Boruto: 42% filler, 6.1 score). Cap filler at 10% max to maintain quality perception.',
            color: 'orange'
        }
    };

    Object.keys(insights).forEach(tabId => {
        const tab = document.getElementById(tabId);
        if (!tab) return;
        
        const insight = insights[tabId];
        const insightCard = document.createElement('div');
        insightCard.className = `mb-6 p-4 bg-${insight.color}-50 border-l-4 border-${insight.color}-500 rounded-r-lg`;
        insightCard.innerHTML = `
            <h4 class="font-bold text-${insight.color}-900 mb-2">${insight.title}</h4>
            <p class="text-${insight.color}-800 text-sm">${insight.content}</p>
        `;
        
        // Insert after first disclaimer div
        const firstDiv = tab.querySelector('.mb-6');
        if (firstDiv && firstDiv.nextElementSibling) {
            tab.insertBefore(insightCard, firstDiv.nextElementSibling);
        } else if (firstDiv) {
            firstDiv.after(insightCard);
        }
    });
    
    console.log('Strategic insight cards added to all tabs');
}
'''
    
    # Find where to insert (after initPhase1Dashboard function call in DOMContentLoaded)
    insert_marker = "initPhase1Dashboard();"
    
    if insert_marker in content:
        # Add the call to addInsightCards
        content = content.replace(
            insert_marker,
            insert_marker + "\n    addInsightCards(); // Phase 3b: Add strategic insights"
        )
        
        # Add the function definition before the initPhase1Dashboard function
        init_function_marker = "function initPhase1Dashboard()"
        if init_function_marker in content:
            content = content.replace(
                init_function_marker,
                insights_function + "\n\n" + init_function_marker
            )
            
            # Write back
            with open(dashboard_js_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Successfully added insight cards function to dashboard.js")
            print("   - addInsightCards() function defined")
            print("   - Called in DOMContentLoaded after initPhase1Dashboard()")
            return True
        else:
            print("❌ Could not find initPhase1Dashboard function")
            return False
    else:
        print("❌ Could not find insert marker")
        return False

if __name__ == '__main__':
    success = add_insights_to_dashboard()
    exit(0 if success else 1)
