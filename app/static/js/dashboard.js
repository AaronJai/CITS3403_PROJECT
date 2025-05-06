document.addEventListener('DOMContentLoaded', () => {
    const GOALS = {
        total: 12.3,
        travel: 2.9,
        home: 3.5,
        food: 3.1,
        shopping: 2.8
    };
    // Calculate the percentage of emissions saved and emitted
    function calculateMetrics(actual, goal) {
        const percentage = Math.min(((goal - actual) / goal) * 100, 100);
        const saved = Math.max(15.01 - actual, 0); //compared to the average Australian household
        return {
            percentage: percentage.toFixed(0),
            saved: saved.toFixed(2),
            emitted: actual.toFixed(2)
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
    function updateProgressBar(elementId, percentage) {
        const bar = document.getElementById(elementId);
        if (!bar || isNaN(percentage)) return;

        const safePercentage = Math.max(0, parseFloat(percentage));

        bar.className = 'progress-bar-fill';
        bar.style.width = `${safePercentage}%`;
        bar.classList.remove('bg-red-500', 'bg-yellow-400', 'bg-green-700', 'bg-transparent');

        if (percentage < 0) {
            bar.classList.add('bg-transparent'); // No fill for negative
        } else if (percentage <= 20) {
            bar.classList.add('bg-red-500');
        } else if (percentage < 50) {
            bar.classList.add('bg-yellow-400');
        } else {
            bar.classList.add('bg-green-700');
        }
    }


    // Update the dashboard with the fetched data
    function updateDashboard(data) {
        const travelEmissions = (
            data.car_emissions +
            data.public_transit_emissions +
            data.air_travel_emissions
        );
        const homeEmissions = (
            data.electricity_emissions +
            data.natural_gas_emissions +
            data.heating_fuels_emissions +
            data.water_emissions +
            data.construction_emissions
        );
        const foodEmissions = (
            data.meat_emissions +
            data.dairy_emissions +
            data.fruits_vegetables_emissions +
            data.cereals_emissions +
            data.snacks_emissions
        );
        const shoppingEmissions = (
            data.furniture_emissions +
            data.clothing_emissions +
            data.other_goods_emissions +
            data.services_emissions
        );

        const totalMetrics = calculateMetrics(data.total_emissions, GOALS.total);
        const travelMetrics = calculateMetrics(travelEmissions, GOALS.travel);
        const homeMetrics = calculateMetrics(homeEmissions, GOALS.home);
        const foodMetrics = calculateMetrics(foodEmissions, GOALS.food);
        const shoppingMetrics = calculateMetrics(shoppingEmissions, GOALS.shopping);

        // Update the dashboard with the calculated metrics
        updateProgressCircle(totalMetrics.percentage);
        document.getElementById('emitted-total').textContent = `${totalMetrics.emitted} metric tons CO₂eq emitted so far`;
        document.getElementById('saved-total').textContent = `${totalMetrics.saved} metric tons CO₂eq saved compared to Australian average households`;

        updateProgressBar('travel-progress', travelMetrics.percentage);
        document.getElementById('travel-fraction').textContent = `Achieved ${travelMetrics.percentage}% for this year's goal`;
        document.getElementById('travel-emitted').innerHTML =
            `<strong>Current emitted: </strong>${travelMetrics.emitted} CO₂eq<br> <strong> Annual goal: </strong> ${GOALS.travel.toFixed(2)} CO₂eq`;

        updateProgressBar('home-progress', homeMetrics.percentage);
        document.getElementById('home-fraction').textContent = `Achieved ${homeMetrics.percentage}% for this year's goal`;
        document.getElementById('home-emitted').innerHTML =
            `<strong>Current emitted:</strong> ${homeMetrics.emitted} CO₂eq<br> <strong> Annual goal: </strong> ${GOALS.home.toFixed(2)} CO₂eq`;

        updateProgressBar('food-progress', foodMetrics.percentage);
        document.getElementById('food-fraction').textContent = `Achieved ${foodMetrics.percentage}% for this year's goal`;
        document.getElementById('food-emitted').innerHTML =
            `<strong>Current emitted:</strong> ${foodMetrics.emitted} CO₂eq<br> <strong> Annual goal: </strong> ${GOALS.food.toFixed(2)} CO₂eq`;

        updateProgressBar('shopping-progress', shoppingMetrics.percentage);
        document.getElementById('shopping-fraction').textContent = `Achieved ${shoppingMetrics.percentage}% for this year's goal`;
        document.getElementById('shopping-emitted').innerHTML =
            `<strong>Current emitted:</strong> ${shoppingMetrics.emitted} CO₂eq<br> <strong> Annual goal:</strong> ${GOALS.shopping.toFixed(2)} CO₂eq`;
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
                document.getElementById(`${category}-fraction`).textContent = '0/100';
                document.getElementById(`${category}-emitted`).textContent = 'Error loading data';
            });
        });
});
