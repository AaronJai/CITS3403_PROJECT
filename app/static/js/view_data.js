//Chart.register(ChartDataLabels);
const ctx = document.getElementById('myChart').getContext('2d');

const data = {
  labels: ['Travel', 'Home', 'Food', 'Shopping'],
  datasets: [
    // Travel
    { label: 'Vehicle', data: [50, 0, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Public Transit', data: [50, 0, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Air Travel', data: [50, 0, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    // Home
    { label: 'Electricity', data: [0, 50, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Clean Energy', data: [0, 30, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Natural Gas', data: [0, 20, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Heating Oil & Other Fuels', data: [0, 50, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Living Space Area', data: [0, 50, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Water Usage', data: [0, 10, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    // Shopping
    { label: 'Meat/Fish/Eggs', data: [0, 0, 50, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Grains/Baked Goods', data: [0, 0, 50, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Dairy', data: [0, 0, 50, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Fruits/Vegetables', data: [0, 0, 50, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Snacks/Drinks/Other Foods Consumption', data: [0, 0, 50, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
  
    // Goods and Services
    { label: 'Goods', data: [0, 0, 0, 50], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Services', data: [0, 0, 0, 50], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' }
  ]
  
};

const options = {
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
    },
    
  }
};

const config = {
  type: 'bar',
  data: data,
  options: options,
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

new Chart(ctx, config);



const chartConfigs = [
  {
    id: 'travelPieChart',
    labels: ['Vehicle', 'Public Transit', 'Air Travel'],
    data: [50, 30, 20],
    colors: ['#2f5c47', '#497f66', '#7fc8a9']
  },
  {
    id: 'homePieChart',
    labels: ['Electricity', 'Clean Energy', 'Natural Gas', 'Living Space Area', 'Heating Oil & Other Fuels', 'Water Usage'],
    data: [20, 15, 10, 25, 20, 10],
    colors: ['#3490dc', '#6574cd', '#38c172', '#4dc0b5', '#9561e2', '#f6993f']
  },
  {
    id: 'foodPieChart',
    labels: ['Grains/Baked Goods', 'Dairy', 'Fruits/Vegetables', 'Snacks/Drinks/Other Foods Consumption'],
    data: [30, 20, 30, 20],
    colors: ['#ffb997', '#ff8fab', '#a4c3b2', '#c5a3ff']
  },
  {
    id: 'shoppingPieChart',
    labels: ['Goods', 'Services'],
    data: [60, 40],
    colors: ['#37637d', '#7b9aa5']
  }
];

// For each chart config, create PieChart instance
chartConfigs.forEach(config => {
  const ctx1 = document.getElementById(config.id)?.getContext('2d');
  if (!ctx1) return; 

  new Chart(ctx1, {
    type: 'pie',
    data: {
      labels: config.labels,
      datasets: [{
        data: config.data,
        backgroundColor: config.colors,
        borderColor: '#ffffff', 
        borderWidth: 2
      }]
    },
    plugins: [ChartDataLabels],
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false  // legend not displayed
        },
        tooltip: {
          backgroundColor: '#2f5c47',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          borderColor: '#497f66',
          borderWidth: 1
        },
        datalabels: {   
          display: false  // Disable data labels
        }
      }
    }
  });
  
});
