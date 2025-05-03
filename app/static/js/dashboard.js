document.addEventListener('DOMContentLoaded', () => {
    // Emission goals (metric tons CO2eq/year)
    const GOALS = {
        total: 2.2, // Total emissions goal
        travel: 0.7, // Vehicles, public transit, air travel
        home: 0.5, // Electricity, natural gas, heating fuels, water, construction
        food: 0.5, // Meat, dairy, fruits/vegetables, cereals, snacks
        shopping: 0.5 // Furniture, clothing, other goods, services
    };

    // Function to calculate percentage and savings
    function calculateMetrics(actual, goal) {
        const percentage = Math.min((goal / actual) * 100, 100); // Cap at 100%
        const saved = Math.max(goal - actual, 0); // Savings cannot be negative
        return {
            percentage: percentage.toFixed(0),
            saved: saved.toFixed(2),
            emitted: actual.toFixed(2)
        };
    }

    // Function to update progress circle
    function updateProgressCircle(percentage) {
        const circle = document.getElementById('progress-circle');
        const text = document.getElementById('progress-text');
        const validPercentage = (typeof percentage === 'string' || typeof percentage === 'number') && !isNaN(percentage) && percentage >= 0 ? parseFloat(percentage) : 0;
        const circumference = 282.74;
        circle.setAttribute('stroke-dasharray', circumference);
        const offset = circumference * (1 - validPercentage / 100);
        circle.setAttribute('stroke-dashoffset', offset);
        text.textContent = `${validPercentage.toFixed(0)}%`;

    }

    // Function to update progress bar
    function updateProgressBar(elementId, percentage) {
        const bar = document.getElementById(elementId);
        if (bar) {
            bar.className = `progress-bar-fill w-[${percentage}%]`;
        }
    }

    // Function to update dashboard with emissions data
    function updateDashboard(data) {
        // Aggregate category emissions
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

        // Calculate metrics
        const totalMetrics = calculateMetrics(data.total_emissions, GOALS.total);
        const travelMetrics = calculateMetrics(travelEmissions, GOALS.travel);
        const homeMetrics = calculateMetrics(homeEmissions, GOALS.home);
        const foodMetrics = calculateMetrics(foodEmissions, GOALS.food);
        const shoppingMetrics = calculateMetrics(shoppingEmissions, GOALS.shopping);

        // Update total emissions section
        updateProgressCircle(totalMetrics.percentage);
        document.getElementById('progress-text').textContent = `${totalMetrics.percentage}%`;
        const emittedTotal = document.getElementById('emitted-total');
        const savedTotal = document.getElementById('saved-total');
        if (emittedTotal && savedTotal) {
            emittedTotal.textContent = `${totalMetrics.emitted} metric tons CO2eq emitted`;
            savedTotal.textContent = `${totalMetrics.saved} metric tons CO2eq saved`;
        }

        // Update category cards
        // Travel
        updateProgressBar('travel-progress', travelMetrics.percentage);
        document.getElementById('travel-fraction').textContent = `${travelMetrics.percentage}/100`;
        document.getElementById('travel-emitted').textContent =
            `You have emitted ${travelMetrics.emitted} CO2eq out of a possible ${GOALS.travel.toFixed(2)} CO2eq`;

        // Home
        updateProgressBar('home-progress', homeMetrics.percentage);
        document.getElementById('home-fraction').textContent = `${homeMetrics.percentage}/100`;
        document.getElementById('home-emitted').textContent =
            `You have emitted ${homeMetrics.emitted} CO2eq out of a possible ${GOALS.home.toFixed(2)} CO2eq`;

        // Food
        updateProgressBar('food-progress', foodMetrics.percentage);
        document.getElementById('food-fraction').textContent = `${foodMetrics.percentage}/100`;
        document.getElementById('food-emitted').textContent =
            `You have emitted ${foodMetrics.emitted} CO2eq out of a possible ${GOALS.food.toFixed(2)} CO2eq`;

        // Shopping
        updateProgressBar('shopping-progress', shoppingMetrics.percentage);
        document.getElementById('shopping-fraction').textContent = `${shoppingMetrics.percentage}/100`;
        document.getElementById('shopping-emitted').textContent =
            `You have emitted ${shoppingMetrics.emitted} CO2eq out of a possible ${GOALS.shopping.toFixed(2)} CO2eq`;
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
            updateDashboard(data);
        })
        .catch(error => {
            // Update with error placeholders
            const progressText = document.getElementById('progress-text');
            if (progressText) {
                progressText.textContent = 'N/A';
            }
            const emittedTotal = document.getElementById('emitted-total');
            const savedTotal = document.getElementById('saved-total');
            if (emittedTotal && savedTotal) {
                emittedTotal.textContent = 'Error loading data';
                savedTotal.textContent = 'Error loading data';
            }
            const categories = ['travel', 'home', 'food', 'shopping'];
            categories.forEach(category => {
                const fraction = document.getElementById(`${category}-fraction`);
                const emitted = document.getElementById(`${category}-emitted`);
                if (fraction && emitted) {
                    fraction.textContent = '0/100';
                    emitted.textContent = 'Error loading data';
                }
            });
        });
});