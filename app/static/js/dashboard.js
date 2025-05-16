document.addEventListener('DOMContentLoaded', () => {
    // Tooltip logic
    // Ensure the tooltip container exists or fallback to the trigger's parent
    const tooltipTrigger = document.getElementById('tooltip-trigger');
    const tooltipText = document.getElementById('tooltip-text');
    const tooltipContainer = document.getElementById('tooltip-container') || tooltipTrigger.parentElement;

    if (tooltipTrigger && tooltipText && tooltipContainer) {
        // Toggle tooltip on click
        tooltipTrigger.addEventListener('click', function (event) {
            event.stopPropagation();  // Prevent click bubbling
            tooltipText.classList.toggle('hidden');
        });

        document.addEventListener('click', function (event) {
            if (!tooltipContainer.contains(event.target)) {
                tooltipText.classList.add('hidden');
            }
        });
    }

    // Click handler for emission goal card
    const emissionGoalCard = document.getElementById('emission-goal-card');
    if (emissionGoalCard) {
        emissionGoalCard.addEventListener('click', function () {
            window.location.href = emissionGoalCard.dataset.url || "view_data";
        });
    }

    // Click handler for category cards
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('click', function () {
            const tabIndex = this.dataset.tab;
            window.location.href = (card.dataset.url || "view_data") + "?tab=" + tabIndex + "#emissions-summary";
        });
    });

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

    // Fetch and update dashboard metrics from backend
    fetch('/api/dashboard_metrics', {
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
            if (data.error) throw new Error(data.error);
            // Use backend-calculated metrics
            const { total, travel, home, food, shopping, goals, au_average } = data;
            updateProgressCircle(total.percentage);
            document.getElementById('emitted-total').textContent = `${total.emitted} metric tons CO₂eq emitted in total`;
            if (total.saved > 0) {
                document.getElementById('saved-total').textContent = `${total.saved} metric tons CO₂eq saved compared to Australian average households`;
            } else {
                document.getElementById('saved-total').textContent = `${(total.emitted - au_average).toFixed(1)} metric tons CO₂eq worse compared to Australian average households`;
            }
            updateCategory('travel', travel, goals.travel);
            updateCategory('home', home, goals.home);
            updateCategory('food', food, goals.food);
            updateCategory('shopping', shopping, goals.shopping);
        })
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