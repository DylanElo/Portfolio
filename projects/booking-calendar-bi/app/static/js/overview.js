let monthlyChart = null;
let supplierChart = null;
let filters = {};

document.addEventListener('DOMContentLoaded', async () => {
    filters = await fetchJSON('/api/filters');
    populateDropdowns();
    loadDashboard();

    document.getElementById('btn-apply').addEventListener('click', loadDashboard);
    document.getElementById('supplier-svc-type').addEventListener('change', loadSuppliers);
    document.getElementById('btn-go-supplier').addEventListener('click', goToSupplier);
});

function populateDropdowns() {
    const countrySelect = document.getElementById('country-filter');
    const countries = [...new Set(filters.agents.map(a => a.agent_country))].sort();
    countries.forEach(c => {
        countrySelect.add(new Option(c, c));
    });

    const svcTypeSelect = document.getElementById('supplier-svc-type');
    filters.service_types.forEach(st => {
        svcTypeSelect.add(new Option(st, st));
    });

    const supplierList = document.getElementById('supplier-list');
    filters.suppliers.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        supplierList.appendChild(opt);
    });
}

async function loadDashboard() {
    const from = document.getElementById('date-from').value;
    const to = document.getElementById('date-to').value;
    const country = document.getElementById('country-filter').value;

    const params = new URLSearchParams({ from, to });
    if (country) params.set('country', country);

    const [kpis, monthly] = await Promise.all([
        fetchJSON('/api/kpis?' + params),
        fetchJSON('/api/monthly?' + params),
    ]);

    renderKPIs(kpis);
    renderMonthly(monthly);
    loadSuppliers();
}

function renderKPIs(data) {
    setText('kpi-bookings', fmt(data.total_bookings));
    setText('kpi-pax', fmt(data.total_pax));
    setText('kpi-services', fmt(data.total_services));
    setText('kpi-trip', data.avg_trip_days ? data.avg_trip_days + 'd' : '--');
    setText('kpi-agents', fmt(data.active_agents));
}

function renderMonthly(data) {
    const ctx = document.getElementById('monthlyChart').getContext('2d');
    if (monthlyChart) monthlyChart.destroy();

    monthlyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.year + '-' + String(d.month).padStart(2, '0')),
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
                y: { position: 'left', beginAtZero: true, title: { display: true, text: 'Bookings' } },
                y1: { position: 'right', beginAtZero: true, grid: { drawOnChartArea: false }, title: { display: true, text: 'PAX' } }
            }
        }
    });
}

async function loadSuppliers() {
    const from = document.getElementById('date-from').value;
    const to = document.getElementById('date-to').value;
    const svcType = document.getElementById('supplier-svc-type').value;

    const params = new URLSearchParams({ from, to, limit: '20' });
    if (svcType) params.set('service_type', svcType);

    const data = await fetchJSON('/api/top-suppliers?' + params);
    renderSuppliers(data);
}

function renderSuppliers(data) {
    const ctx = document.getElementById('supplierChart').getContext('2d');
    if (supplierChart) supplierChart.destroy();

    supplierChart = new Chart(ctx, {
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
                                'PAX: ' + fmt(item.total_pax),
                                'Bookings: ' + fmt(item.unique_bookings)
                            ];
                        }
                    }
                }
            },
            scales: { x: { beginAtZero: true } },
            onClick: (e, elements) => {
                if (elements.length > 0) {
                    const supplier = data[elements[0].index].supplier_name;
                    window.location.href = '/supplier?name=' + encodeURIComponent(supplier);
                }
            }
        }
    });
}

function goToSupplier() {
    const name = document.getElementById('supplier-search').value;
    if (name) {
        window.location.href = '/supplier?name=' + encodeURIComponent(name);
    }
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
