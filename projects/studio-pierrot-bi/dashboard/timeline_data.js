// Timeline Revenue Data 2020-2024
// Simulated to show typical patterns: legacy declining slowly, new hits ramping up

export const timelineData = [
    // Naruto Shippuden - Legacy tail, slow decline
    { year: 2020, title: "Naruto Shippuden", studio: "Pierrot", revenue: 42, profile: "LegacyTail" },
    { year: 2021, title: "Naruto Shippuden", studio: "Pierrot", revenue: 39, profile: "LegacyTail" },
    { year: 2022, title: "Naruto Shippuden", studio: "Pierrot", revenue: 37, profile: "LegacyTail" },
    { year: 2023, title: "Naruto Shippuden", studio: "Pierrot", revenue: 35, profile: "LegacyTail" },
    { year: 2024, title: "Naruto Shippuden", studio: "Pierrot", revenue: 34, profile: "LegacyTail" },

    // Jujutsu Kaisen - New hit, sharp ramp-up
    { year: 2020, title: "Jujutsu Kaisen", studio: "MAPPA", revenue: 20, profile: "NewHit" },
    { year: 2021, title: "Jujutsu Kaisen", studio: "MAPPA", revenue: 32, profile: "NewHit" },
    { year: 2022, title: "Jujutsu Kaisen", studio: "MAPPA", revenue: 45, profile: "NewHit" },
    { year: 2023, title: "Jujutsu Kaisen", studio: "MAPPA", revenue: 48, profile: "NewHit" },
    { year: 2024, title: "Jujutsu Kaisen", studio: "MAPPA", revenue: 40, profile: "NewHit" },

    // Demon Slayer - New hit peak then plateau
    { year: 2020, title: "Demon Slayer", studio: "ufotable", revenue: 38, profile: "NewHit" },
    { year: 2021, title: "Demon Slayer", studio: "ufotable", revenue: 52, profile: "NewHit" },
    { year: 2022, title: "Demon Slayer", studio: "ufotable", revenue: 50, profile: "NewHit" },
    { year: 2023, title: "Demon Slayer", studio: "ufotable", revenue: 46, profile: "NewHit" },
    { year: 2024, title: "Demon Slayer", studio: "ufotable", revenue: 44, profile: "NewHit" },

    // Bleach TYBW - Revival hit
    { year: 2020, title: "Bleach TYBW", studio: "Pierrot", revenue: 0, profile: "RevivalHit" },
    { year: 2021, title: "Bleach TYBW", studio: "Pierrot", revenue: 0, profile: "RevivalHit" },
    { year: 2022, title: "Bleach TYBW", studio: "Pierrot", revenue: 18, profile: "RevivalHit" },
    { year: 2023, title: "Bleach TYBW", studio: "Pierrot", revenue: 28, profile: "RevivalHit" },
    { year: 2024, title: "Bleach TYBW", studio: "Pierrot", revenue: 32, profile: "RevivalHit" },

    // Boruto - Long run struggling
    { year: 2020, title: "Boruto", studio: "Pierrot", revenue: 14, profile: "LongRun" },
    { year: 2021, title: "Boruto", studio: "Pierrot", revenue: 13, profile: "LongRun" },
    { year: 2022, title: "Boruto", studio: "Pierrot", revenue: 11, profile: "LongRun" },
    { year: 2023, title: "Boruto", studio: "Pierrot", revenue: 10, profile: "LongRun" },
    { year: 2024, title: "Boruto", studio: "Pierrot", revenue: 9, profile: "LongRun" },

    // Black Clover - Long run stable
    { year: 2020, title: "Black Clover", studio: "Pierrot", revenue: 16, profile: "LongRun" },
    { year: 2021, title: "Black Clover", studio: "Pierrot", revenue: 15, profile: "LongRun" },
    { year: 2022, title: "Black Clover", studio: "Pierrot", revenue: 14, profile: "LongRun" },
    { year: 2023, title: "Black Clover", studio: "Pierrot", revenue: 14, profile: "LongRun" },
    { year: 2024, title: "Black Clover", studio: "Pierrot", revenue: 13, profile: "LongRun" },

    // Attack on Titan - Declining after finale
    { year: 2020, title: "Attack on Titan", studio: "MAPPA", revenue: 35, profile: "LegacyTail" },
    { year: 2021, title: "Attack on Titan", studio: "MAPPA", revenue: 40, profile: "LegacyTail" },
    { year: 2022, title: "Attack on Titan", studio: "MAPPA", revenue: 38, profile: "LegacyTail" },
    { year: 2023, title: "Attack on Titan", studio: "MAPPA", revenue: 30, profile: "LegacyTail" },
    { year: 2024, title: "Attack on Titan", studio: "MAPPA", revenue: 22, profile: "LegacyTail" },
];

export const revenueProfiles = {
    LegacyTail: {
        label: "Legacy Evergreen",
        color: "#8B5CF6",
        description: "Finished airing but maintains strong long-tail monetization through streaming and merchandise"
    },
    NewHit: {
        label: "Recent Hit",
        color: "#10B981",
        description: "Currently airing or recent completion with high momentum and growing revenue"
    },
    RevivalHit: {
        label: "Revival Success",
        color: "#6366F1",
        description: "Returning franchise with renewed production and strong comeback performance"
    },
    LongRun: {
        label: "Long-Run Series",
        color: "#F59E0B",
        description: "Ongoing continuous production with stable but moderate performance"
    }
};
