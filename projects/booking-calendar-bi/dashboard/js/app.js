document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('data/dashboard_data.json');
        const data = await response.json();
        initDashboard(data);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
});

function initDashboard(data) {
    renderKPIs(data.kpis);
    renderMonthlyTrend(data.monthly_trend);
    renderYoY(data.yearly_summary);
    renderServiceBreakdown(data.service_breakdown);
    renderTopClients(data.top_clients);
    renderAgentPerformance(data.agent_performance);
    renderDestinations(data.destination_performance);
    renderStatusChart(data.status_breakdown);
    renderLeadTime(data.lead_time);
    renderSeasonality(data.seasonality);
}

// --- KPIs ---
function renderKPIs(kpis) {
    document.getElementById('kpi-bookings').textContent =
        kpis.total_bookings ? kpis.total_bookings.toLocaleString() : 'N/A';
    document.getElementById('kpi-revenue').textContent =
        kpis.total_revenue ? '\u20ac' + Number(kpis.total_revenue).toLocaleString() : 'N/A';
    document.getElementById('kpi-pax').textContent =
        kpis.total_pax ? kpis.total_pax.toLocaleString() : 'N/A';
    document.getElementById('kpi-margin').textContent =
        kpis.avg_margin_pct ? kpis.avg_margin_pct + '%' : 'N/A';
    document.getElementById('kpi-avg-value').textContent =
        kpis.avg_booking_value ? '\u20ac' + Number(kpis.avg_booking_value).toLocaleString() : 'N/A';
}

// --- Monthly Revenue + Booking Trend ---
function renderMonthlyTrend(data) {
    const ctx = document.getElementById('monthlyTrendChart').getContext('2d');

    const labels = data.map(d => d.year + '-' + String(d.month).padStart(2, '0'));
    const revenue = data.map(d => d.total_revenue);
    const bookings = data.map(d => d.total_bookings);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Revenue (\u20ac)',
                    data: revenue,
                    backgroundColor: 'rgba(37, 99, 235, 0.6)',
                    yAxisID: 'y',
                    order: 2
                },
                {
                    label: 'Bookings',
                    data: bookings,
                    borderColor: '#ff6384',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    type: 'line',
                    yAxisID: 'y1',
                    tension: 0.4,
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    title: { display: true, text: 'Revenue (\u20ac)' },
                    beginAtZero: true,
                    ticks: {
                        callback: v => '\u20ac' + (v / 1000).toFixed(0) + 'k'
                    }
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    title: { display: true, text: 'Bookings' },
                    grid: { drawOnChartArea: false },
                    beginAtZero: true
                }
            }
        }
    });
}

// --- Year-over-Year ---
function renderYoY(data) {
    const ctx = document.getElementById('yoyChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.year),
            datasets: [
                {
                    label: 'Revenue (\u20ac)',
                    data: data.map(d => d.total_revenue),
                    backgroundColor: '#2563eb',
                    yAxisID: 'y'
                },
                {
                    label: 'Margin (\u20ac)',
                    data: data.map(d => d.total_margin),
                    backgroundColor: '#16a085',
                    yAxisID: 'y'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: v => '\u20ac' + (v / 1000000).toFixed(1) + 'M'
                    }
                }
            }
        }
    });
}

// --- Service Category ---
function renderServiceBreakdown(data) {
    const ctx = document.getElementById('serviceChart').getContext('2d');
    const colors = ['#2563eb', '#ff6384', '#4bc0c0', '#ff9f40'];

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.service_category),
            datasets: [{
                data: data.map(d => d.total_revenue),
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: ctx => {
                            const item = data[ctx.dataIndex];
                            return [
                                ctx.label + ': \u20ac' + Number(item.total_revenue).toLocaleString(),
                                'Bookings: ' + item.booking_count,
                                'Margin: ' + item.avg_margin_pct + '%'
                            ];
                        }
                    }
                }
            }
        }
    });
}

// --- Top Clients ---
function renderTopClients(data) {
    const ctx = document.getElementById('clientChart').getContext('2d');

    const typeColors = {
        'Agency': '#2563eb',
        'Corporate': '#16a085',
        'Individual': '#ff9f40'
    };

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.client_name),
            datasets: [{
                label: 'Revenue (\u20ac)',
                data: data.map(d => d.total_revenue),
                backgroundColor: data.map(d => typeColors[d.client_type] || '#95a5a6')
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
                        label: ctx => {
                            const item = data[ctx.dataIndex];
                            return [
                                'Revenue: \u20ac' + Number(item.total_revenue).toLocaleString(),
                                'Type: ' + item.client_type,
                                'Region: ' + item.client_region,
                                'Bookings: ' + item.booking_count,
                                'Margin: ' + item.avg_margin_pct + '%'
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: v => '\u20ac' + (v / 1000).toFixed(0) + 'k'
                    }
                }
            }
        }
    });
}

// --- Agent Performance ---
function renderAgentPerformance(data) {
    const ctx = document.getElementById('agentChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.agent_name),
            datasets: [
                {
                    label: 'Revenue (\u20ac)',
                    data: data.map(d => d.total_revenue),
                    backgroundColor: '#2563eb',
                    yAxisID: 'y',
                    order: 2
                },
                {
                    label: 'Margin %',
                    data: data.map(d => d.avg_margin_pct),
                    borderColor: '#16a085',
                    backgroundColor: 'rgba(22, 160, 133, 0.1)',
                    type: 'line',
                    yAxisID: 'y1',
                    tension: 0.4,
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                tooltip: {
                    callbacks: {
                        afterBody: ctx => {
                            const item = data[ctx[0].dataIndex];
                            return 'Team: ' + item.team + '\nBookings: ' + item.booking_count;
                        }
                    }
                }
            },
            scales: {
                y: {
                    position: 'left',
                    beginAtZero: true,
                    ticks: { callback: v => '\u20ac' + (v / 1000000).toFixed(1) + 'M' }
                },
                y1: {
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    min: 0,
                    max: 50,
                    ticks: { callback: v => v + '%' }
                }
            }
        }
    });
}

// --- Destinations ---
function renderDestinations(data) {
    const ctx = document.getElementById('destChart').getContext('2d');
    const colors = ['#2563eb', '#ff6384', '#4bc0c0', '#ff9f40', '#9966ff',
                    '#ff6b6b', '#51cf66', '#ffd43b', '#845ef7', '#339af0'];

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.map(d => d.destination),
            datasets: [{
                data: data.map(d => d.total_revenue),
                backgroundColor: colors.slice(0, data.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { font: { size: 11 } } },
                tooltip: {
                    callbacks: {
                        label: ctx => {
                            const item = data[ctx.dataIndex];
                            return [
                                ctx.label + ': \u20ac' + Number(item.total_revenue).toLocaleString(),
                                'Bookings: ' + item.booking_count,
                                'PAX: ' + item.total_pax
                            ];
                        }
                    }
                }
            }
        }
    });
}

// --- Status Distribution ---
function renderStatusChart(data) {
    const ctx = document.getElementById('statusChart').getContext('2d');

    const statusColors = {
        'Completed': '#16a085',
        'Confirmed': '#2563eb',
        'Pending': '#ff9f40',
        'Cancelled': '#e74c3c'
    };

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.status_name),
            datasets: [{
                data: data.map(d => d.count),
                backgroundColor: data.map(d => statusColors[d.status_name] || '#95a5a6'),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: ctx => {
                            const item = data[ctx.dataIndex];
                            const total = data.reduce((s, d) => s + d.count, 0);
                            const pct = ((item.count / total) * 100).toFixed(1);
                            return [
                                item.status_name + ': ' + item.count + ' (' + pct + '%)',
                                'Revenue: \u20ac' + Number(item.revenue).toLocaleString()
                            ];
                        }
                    }
                }
            }
        }
    });
}

// --- Lead Time ---
function renderLeadTime(data) {
    const ctx = document.getElementById('leadTimeChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.lead_time_bucket),
            datasets: [
                {
                    label: 'Bookings',
                    data: data.map(d => d.booking_count),
                    backgroundColor: '#2563eb',
                    yAxisID: 'y'
                },
                {
                    label: 'Avg Revenue (\u20ac)',
                    data: data.map(d => d.avg_revenue),
                    borderColor: '#ff6384',
                    type: 'line',
                    yAxisID: 'y1',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            scales: {
                y: {
                    position: 'left',
                    beginAtZero: true,
                    title: { display: true, text: 'Count' }
                },
                y1: {
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    beginAtZero: true,
                    title: { display: true, text: 'Avg Revenue (\u20ac)' }
                }
            }
        }
    });
}

// --- Seasonality by Region ---
function renderSeasonality(data) {
    const ctx = document.getElementById('seasonChart').getContext('2d');

    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    // Group by region
    const regionMap = {};
    data.forEach(d => {
        if (!regionMap[d.client_region]) {
            regionMap[d.client_region] = Array(12).fill(0);
        }
        regionMap[d.client_region][d.month - 1] += d.booking_count;
    });

    const colors = ['#2563eb', '#ff6384', '#4bc0c0', '#ff9f40', '#9966ff', '#ff6b6b'];
    const regions = Object.keys(regionMap);

    const datasets = regions.map((region, i) => ({
        label: region,
        data: regionMap[region],
        backgroundColor: colors[i % colors.length],
        stack: 'seasonality'
    }));

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: monthNames,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: ctx => ctx.dataset.label + ': ' + ctx.parsed.y.toLocaleString() + ' bookings'
                    }
                }
            },
            scales: {
                x: { stacked: true },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    title: { display: true, text: 'Bookings' }
                }
            }
        }
    });
}
