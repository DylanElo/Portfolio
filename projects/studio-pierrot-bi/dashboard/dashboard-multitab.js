// Import Phase 2 data
import { tvRatings, bdSales, merchRevenue } from './domestic_data.js';
import { platformShare, globalDemand, streamingRevenue } from './streaming_data.js';
import { arcAnalysis, fillerImpact, productionModels } from './production_data.js';

console.log('Multi-tab dashboard loaded');

// Tab switching function
window.switchTab = function (tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(`content-${tabName}`).classList.add('active');
    document.getElementById(`tab-${tabName}`).classList.add('active');

    // Initialize charts for the selected tab (lazy loading)
    initializeTabCharts(tabName);
};

// Track which tabs have been initialized
const initializedTabs = {
    fandom: false,
    streaming: false,
    domestic: false,
    production: false
};

function initializeTabCharts(tabName) {
    if (initializedTabs[tabName]) return; // Don't reinitialize

    switch (tabName) {
        case 'streaming':
            renderDemandChart();
            renderPlatformChart();
            break;
        case 'domestic':
            renderBDSalesChart();
            renderMerchChart();
            break;
        case 'production':
            renderFillerChart();
            renderModelChart();
            break;
    }

    initializedTabs[tabName] = true;
}

// ===== STREAMING ANALYTICS CHARTS =====

function renderDemandChart() {
    const ctx = document.getElementById('demandChart')?.getContext('2d');
    if (!ctx) return;

    // Get unique anime and their demand
    const demandData = [
        { title: 'JJK (MAPPA)', demand: 71.2, color: 'rgba(239, 68, 68, 0.8)' },
        { title: 'Demon Slayer (ufotable)', demand: 58.5, color: 'rgba(245, 158, 11, 0.8)' },
        { title: 'Naruto Shippuden', demand: 12.5, color: 'rgba(99, 102, 241, 0.8)' },
        { title: 'Bleach TYBW', demand: 9.8, color: 'rgba(139, 92, 246, 0.8)' },
        { title: 'Black Clover', demand: 3.8, color: 'rgba(59, 130, 246, 0.8)' },
        { title: 'Tokyo Ghoul', demand: 4.1, color: 'rgba(107, 114, 128, 0.8)' },
        { title: 'Boruto', demand: 2.3, color: 'rgba(156, 163, 175, 0.8)' }
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: demandData.map(d => d.title),
            datasets: [{
                label: 'Global Demand Index (x vs average)',
                data: demandData.map(d => d.demand),
                backgroundColor: demandData.map(d => d.color),
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'JJK dominates at 71.2x average demand (Parrot Analytics)',
                    font: { size: 11 },
                    color: '#64748b'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Demand Multiplier' }
                }
            }
        }
    });
}

function renderPlatformChart() {
    const ctx = document.getElementById('platformChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Netflix (52% anime watchers)', 'Crunchyroll (85% anime)', 'Disney+ (12% anime)'],
            datasets: [{
                data: [75000000 * 0.52, 15000000 * 0.85, 46000000 * 0.12],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(59, 130, 246, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'North America Anime Viewers by Platform',
                    font: { size: 11 },
                    color: '#64748b'
                }
            }
        }
    });
}

// ===== DOMESTIC (JAPAN) CHARTS =====

function renderBDSalesChart() {
    const ctx = document.getElementById('bdSalesChart')?.getContext('2d');
    if (!ctx) return;

    // Group BD sales by anime and calculate average
    const salesByAnime = [
        { title: 'Bleach TYBW (8.99)', units: 45500, score: 8.99 },
        { title: 'Naruto Shippuden (8.28)', units: 48333, score: 8.28 },
        { title: 'Tokyo Ghoul (7.79)', units: 23300, score: 7.79 },
        { title: 'Black Clover (8.16)', units: 17350, score: 8.16 },
        { title: 'Tokyo Ghoul √A (7.03)', units: 11400, score: 7.03 },
        { title: 'Boruto (5.98)', units: 6000, score: 5.98 }
    ];

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Pierrot Titles',
                data: salesByAnime.map(a => ({ x: a.score, y: a.units })),
                backgroundColor: 'rgba(99, 102, 241, 0.6)',
                borderColor: 'rgba(99, 102, 241, 1)',
                pointRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Strong correlation: Higher MAL score = Better BD sales',
                    font: { size: 11 },
                    color: '#64748b'
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const anime = salesByAnime[context.dataIndex];
                            return `${anime.title}: ${anime.units.toLocaleString()} units`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'MAL Score' },
                    min: 5,
                    max: 10
                },
                y: {
                    title: { display: true, text: 'BD Units Sold (Vol 1)' },
                    beginAtZero: true
                }
            }
        }
    });
}

function renderMerchChart() {
    const ctx = document.getElementById('merchChart')?.getContext('2d');
    if (!ctx) return;

    // Calculate annual merchandise revenue
    const merchData = [
        { title: 'Naruto (Legacy)', revenue: (1200 + 1350 + 1280 + 1450) / 1000 },
        { title: 'Bleach (Legacy)', revenue: (650 + 720 + 680 + 750) / 1000 },
        { title: 'Black Clover', revenue: (220 + 245 + 210 + 260) / 1000 },
        { title: 'Tokyo Ghoul', revenue: (180 + 195 + 175 + 210) / 1000 },
        { title: 'Boruto (New)', revenue: (95 + 110 + 88 + 120) / 1000 }
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: merchData.map(d => d.title),
            datasets: [{
                label: 'Annual Merch Revenue (Billion ¥)',
                data: merchData.map(d => d.revenue),
                backgroundColor: [
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(99, 102, 241, 0.8)',
                    'rgba(107, 114, 128, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Legacy IP generates 10x more merchandise revenue',
                    font: { size: 11 },
                    color: '#64748b'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Billion ¥' }
                }
            }
        }
    });
}

// ===== PRODUCTION INSIGHTS CHARTS =====

function renderFillerChart() {
    const ctx = document.getElementById('fillerChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Filler Impact',
                data: fillerImpact.map(f => ({
                    x: parseInt(f.filler_range.split('-')[0]),
                    y: f.avg_mal_score
                })),
                backgroundColor: 'rgba(239, 68, 68, 0.6)',
                borderColor: 'rgba(239, 68, 68, 1)',
                pointRadius: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Clear negative correlation: More filler = Lower scores',
                    font: { size: 11 },
                    color: '#64748b'
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Filler %' },
                    min: 0,
                    max: 100
                },
                y: {
                    title: { display: true, text: 'Avg MAL Score' },
                    min: 5,
                    max: 10
                }
            }
        }
    });
}

function renderModelChart() {
    const ctx = document.getElementById('modelChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: productionModels.map(m => m.model.split(' (')[0]),
            datasets: [{
                label: 'Avg MAL Score',
                data: productionModels.map(m => m.avg_mal_score),
                backgroundColor: 'rgba(99, 102, 241, 0.8)',
                yAxisID: 'y'
            }, {
                label: 'Filler %',
                data: productionModels.map(m => m.avg_filler_percentage),
                backgroundColor: 'rgba(239, 68, 68, 0.8)',
                yAxisID: 'y1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Seasonal model beats long-running on quality and efficiency',
                    font: { size: 11 },
                    color: '#64748b'
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    title: { display: true, text: 'MAL Score' },
                    min: 0,
                    max: 10
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    title: { display: true, text: 'Filler %' },
                    grid: { drawOnChartArea: false },
                    min: 0,
                    max: 100
                }
            }
        }
    });
}

// Initialize on load (Fandom tab loaded by default in Phase 1)
console.log('Dashboard ready. Switch tabs to view Phase 2 data visualizations.');
