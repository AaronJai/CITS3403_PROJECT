document.addEventListener('DOMContentLoaded', () => {
  // Initialize chart variables
  let barChart = null;
  const chartInstances = {};
  let emissionsData = null;

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

    const chartId = canvasIds[index];
    // Destroy existing chart to ensure fresh data
    if (chartInstances[chartId]) {
      chartInstances[chartId].destroy();
      delete chartInstances[chartId];
    }

    const config = chartConfigs.find(c => c.id === chartId);
    const ctx = document.getElementById(chartId)?.getContext('2d');
    if (ctx && config) {
      const data = emissionsData
        ? config.dataKey.map(key => emissionsData[key] || 0)
        : new Array(config.labels.length).fill(0);
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
    }
  }

  // Fetch emissions data via AJAX
  fetch('/api/emissions', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(response.status === 401 ? 'User not logged in' : 'No emissions data found');
      }
      return response.json();
    })
    .then(data => {
      // Update total emissions
      const totalElement = document.getElementById('total-emissions');
      if (totalElement) {
        totalElement.textContent = `${data.total_emissions.toFixed(2)} metric tons CO₂/year`;
      }

      updateCharts(data);
      showTab(0);
    })
    .catch(error => {
      const totalElement = document.getElementById('total-emissions');
      if (totalElement) {
        totalElement.textContent = 'Error loading emissions data';
      }
      console.error('Error fetching emissions:', error);
      showTab(0);
    });

  window.showTab = showTab;
});