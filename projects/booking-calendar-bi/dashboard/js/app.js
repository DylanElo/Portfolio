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
    renderTopAgents(data.top_agents);
    renderCountries(data.agent_countries);
    renderRegions(data.region_distribution);
    renderLocations(data.top_locations);
    renderStatusChart(data.status_breakdown);
    renderLeadTime(data.lead_time);
    renderSuppliers(data.top_suppliers);
    renderSeasonality(data.seasonality);
    renderDepartments(data.department_breakdown);
}

// --- KPIs ---
function renderKPIs(kpis) {
    setText('kpi-bookings', fmt(kpis.total_bookings));
    setText('kpi-pax', fmt(kpis.total_pax));
    setText('kpi-services', fmt(kpis.total_services));
    setText('kpi-trip-days', kpis.avg_trip_days + ' days');
    setText('kpi-2024', fmt(kpis.bookings_2024));
    setText('kpi-2025', fmt(kpis.bookings_2025));
}

function setText(id, val) {
    document.getElementById(id).textContent = val || '--';
}

function fmt(n) {
    return n != null ? Number(n).toLocaleString() : '--';
}

// --- Monthly Trend ---
function renderMonthlyTrend(data) {
    const ctx = document.getElementById('monthlyTrendChart').getContext('2d');
    const labels = data.map(d => d.year + '-' + String(d.month).padStart(2, '0'));

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [
                {
                    label: 'Bookings',
                    data: data.map(d => d.total_bookings),
                    backgroundColor: 'rgba(37, 99, 235, 0.6)',
                    yAxisID: 'y',
                    order: 2
                },
                {
                    label: 'PAX',
                    data: data.map(d => d.total_pax),
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
                    position: 'left',
                    title: { display: true, text: 'Bookings' },
                    beginAtZero: true
                },
                y1: {
                    position: 'right',
                    title: { display: true, text: 'PAX' },
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
                    label: 'Bookings',
                    data: data.map(d => d.total_bookings),
                    backgroundColor: '#2563eb',
                    yAxisID: 'y'
                },
                {
                    label: 'Avg Trip Days',
                    data: data.map(d => d.avg_trip_days),
                    borderColor: '#16a085',
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
            plugins: { legend: { position: 'bottom' } },
            scales: {
                y: { beginAtZero: true, title: { display: true, text: 'Bookings' } },
                y1: {
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    title: { display: true, text: 'Avg Trip Days' }
                }
            }
        }
    });
}

// --- Service Type ---
function renderServiceBreakdown(data) {
    const ctx = document.getElementById('serviceChart').getContext('2d');
    const colors = ['#2563eb', '#ff6384', '#4bc0c0', '#ff9f40', '#9966ff',
        '#ff6b6b', '#51cf66', '#ffd43b', '#845ef7', '#339af0',
        '#20c997', '#f06595', '#94d82d', '#ffa94d', '#748ffc'];

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.service_type),
            datasets: [{
                data: data.map(d => d.service_count),
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
                                ctx.label + ': ' + fmt(item.service_count) + ' services',
                                'In ' + fmt(item.booking_count) + ' bookings'
                            ];
                        }
                    }
                }
            }
        }
    });
}

// --- Top Agents ---
function renderTopAgents(data) {
    const ctx = document.getElementById('agentChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.agent_name),
            datasets: [{
                label: 'Bookings',
                data: data.map(d => d.booking_count),
                backgroundColor: '#2563eb'
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
                                'Bookings: ' + fmt(item.booking_count),
                                'Country: ' + item.agent_country,
                                'PAX: ' + fmt(item.total_pax),
                                'Avg trip: ' + item.avg_trip_days + ' days'
                            ];
                        }
                    }
                }
            },
            scales: { x: { beginAtZero: true } }
        }
    });
}

// --- Source Countries ---
function renderCountries(data) {
    const ctx = document.getElementById('countryChart').getContext('2d');
    const colors = ['#2563eb', '#ff6384', '#4bc0c0', '#ff9f40', '#9966ff',
        '#ff6b6b', '#51cf66', '#ffd43b', '#845ef7', '#339af0',
        '#20c997', '#f06595', '#94d82d', '#ffa94d', '#748ffc'];

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.map(d => d.agent_country),
            datasets: [{
                data: data.map(d => d.booking_count),
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
                            const total = data.reduce((s, d) => s + d.booking_count, 0);
                            const pct = ((item.booking_count / total) * 100).toFixed(1);
                            return item.agent_country + ': ' + fmt(item.booking_count) + ' (' + pct + '%)';
                        }
                    }
                }
            }
        }
    });
}

// --- Regions ---
function renderRegions(data) {
    const ctx = document.getElementById('regionChart').getContext('2d');
    const colors = ['#2563eb', '#ff6384', '#4bc0c0', '#ff9f40', '#9966ff',
        '#ff6b6b', '#51cf66', '#ffd43b', '#845ef7', '#339af0', '#20c997'];

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.region),
            datasets: [{
                data: data.map(d => d.service_count),
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
                                item.region + ': ' + fmt(item.service_count) + ' services',
                                fmt(item.booking_count) + ' bookings'
                            ];
                        }
                    }
                }
            }
        }
    });
}

// --- Locations ---
function renderLocations(data) {
    const ctx = document.getElementById('locationChart').getContext('2d');

    const regionColors = {
        'Kanto': '#2563eb', 'Kansai': '#ff6384', 'Chubu': '#4bc0c0',
        'Chugoku': '#ff9f40', 'Kyushu': '#9966ff', 'Hokkaido': '#51cf66',
        'Others': '#95a5a6', 'Shikoku': '#ffd43b', 'Tohoku': '#845ef7',
        'HokkaidoD': '#51cf66', 'OkinawaD': '#20c997'
    };

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.location_name),
            datasets: [{
                label: 'Services',
                data: data.map(d => d.service_count),
                backgroundColor: data.map(d => regionColors[d.region] || '#95a5a6')
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
                                'Services: ' + fmt(item.service_count),
                                'Bookings: ' + fmt(item.booking_count),
                                'Region: ' + item.region
                            ];
                        }
                    }
                }
            },
            scales: { x: { beginAtZero: true } }
        }
    });
}

// --- Status Distribution ---
function renderStatusChart(data) {
    const ctx = document.getElementById('statusChart').getContext('2d');

    const statusColors = {
        'IV': '#2563eb', 'CF': '#16a085', 'CX': '#e74c3c',
        'CP': '#27ae60', 'CC': '#f39c12', 'IX': '#95a5a6', 'FC': '#8e44ad'
    };

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.status_code + ' (' + d.status_name + ')'),
            datasets: [{
                data: data.map(d => d.booking_count),
                backgroundColor: data.map(d => statusColors[d.status_code] || '#95a5a6'),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { font: { size: 11 } } },
                tooltip: {
                    callbacks: {
                        label: ctx => {
                            const item = data[ctx.dataIndex];
                            const total = data.reduce((s, d) => s + d.booking_count, 0);
                            const pct = ((item.booking_count / total) * 100).toFixed(1);
                            return item.status_name + ': ' + fmt(item.booking_count) + ' (' + pct + '%)';
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
                    label: 'Avg Trip Days',
                    data: data.map(d => d.avg_trip_days),
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
                y: { position: 'left', beginAtZero: true, title: { display: true, text: 'Bookings' } },
                y1: {
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    title: { display: true, text: 'Avg Trip Days' }
                }
            }
        }
    });
}

// --- Top Suppliers ---
function renderSuppliers(data) {
    const ctx = document.getElementById('supplierChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.supplier_name),
            datasets: [{
                label: 'Services',
                data: data.map(d => d.service_count),
                backgroundColor: '#2563eb'
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
                                'Services: ' + fmt(item.service_count),
                                'Bookings: ' + fmt(item.booking_count)
                            ];
                        }
                    }
                }
            },
            scales: { x: { beginAtZero: true } }
        }
    });
}

// --- Seasonality by Source Market ---
function renderSeasonality(data) {
    const ctx = document.getElementById('seasonChart').getContext('2d');
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    const countryMap = {};
    data.forEach(d => {
        if (!countryMap[d.agent_country]) countryMap[d.agent_country] = Array(12).fill(0);
        countryMap[d.agent_country][d.month - 1] += d.booking_count;
    });

    const colors = ['#2563eb', '#ff6384', '#4bc0c0', '#ff9f40', '#9966ff',
        '#ff6b6b', '#51cf66', '#ffd43b'];
    const countries = Object.keys(countryMap);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: monthNames,
            datasets: countries.map((country, i) => ({
                label: country,
                data: countryMap[country],
                backgroundColor: colors[i % colors.length],
                stack: 'seasonality'
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            scales: {
                x: { stacked: true },
                y: { stacked: true, beginAtZero: true, title: { display: true, text: 'Bookings' } }
            }
        }
    });
}

// --- Departments ---
function renderDepartments(data) {
    const ctx = document.getElementById('deptChart').getContext('2d');
    const colors = ['#2563eb', '#ff6384', '#4bc0c0', '#ff9f40', '#9966ff',
        '#ff6b6b', '#51cf66', '#ffd43b', '#845ef7', '#339af0',
        '#20c997', '#f06595', '#94d82d', '#ffa94d', '#748ffc',
        '#e64980', '#12b886', '#fab005', '#7048e8'];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.department),
            datasets: [{
                label: 'Bookings',
                data: data.map(d => d.booking_count),
                backgroundColor: colors.slice(0, data.length)
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => {
                            const item = data[ctx.dataIndex];
                            return [
                                'Bookings: ' + fmt(item.booking_count),
                                'PAX: ' + fmt(item.total_pax)
                            ];
                        }
                    }
                }
            },
            scales: { y: { beginAtZero: true } }
        }
    });
}
