// Domestic (Japan) Market Data
// Simulated data calibrated against industry benchmarks

// TV Tokyo Weekly Ratings
// Prime-time shows (Naruto era): 2-4% ratings
// Late-night shows (Boruto): 0.5-1.5% ratings
export const tvRatings = [
    // Naruto Shippuden (2007-2017, prime-time)
    { anime_id: 'naruto-shippuden', week: '2015-W10', timeslot: 'prime_time', viewership_rating: 3.4, rank_in_slot: 1 },
    { anime_id: 'naruto-shippuden', week: '2015-W20', timeslot: 'prime_time', viewership_rating: 3.8, rank_in_slot: 1 },
    { anime_id: 'naruto-shippuden', week: '2016-W10', timeslot: 'prime_time', viewership_rating: 3.2, rank_in_slot: 1 },
    { anime_id: 'naruto-shippuden', week: '2017-W10', timeslot: 'prime_time', viewership_rating: 2.9, rank_in_slot: 2 },

    // Bleach TYBW (2022-2023, late-night)
    { anime_id: 'bleach-tybw', week: '2022-W42', timeslot: 'late_night', viewership_rating: 2.1, rank_in_slot: 1 },
    { anime_id: 'bleach-tybw', week: '2023-W05', timeslot: 'late_night', viewership_rating: 2.4, rank_in_slot: 1 },
    { anime_id: 'bleach-tybw', week: '2023-W15', timeslot: 'late_night', viewership_rating: 2.2, rank_in_slot: 1 },

    // Boruto (2017-present, late-night)
    { anime_id: 'boruto', week: '2023-W10', timeslot: 'late_night', viewership_rating: 1.1, rank_in_slot: 3 },
    { anime_id: 'boruto', week: '2023-W20', timeslot: 'late_night', viewership_rating: 0.9, rank_in_slot: 4 },
    { anime_id: 'boruto', week: '2024-W10', timeslot: 'late_night', viewership_rating: 0.8, rank_in_slot: 5 },

    // Tokyo Ghoul (2014-2015, late-night)
    { anime_id: 'tokyo-ghoul', week: '2014-W30', timeslot: 'late_night', viewership_rating: 1.8, rank_in_slot: 2 },
    { anime_id: 'tokyo-ghoul', week: '2014-W35', timeslot: 'late_night', viewership_rating: 2.0, rank_in_slot: 1 },

    // Black Clover (2017-2021, prime-time)
    { anime_id: 'black-clover', week: '2019-W10', timeslot: 'prime_time', viewership_rating: 1.5, rank_in_slot: 4 },
    { anime_id: 'black-clover', week: '2020-W10', timeslot: 'prime_time', viewership_rating: 1.3, rank_in_slot: 5 }
];

// Blu-ray/DVD Sales (Oricon Rankings)
// Correlation with MAL scores: 8.5+ → 30K+ units, 7.0-8.5 → 10K-30K, <7.0 → <10K
export const bdSales = [
    // Bleach TYBW (MAL: 8.99) - Strong sales
    { anime_id: 'bleach-tybw', volume: 1, release_date: '2023-04-15', units_sold: 48500, oricon_rank: 1 },
    { anime_id: 'bleach-tybw', volume: 2, release_date: '2023-05-20', units_sold: 45200, oricon_rank: 2 },
    { anime_id: 'bleach-tybw', volume: 3, release_date: '2023-06-18', units_sold: 42800, oricon_rank: 2 },

    // Naruto Shippuden (MAL: 8.28) - Very strong legacy sales
    { anime_id: 'naruto-shippuden', volume: 1, release_date: '2009-04-01', units_sold: 52000, oricon_rank: 1 },
    { anime_id: 'naruto-shippuden', volume: 10, release_date: '2010-01-15', units_sold: 48000, oricon_rank: 1 },
    { anime_id: 'naruto-shippuden', volume: 20, release_date: '2011-08-20', units_sold: 45000, oricon_rank: 2 },

    // Tokyo Ghoul (MAL: 7.79) - Moderate sales
    { anime_id: 'tokyo-ghoul', volume: 1, release_date: '2014-09-24', units_sold: 24500, oricon_rank: 3 },
    { anime_id: 'tokyo-ghoul', volume: 2, release_date: '2014-10-22', units_sold: 22100, oricon_rank: 4 },

    // Tokyo Ghoul √A (MAL: 7.03) - Weaker sales
    { anime_id: 'tokyo-ghoul-root-a', volume: 1, release_date: '2015-04-15', units_sold: 12300, oricon_rank: 8 },
    { anime_id: 'tokyo-ghoul-root-a', volume: 2, release_date: '2015-05-20', units_sold: 10500, oricon_rank: 12 },

    // Boruto (MAL: 5.98) - Poor sales
    { anime_id: 'boruto', volume: 1, release_date: '2017-07-26', units_sold: 6800, oricon_rank: 18 },
    { anime_id: 'boruto', volume: 2, release_date: '2017-08-23', units_sold: 5200, oricon_rank: 24 },

    // Black Clover (MAL: 8.16) - Good sales
    { anime_id: 'black-clover', volume: 1, release_date: '2018-01-24', units_sold: 18500, oricon_rank: 5 },
    { anime_id: 'black-clover', volume: 2, release_date: '2018-02-21', units_sold: 16200, oricon_rank: 6 }
];

// Merchandise & Licensing Revenue (Quarterly, in JPY)
// Legacy IP generates 5-10x more than new IP
export const merchRevenue = [
    // Naruto (massive legacy IP)
    { anime_id: 'naruto', year: 2023, quarter: 1, merch_revenue_jpy: 1200000000, licensing_revenue_jpy: 450000000, event_revenue_jpy: 80000000 },
    { anime_id: 'naruto', year: 2023, quarter: 2, merch_revenue_jpy: 1350000000, licensing_revenue_jpy: 480000000, event_revenue_jpy: 120000000 },
    { anime_id: 'naruto', year: 2023, quarter: 3, merch_revenue_jpy: 1280000000, licensing_revenue_jpy: 460000000, event_revenue_jpy: 95000000 },
    { anime_id: 'naruto', year: 2023, quarter: 4, merch_revenue_jpy: 1450000000, licensing_revenue_jpy: 520000000, event_revenue_jpy: 140000000 },

    // Bleach (strong legacy IP, resurgence with TYBW)
    { anime_id: 'bleach', year: 2023, quarter: 1, merch_revenue_jpy: 650000000, licensing_revenue_jpy: 220000000, event_revenue_jpy: 45000000 },
    { anime_id: 'bleach', year: 2023, quarter: 2, merch_revenue_jpy: 720000000, licensing_revenue_jpy: 250000000, event_revenue_jpy: 60000000 },
    { anime_id: 'bleach', year: 2023, quarter: 3, merch_revenue_jpy: 680000000, licensing_revenue_jpy: 230000000, event_revenue_jpy: 50000000 },
    { anime_id: 'bleach', year: 2023, quarter: 4, merch_revenue_jpy: 750000000, licensing_revenue_jpy: 270000000, event_revenue_jpy: 70000000 },

    // Tokyo Ghoul (moderate IP)
    { anime_id: 'tokyo-ghoul', year: 2023, quarter: 1, merch_revenue_jpy: 180000000, licensing_revenue_jpy: 65000000, event_revenue_jpy: 12000000 },
    { anime_id: 'tokyo-ghoul', year: 2023, quarter: 2, merch_revenue_jpy: 195000000, licensing_revenue_jpy: 70000000, event_revenue_jpy: 15000000 },
    { anime_id: 'tokyo-ghoul', year: 2023, quarter: 3, merch_revenue_jpy: 175000000, licensing_revenue_jpy: 62000000, event_revenue_jpy: 10000000 },
    { anime_id: 'tokyo-ghoul', year: 2023, quarter: 4, merch_revenue_jpy: 210000000, licensing_revenue_jpy: 75000000, event_revenue_jpy: 18000000 },

    // Boruto (weak new IP)
    { anime_id: 'boruto', year: 2023, quarter: 1, merch_revenue_jpy: 95000000, licensing_revenue_jpy: 28000000, event_revenue_jpy: 5000000 },
    { anime_id: 'boruto', year: 2023, quarter: 2, merch_revenue_jpy: 110000000, licensing_revenue_jpy: 32000000, event_revenue_jpy: 8000000 },
    { anime_id: 'boruto', year: 2023, quarter: 3, merch_revenue_jpy: 88000000, licensing_revenue_jpy: 25000000, event_revenue_jpy: 4000000 },
    { anime_id: 'boruto', year: 2023, quarter: 4, merch_revenue_jpy: 120000000, licensing_revenue_jpy: 35000000, event_revenue_jpy: 10000000 },

    // Black Clover (moderate-strong IP)
    { anime_id: 'black-clover', year: 2023, quarter: 1, merch_revenue_jpy: 220000000, licensing_revenue_jpy: 85000000, event_revenue_jpy: 18000000 },
    { anime_id: 'black-clover', year: 2023, quarter: 2, merch_revenue_jpy: 245000000, licensing_revenue_jpy: 92000000, event_revenue_jpy: 22000000 },
    { anime_id: 'black-clover', year: 2023, quarter: 3, merch_revenue_jpy: 210000000, licensing_revenue_jpy: 80000000, event_revenue_jpy: 16000000 },
    { anime_id: 'black-clover', year: 2023, quarter: 4, merch_revenue_jpy: 260000000, licensing_revenue_jpy: 98000000, event_revenue_jpy: 25000000 }
];
