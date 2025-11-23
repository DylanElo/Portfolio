// International Streaming Market Data
// Simulated data calibrated against public reports

// Platform Market Share by Region
// Based on: Netflix ~40M anime viewers globally, Crunchyroll ~15M subscribers
export const platformShare = [
    // North America (Netflix dominates)
    { platform: 'Netflix', region: 'North America', year: 2024, quarter: 1, subscriber_count: 75000000, anime_viewer_share: 52 },
    { platform: 'Crunchyroll', region: 'North America', year: 2024, quarter: 1, subscriber_count: 15000000, anime_viewer_share: 85 },
    { platform: 'Disney+', region: 'North America', year: 2024, quarter: 1, subscriber_count: 46000000, anime_viewer_share: 12 },

    // Europe (Mixed)
    { platform: 'Netflix', region: 'Europe', year: 2024, quarter: 1, subscriber_count: 78000000, anime_viewer_share: 45 },
    { platform: 'Crunchyroll', region: 'Europe', year: 2024, quarter: 1, subscriber_count: 12000000, anime_viewer_share: 82 },
    { platform: 'Disney+', region: 'Europe', year: 2024, quarter: 1, subscriber_count: 38000000, anime_viewer_share: 10 },

    // Asia-Pacific (Crunchyroll strong)
    { platform: 'Netflix', region: 'Asia-Pacific', year: 2024, quarter: 1, subscriber_count: 35000000, anime_viewer_share: 58 },
    { platform: 'Crunchyroll', region: 'Asia-Pacific', year: 2024, quarter: 1, subscriber_count: 18000000, anime_viewer_share: 88 },
    { platform: 'Disney+', region: 'Asia-Pacific', year: 2024, quarter: 1, subscriber_count: 24000000, anime_viewer_share: 15 }
];

// Global Demand Index (Parrot Analytics style)
// JJK = 71.2x (known benchmark), scale others realistically
export const globalDemand = [
    // Current Top Performers (MAPPA, ufotable)
    { anime_id: 'jujutsu-kaisen', week: '2024-W10', global_demand_index: 71.2, rank_global: 1, rank_anime: 1 },
    { anime_id: 'demon-slayer', week: '2024-W10', global_demand_index: 58.5, rank_global: 2, rank_anime: 2 },
    { anime_id: 'attack-on-titan', week: '2024-W10', global_demand_index: 42.3, rank_global: 3, rank_anime: 3 },

    // Pierrot Legacy IP (Strong but not top-tier)
    { anime_id: 'naruto-shippuden', week: '2024-W10', global_demand_index: 12.5, rank_global: 8, rank_anime: 6 },
    { anime_id: 'bleach-tybw', week: '2024-W10', global_demand_index: 9.8, rank_global: 12, rank_anime: 9 },
    { anime_id: 'naruto', week: '2024-W10', global_demand_index: 8.2, rank_global: 15, rank_anime: 11 },

    // Pierrot Mid-tier IP
    { anime_id: 'tokyo-ghoul', week: '2024-W10', global_demand_index: 4.1, rank_global: 28, rank_anime: 18 },
    { anime_id: 'black-clover', week: '2024-W10', global_demand_index: 3.8, rank_global: 32, rank_anime: 21 },

    // Pierrot Weak New IP
    { anime_id: 'boruto', week: '2024-W10', global_demand_index: 2.3, rank_global: 45, rank_anime: 32 },
    { anime_id: 'tokyo-ghoul-root-a', week: '2024-W10', global_demand_index: 1.7, rank_global: 58, rank_anime: 41 }
];

// Streaming Platform Revenue (Estimated)
// Based on typical $1-3M per title per platform per quarter for popular shows
export const streamingRevenue = [
    // Naruto Shippuden (massive on Netflix - #1 anime H1 2025)
    { anime_id: 'naruto-shippuden', platform: 'Netflix', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 3200000 },
    { anime_id: 'naruto-shippuden', platform: 'Netflix', region: 'Europe', year: 2024, quarter: 1, estimated_revenue_usd: 2800000 },
    { anime_id: 'naruto-shippuden', platform: 'Netflix', region: 'Asia-Pacific', year: 2024, quarter: 1, estimated_revenue_usd: 1900000 },
    { anime_id: 'naruto-shippuden', platform: 'Crunchyroll', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 1200000 },

    // Bleach TYBW (strong resurgence)
    { anime_id: 'bleach-tybw', platform: 'Netflix', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 1800000 },
    { anime_id: 'bleach-tybw', platform: 'Netflix', region: 'Europe', year: 2024, quarter: 1, estimated_revenue_usd: 1500000 },
    { anime_id: 'bleach-tybw', platform: 'Crunchyroll', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 950000 },

    // Tokyo Ghoul (moderate)
    { anime_id: 'tokyo-ghoul', platform: 'Netflix', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 850000 },
    { anime_id: 'tokyo-ghoul', platform: 'Crunchyroll', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 420000 },

    // Boruto (weak - can't retain Naruto audience)
    { anime_id: 'boruto', platform: 'Netflix', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 320000 },
    { anime_id: 'boruto', platform: 'Crunchyroll', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 180000 },

    // Black Clover (moderate-strong)
    { anime_id: 'black-clover', platform: 'Netflix', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 950000 },
    { anime_id: 'black-clover', platform: 'Crunchyroll', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 520000 },

    // Competitor Benchmarks (for comparison)
    { anime_id: 'jujutsu-kaisen', platform: 'Netflix', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 8500000 },
    { anime_id: 'jujutsu-kaisen', platform: 'Crunchyroll', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 4200000 },
    { anime_id: 'demon-slayer', platform: 'Netflix', region: 'North America', year: 2024, quarter: 1, estimated_revenue_usd: 7200000 }
];

// Regional Streaming Growth (Year-over-Year)
export const regionalGrowth = [
    { region: 'North America', year: 2023, total_revenue_usd: 45000000, yoy_growth_percent: 18 },
    { region: 'North America', year: 2024, total_revenue_usd: 53100000, yoy_growth_percent: 18 },
    { region: 'Europe', year: 2023, total_revenue_usd: 32000000, yoy_growth_percent: 15 },
    { region: 'Europe', year: 2024, total_revenue_usd: 36800000, yoy_growth_percent: 15 },
    { region: 'Asia-Pacific', year: 2023, total_revenue_usd: 28000000, yoy_growth_percent: 22 },
    { region: 'Asia-Pacific', year: 2024, total_revenue_usd: 34160000, yoy_growth_percent: 22 }
];
