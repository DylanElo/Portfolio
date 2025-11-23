-- Studio Pierrot Anime BI - Analytical Queries
-- Answers key business questions using the data warehouse

-- ===========================================================================
-- Q1: How do recent anime perform vs historical hits?
-- ===========================================================================

-- Performance comparison: Recent (2015+) vs Classic (<2015)
SELECT 
    CASE 
        WHEN CAST(SUBSTR(a.start_date, 1, 4) AS INTEGER) >= 2015 THEN 'Recent (2015+)'
        ELSE 'Classic (< 2015)'
    END AS era,
    COUNT(DISTINCT a.anime_id) AS num_anime,
    ROUND(AVG(m.score), 2) AS avg_score,
    ROUND(AVG(m.members), 0) AS avg_members,
    ROUND(AVG(m.favorites), 0) AS avg_favorites,
    ROUND(AVG(CAST(m.dropped AS REAL) / NULLIF(m.members, 0) * 100), 2) AS avg_drop_rate_pct,
    ROUND(AVG(CAST(m.completed AS REAL) / NULLIF(m.members, 0) * 100), 2) AS avg_completion_rate_pct
FROM dim_anime a
JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
WHERE a.start_date IS NOT NULL
GROUP BY era
ORDER BY era DESC;

-- ===========================================================================
-- Q2: Individual anime performance rankings
-- ===========================================================================

-- Top and bottom performers by score
SELECT 
    a.title,
    a.studio,
    SUBSTR(a.start_date, 1, 4) AS year,
    a.episodes,
    m.score,
    m.members,
    m.favorites,
    m.rank AS mal_rank,
    s.filler_ratio,
    ROUND(CAST(m.dropped AS REAL) / NULLIF(m.members, 0) * 100, 2) AS drop_rate_pct
FROM dim_anime a
JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
LEFT JOIN dim_season s ON a.anime_id = s.anime_id
ORDER BY m.score DESC;

-- ===========================================================================
-- Q3: Does filler ratio correlate with performance?
-- ===========================================================================

-- Filler ratio analysis
SELECT 
    CASE 
        WHEN s.filler_ratio < 0.10 THEN 'Low (<10%)'
        WHEN s.filler_ratio < 0.25 THEN 'Medium (10-25%)'
        WHEN s.filler_ratio < 0.40 THEN 'High (25-40%)'
        ELSE 'Very High (40%+)'
    END AS filler_category,
    COUNT(*) AS num_anime,
    ROUND(AVG(m.score), 2) AS avg_score,
    ROUND(AVG(CAST(m.dropped AS REAL) / NULLIF(m.members, 0) * 100), 2) AS avg_drop_rate_pct,
    ROUND(AVG(s.production_stability), 2) AS avg_production_stability
FROM dim_season s
JOIN dim_anime a ON s.anime_id = a.anime_id
JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
GROUP BY filler_category
ORDER BY 
    CASE filler_category
        WHEN 'Low (<10%)' THEN 1
        WHEN 'Medium (10-25%)' THEN 2
        WHEN 'High (25-40%)' THEN 3
        ELSE 4
    END;

-- ===========================================================================
-- Q4: Production stability impact
-- ===========================================================================

-- Production stability vs performance
SELECT 
    CASE 
        WHEN s.production_stability < 0.60 THEN 'Low Stability (<0.60)'
        WHEN s.production_stability < 0.75 THEN 'Medium Stability (0.60-0.75)'
        ELSE 'High Stability (0.75+)'
    END AS stability_category,
    COUNT(*) AS num_anime,
    ROUND(AVG(m.score), 2) AS avg_score,
    ROUND(AVG(m.members), 0) AS avg_members,
    ROUND(AVG(s.quality_score_internal), 2) AS avg_internal_quality
FROM dim_season s
JOIN dim_anime a ON s.anime_id = a.anime_id
JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
GROUP BY stability_category
ORDER BY 
    CASE stability_category
        WHEN 'Low Stability (<0.60)' THEN 1
        WHEN 'Medium Stability (0.60-0.75)' THEN 2
        ELSE 3
    END;

-- ===========================================================================
-- Q5: Long-running vs short seasons
-- ===========================================================================

-- Season type performance comparison
SELECT 
    s.season_type,
    COUNT(*) AS num_anime,
    ROUND(AVG(a.episodes), 0) AS avg_episodes,
    ROUND(AVG(m.score), 2) AS avg_score,
    ROUND(AVG(m.members), 0) AS avg_members,
    ROUND(AVG(s.filler_ratio * 100), 1) AS avg_filler_pct,
    ROUND(AVG(CAST(m.completed AS REAL) / NULLIF(m.members, 0) * 100), 2) AS avg_completion_rate
FROM dim_season s
JOIN dim_anime a ON s.anime_id = a.anime_id
JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
GROUP BY s.season_type
ORDER BY s.season_type;

-- ===========================================================================
-- Q6: Financial performance and ROI
-- ===========================================================================

-- ROI analysis by anime
SELECT 
    a.title,
    SUBSTR(a.start_date, 1, 4) AS year,
    f.tier,
    f.production_budget,
    f.total_revenue,
    f.profit,
    ROUND(f.roi * 100, 1) AS roi_pct,
    m.score,
    m.members
FROM dim_anime a
JOIN fact_finance f ON a.anime_id = f.anime_id
JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
ORDER BY profit DESC;

-- ===========================================================================
-- Q7: Marketing efficiency
-- ===========================================================================

-- Marketing spend vs engagement
SELECT 
    a.title,
    COUNT(mk.campaign_id) AS num_campaigns,
    SUM(mk.cost) AS total_marketing_spend,
    SUM(mk.impressions) AS total_impressions,
    ROUND(SUM(mk.cost) / NULLIF(SUM(mk.impressions), 0) * 1000, 2) AS cost_per_1k_impressions,
    m.members,
    ROUND(SUM(mk.cost) / NULLIF(m.members, 0), 2) AS cost_per_member
FROM dim_anime a
JOIN fact_marketing mk ON a.anime_id = mk.anime_id
JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
GROUP BY a.anime_id, a.title, m.members
ORDER BY total_marketing_spend DESC;

-- ===========================================================================
-- Q8: Risk identification - underperforming recent titles
-- ===========================================================================

-- Recent anime with warning signs
SELECT 
    a.title,
    SUBSTR(a.start_date, 1, 4) AS year,
    m.score,
    m.rank AS mal_rank,
    ROUND(CAST(m.dropped AS REAL) / NULLIF(m.members, 0) * 100, 2) AS drop_rate_pct,
    s.filler_ratio,
    s.production_stability,
    f.profit,
    CASE
        WHEN m.score < 7.5 THEN '⚠ Low Score'
        WHEN CAST(m.dropped AS REAL) / NULLIF(m.members, 0) > 0.15 THEN '⚠ High Drop Rate'
        WHEN s.filler_ratio > 0.40 THEN '⚠ High Filler'
        WHEN s.production_stability < 0.60 THEN '⚠ Production Issues'
        ELSE '✓ Healthy'
    END AS risk_flag
FROM dim_anime a
JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
JOIN dim_season s ON a.anime_id = s.anime_id
JOIN fact_finance f ON a.anime_id = f.anime_id
WHERE CAST(SUBSTR(a.start_date, 1, 4) AS INTEGER) >= 2015
ORDER BY m.score ASC, drop_rate_pct DESC;

-- ===========================================================================
-- Q9: Studio Pierrot vs competitors
-- ===========================================================================

-- Studio comparison (if non-Pierrot studios exist in dataset)
SELECT 
    a.studio,
    COUNT(DISTINCT a.anime_id) AS num_anime,
    ROUND(AVG(m.score), 2) AS avg_score,
    ROUND(AVG(m.members), 0) AS avg_members,
    ROUND(AVG(s.filler_ratio * 100), 1) AS avg_filler_pct,
    ROUND(AVG(f.profit), 0) AS avg_profit
FROM dim_anime a
JOIN fact_anime_metrics m ON a.anime_id = m.anime_id
LEFT JOIN dim_season s ON a.anime_id = s.anime_id
LEFT JOIN fact_finance f ON a.anime_id = f.anime_id
GROUP BY a.studio
HAVING COUNT(DISTINCT a.anime_id) >= 2
ORDER BY avg_score DESC;

-- ===========================================================================
-- Q10: Marketing campaign effectiveness by type
-- ===========================================================================

-- Which campaign types deliver best impressions per dollar?
SELECT 
    mk.campaign_type,
    COUNT(*) AS num_campaigns,
    ROUND(AVG(mk.cost), 0) AS avg_cost,
    ROUND(AVG(mk.impressions), 0) AS avg_impressions,
    ROUND(AVG(CAST(mk.impressions AS REAL) / NULLIF(mk.cost, 0)), 0) AS avg_impressions_per_dollar
FROM fact_marketing mk
GROUP BY mk.campaign_type
ORDER BY avg_impressions_per_dollar DESC;
