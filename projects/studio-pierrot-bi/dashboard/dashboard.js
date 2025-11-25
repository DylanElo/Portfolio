// Import Phase 1 data (MAL)
// Import Phase 1 data (MAL)
import { animeData, lastUpdated, financialData } from './data.js';

// Import Phase 2 data
import { tvRatings, bdSales, merchRevenue } from './domestic_data.js';
import { platformShare, globalDemand, streamingRevenue } from './streaming_data.js';
import { arcAnalysis, fillerImpact, productionModels } from './production_data.js';

console.log('Multi-tab dashboard loaded');

// Initialize Phase 1 dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing Phase 1 dashboard...');

    if (!animeData || animeData.length === 0) {
        console.error('No anime data found!');
        document.getElementById('kpi-top-rated-value').textContent = 'Error';
        return;
    }

    console.log('Anime data loaded:', animeData.length, 'entries');

    // Display Last Updated timestamp
    if (lastUpdated) {
        const footer = document.querySelector('footer div');
        if (footer) {
            const date = new Date(lastUpdated).toLocaleString();
            const p = document.createElement('p');
            p.className = 'mt-2 text-xs text-slate-400';
            p.innerHTML = `🔄 <strong>Data Last Refreshed:</strong> ${date} (Source: SQL Warehouse)`;
            footer.appendChild(p);
        }
    }

    initPhase1Dashboard();
});

function initPhase1Dashboard() {
    // Calculate KPIs
    const topRated = [...animeData].sort((a, b) => b.score - a.score)[0];
    const mostMembers = [...animeData].sort((a, b) => b.members - a.members)[0];
    const mostFavorited = [...animeData].sort((a, b) => b.favorites - a.favorites)[0];

    // Update KPI Cards
    if (topRated) updateKPI('kpi-top-rated', topRated.score, topRated.title);
    if (mostMembers) updateKPI('kpi-most-popular', formatNumber(mostMembers.members), mostMembers.title);
    if (mostFavorited) updateKPI('kpi-most-favorited', formatNumber(mostFavorited.favorites), mostFavorited.title);

    // Render Phase 1 charts immediately (fandom tab active by default)
    renderPhase1ScoreChart(animeData);
    renderPhase1PopularityChart(animeData);
    populatePhase1Table(animeData);

    // Mark fandom tab as initialized
    initializedTabs.fandom = true;
}

function updateKPI(idPrefix, value, title) {
    const valueEl = document.getElementById(`${idPrefix}-value`);
    const titleEl = document.getElementById(`${idPrefix}-title`);
    if (valueEl) valueEl.textContent = value;
    if (titleEl) titleEl.textContent = title;
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}


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
            renderReleaseYearChart(animeData);
            break;
        case 'financial':
            initFinancialDashboard();
            break;
    }

    initializedTabs[tabName] = true;
}

// ===== PHASE 1: GLOBAL FANDOM CHARTS =====

function renderPhase1ScoreChart(data) {
    const ctx = document.getElementById('scoreChart')?.getContext('2d');
    if (!ctx) return;

    // Sort by score and take top 10
    const topAnime = [...data].sort((a, b) => b.score - a.score).slice(0, 10);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topAnime.map(a => a.title.length > 20 ? a.title.substring(0, 20) + '...' : a.title),
            datasets: [{
                label: 'MAL Score',
                data: topAnime.map(a => a.score),
                backgroundColor: 'rgba(99, 102, 241, 0.8)', // Indigo-500
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'Top Rated Studio Pierrot Anime (MAL)',
                    color: '#94a3b8'
                }
            },
            scales: {
                x: {
                    min: 7,
                    max: 10,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#f8fafc' }
                }
            }
        }
    });
}

function renderPhase1PopularityChart(data) {
    const ctx = document.getElementById('popularityChart')?.getContext('2d');
    if (!ctx) return;

    // Sort by members and take top 10
    const popularAnime = [...data].sort((a, b) => b.members - a.members).slice(0, 10);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: popularAnime.map(a => a.title.length > 15 ? a.title.substring(0, 15) + '...' : a.title),
            datasets: [{
                label: 'Members',
                data: popularAnime.map(a => a.members),
                backgroundColor: 'rgba(139, 92, 246, 0.8)', // Violet-500
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'Most Popular Titles (Member Count)',
                    color: '#94a3b8'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: {
                        color: '#94a3b8',
                        callback: function (value) {
                            return (value / 1000000).toFixed(1) + 'M';
                        }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#f8fafc' }
                }
            }
        }
    });
}

function populatePhase1Table(data) {
    const tbody = document.getElementById('anime-table-body');
    if (!tbody) return;

    // Sort by score descending
    const sortedData = [...data].sort((a, b) => b.score - a.score);

    tbody.innerHTML = sortedData.map(anime => `
        <tr class="hover:bg-slate-700/30 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-200">${anime.title}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-400">${anime.score}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-400">${formatNumber(anime.members)}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-400">${anime.episodes || '?'}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-400">${anime.year || 'N/A'}</td>
        </tr>
    `).join('');
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

// ===== FINANCIAL PERFORMANCE DASHBOARD =====

function initFinancialDashboard() {
    if (!financialData || financialData.length === 0) {
        console.warn('No financial data available');
        return;
    }

    // Calculate KPIs
    const avgROI = (financialData.reduce((sum, d) => sum + d.roi, 0) / financialData.length) * 100;
    const sortedByROI = [...financialData].sort((a, b) => b.roi - a.roi);
    const bestROI = sortedByROI[0];
    const worstROI = sortedByROI[sortedByROI.length - 1];

    // Update KPIs
    document.getElementById('kpi-avg-roi').textContent = avgROI.toFixed(1) + '%';
    if (bestROI) {
        document.getElementById('kpi-best-roi').textContent = (bestROI.roi * 100).toFixed(1) + '%';
        document.getElementById('kpi-best-roi-title').textContent = bestROI.title;
    }
    if (worstROI) {
        document.getElementById('kpi-worst-roi').textContent = (worstROI.roi * 100).toFixed(1) + '%';
        document.getElementById('kpi-worst-roi-title').textContent = worstROI.title;
    }

    // Render charts
    renderROITierChart();
    renderBudgetRevenueChart();
    renderProfitPerEpChart();
    renderRevenueBreakdownChart();
    populateFinancialTable();
}

function renderROITierChart() {
    const ctx = document.getElementById('roiTierChart')?.getContext('2d');
    if (!ctx) return;

    const tierROI = { S: [], A: [], B: [], C: [] };
    financialData.forEach(d => {
        if (tierROI[d.tier]) tierROI[d.tier].push(d.roi * 100);
    });

    const avgByTier = Object.keys(tierROI).map(tier => ({
        tier,
        avgROI: tierROI[tier].length > 0 ? tierROI[tier].reduce((a, b) => a + b) / tierROI[tier].length : 0
    }));

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: avgByTier.map(d => `Tier ${d.tier}`),
            datasets: [{
                label: 'Average ROI %',
                data: avgByTier.map(d => d.avgROI),
                backgroundColor: ['#10B981', '#3B82F6', '#F59E0B', '#EF4444']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { callback: v => v + '%' }
                }
            }
        }
    });
}

function renderBudgetRevenueChart() {
    const ctx = document.getElementById('budgetRevenueChart')?.getContext('2d');
    if (!ctx) return;

    const tierColors = { S: '#10B981', A: '#3B82F6', B: '#F59E0B', C: '#EF4444' };

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Budget vs Revenue',
                data: financialData.map(d => ({
                    x: d.production_budget / 1000000,
                    y: d.total_revenue / 1000000,
                    tier: d.tier,
                    title: d.title
                })),
                backgroundColor: financialData.map(d => tierColors[d.tier]),
                pointRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: (ctx) => {
                            const d = ctx.raw;
                            return `${d.title} (${d.tier}): Budget $${d.x.toFixed(1)}M, Revenue $${d.y.toFixed(1)}M`;
                        }
                    }
                }
            },
            scales: {
                x: { title: { display: true, text: 'Budget ($M)' } },
                y: { title: { display: true, text: 'Revenue ($M)' } }
            }
        }
    });
}

function renderProfitPerEpChart() {
    const ctx = document.getElementById('profitPerEpChart')?.getContext('2d');
    if (!ctx) return;

    const top8 = [...financialData].sort((a, b) => b.profit_per_episode - a.profit_per_episode).slice(0, 8);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: top8.map(d => d.title.length > 15 ? d.title.substring(0, 15) + '...' : d.title),
            datasets: [{
                label: 'Profit/Ep ($K)',
                data: top8.map(d => d.profit_per_episode / 1000),
                backgroundColor: top8.map(d => d.profit_per_episode > 0 ? '#10B981' : '#EF4444')
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    ticks: { callback: v => '$' + v + 'K' }
                }
            }
        }
    });
}

function renderRevenueBreakdownChart() {
    const ctx = document.getElementById('revenueBreakdownChart')?.getContext('2d');
    if (!ctx) return;

    const totalStreaming = financialData.reduce((sum, d) => sum + d.streaming_revenue, 0);
    const totalDisc = financialData.reduce((sum, d) => sum + d.disc_revenue, 0);
    const totalMerch = financialData.reduce((sum, d) => sum + d.merch_revenue, 0);

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Streaming', 'Disc Sales', 'Merchandise'],
            datasets: [{
                data: [totalStreaming, totalDisc, totalMerch],
                backgroundColor: ['#3B82F6', '#8B5CF6', '#10B981']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.label}: $${(ctx.parsed / 1000000).toFixed(1)}M`
                    }
                }
            }
        }
    });
}

function populateFinancialTable() {
    const tbody = document.getElementById('financial-table-body');
    if (!tbody) return;

    tbody.innerHTML = financialData.map(d => `
        <tr>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">${d.title}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                <span class="px-2 py-1 text-xs font-semibold rounded ${d.tier === 'S' ? 'bg-green-100 text-green-800' :
            d.tier === 'A' ? 'bg-blue-100 text-blue-800' :
                d.tier === 'B' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
        }">${d.tier}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">$${(d.production_budget / 1000000).toFixed(1)}M</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">$${(d.total_revenue / 1000000).toFixed(1)}M</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm ${d.profit > 0 ? 'text-green-600' : 'text-red-600'}">
                $${(d.profit / 1000000).toFixed(1)}M
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold ${d.roi > 0 ? 'text-green-600' : 'text-red-600'}">
                ${(d.roi * 100).toFixed(1)}%
            </td>
        </tr>
    `).join('');
}

// Initialize on load (Fandom tab loaded by default in Phase 1)
console.log('Dashboard ready. Switch tabs to view Phase 2 data visualizations.');


function renderReleaseYearChart(data) {
    const ctx = document.getElementById('releaseYearChart')?.getContext('2d');
    if (!ctx) return;

    // Group data by year
    const yearGroups = {};
    data.forEach(anime => {
        if (!anime.air_date_start) return;
        const year = new Date(anime.air_date_start).getFullYear();
        if (!yearGroups[year]) {
            yearGroups[year] = { totalScore: 0, count: 0, titles: [] };
        }
        yearGroups[year].totalScore += anime.score;
        yearGroups[year].count += 1;
        yearGroups[year].titles.push(anime.title);
    });

    // Calculate averages and sort by year
    const years = Object.keys(yearGroups).sort();
    const avgScores = years.map(year => (yearGroups[year].totalScore / yearGroups[year].count).toFixed(2));
    const counts = years.map(year => yearGroups[year].count);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Average MAL Score',
                    data: avgScores,
                    borderColor: 'rgba(249, 115, 22, 1)', // Orange-500
                    backgroundColor: 'rgba(249, 115, 22, 0.2)',
                    borderWidth: 2,
                    tension: 0.3,
                    yAxisID: 'y'
                },
                {
                    label: 'Releases Count',
                    data: counts,
                    type: 'bar',
                    backgroundColor: 'rgba(203, 213, 225, 0.5)', // Slate-300
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        afterBody: function (context) {
                            const year = context[0].label;
                            const titles = yearGroups[year].titles.slice(0, 5); // Show top 5
                            return `Releases: ${titles.join(', ')}${titles.length > 5 ? '...' : ''}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Avg Score' },
                    min: 6,
                    max: 10
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: { display: true, text: 'Count' },
                    grid: { drawOnChartArea: false },
                    min: 0
                }
            }
        }
    });
}
