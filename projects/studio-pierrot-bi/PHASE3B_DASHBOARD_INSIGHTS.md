# Phase 3b Dashboard Enhancement - Manual Implementation Guide

Given HTML editing reliability issues, this document provides the exact HTML to add to each tab for insight cards.

## Implementation Steps

For each tab, add the insight card HTML IMMEDIATELY AFTER the data source disclaimer div and BEFORE the content (KPI cards/charts).

---

## Tab 1: Global Fandom
**Location:** After line ~120 (after data source div, before KPI cards)

```html
<!-- Key Insight Card -->
<div class="mb-6 p-4 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
  <h4 class="font-bold text-blue-900 mb-2">💡 Key Insight: Legacy Quality Still Competitive</h4>
  <p class="text-blue-800 text-sm">Bleach TYBW (8.99) matches JJK quality benchmarks, but new IP like Boruto (5.98) significantly underperforms. Quality perception matters more than episode quantity.</p>
</div>
```

---

## Tab 2: Streaming Analytics
**Location:** After line ~234 (after data source div, before charts)

```html
<!-- Key Insight Card -->
<div class="mb-6 p-4 bg-purple-50 border-l-4 border-purple-500 rounded-r-lg">
  <h4 class="font-bold text-purple-900 mb-2">💡 Key Insight: Competitive Gap vs MAPPA/ufotable</h4>
  <p class="text-purple-800 text-sm">JJK dominates at 71.2x average demand vs Pierrot titles at 2-12x. Netflix + Crunchyroll control >80% of overseas market—Pierrot needs premium-quality new IP to compete globally.</p>
</div>
```

---

## Tab 3: Domestic (Japan)
**Location:** After line ~257 (after data source div, before charts)

```html
<!-- Key Insight Card -->
<div class="mb-6 p-4 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
  <h4 class="font-bold text-green-900 mb-2">💡 Key Insight: Strong MAL-BD Sales Correlation</h4>
  <p class="text-green-800 text-sm">Clear linear relationship (R² > 0.7): Higher MAL score = Better BD sales. Bleach TYBW (8.99, 48K units) vs Boruto (5.98, 6K units). Invest in quality for domestic monetization.</p>
</div>
```

---

## Tab 4: Production Insights
**Location:** After line ~280 (after data source div, before charts)

```html
<!-- Key Insight Card -->
<div class="mb-6 p-4 bg-orange-50 border-l-4 border-orange-500 rounded-r-lg">
  <h4 class="font-bold text-orange-900 mb-2">💡 Key Insight: Filler Kills Engagement</h4>
  <p class="text-orange-800 text-sm">Seasonal model (JJK/TYBW: <10% filler, 8.7 avg score) vastly outperforms continuous production (Boruto: 42% filler, 6.1 score). Cap filler at 10% max to maintain quality perception.</p>
</div>
```

---

## Alternative: JavaScript Implementation

If manual HTML editing is too fragile, add these insights via JavaScript in `dashboard.js`:

```javascript
// Add insight cards dynamically
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
    
    // Insert after first child (data source disclaimer)
    const firstChild = tab.querySelector('.mb-6');
    if (firstChild && firstChild.nextSibling) {
      tab.insertBefore(insightCard, firstChild.nextSibling);
    }
  });
}

// Call on DOMContentLoaded
document.addEventListener('DOMContentLoaded', addInsightCards);
```

---

## Strategic Value

These insight cards transform the dashboard from "here's some data" to "here's what the data means for Pierrot's strategy":

1. **Fandom Tab:** Legacy IP competitive on quality, new IP fails
2. **Streaming Tab:** Competitive gap vs JJK/Demon Slayer
3. **Domestic Tab:** Quality directly drives monetization  
4. **Production Tab:** Filler percentage kills engagement

Each insight directly answers a Studio Pierrot executive question with data evidence.
