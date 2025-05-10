document.addEventListener('DOMContentLoaded', () => {
    const tooltipTrigger = document.getElementById('tooltip-trigger');
    const tooltipText = document.getElementById('tooltip-text');

    if (tooltipTrigger && tooltipText) {
        tooltipTrigger.addEventListener('mouseenter', () => {
            tooltipText.classList.remove('hidden');
        });
        tooltipTrigger.addEventListener('mouseleave', () => {
            tooltipText.classList.add('hidden');
        });
    }

    const GOALS = {
        total: 12.3,
        travel: 2.9,
        home: 3.5,
        food: 3.1,
        shopping: 2.8
    };

    // Calculate the percentage of emissions saved and emitted
    function calculateMetrics(actual, goal) {
        const percentage = (actual / goal) * 100;
        const isBelow = actual <= goal;
        const saved = Math.max(15.01 - actual, 0); // Assuming 15.01tons is the average emissions for Australian households
        return {
            percentage: percentage.toFixed(0),
            saved: saved.toFixed(2),
            emitted: actual.toFixed(2),
            isBelow
        };
    }

    // Update the progress circle and text
    function updateProgressCircle(percentage) {
        const arc = document.getElementById('gauge-arc');
        const text = document.getElementById('progress-text');
        const validPercentage = (typeof percentage === 'string' || typeof percentage === 'number') && !isNaN(percentage) && percentage >= 0 ? parseFloat(percentage) : 0;

        const maxOffset = 282.743;
        const offset = maxOffset * (1 - Math.min(validPercentage, 100) / 100);
        arc.setAttribute('stroke-dashoffset', offset);
        text.textContent = `${validPercentage.toFixed(0)}%`;
    }

    // Update the progress bar and text
    function updateProgressBar(elementId, percentage, isBelow) {
        const bar = document.getElementById(elementId);
        if (!bar || isNaN(percentage)) return;

        const safePercentage = Math.max(0, parseFloat(percentage));
        bar.className = 'progress-bar-fill';
        bar.style.width = `${Math.min(safePercentage, 100)}%`;
        bar.classList.remove('bg-red-500', 'bg-yellow-400', 'bg-green-700', 'bg-transparent');

        if (percentage < 0) {
            bar.classList.add('bg-transparent');
        } else {
            bar.classList.add(isBelow ? 'bg-green-700' : 'bg-red-500');
        }
    }

    // Update a single category's dashboard elements
    function updateCategory(category, metrics, goal) {
        const prefix = `${category}-`;
        updateProgressBar(`${prefix}progress`, metrics.percentage, metrics.isBelow);
        document.getElementById(`${prefix}fraction`).innerHTML = `${metrics.isBelow
            ? `You've used <strong> ${metrics.percentage}%</strong> of your annual goal! <br> Great work!`
            : `You've used <strong>${metrics.percentage}%</strong> of your annual goal (<strong>${metrics.percentage - 100}%</strong> over) <br> Keep reducing your emissions!`}`;
        document.getElementById(`${prefix}emitted`).innerHTML = `
            <span style="font-weight: bold">Current emitted: </span>${metrics.emitted} CO₂eq<br>
            <span style="font-weight: bold">Annual goal: </span>${goal.toFixed(2)} CO₂eq`;
        const status = document.getElementById(`${prefix}status`);
        if (status) {
            status.textContent = metrics.isBelow ? 'better than other households' : 'worse off';
            status.classList.remove('text-green-700', 'text-red-500');
            status.classList.add(metrics.isBelow ? 'text-green-700' : 'text-red-500');
        }
    }

    // Update the dashboard with the fetched data
    function updateDashboard(data) {
        const travelEmissions = data.car_emissions + data.public_transit_emissions + data.air_travel_emissions;
        const homeEmissions = data.electricity_emissions + data.natural_gas_emissions + data.heating_fuels_emissions +
            data.water_emissions + data.construction_emissions;
        const foodEmissions = data.meat_emissions + data.dairy_emissions + data.fruits_vegetables_emissions +
            data.cereals_emissions + data.snacks_emissions;
        const shoppingEmissions = data.furniture_emissions + data.clothing_emissions + data.other_goods_emissions +
            data.services_emissions;

        const totalMetrics = calculateMetrics(data.total_emissions, GOALS.total);
        const travelMetrics = calculateMetrics(travelEmissions, GOALS.travel);
        const homeMetrics = calculateMetrics(homeEmissions, GOALS.home);
        const foodMetrics = calculateMetrics(foodEmissions, GOALS.food);
        const shoppingMetrics = calculateMetrics(shoppingEmissions, GOALS.shopping);

        updateProgressCircle(totalMetrics.percentage);
        document.getElementById('emitted-total').textContent = `${totalMetrics.emitted} metric tons CO₂eq emitted in total`;
        document.getElementById('saved-total').textContent = `${totalMetrics.saved} metric tons CO₂eq saved compared to Australian average households`;

        updateCategory('travel', travelMetrics, GOALS.travel);
        updateCategory('home', homeMetrics, GOALS.home);
        updateCategory('food', foodMetrics, GOALS.food);
        updateCategory('shopping', shoppingMetrics, GOALS.shopping);
    }

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
        .then(data => updateDashboard(data))
        .catch(error => {
            document.getElementById('progress-text').textContent = 'N/A';
            document.getElementById('emitted-total').textContent = 'Error loading data';
            document.getElementById('saved-total').textContent = 'Error loading data';
            ['travel', 'home', 'food', 'shopping'].forEach(category => {
                const prefix = `${category}-`;
                document.getElementById(`${prefix}fraction`).textContent = '0%';
                document.getElementById(`${prefix}emitted`).textContent = 'Error loading data';
                const status = document.getElementById(`${prefix}status`);
                if (status) {
                    status.textContent = 'Error loading data';
                    status.classList.remove('text-green-700', 'text-red-500');
                }
            });
        });
});