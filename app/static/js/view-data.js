document.addEventListener('DOMContentLoaded', () => {
  let barChart = null;
  let originalConfig = null; // ✅ 加上这一行
  let emissionsData = null;
  const chartInstances = {};


  // Handle URL parameter for tab selection
  function getTabFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get('tab');
    return tabParam ? parseInt(tabParam) : 0; // Default to first tab if not specified
  }
  
  // Scroll to charts section if tab parameter is present
  function scrollToChartsIfNeeded() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('tab')) {
      // Find the charts section element (fixed selector)
      const chartsSection = document.querySelector('.bg-white.relative.rounded-2xl');
      if (chartsSection) {
        // Slight delay to ensure everything is loaded
        setTimeout(() => {
          chartsSection.scrollIntoView({ behavior: 'smooth' });
        }, 0);
      }
    }
  }

  const barChartConfig = {
    type: 'bar',
    data: {
      labels: ['Travel', 'Home', 'Food', 'Shopping'],
      datasets: [
        { label: 'Vehicle', data: [0, 0, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Public Transit', data: [0, 0, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Air Travel', data: [0, 0, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Electricity', data: [0, 0, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Natural Gas', data: [0, 0, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Heating Oil & Other Fuels', data: [0, 0, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Living Space Area', data: [0, 0, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Water Usage', data: [0, 0, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Meat/Fish/Eggs', data: [0, 0, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Grains/Baked Goods', data: [0, 0, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Dairy', data: [0, 0, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Fruits/Vegetables', data: [0, 0, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Snacks/Drinks', data: [0, 0, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Furniture', data: [0, 0, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Clothing', data: [0, 0, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Other Goods', data: [0, 0, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
        { label: 'Services', data: [0, 0, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#2f5c47',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          cornerRadius: 6,
          borderWidth: 1,
          borderColor: '#497f66'
        }
      },
      scales: {
        x: {
          stacked: true,
          ticks: {
            color: '#222222',
            font: { size: 16, weight: 'bold' },
            padding: 10
          },
          grid: {
            color: 'rgba(0,0,0,0.1)',
            lineWidth: 1.5,
          },
          border: {
            color: '#222222',
            width: 2
          }
        },
        y: {
          stacked: true,
          beginAtZero: true,
          title: {
            display: true,
            text: 'Metric tons CO₂/year',
            color: '#222222',
            font: { size: 16, weight: 'bold' }
          },
          ticks: {
            color: '#222222',
            font: { size: 14 }
          },
          grid: {
            color: 'rgba(0,0,0,0.1)',
            lineWidth: 1.5
          },
          border: {
            color: '#222222',
            width: 2
          }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#2f5c47',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          cornerRadius: 6,
          borderWidth: 1,
          borderColor: '#497f66'
        }
      }
    },
    plugins: [
      {
        id: 'textShadow',
        beforeDraw(chart) {
          const ctx = chart.ctx;
          ctx.save();
          ctx.shadowColor = 'rgba(255,255,255,0.6)';
          ctx.shadowBlur = 6;
          ctx.shadowOffsetX = 0;
          ctx.shadowOffsetY = 0;
        },
        afterDraw(chart) {
          chart.ctx.restore();
        }
      }
    ]
  };

  // Pie chart configurations
  const chartConfigs = [
    {
      id: 'travelPieChart',
      labels: ['Vehicle', 'Public Transit', 'Air Travel'],
      dataKey: ['car_emissions', 'public_transit_emissions', 'air_travel_emissions'],
      colors: ['#2f5c47', '#497f66', '#7fc8a9']
    },
    {
      id: 'homePieChart',
      labels: ['Electricity', 'Natural Gas', 'Heating Oil & Other Fuels', 'Living Space Area', 'Water Usage'],
      dataKey: ['electricity_emissions', 'natural_gas_emissions', 'heating_fuels_emissions', 'construction_emissions', 'water_emissions'],
      colors: ['#3490dc', '#6574cd', '#38c172', '#4dc0b5', '#9561e2']
    },
    {
      id: 'foodPieChart',
      labels: ['Meat/Fish/Eggs', 'Grains/Baked Goods', 'Dairy', 'Fruits/Vegetables', 'Snacks/Drinks'],
      dataKey: ['meat_emissions', 'cereals_emissions', 'dairy_emissions', 'fruits_vegetables_emissions', 'snacks_emissions'],
      colors: ['#ffb997', '#ff8fab', '#a4c3b2', '#c5a3ff', '#f6993f']
    },
    {
      id: 'shoppingPieChart',
      labels: ['Furniture', 'Clothing', 'Other Goods', 'Services'],
      dataKey: ['furniture_emissions', 'clothing_emissions', 'other_goods_emissions', 'services_emissions'],
      colors: ['#37637d', '#7b9aa5', '#a3bffa', '#d6bcfa']
    }
  ];

  // Initialize bar chart
  const barCtx = document.getElementById('myChart')?.getContext('2d');
  if (barCtx) {
    barChart = new Chart(barCtx, barChartConfig);
  }

  // Function to update charts with emissions data
  function updateCharts(data) {
    if (barChart) {
      barChart.data.datasets.forEach(dataset => {
        switch (dataset.label) {
          case 'Vehicle':
            dataset.data = [data.car_emissions, 0, 0, 0];
            break;
          case 'Public Transit':
            dataset.data = [data.public_transit_emissions, 0, 0, 0];
            break;
          case 'Air Travel':
            dataset.data = [data.air_travel_emissions, 0, 0, 0];
            break;
          case 'Electricity':
            dataset.data = [0, data.electricity_emissions, 0, 0];
            break;
          case 'Natural Gas':
            dataset.data = [0, data.natural_gas_emissions, 0, 0];
            break;
          case 'Heating Oil & Other Fuels':
            dataset.data = [0, data.heating_fuels_emissions, 0, 0];
            break;
          case 'Living Space Area':
            dataset.data = [0, data.construction_emissions, 0, 0];
            break;
          case 'Water Usage':
            dataset.data = [0, data.water_emissions, 0, 0];
            break;
          case 'Meat/Fish/Eggs':
            dataset.data = [0, 0, data.meat_emissions, 0];
            break;
          case 'Grains/Baked Goods':
            dataset.data = [0, 0, data.cereals_emissions, 0];
            break;
          case 'Dairy':
            dataset.data = [0, 0, data.dairy_emissions, 0];
            break;
          case 'Fruits/Vegetables':
            dataset.data = [0, 0, data.fruits_vegetables_emissions, 0];
            break;
          case 'Snacks/Drinks':
            dataset.data = [0, 0, data.snacks_emissions, 0];
            break;
          case 'Furniture':
            dataset.data = [0, 0, 0, data.furniture_emissions];
            break;
          case 'Clothing':
            dataset.data = [0, 0, 0, data.clothing_emissions];
            break;
          case 'Other Goods':
            dataset.data = [0, 0, 0, data.other_goods_emissions];
            break;
          case 'Services':
            dataset.data = [0, 0, 0, data.services_emissions];
            break;
        }
      });
      barChart.update();
    }

    // Store emissions data for pie charts
    emissionsData = data;
  }

function showTab(index) {
  const canvasIds = ['travelPieChart', 'homePieChart', 'foodPieChart', 'shoppingPieChart'];
  const contentIds = ['tabContent0', 'tabContent1', 'tabContent2', 'tabContent3'];
  const buttons = document.querySelectorAll('.tab-btn');
  const chartId = canvasIds[index];

  // Hide all canvas elements and destroy existing charts
  canvasIds.forEach((id, i) => {
    const canvas = document.getElementById(id);
    if (i === index) {
      canvas.classList.remove('hidden');
    } else {
      canvas.classList.add('hidden');
      if (chartInstances[id]) {
        chartInstances[id].destroy();
        delete chartInstances[id];
      }
    }
  });

  // Show the selected content and hide others
  contentIds.forEach((id, i) => {
    const content = document.getElementById(id);
    content.classList.toggle('hidden', i !== index);
  });

  // Update button styles
  buttons.forEach((btn, i) => {
    btn.classList.toggle('border-b-2', i === index);
    btn.classList.toggle('text-[#16372c]', i === index);
    btn.classList.toggle('border-[#16372c]', i === index);
  });

  // Re-create the chart
  const config = chartConfigs.find(c => c.id === chartId);
  const ctx = document.getElementById(chartId)?.getContext('2d');
  if (ctx && config) {
    const data = emissionsData
      ? config.dataKey.map(key => emissionsData[key] || 0)
      : new Array(config.labels.length).fill(0);

    // Destroy existing
    if (chartInstances[chartId]) {
      chartInstances[chartId].destroy();
      delete chartInstances[chartId];
    }

    // Create new chart
    chartInstances[chartId] = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: config.labels,
        datasets: [{
          data: data,
          backgroundColor: config.colors,
          borderColor: '#ffffff',
          borderWidth: 2
        }]
      },
      plugins: [ChartDataLabels],
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#2f5c47',
            titleColor: '#ffffff',
            bodyColor: '#ffffff',
            borderColor: '#497f66',
            borderWidth: 1
          },
          datalabels: { display: false }
        }
      }
    });

    // Update legend
    const legendDivIds = {
      travelPieChart: 'travelLegend',
      homePieChart: 'homeLegend',
      foodPieChart: 'foodLegend',
      shoppingPieChart: 'shoppingLegend'
    };

    // Hide all legends
    Object.values(legendDivIds).forEach(id => {
      const el = document.getElementById(id);
      if (el) el.classList.add('hidden');
    });

    // Show the current chart's legend
    const legendDiv = document.getElementById(legendDivIds[chartId]);
    if (legendDiv) {
      legendDiv.classList.remove('hidden');

      // Generate legend HTML
      let legendHTML = `
        <div class="flex flex-wrap justify-center gap-x-6 gap-y-1 text-sm">
          ${config.labels.map((label, i) => {
            const value = data[i];
            const color = config.colors[i];
            return `
              <div class="flex items-center gap-1">
                <span class="inline-block w-3 h-3 rounded-full" style="background:${color}"></span>
                <span class="font-semibold text-gray-800">${label}:</span>
                <span class="text-gray-700">${value.toFixed(2)} kg</span>
              </div>
            `;
          }).join('')}
        </div>
      `;

      // If the chart is food or home, split into two rows
      if (chartId === 'foodPieChart' || chartId === 'homePieChart') {
        const firstRow = config.labels.slice(0, 3).map((label, i) => {
          const value = data[i];
          const color = config.colors[i];
          return `
            <div class="flex items-center gap-1">
              <span class="inline-block w-3 h-3 rounded-full" style="background:${color}"></span>
              <span class="font-semibold text-gray-800">${label}:</span>
              <span class="text-gray-700">${value.toFixed(2)} kg</span>
            </div>
          `;
        }).join('');

        const secondRow = config.labels.slice(3).map((label, i) => {
          const realIndex = i + 3;
          const value = data[realIndex];
          const color = config.colors[realIndex];
          return `
            <div class="flex items-center gap-1">
              <span class="inline-block w-3 h-3 rounded-full" style="background:${color}"></span>
              <span class="font-semibold text-gray-800">${label}:</span>
              <span class="text-gray-700">${value.toFixed(2)} kg</span>
            </div>
          `;
        }).join('');

        legendHTML = `
          <div class="flex flex-wrap justify-center gap-x-6 gap-y-1 text-sm">
            ${firstRow}
          </div>
          <div class="flex flex-wrap justify-center gap-x-6 gap-y-1 text-sm mt-1">
            ${secondRow}
          </div>
        `;
      }

      // Insert legend
      legendDiv.innerHTML = legendHTML;
    }
  }
}
  window.showTab = showTab;
  // Fetch emissions and show default chart
  fetch('/api/emissions')
    .then(res => {
      if (!res.ok) throw new Error('Failed to fetch emissions');
      return res.json();
    })
    .then(data => {
      // ✅ Update total emissions
      const totalElement = document.getElementById('total-emissions');
      if (totalElement) {
        totalElement.textContent = `${data.total_emissions.toFixed(2)} metric tons CO₂eq`;
      }
      updateCharts(data);
      showTab(getTabFromUrl());
      // ✅ Scroll to charts section after tab is shown
      scrollToChartsIfNeeded();
    })
    .catch(error => {
      const totalElement = document.getElementById('total-emissions');
      if (totalElement) {
        totalElement.textContent = 'Error loading emissions data';
      }
      console.error('Error fetching emissions:', error);
      showTab(getTabFromUrl());
      // ✅ Still attempt to scroll even if there’s an error
      scrollToChartsIfNeeded();
    });

    // Initial chart configuration
    originalConfig = {
      type: 'bar',
      data: {
        labels: ['Travel', 'Home', 'Food', 'Shopping'],
        datasets: [
          {
            label: 'Vehicle',
            data: [1, 0, 0, 0],
            backgroundColor: '#2f5c47'
          },
          {
            label: 'Public Transit',
            data: [2, 0, 0, 0],
            backgroundColor: '#497f66'
          },
          {
            label: 'Electricity',
            data: [0, 3, 0, 0],
            backgroundColor: '#7fc8a9'
          },
          {
            label: 'Meat',
            data: [0, 0, 4, 0],
            backgroundColor: '#a0d9a0'
          },
          {
            label: 'Furniture',
            data: [0, 0, 0, 5],
            backgroundColor: '#d0e7c3'
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: true }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    };

    // Create Chart
    function restoreOriginalChart() {
      if (barChart) {
        barChart.destroy();
      }

      const ctx = document.getElementById('myChart').getContext('2d');
      barChart = new Chart(ctx, originalConfig);
  }

  // Comparison chart
  function toggleSharedUserEmissions(email) {
    console.log('Fetching emissions for:', email);

    fetch(`/api/compare_emissions?email=${encodeURIComponent(email)}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch compare data');
        return res.json();
      })
      .then(data => {
        if (data.error) {
          alert(data.error);
          return;
        }
        const chartId = 'myChart';
        const existingChart = Chart.getChart(chartId);
        if (existingChart) {
          existingChart.destroy();
        }

        const ctx = document.getElementById(chartId).getContext('2d');

        barChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Travel', 'Food', 'Home', 'Shopping'],
            datasets: [
              {
                label: 'You',
                data: data.your_emissions,
                backgroundColor: '#2f5c47'
              },
              {
                label: data.other_name,
                data: data.other_emissions,
                backgroundColor: '#a0d9a0'
              }
            ]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { display: true }
            },
            scales: {
              y: {
                beginAtZero: true
              },
              x: {
                ticks: {
                  color: '#222222',
                  font: { size: 16, weight: 'bold' },
                  padding: 10
                }
              }
            }
          }
        });
      })
      .catch(err => {
        alert("Error: " + err.message);
        console.error(err);
      });
  }

// Restore original chart on page load
window.toggleSharedUserEmissions = toggleSharedUserEmissions;
});