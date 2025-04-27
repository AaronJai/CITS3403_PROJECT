// 1. 找到画布
const ctx = document.getElementById('myChart').getContext('2d');

// 2. 写数据
const data = {
  labels: ['Travel', 'Home', 'Food', 'Shopping'],
  datasets: [
    { label: 'Vehicle', data: [50, 0, 0, 0] },
    { label: 'Public Transit', data: [50, 0, 0, 0] },
    { label: 'Air Travel', data: [50, 0, 0, 0] },
    { label: 'Electricity', data: [0, 50, 0, 0] },
    { label: 'Clean Energy', data: [0, 30, 0, 0] },
    { label: 'Natural Gas', data: [0, 20, 0, 0] },
    { label: 'Heating Oil & Other Fuels', data: [0, 50, 0, 0] },
    { label: 'Living Space Area', data: [0, 50, 0, 0] },
    { label: 'Water Usage', data: [0, 10, 0, 0] },
    { label: 'Meat/Fish/Eggs', data: [0, 0, 50, 0] },
    { label: 'Grains/Baked Goods', data: [0, 0, 0, 50] },
    { label: 'Dairy', data: [0, 0, 0, 50] },
    { label: 'Fruits/Vegetables', data: [0, 0, 50, 50] },
    { label: 'Snacks/Drinks/Other Foods Consumption', data: [0, 0, 0, 50] }
  ]
};

// 3. 写设置
const options = {
  responsive: true,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    x: { stacked: true },
    y: { 
      stacked: true,
      title: {
        display: true,
        text: 'Metric tons CO₂/year'
      }
    }
  }
};

// 4. 配置
const config = {
  type: 'bar',
  data: data,
  options: options
};

// 5. 画图！
new Chart(ctx, config);
