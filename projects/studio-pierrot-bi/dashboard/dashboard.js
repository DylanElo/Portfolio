import { animeData } from './data.js';

console.log('Dashboard script loaded');

document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded, initializing dashboard...');
  try {
    if (!animeData || animeData.length === 0) {
      console.error('No anime data found!');
      document.getElementById('kpi-top-rated-value').textContent = 'Error';
      return;
    }
    console.log('Anime data loaded:', animeData.length, 'entries');
    initDashboard();
  } catch (error) {
    console.error('Error initializing dashboard:', error);
  }
});

function initDashboard() {
  // 1. Calculate KPIs
  const topRated = [...animeData].sort((a, b) => b.score - a.score)[0];
  const mostPopular = [...animeData].sort((a, b) => b.popularity - a.popularity)[0]; // Lower rank is better for popularity rank, but here we want max members? No, Jikan popularity is a rank. 
  // Actually, let's sort by 'members' for popularity to be safe, as 'popularity' field is a rank (1 is best).
  const mostMembers = [...animeData].sort((a, b) => b.members - a.members)[0];
  const mostFavorited = [...animeData].sort((a, b) => b.favorites - a.favorites)[0];

  // 2. Update KPI Cards
  if (topRated) updateKPI('kpi-top-rated', topRated.score, topRated.title);
  if (mostMembers) updateKPI('kpi-most-popular', formatNumber(mostMembers.members), mostMembers.title);
  if (mostFavorited) updateKPI('kpi-most-favorited', formatNumber(mostFavorited.favorites), mostFavorited.title);

  // 3. Render Charts
  renderScoreChart(animeData);
  renderPopularityChart(animeData);

  // 4. Populate Table
  populateTable(animeData);
}

function updateKPI(idPrefix, value, title) {
  const valueEl = document.getElementById(`${idPrefix}-value`);
  const titleEl = document.getElementById(`${idPrefix}-title`);
  if (valueEl) valueEl.textContent = value;
  if (titleEl) titleEl.textContent = title;
}

function formatNumber(num) {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
}

function renderScoreChart(data) {
  const ctx = document.getElementById('scoreChart').getContext('2d');
  const sortedData = [...data].sort((a, b) => b.score - a.score); // Top scores first

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sortedData.map(d => d.title),
      datasets: [{
        label: 'MAL Score',
        data: sortedData.map(d => d.score),
        backgroundColor: 'rgba(99, 102, 241, 0.8)', // Indigo
        borderColor: 'rgba(99, 102, 241, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: false,
          min: 6, // Focus on the 6-10 range for better visibility
          max: 10
        },
        x: {
          ticks: {
            autoSkip: false,
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    }
  });
}

function renderPopularityChart(data) {
  const ctx = document.getElementById('popularityChart').getContext('2d');
  // Sort by members
  const sortedData = [...data].sort((a, b) => b.members - a.members);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sortedData.map(d => d.title),
      datasets: [{
        label: 'Members',
        data: sortedData.map(d => d.members),
        backgroundColor: 'rgba(168, 85, 247, 0.8)', // Purple
        borderColor: 'rgba(168, 85, 247, 1)',
        borderWidth: 1,
        yAxisID: 'y'
      }, {
        label: 'Favorites',
        data: sortedData.map(d => d.favorites),
        backgroundColor: 'rgba(236, 72, 153, 0.8)', // Pink
        borderColor: 'rgba(236, 72, 153, 1)',
        borderWidth: 1,
        yAxisID: 'y1'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: { display: true, text: 'Members' }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: { display: true, text: 'Favorites' },
          grid: {
            drawOnChartArea: false
          }
        },
        x: {
          ticks: {
            autoSkip: false,
            maxRotation: 45,
            minRotation: 45
          }
        }
      }
    }
  });
}

function populateTable(data) {
  const tbody = document.getElementById('metrics-table-body');
  if (!tbody) return;
  tbody.innerHTML = '';

  data.forEach(anime => {
    const row = document.createElement('tr');
    row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">${anime.title}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">${anime.type}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900 font-bold">${anime.score}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">${formatNumber(anime.members)}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(anime.status)}">
                    ${anime.status}
                </span>
            </td>
        `;
    tbody.appendChild(row);
  });
}

function getStatusColor(status) {
  if (status.includes('Finished')) return 'bg-green-100 text-green-800';
  if (status.includes('Airing')) return 'bg-blue-100 text-blue-800';
  return 'bg-gray-100 text-gray-800';
}
