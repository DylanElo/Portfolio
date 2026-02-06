document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('data/dashboard_data.json');
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        const data = await response.json();
        initDashboard(data);
    } catch (error) {
        const container = document.querySelector('.container');
        if (container) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'card';
            errorDiv.style.cssText = 'background:#fee2e2;border-left:4px solid #ef4444;padding:1.5rem;margin:1rem 0;';
            errorDiv.textContent = 'Failed to load dashboard data. Please try refreshing the page.';
            container.prepend(errorDiv);
        }
    }
});

function initDashboard(data) {
    renderKPIs(data);
    renderTrendChart(data.monthly_trend);
    renderMarketChart(data.top_countries_2024);
    renderSeasonalityChart(data.seasonality);
    renderFXChart(data.fx_impact);
    renderWeatherChart(data.weather_risk);
    renderFlightsChart(data.airport_capacity);
    // NEW: Prescriptive analytics
    renderMarketingChart(data.marketing_recommendations);
    renderStaffingChart(data.staffing_forecast);
    renderCapacityChart(data.capacity_health);
}

function renderKPIs(data) {
    // Calculate Total 2024
    const total2024 = data.monthly_trend
        .filter(d => d.year === 2024)
        .reduce((sum, d) => sum + d.total_visitors, 0);

    document.getElementById('kpi-total-2024').textContent = total2024.toLocaleString();

    // Top Market
    const topMarket = data.top_countries_2024[0];
    document.getElementById('kpi-top-market').textContent = topMarket ? topMarket.country_name_en : "N/A";

    // Recovery (2024 vs 2019) - simplified
    const total2019 = data.monthly_trend
        .filter(d => d.year === 2019)
        .reduce((sum, d) => sum + d.total_visitors, 0);

    // Assuming 2024 is full year or YTD comparison (simplified for mock)
    const recovery = total2019 > 0 ? (total2024 / total2019 * 100).toFixed(1) + "%" : "N/A";
    document.getElementById('kpi-recovery').textContent = recovery;
}

function renderTrendChart(trendData) {
    const ctx = document.getElementById('trendChart').getContext('2d');

    const labels = trendData.map(d => `${d.year}-${String(d.month).padStart(2, '0')}`);
    const values = trendData.map(d => d.total_visitors);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Visitors',
                data: values,
                borderColor: '#e60012',
                backgroundColor: 'rgba(230, 0, 18, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderMarketChart(marketData) {
    const ctx = document.getElementById('marketChart').getContext('2d');

    const labels = marketData.map(d => d.country_name_en);
    const values = marketData.map(d => d.total_visitors);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Visitors (2024)',
                data: values,
                backgroundColor: '#36a2eb'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderSeasonalityChart(seasonalityData) {
    const ctx = document.getElementById('seasonalityChart').getContext('2d');

    // Aggregate by country and month
    const countryMonthMap = {};
    seasonalityData.forEach(d => {
        if (!countryMonthMap[d.country_name_en]) {
            countryMonthMap[d.country_name_en] = Array(12).fill(0);
        }
        countryMonthMap[d.country_name_en][d.month - 1] = d.avg_visitors;
    });

    // Pick top 5 markets by total visitors
    const topCountries = Object.entries(countryMonthMap)
        .map(([country, months]) => ({
            country,
            months,
            total: months.reduce((sum, v) => sum + v, 0)
        }))
        .sort((a, b) => b.total - a.total)
        .slice(0, 5);

    const monthLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const colors = ['#36a2eb', '#ff6384', '#4bc0c0', '#ff9f40', '#9966ff'];

    const datasets = topCountries.map((item, idx) => ({
        label: item.country,
        data: item.months,
        backgroundColor: colors[idx % colors.length],
        stack: 'seasonality'
    }));

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: monthLabels,
            datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { stacked: true },
                y: { stacked: true, beginAtZero: true, title: { display: true, text: 'Avg Visitors per Month' } }
            },
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: (context) => `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`
                    }
                }
            }
        }
    });
}

function renderFXChart(fxData) {
    const ctx = document.getElementById('fxChart').getContext('2d');

    // Filter out nulls if any
    const validData = fxData.filter(d => d.usd_rate && d.total_visitors);

    const labels = validData.map(d => `${d.year}-${String(d.month).padStart(2, '0')}`);
    const visitors = validData.map(d => d.total_visitors);
    const rates = validData.map(d => d.usd_rate);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Total Visitors',
                    data: visitors,
                    borderColor: '#36a2eb',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    yAxisID: 'y',
                    order: 2
                },
                {
                    label: 'JPY per USD',
                    data: rates,
                    borderColor: '#e60012',
                    borderDash: [5, 5],
                    yAxisID: 'y1',
                    order: 1
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
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Visitors' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: { display: true, text: 'JPY/USD Rate' },
                    grid: {
                        drawOnChartArea: false,
                    },
                },
            }
        }
    });
}

function renderWeatherChart(weatherData) {
    const ctx = document.getElementById('weatherChart').getContext('2d');

    // Filter last 2 years for clarity
    const recentData = weatherData.filter(d => d.year >= 2023);

    const labels = recentData.map(d => `${d.year}-${String(d.month).padStart(2, '0')}`);
    const temp = recentData.map(d => d.avg_max_temp);
    const heatwave = recentData.map(d => d.heatwave_days);
    const rain = recentData.map(d => d.rainy_days);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Avg Max Temp (°C)',
                    data: temp,
                    type: 'line',
                    borderColor: '#ff9f40',
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    yAxisID: 'y',
                    tension: 0.4
                },
                {
                    label: 'Heatwave Days',
                    data: heatwave,
                    backgroundColor: '#ff6384',
                    yAxisID: 'y1'
                },
                {
                    label: 'Rainy/Typhoon Days',
                    data: rain,
                    backgroundColor: '#4bc0c0',
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
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Temperature (°C)' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: { display: true, text: 'Days Count' },
                    grid: { drawOnChartArea: false }
                },
            }
        }
    });
}

function renderFlightsChart(flightsData) {
    const ctx = document.getElementById('flightsChart').getContext('2d');

    // Group by Month, then Airport
    const months = [...new Set(flightsData.map(d => `${d.year}-${String(d.month).padStart(2, '0')}`))];
    const airports = [...new Set(flightsData.map(d => d.airport_code))];

    const datasets = airports.map((code, index) => {
        const colors = ['#36a2eb', '#ff6384', '#4bc0c0', '#ff9f40', '#9966ff'];
        return {
            label: code,
            data: months.map(m => {
                const record = flightsData.find(d => `${d.year}-${String(d.month).padStart(2, '0')}` === m && d.airport_code === code);
                return record ? record.total_flights : 0;
            }),
            backgroundColor: colors[index % colors.length]
        };
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { stacked: true },
                y: { stacked: true, beginAtZero: true }
            }
        }
    });
}

// NEW: Marketing Recommendations Chart
function renderMarketingChart(marketingData) {
    const ctx = document.getElementById('marketingChart').getContext('2d');

    const labels = marketingData.map(d => d.country_name_en);
    const growthRates = marketingData.map(d => d.growth_rate);
    const colors = marketingData.map(d => {
        if (d.recommendation === 'High Priority') return '#16a085';
        if (d.recommendation === 'Medium Priority') return '#3498db';
        return '#95a5a6';
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'YoY Growth Rate (%)',
                data: growthRates,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (context) => `${context.parsed.x}% growth`
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Growth Rate (%)' },
                    beginAtZero: true
                }
            }
        }
    });
}

// NEW: Staffing Forecast Chart
function renderStaffingChart(staffingData) {
    const ctx = document.getElementById('staffingChart').getContext('2d');

    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const labels = staffingData.map(d => monthNames[d.month - 1]);
    const projectedVisitors = staffingData.map(d => d.projected_visitors);
    const recommendedStaff = staffingData.map(d => d.recommended_staff);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Projected Visitors',
                    data: projectedVisitors,
                    backgroundColor: '#3498db',
                    yAxisID: 'y',
                    order: 2
                },
                {
                    label: 'Recommended Staff',
                    data: recommendedStaff,
                    borderColor: '#e74c3c',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    type: 'line',
                    yAxisID: 'y1',
                    order: 1,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    title: { display: true, text: 'Visitors' },
                    beginAtZero: true
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    title: { display: true, text: 'Staff Count' },
                    grid: { drawOnChartArea: false },
                    beginAtZero: true
                }
            }
        }
    });
}

// NEW: Capacity Health Chart
function renderCapacityChart(capacityData) {
    const ctx = document.getElementById('capacityChart').getContext('2d');

    const labels = capacityData.map(d => `${d.airport_code} (${d.airport_name})`);
    const utilization = capacityData.map(d => d.utilization_pct);
    const colors = capacityData.map(d => {
        if (d.status === 'Critical') return '#e74c3c';
        if (d.status === 'Warning') return '#f39c12';
        return '#2ecc71';
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Utilization (%)',
                data: utilization,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const item = capacityData[context.dataIndex];
                            return [
                                `Utilization: ${item.utilization_pct}%`,
                                `Current: ${item.current_flights} flights/month`,
                                `Capacity: ${item.max_capacity} flights/month`,
                                `Status: ${item.status}`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    max: 100,
                    title: { display: true, text: 'Utilization (%)' },
                    beginAtZero: true
                }
            }
        }
    });
}

