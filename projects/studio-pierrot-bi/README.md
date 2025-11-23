# Studio Pierrot BI Analysis

> **Project Context:** I am acting as a BI Analyst at Studio Pierrot Japan, tasked with answering a critical strategic question: *Why are our flagship IPs (Naruto, Bleach, Tokyo Ghoul, Black Clover) struggling to capture the same global momentum as newer titles like Jujutsu Kaisen (MAPPA), Demon Slayer (ufotable), and Attack on Titan—and what should we do about it?*

This project simulates a real-world Business Intelligence environment where I combine **domestic (Japan), international (streaming), and global fandom data** to provide actionable recommendations to studio leadership.

---

## 🎯 Business Objective

Studio Pierrot has dominated anime for decades with legendary franchises. However, the industry landscape has shifted:
- **Netflix reports 4.4 billion hours of anime watched in H1 2025 alone**, with over 50% of subscribers watching anime
- **Jujutsu Kaisen (MAPPA)** was named the "Most in-demand TV series in the world" in 2023, at **71.2x** the average demand
- **Streaming is projected to grow from $3.7B (2023) to $12.5B (2030)**, with Netflix + Crunchyroll controlling ~80% of the market

Meanwhile, Pierrot's newer titles (Boruto, Tokyo Ghoul:re) face criticism for:
- Long-running formats with high filler percentages
- Inconsistent production quality
- Lower engagement compared to "new wave" anime

**The Question:** How do we compete in this new era?

---

## 📊 Data Architecture

This project uses a **three-lens approach** to simulate a comprehensive BI environment:

### 1️⃣ Global Fandom Lens (Real Data)
**Source:** [Jikan API](https://jikan.moe/) (MyAnimeList public data)

Live metrics for understanding international fan sentiment:
- **Score:** Critical reception (0-10 scale)
- **Members:** Total audience reach
- **Favorites:** Core fanbase engagement
- **Popularity Rank:** Relative demand

**Limitation:** MAL has a Western/international bias and doesn't fully represent Japanese domestic audience preferences.

**ETL Process:**
- Script: `etl/fetch_data.js`
- Output: `dashboard/data.js`

### 2️⃣ International Streaming Lens (Modeled)
**Simulated based on industry reports:**
- Netflix viewership patterns (e.g., Naruto Shippuden = #1 anime in 2025)
- Crunchyroll/HBO Max demand analytics
- Regional streaming revenue breakdown (North America, Europe, Asia-Pacific)

**Key Insight:** Legacy Pierrot IPs (Naruto, Bleach) still dominate Netflix, but new titles struggle to compete with MAPPA/ufotable quality perception.

### 3️⃣ Domestic (Japan) Lens (Modeled)
**Simulated based on industry standards:**
- TV Tokyo broadcast ratings
- Blu-ray/DVD sales (Oricon rankings)
- Merchandise and licensing revenue
- Production costs (per episode, based on animation quality tiers)

**Why Simulate?** Private studio financials are not publicly available, but we can model realistic scenarios using:
- Industry benchmarks (e.g., ~$34B global anime market in 2024)
- Known patterns (late-night vs prime-time slots, filler impact on BD sales)

---

## 🗂️ Project Structure

```text
/
├── dashboard/          # Interactive Dashboard (Phase 1: Live MAL Data)
│   ├── index.html      # Dashboard UI
│   ├── dashboard.js    # Chart.js logic & Data binding
│   └── data.js         # Auto-generated from Jikan API
├── docs/               # Strategic Documentation (Google BI Framework)
│   ├── executive_requirements.md    # High-level business goals
│   ├── stakeholder_requirements.md  # Production, Marketing, Finance needs
│   └── strategy_document.md         # BI implementation roadmap
├── etl/                # Data Pipeline
│   └── fetch_data.js   # Node.js script to fetch Jikan data
├── ROADMAP_PHASE_2.md  # Future vision: Full 3-lens integration
└── README.md           # This file
```

---

## 🔍 Current State (Phase 1)

**What's Live:**
- ✅ Real-time MAL metrics for 12 Studio Pierrot titles
- ✅ KPI cards: Top Rated, Most Popular, Fan Favorite
- ✅ Charts: Critical Reception (Score), Popularity vs Engagement
- ✅ Detailed metrics table with sortable data

**What's Acknowledged:**
- ⚠️ MAL data alone is insufficient for strategic decisions
- ⚠️ Financial metrics (Revenue, ROI) referenced in case study are **simulated** for demonstration purposes
- ⚠️ Domestic (Japan) data is not yet integrated

**Dashboard Disclaimer:**
The live dashboard clearly states: *"Public metrics (Score, Members, Favorites) are fetched live from the Jikan API. Financial data (Revenue, ROI) referenced in the case study is simulated for demonstration purposes."*

---

## 🚀 Key Findings (Phase 1 - Global Fandom Lens)

Based on MAL data analysis:

1. **Legacy Dominance:** Naruto Shippuden (8.28) and Bleach: TYBW (8.99) score highest, showing enduring quality
2. **New Title Struggles:** Boruto (5.98) and Tokyo Ghoul √A (7.03) significantly underperform
3. **Engagement Gaps:** Top legacy titles have 2.6M+ members, while newer titles plateau at <1M

**Strategic Implication:** Pierrot's legacy IP remains strong, but new IP development is failing to match competitor standards (JJK = 8.6+, Demon Slayer = 8.7+).

---

## 🛠️ How to Run

1. **View the Dashboard:** Open `dashboard/index.html` or visit the [live deployment](https://dylanelo.github.io/Portfolio/projects/studio-pierrot-bi/dashboard/index.html)
2. **Run ETL Pipeline:**
   ```bash
   node etl/fetch_data.js
   ```
   *Requires Node.js 16+*

---

## 🗺️ Next Steps (Phase 2)

See [ROADMAP_PHASE_2.md](./ROADMAP_PHASE_2.md) for the full vision of integrating:
- Streaming platform analytics (Netflix, Crunchyroll market share)
- Domestic TV ratings and merchandise data
- Production quality metrics (filler %, animation budget tiers)
- Multi-lens dashboards for holistic decision-making

---

## 📚 References

- [Netflix Anime Statistics (2025)](https://www.gamesradar.com/entertainment/anime-shows/)
- [Jujutsu Kaisen Global Demand Analysis](https://www.parrotanalytics.com/announcements/)
- [Anime Streaming Market Projections](https://www.parrotanalytics.com/press/)
- [Grand View Research: Anime Market Report (2030)](https://www.grandviewresearch.com/industry-analysis/anime-market)
