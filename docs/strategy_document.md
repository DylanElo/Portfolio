# 3️⃣ Strategy Document

**(The bridge between "we have a problem" and "here is how we address it with data")**

**Project**: Performance Analysis Strategy for Recent Anime
**BI Lead**: Dylan Elo

## 1. Vision

Establish a foundational analytical framework allowing the studio to understand what drives the success or failure of its recent anime, and reuse this framework for future projects.

## 2. General Approach

### Understand Business Needs
*   Collect questions from stakeholders (production, marketing, management).
*   Reformulate them into analytical questions and KPIs.

### Design Data Model
Structure data around:
*   A **Dim_Anime** table (general info),
*   Fact tables (**Fact_Rating**, **Fact_Audience**, **Fact_Sentiment**, **Fact_Production**).

### Build the Pipeline
*   Public data collection (scraping/API).
*   Cleaning, joining, and metric calculation (Python/SQL).
*   Export to a clean model (CSV / SQL database).

### Develop the Dashboard
*   1 Executive page + 1 Detail page per anime.
*   Simple filters (Legacy vs. Recent, Genre, Series Type).

### Synthesis & Recommendations
*   Interpretation of results.
*   Concrete proposals for the production & marketing roadmap.

## 3. Data & Sources

**Public Sources:**
*   Ratings, votes, genres, broadcast years.
*   Comments / reviews for sentiment.

**Simulated Data:**
*   Category Budget (Low / Medium / High).
*   Production Issues (Delay, Staff Change, Rush).
*   Marketing Intensity (Low / Medium / High).

*Note: These data points are used as realistic proxies for a BI exercise.*

### ROI Modeling Approach (Finance Lens)
> ROI Modeling Approach
> – True per-title budgets & revenues are not public.
> – I use real fandom data (MAL score + members) to estimate demand.
> – Production costs are modeled via tiers (S/A/B/C) and episodes.
> – Revenues are modeled via streaming, discs, and merch with transparent rules calibrated to public industry ranges.
> – ROI, profit per episode, and other KPIs are computed from this model and used only as directional indicators for strategic decisions.

## 4. Tools & Stack

*   **Collection / Transformation**: Python + Pandas / SQL.
*   **Storage**: SQLite.
*   **Visualization**: Chart.js (Custom Web Dashboard).
*   **Documentation**: GitHub README + Google Docs/Slides for the business part.

## 5. Roadmap (Simple)

**Week 1:**
*   Finalize Stakeholder + Executive + Strategy docs.
*   Select 4–6 target anime.
*   Collect raw data.

**Week 2:**
*   Cleaning + Data Model construction.
*   KPI creation.

**Week 3:**
*   Dashboard construction.
*   Drafting insights + recommendations.

**Week 4 (Optional – Portfolio Polish):**
*   Screenshots, clean README, "Case Study" style presentation.
