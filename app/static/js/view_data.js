const ctx = document.getElementById('myChart').getContext('2d');

const data = {
  labels: ['Travel', 'Home', 'Food', 'Shopping'],
  datasets: [
    { label: 'Vehicle', data: [50, 0, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Public Transit', data: [50, 0, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Air Travel', data: [50, 0, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Electricity', data: [0, 50, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Clean Energy', data: [0, 30, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Natural Gas', data: [0, 20, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Heating Oil & Other Fuels', data: [0, 50, 0, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Living Space Area', data: [0, 50, 0, 0], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Water Usage', data: [0, 10, 0, 0], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Meat/Fish/Eggs', data: [0, 0, 50, 0], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Grains/Baked Goods', data: [0, 0, 0, 50], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Dairy', data: [0, 0, 0, 50], backgroundColor: '#7fc8a9', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Fruits/Vegetables', data: [0, 0, 50, 50], backgroundColor: '#2f5c47', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' },
    { label: 'Snacks/Drinks/Other Foods Consumption', data: [0, 0, 0, 50], backgroundColor: '#497f66', borderColor: 'rgba(255,255,255,0.8)', borderWidth: 1, hoverBorderWidth: 3, hoverBorderColor: '#16372c' }
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
    }
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
