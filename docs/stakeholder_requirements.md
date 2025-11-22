# 1️⃣ Stakeholder Requirements Document

**Project**: Performance Diagnostic of Recent Studio Pierrot Anime
**Role**: BI Analyst
**Date**: 2024-11-22

## 1. Context

Studio Pierrot is noticing a performance decline in several recent anime titles (viewership, ratings, fan perception) compared to its historical franchises (e.g., Naruto Shippuden, Bleach).
Management wants to understand what is no longer working and identify concrete levers to improve the performance of future projects.

## 2. Business Objectives (High Level)

*   Identify key factors associated with the underperformance of recent anime (content, format, production, marketing, broadcasting, etc.).
*   Compare the performance of new titles with that of the studio's historical franchises.
*   Prioritize 3–5 actionable recommendations for future projects (format, episode count, filler management, visual quality, etc.).
*   Provide a simple dashboard allowing business teams to track these indicators over time.

## 3. Key Stakeholders

| Stakeholder | Role / Function | Main Interest |
| :--- | :--- | :--- |
| **Production Director** | Supervises all anime | Understanding the impact of planning & fillers |
| **Executive Producer** | Responsible for major IPs | Protecting IP value, arbitrating investments |
| **Marketing Manager** | Manages promo & campaigns | Optimizing campaigns based on series potential |
| **Broadcasting Manager** | Manages schedules / channels / platforms | Maximizing viewership by slot & platform |
| **Finance / Management** | Global profitability vision | Deciding where to invest, stop, or pivot projects |
| **BI / Data Team Lead** | Leads the data project | Ensuring KPIs are reliable and reusable |

## 4. Needs by Stakeholder

### Production Director

**Questions:**
*   Which recent anime have the steepest viewership drop-off per episode?
*   Is there a correlation between % of filler episodes and a drop in ratings/fan sentiment?
*   Do staff changes or planning issues (rush) impact fan perception?

**Needs:**
*   View comparing performance of recent vs. legacy anime.
*   KPIs: Drop-off per episode, % fillers, "production stability index".
*   Drilldown by series / episode.

### Marketing Manager

**Questions:**
*   Which anime generate the most positive buzz vs. bad buzz?
*   Which campaigns (teasers, collabs, OP/ED) are associated with good performance?
*   Which audience segments (youth, legacy fans, platforms) react best?

**Needs:**
*   KPIs: Sentiment score, comment volume, evolution before / during / after broadcast.
*   Segmentation by series, period, campaign type.

### Broadcasting Manager

**Questions:**
*   Which time slots / broadcast seasons produce the best audience retention?
*   Do recent anime suffer from stronger competition in certain slots?

**Needs:**
*   View by series + time slot + platform.
*   KPIs: Average viewership, completion rate, drop-off.

### Finance / Management

**Questions:**
*   Which series are "underperforming" relative to their budget / strategic importance?
*   What types of projects should be prioritized in the future?

**Needs:**
*   Synthetic view: Top / Flop of recent anime.
*   3–5 clear recommendations with estimated impact (e.g., reduce fillers, switch to shorter seasons).

## 5. Priority Analytical Questions (Cross-Stakeholder)

*   How does the performance of recent anime (viewership, ratings, sentiment) compare to Pierrot's legacy hits?
*   What is the drop-off pattern between episodes (when do viewers drop out)?
*   What is the impact of:
    *   Episode count,
    *   Fillers,
    *   Production issues (simulated),
    *   On fan satisfaction (ratings, sentiment)?
*   How do broadcasting and marketing decisions influence overall performance?

## 6. Constraints & Assumptions

*   Some data is public (ratings, votes, dates, etc.), while other data is simulated (budget, production issues, marketing campaigns).
*   The initial scope focuses on 4–6 key anime for a POC (Naruto Shippuden, Bleach, Boruto, Tokyo Ghoul:re, etc.).
*   The project is conducted for BI illustration purposes (portfolio) and does not reflect actual internal data of Studio Pierrot.
