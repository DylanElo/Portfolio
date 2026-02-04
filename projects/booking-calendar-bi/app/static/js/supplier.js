let dailyChart = null;
let monthlyChart = null;

document.addEventListener('DOMContentLoaded', async () => {
    const filters = await fetchJSON('/api/filters');
    populateDropdowns(filters);

    // Pre-fill from URL params
    const params = new URLSearchParams(window.location.search);
    const name = params.get('name');
    if (name) {
        document.getElementById('supplier-select').value = name;
        loadSupplierData();
    }

    document.getElementById('btn-load').addEventListener('click', loadSupplierData);
    document.getElementById('supplier-select').addEventListener('keydown', e => {
        if (e.key === 'Enter') loadSupplierData();
    });
});

function populateDropdowns(filters) {
    const datalist = document.getElementById('supplier-datalist');
    filters.suppliers.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        datalist.appendChild(opt);
    });

    const svcSelect = document.getElementById('svc-type-filter');
    filters.service_types.forEach(st => {
        svcSelect.add(new Option(st, st));
    });
}

async function loadSupplierData() {
    const supplier = document.getElementById('supplier-select').value.trim();
    if (!supplier) return;

    const from = document.getElementById('svc-date-from').value;
    const to = document.getElementById('svc-date-to').value;
    const svcType = document.getElementById('svc-type-filter').value;

    const params = new URLSearchParams({ supplier, from, to });
    if (svcType) params.set('service_type', svcType);

    const monthParams = new URLSearchParams({ supplier, from, to });

    const [daily, monthly] = await Promise.all([
        fetchJSON('/api/supplier/daily?' + params),
        fetchJSON('/api/supplier/summary?' + monthParams),
    ]);

    // Show sections
    document.getElementById('supplier-kpis').style.display = '';
    document.getElementById('supplier-charts').style.display = '';
    document.getElementById('data-table-container').style.display = '';
    document.getElementById('empty-state').style.display = 'none';

    renderKPIs(daily);
    renderDailyChart(daily, supplier);
    renderMonthlyChart(monthly, supplier);
    renderTable(daily);
}

function renderKPIs(data) {
    if (!data.length) {
        ['skpi-days', 'skpi-services', 'skpi-pax', 'skpi-bookings', 'skpi-avg', 'skpi-peak']
            .forEach(id => setText(id, '0'));
        return;
    }

    const totalServices = data.reduce((s, d) => s + d.service_count, 0);
    const totalPax = data.reduce((s, d) => s + (d.total_pax || 0), 0);
    const totalBookings = data.reduce((s, d) => s + d.unique_bookings, 0);
    const peak = data.reduce((max, d) => d.service_count > max.service_count ? d : max, data[0]);

    setText('skpi-days', fmt(data.length));
    setText('skpi-services', fmt(totalServices));
    setText('skpi-pax', fmt(totalPax));
    setText('skpi-bookings', fmt(totalBookings));
    setText('skpi-avg', (totalServices / data.length).toFixed(1));
    setText('skpi-peak', peak.date + ' (' + peak.service_count + ')');
}

function renderDailyChart(data, supplier) {
    const ctx = document.getElementById('dailyChart').getContext('2d');
    if (dailyChart) dailyChart.destroy();

    const colors = data.map(d => d.is_weekend ? 'rgba(251, 191, 36, 0.7)' : 'rgba(37, 99, 235, 0.6)');

    dailyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.date),
            datasets: [
                {
                    label: 'Services/Rooms',
                    data: data.map(d => d.service_count),
                    backgroundColor: colors,
                    yAxisID: 'y',
                    order: 2
                },
                {
                    label: 'PAX',
                    data: data.map(d => d.total_pax),
                    borderColor: '#ff6384',
                    type: 'line',
                    yAxisID: 'y1',
                    tension: 0.3,
                    pointRadius: 1,
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                title: { display: true, text: supplier, font: { size: 14 } },
                tooltip: {
                    callbacks: {
                        afterBody: ctx => {
                            const item = data[ctx[0].dataIndex];
                            return [
                                'Day: ' + item.day_name,
                                'Bookings: ' + item.unique_bookings,
                                'Types: ' + (item.service_types || 'N/A')
                            ];
                        }
                    }
                },
                legend: { position: 'bottom' }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 90,
                        autoSkip: true,
                        maxTicksLimit: 60
                    }
                },
                y: { position: 'left', beginAtZero: true, title: { display: true, text: 'Services' } },
                y1: { position: 'right', beginAtZero: true, grid: { drawOnChartArea: false }, title: { display: true, text: 'PAX' } }
            }
        }
    });
}

function renderMonthlyChart(data, supplier) {
    const ctx = document.getElementById('monthlySupplierChart').getContext('2d');
    if (monthlyChart) monthlyChart.destroy();

    monthlyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.year + '-' + String(d.month).padStart(2, '0')),
            datasets: [
                {
                    label: 'Services',
                    data: data.map(d => d.service_count),
                    backgroundColor: '#2563eb',
                    yAxisID: 'y'
                },
                {
                    label: 'Bookings',
                    data: data.map(d => d.unique_bookings),
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
                y: { position: 'left', beginAtZero: true, title: { display: true, text: 'Services' } },
                y1: { position: 'right', beginAtZero: true, grid: { drawOnChartArea: false }, title: { display: true, text: 'Bookings' } }
            }
        }
    });
}

function renderTable(data) {
    const tbody = document.querySelector('#daily-table tbody');
    tbody.innerHTML = '';

    data.forEach(d => {
        const tr = document.createElement('tr');
        if (d.is_weekend) tr.className = 'weekend';
        tr.innerHTML = `
            <td>${d.date}</td>
            <td>${d.day_name}</td>
            <td><strong>${d.service_count}</strong></td>
            <td>${d.total_pax || 0}</td>
            <td>${d.unique_bookings}</td>
            <td>${d.service_types || ''}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Utilities
async function fetchJSON(url) {
    const res = await fetch(url);
    return res.json();
}

function fmt(n) {
    return n != null ? Number(n).toLocaleString() : '--';
}

function setText(id, val) {
    document.getElementById(id).textContent = val || '--';
}
