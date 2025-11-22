import './dashboard-style.css';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

let rawData = null;
let charts = {
  trend: null,
  platform: null,
  platformBattle: null,
  heatmap: null,
  scatter: null,
  completion: null,
  radar: null,
  region: null,
  legacy: null,
  studioShare: null,
  studioPerformance: null,
  studioSentiment: null,
  studioOutput: null
};
let activeTab = 'executive';

// Theme Colors
const colors = {
  primary: '#2563eb',
  secondary: '#0ea5e9',
  accent: '#8b5cf6',
  success: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
  slate: '#64748b',
  grid: '#e2e8f0'
};

Chart.defaults.color = colors.slate;
Chart.defaults.borderColor = colors.grid;
Chart.defaults.font.family = "'Inter', sans-serif";

// Aggregation Logic
function aggregateFranchises(data) {
  // Simplified to avoid build errors for now
  return data;
}

// Utility function
function formatValue(val, type) {
  if (!val && val !== 0) return '-';
  if (type === 'currency') return '$' + val.toLocaleString(undefined, { maximumFractionDigits: 0 });
  if (type === 'number') return val.toLocaleString();
  if (type === 'decimal') return val.toFixed(2);
  return val;
}

// Initialize Dashboard
function initDashboard(data) {
  // Populate Filters (Grouped by Era)
  const animeFilter = document.getElementById('animeFilter');
  animeFilter.innerHTML = '<option value="all">All Franchises</option>';

  const modernGroup = document.createElement('optgroup');
  modernGroup.label = "Modern Era (2016-Present)";
  const legacyGroup = document.createElement('optgroup');
  legacyGroup.label = "Legacy Era (2000-2015)";

  const sortedAnime = (data.anime_performance || []).sort((a, b) => a.title.localeCompare(b.title));

  sortedAnime.forEach(a => {
    const opt = document.createElement('option');
    opt.value = a.title;
    opt.textContent = a.title;

    if (a.category === 'modern') modernGroup.appendChild(opt);
    else legacyGroup.appendChild(opt);
  });

  animeFilter.appendChild(modernGroup);
  animeFilter.appendChild(legacyGroup);

  const platformContainer = document.getElementById('platformFilters');
  if (data.platform_split) {
    data.platform_split.forEach(p => {
      const name = p.platform_name || p.name || 'Unknown';
      const div = document.createElement('div');
      div.innerHTML = `
        <label class="inline-flex items-center bg-slate-100 px-3 py-1 rounded-full cursor-pointer hover:bg-slate-200 transition">
          <input type="checkbox" checked value="${name}" class="platform-checkbox form-checkbox h-4 w-4 text-blue-600 border-slate-300 rounded focus:ring-blue-500">
          <span class="ml-2 text-sm text-slate-700">${name}</span>
        </label>
      `;
      platformContainer.appendChild(div);
    });
  }

  // Listeners
  document.getElementById('startDate').addEventListener('change', applyFilters);
  document.getElementById('endDate').addEventListener('change', applyFilters);
  document.getElementById('animeFilter').addEventListener('change', applyFilters);
  document.getElementById('resetFilters').addEventListener('click', resetFilters);
  document.querySelectorAll('.platform-checkbox').forEach(cb => cb.addEventListener('change', applyFilters));

  // Tab switching
  document.querySelectorAll('[onclick^="switchTab"]').forEach(el => {
    const tabId = el.getAttribute('onclick').match(/switchTab\('(.+)'\)/)[1];
    el.onclick = () => switchTab(tabId);
  });

  // Initial Render
  renderAllCharts(data);
}

function switchTab(tabId) {
  activeTab = tabId;
  // Update Nav
  document.querySelectorAll('.nav-link').forEach(el => {
    el.classList.remove('active', 'text-slate-900');
    el.classList.add('text-slate-500');
  });
  const activeLink = document.getElementById(`tab-${tabId}`);
  activeLink.classList.add('active', 'text-slate-900');
  activeLink.classList.remove('text-slate-500');

  // Update Content
  ['executive', 'strategy', 'platform', 'studio'].forEach(id => {
    const el = document.getElementById(`view-${id}`);
    if (id === tabId) {
      el.classList.remove('hidden');
    } else {
      el.classList.add('hidden');
    }
  });
}

function resetFilters() {
  // Reset Dates
  if (rawData.daily_anime_trend && rawData.daily_anime_trend.length) {
    const dates = rawData.daily_anime_trend.map(d => d.date).sort();
    document.getElementById('startDate').value = dates[0];
    document.getElementById('endDate').value = dates[dates.length - 1];
  }
  // Reset anime filter
  document.getElementById('animeFilter').value = 'all';
  // Reset platform checkboxes
  document.querySelectorAll('.platform-checkbox').forEach(cb => cb.checked = true);
  applyFilters();
}

function updateHighlights(animeData) {
  if (!animeData.length) return;

  // Top Revenue
  const top = [...animeData].sort((a, b) => b.revenue - a.revenue)[0];
  document.getElementById('topPerformerName').textContent = top.title;
  document.getElementById('topPerformerName').title = top.title;
  document.getElementById('topPerformerValue').textContent = formatValue(top.revenue, 'currency');

  // Worst Sentiment
  const worst = [...animeData].sort((a, b) => a.sentiment - b.sentiment)[0];
  document.getElementById('worstPerformerName').textContent = worst.title;
  document.getElementById('worstPerformerValue').textContent = worst.sentiment.toFixed(2) + ' Score';
}

function renderAllCharts(data) {
  renderKPIs(data.kpis || {});
  renderTrendChart(data.daily_trend || []);
  renderPlatformChart(data.platform_split || []);
  renderPlatformBattleChart(data.platform_split || []);
  renderScatterChart(data.scatter_plot || []);
  renderHeatmap(data.heatmap || []);
  renderCompletionChart(data.anime_performance || []);
  renderRadarChart(data.anime_performance || []);
  renderRegionChart(data.region_split || []);
  renderLegacyChart(data.anime_performance || []);
  updateAnimeTable(data.anime_performance || []);
  renderStudioCharts(data.studio_comparison || []);

  applyFilters();
}

// Chart Renderers
function renderKPIs(kpis) {
  const items = [
    { label: 'Total Revenue', value: kpis.total_revenue, fmt: 'currency', icon: '💰', color: 'text-blue-600', bg: 'bg-blue-50' },
    { label: 'Total Views', value: kpis.total_views, fmt: 'number', icon: '👁️', color: 'text-violet-600', bg: 'bg-violet-50' },
    { label: 'Watch Time (Hrs)', value: kpis.total_watch_time, fmt: 'number', icon: '⏱️', color: 'text-emerald-600', bg: 'bg-emerald-50' },
    { label: 'Avg Sentiment', value: kpis.avg_sentiment, fmt: 'decimal', icon: '😊', color: 'text-amber-600', bg: 'bg-amber-50' }
  ];

  document.getElementById('kpiContainer').innerHTML = items.map(item => `
    <div class="card p-6 flex items-center space-x-4">
            <div class="p-3 rounded-full ${item.bg} ${item.color} text-2xl">
                ${item.icon}
            </div>
            <div>
                <p class="text-sm font-medium text-slate-500">${item.label}</p>
                <p class="text-2xl font-bold text-slate-900">${formatValue(item.value, item.fmt)}</p>
            </div>
        </div>
  `).join('');
}

function renderTrendChart(data) {
  if (charts.trend) charts.trend.destroy();
  const ctx = document.getElementById('trendChart').getContext('2d');
  charts.trend = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        { label: 'Revenue ($)', data: [], borderColor: colors.primary, backgroundColor: 'rgba(37, 99, 235, 0.1)', fill: true, tension: 0.3 },
        { label: 'Views', data: [], borderColor: colors.secondary, backgroundColor: 'rgba(14, 165, 233, 0.1)', fill: true, tension: 0.3, yAxisID: 'y1' }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      scales: {
        y: { position: 'left', grid: { borderDash: [4, 4] } },
        y1: { position: 'right', grid: { display: false } },
        x: { grid: { display: false } }
      }
    }
  });
}

function updateTrendChart(data) {
  if (!charts.trend) return;
  charts.trend.data.labels = data.map(d => d.date);
  charts.trend.data.datasets[0].data = data.map(d => d.revenue);
  charts.trend.data.datasets[1].data = data.map(d => d.views);
  charts.trend.update();
}

function renderPlatformChart(data) {
  if (charts.platform) charts.platform.destroy();
  const ctx = document.getElementById('platformChart').getContext('2d');
  charts.platform = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: [],
      datasets: [{ data: [], backgroundColor: [colors.primary, colors.secondary, colors.accent, colors.success, colors.warning] }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
  });
}

function updatePlatformChart(data) {
  if (!charts.platform) return;
  charts.platform.data.labels = data.map(d => d.platform_name || d.name);
  charts.platform.data.datasets[0].data = data.map(d => d.revenue || d.value);
  charts.platform.update();
}

function renderPlatformBattleChart(data) {
  if (charts.platformBattle) charts.platformBattle.destroy();
  const ctx = document.getElementById('platformBattleChart').getContext('2d');
  charts.platformBattle = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [
        { label: 'Revenue ($)', data: [], backgroundColor: colors.primary, yAxisID: 'y', order: 1 },
        { label: 'Views', data: [], backgroundColor: colors.secondary, yAxisID: 'y1', order: 2 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { type: 'linear', display: true, position: 'left', title: { display: true, text: 'Revenue ($)' } },
        y1: { type: 'linear', display: true, position: 'right', grid: { drawOnChartArea: false }, title: { display: true, text: 'Views' } }
      }
    }
  });
}

function updatePlatformBattleChart(data) {
  if (!charts.platformBattle) return;
  charts.platformBattle.data.labels = data.map(d => d.platform_name || d.name);
  charts.platformBattle.data.datasets[0].data = data.map(d => d.revenue || d.value);
  charts.platformBattle.data.datasets[1].data = data.map(d => d.views);
  charts.platformBattle.update();
}

function renderScatterChart(data) {
  if (charts.scatter) charts.scatter.destroy();
  const ctx = document.getElementById('scatterChart').getContext('2d');
  charts.scatter = new Chart(ctx, {
    type: 'bubble',
    data: { datasets: [{ label: 'Franchises', data: [], backgroundColor: 'rgba(239, 68, 68, 0.6)', borderColor: colors.danger }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        tooltip: { callbacks: { label: c => `${c.raw.anime}: ROI ${c.raw.y.toFixed(1)}%, Filler ${c.raw.x}%` } },
        legend: { display: false }
      },
      scales: {
        x: { title: { display: true, text: 'Filler %' } },
        y: { title: { display: true, text: 'ROI %' } }
      }
    }
  });
}

function updateScatterChart(data) {
  if (!charts.scatter) return;
  charts.scatter.data.datasets[0].data = data.map(d => ({
    x: d.filler_percentage, y: d.roi_percentage, r: Math.sqrt(d.total_views) / 2500, anime: d.title
  }));
  charts.scatter.update();
}

function renderHeatmap(data) {
  if (charts.heatmap) charts.heatmap.destroy();
  const ctx = document.getElementById('heatmapChart').getContext('2d');
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const sorted = [...data].sort((a, b) => days.indexOf(a.day_name) - days.indexOf(b.day_name));

  charts.heatmap = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sorted.map(d => d.day_name),
      datasets: [{ label: 'Avg Views', data: sorted.map(d => d.views), backgroundColor: colors.success, borderRadius: 4 }]
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
  });
}

function updateHeatmap(data) {
  // Heatmap is static/precomputed, no need to update
}

function renderCompletionChart(data) {
  if (charts.completion) charts.completion.destroy();
  const ctx = document.getElementById('completionChart').getContext('2d');
  charts.completion = new Chart(ctx, {
    type: 'bar',
    data: { labels: [], datasets: [{ label: 'Retention Rate %', data: [], backgroundColor: colors.warning, borderRadius: 4 }] },
    options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y', scales: { x: { max: 100 } } }
  });
}

function updateCompletionChart(data) {
  if (!charts.completion) return;
  const sorted = [...data].sort((a, b) => b.completion_rate - a.completion_rate);
  charts.completion.data.labels = sorted.map(d => d.title);
  charts.completion.data.datasets[0].data = sorted.map(d => d.completion_rate * 100);
  charts.completion.update();
}

function renderRadarChart(data) {
  if (charts.radar) charts.radar.destroy();
  const ctx = document.getElementById('radarChart').getContext('2d');
  charts.radar = new Chart(ctx, {
    type: 'radar',
    data: { labels: ['Revenue', 'Views', 'Sentiment', 'ROI', 'Retention'], datasets: [] },
    options: {
      responsive: true, maintainAspectRatio: false,
      elements: { line: { borderWidth: 2 } }
    }
  });
}

function updateRadarChart(data) {
  if (!charts.radar) return;
  const top3 = [...data].sort((a, b) => b.revenue - a.revenue).slice(0, 3);

  const maxRev = Math.max(...data.map(d => d.revenue)) || 1;
  const maxView = Math.max(...data.map(d => d.views)) || 1;

  charts.radar.data.datasets = top3.map((d, i) => {
    const color = [colors.primary, colors.accent, colors.success][i % 3];
    return {
      label: d.title,
      data: [
        (d.revenue / maxRev) * 100,
        (d.views / maxView) * 100,
        d.sentiment * 100,
        Math.max(0, d.roi) * 2,
        d.completion_rate * 100
      ],
      borderColor: color,
      backgroundColor: color + '33'
    };
  });
  charts.radar.update();
}

function renderRegionChart(data) {
  if (charts.region) charts.region.destroy();
  const ctx = document.getElementById('regionChart').getContext('2d');
  const sorted = [...data].sort((a, b) => b.views - a.views);

  charts.region = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sorted.map(d => d.region_name),
      datasets: [
        {
          label: 'Views',
          data: sorted.map(d => d.views),
          backgroundColor: colors.secondary,
          yAxisID: 'y'
        },
        {
          label: 'Revenue',
          data: sorted.map(d => d.revenue),
          backgroundColor: colors.primary,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { type: 'linear', display: true, position: 'left' },
        y1: { type: 'linear', display: true, position: 'right', grid: { drawOnChartArea: false } }
      }
    }
  });
}

function updateRegionChart(data) {
  if (!charts.region) return;
  const sorted = [...data].sort((a, b) => b.views - a.views);

  charts.region.data.labels = sorted.map(d => d.region_name);
  charts.region.data.datasets[0].data = sorted.map(d => d.views);
  charts.region.data.datasets[1].data = sorted.map(d => d.revenue);
  charts.region.update();
}

function renderLegacyChart() {
  if (charts.legacy) charts.legacy.destroy();
  const ctx = document.getElementById('legacyChart').getContext('2d');
  charts.legacy = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Legacy', 'Gen 1', 'Gen 2', 'Gen 3'],
      datasets: [{
        label: 'Avg Revenue (USD)',
        data: [0, 0, 0, 0],
        backgroundColor: ['#6366F1', '#10B981', '#F59E0B', '#EF4444'],
        borderColor: ['#4F46E5', '#059669', '#D97706', '#DC2626'],
        borderWidth: 1,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return '$' + (value / 1_000_000).toLocaleString() + 'M';
            },
          },
        },
      },
    },
  });
}

function updateLegacyChart(filteredPerformance) {
  if (!charts.legacy) return;
  const genMap = {
    'Legacy (Pre-2016)': 'Legacy',
    'Gen 1 (2016-2019)': 'Gen 1',
    'Gen 2 (2020-2022)': 'Gen 2',
    'Gen 3 (2023-Present)': 'Gen 3',
  };
  const sums = {
    Legacy: 0,
    'Gen 1': 0,
    'Gen 2': 0,
    'Gen 3': 0
  };
  const counts = {
    Legacy: 0,
    'Gen 1': 0,
    'Gen 2': 0,
    'Gen 3': 0
  };
  filteredPerformance.forEach(p => {
    const genKey = genMap[p.generation] || 'Legacy';
    sums[genKey] += p.revenue;
    counts[genKey] += 1;
  });
  const averages = [
    counts.Legacy ? sums.Legacy / counts.Legacy : 0,
    counts['Gen 1'] ? sums['Gen 1'] / counts['Gen 1'] : 0,
    counts['Gen 2'] ? sums['Gen 2'] / counts['Gen 2'] : 0,
    counts['Gen 3'] ? sums['Gen 3'] / counts['Gen 3'] : 0,
  ];
  charts.legacy.data.datasets[0].data = averages;
  charts.legacy.update();
}

function renderStudioCharts(data) {
  if (charts.studioShare) charts.studioShare.destroy();
  if (charts.studioPerformance) charts.studioPerformance.destroy();
  if (charts.studioSentiment) charts.studioSentiment.destroy();
  if (charts.studioOutput) charts.studioOutput.destroy();

  if (!data || !data.length) return;

  // 1. Market Share (Revenue)
  const ctxShare = document.getElementById('studioShareChart').getContext('2d');
  charts.studioShare = new Chart(ctxShare, {
    type: 'doughnut',
    data: {
      labels: data.map(d => d.studio),
      datasets: [{
        data: data.map(d => d.total_revenue),
        backgroundColor: [colors.primary, colors.secondary, colors.accent, colors.success, colors.warning, colors.danger],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' },
        title: { display: true, text: 'Total Revenue Share' }
      }
    }
  });

  // 2. Performance (Revenue vs Views)
  const ctxPerf = document.getElementById('studioPerformanceChart').getContext('2d');
  charts.studioPerformance = new Chart(ctxPerf, {
    type: 'bar',
    data: {
      labels: data.map(d => d.studio),
      datasets: [
        {
          label: 'Revenue ($)',
          data: data.map(d => d.total_revenue),
          backgroundColor: colors.primary,
          yAxisID: 'y',
          order: 1
        },
        {
          label: 'Views',
          data: data.map(d => d.total_views),
          backgroundColor: colors.secondary,
          yAxisID: 'y1',
          order: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { type: 'linear', display: true, position: 'left', title: { display: true, text: 'Revenue ($)' } },
        y1: { type: 'linear', display: true, position: 'right', grid: { drawOnChartArea: false }, title: { display: true, text: 'Views' } }
      }
    }
  });

  // 3. Sentiment
  const ctxSent = document.getElementById('studioSentimentChart').getContext('2d');
  charts.studioSentiment = new Chart(ctxSent, {
    type: 'bar',
    data: {
      labels: data.map(d => d.studio),
      datasets: [{
        label: 'Avg MAL Score',
        data: data.map(d => d.avg_sentiment * 10), // Scale back to 1-10
        backgroundColor: data.map(d => d.studio === 'Studio Pierrot' ? colors.primary : colors.slate),
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { y: { min: 5, max: 10 } },
      plugins: { legend: { display: false } }
    }
  });

  // 4. Output
  const ctxOut = document.getElementById('studioOutputChart').getContext('2d');
  charts.studioOutput = new Chart(ctxOut, {
    type: 'bar',
    data: {
      labels: data.map(d => d.studio),
      datasets: [{
        label: 'Titles Analyzed',
        data: data.map(d => d.title_count),
        backgroundColor: colors.accent,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } }
    }
  });
}

function updateAnimeTable(data) {
  const tbody = document.getElementById('animeTableBody');
  const sorted = [...data].sort((a, b) => b.revenue - a.revenue);

  tbody.innerHTML = sorted.map(anime => `
    <tr class="hover:bg-slate-50">
            <td class="px-6 py-3 font-medium text-slate-900">${anime.title}</td>
            <td class="px-6 py-3 text-right">${formatValue(anime.revenue, 'currency')}</td>
            <td class="px-6 py-3 text-right">${formatValue(anime.views, 'number')}</td>
            <td class="px-6 py-3 text-center">${anime.sentiment.toFixed(2)}</td>
            <td class="px-6 py-3 text-center">${anime.roi.toFixed(1)}%</td>
        </tr>
  `).join('');
}

// Apply Filters
function applyFilters() {
  const startDate = document.getElementById('startDate').value;
  const endDate = document.getElementById('endDate').value;
  const selectedAnime = document.getElementById('animeFilter').value;
  const selectedPlatforms = Array.from(document.querySelectorAll('.platform-checkbox:checked')).map(cb => cb.value);

  // Filter daily_anime_trend data
  let filteredTrend = rawData.daily_anime_trend || [];
  if (startDate && endDate) {
    filteredTrend = filteredTrend.filter(d => d.date >= startDate && d.date <= endDate);
  }
  if (selectedAnime !== 'all') {
    filteredTrend = filteredTrend.filter(d => d.title === selectedAnime);
  }

  // Aggregate by date only
  const trendByDate = {};
  filteredTrend.forEach(entry => {
    if (!trendByDate[entry.date]) trendByDate[entry.date] = { date: entry.date, views: 0, revenue: 0 };
    trendByDate[entry.date].views += entry.views;
    trendByDate[entry.date].revenue += entry.revenue;
  });
  const aggregatedTrend = Object.values(trendByDate).sort((a, b) => a.date.localeCompare(b.date));

  // Filter anime_performance data
  let filteredPerformance = rawData.anime_performance || [];
  if (selectedAnime !== 'all') {
    filteredPerformance = filteredPerformance.filter(d => d.title === selectedAnime);
  }

  // Filter scatter_plot data
  let filteredScatter = rawData.scatter_plot || [];
  if (selectedAnime !== 'all') {
    filteredScatter = filteredScatter.filter(d => d.title === selectedAnime);
  }

  // Filter platform_split data
  let filteredPlatform = (rawData.platform_split || []).filter(p => selectedPlatforms.includes(p.platform_name || p.name));

  // Filter Studio Comparison Data
  let filteredStudioData = [];
  if (rawData.competitor_raw_data) {
    // const startYear = startDate ? new Date(startDate).getFullYear() : 2000;
    // const endYear = endDate ? new Date(endDate).getFullYear() : 2024;

    // SHOW ALL DATA by default (Fix for "only 2 studios" issue)
    // The date filter was restricting to only anime starting in the last 30 days (2024),
    // which hid 90% of the data.
    const filteredRaw = rawData.competitor_raw_data; // .filter(d => d.start_year >= startYear && d.start_year <= endYear);

    // Aggregate by Studio
    const studioAgg = {};
    filteredRaw.forEach(d => {
      if (!studioAgg[d.studio]) {
        studioAgg[d.studio] = {
          studio: d.studio,
          total_revenue: 0,
          total_views: 0,
          sentiment_sum: 0,
          count: 0
        };
      }
      studioAgg[d.studio].total_revenue += d.revenue;
      studioAgg[d.studio].total_views += d.views;
      studioAgg[d.studio].sentiment_sum += d.sentiment;
      studioAgg[d.studio].count++;
    });

    filteredStudioData = Object.values(studioAgg).map(s => ({
      studio: s.studio,
      total_revenue: s.total_revenue,
      total_views: s.total_views,
      avg_sentiment: s.count ? s.sentiment_sum / s.count : 0,
      title_count: s.count
    }));
  } else {
    filteredStudioData = rawData.studio_comparison || [];
  }

  // Calculate filtered ratio for static charts
  const totalViews = (rawData.daily_anime_trend || []).reduce((sum, d) => sum + d.views, 0);
  const filteredViews = filteredTrend.reduce((sum, d) => sum + d.views, 0);
  const filterRatio = totalViews > 0 ? filteredViews / totalViews : 1;

  // Apply filter ratio to heatmap and region_split
  const filteredHeatmap = (rawData.heatmap || []).map(d => ({ ...d, views: d.views * filterRatio }));
  const filteredRegion = (rawData.region_split || []).map(d => ({ ...d, views: d.views * filterRatio, revenue: d.revenue * filterRatio }));

  // Recalculate KPIs based on filtered trend data
  const filteredKpis = {
    total_revenue: filteredTrend.reduce((sum, d) => sum + d.revenue, 0),
    total_views: filteredTrend.reduce((sum, d) => sum + d.views, 0),
    total_watch_time: filteredPerformance.reduce((sum, d) => sum + (d.views * 20 / 60), 0), // Estimate
    avg_sentiment: filteredPerformance.length ? filteredPerformance.reduce((sum, d) => sum + d.sentiment, 0) / filteredPerformance.length : 0
  };

  // Update charts
  renderKPIs(filteredKpis);
  updateTrendChart(aggregatedTrend);
  updatePlatformChart(filteredPlatform);
  updatePlatformBattleChart(filteredPlatform);
  updateScatterChart(filteredScatter);
  updateHeatmap(filteredHeatmap);
  updateCompletionChart(filteredPerformance);
  updateRadarChart(filteredPerformance);
  updateRegionChart(filteredRegion);
  updateLegacyChart(filteredPerformance);
  updateAnimeTable(filteredPerformance);
  renderStudioCharts(filteredStudioData);
  updateHighlights(filteredPerformance);
}

// Data Loading
fetch('data.json')
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then(data => {
    data = aggregateFranchises(data);
    rawData = data;

    // Set default date range
    if (data.daily_anime_trend && data.daily_anime_trend.length) {
      const dates = data.daily_anime_trend.map(d => d.date).sort();
      document.getElementById('startDate').value = dates[0];
      document.getElementById('endDate').value = dates[dates.length - 1];
    }

    document.getElementById('loadingScreen').style.display = 'none';
    document.getElementById('dashboardContent').style.display = 'block';
    initDashboard(data);
  })
  .catch(err => {
    console.error(err);
    document.getElementById('loadingScreen').innerHTML = `<p class="text-red-500">Error loading data: ${err.message}</p>`;
  });
