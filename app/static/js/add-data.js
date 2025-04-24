// Function for stepper navigation, vehicle addition, and slider functionality for the carbon footprint calculator
document.addEventListener('DOMContentLoaded', function () {
    const stepper = document.querySelector('[data-stepper]');
    const navItems = document.querySelectorAll('[data-stepper-nav-item]');
    const contentItems = document.querySelectorAll('[data-stepper-content-item]');
    const prevBtn = document.querySelector('[data-stepper-back-btn]');
    const nextBtn = document.querySelector('[data-stepper-next-btn]');
    const finishBtn = document.querySelector('[data-stepper-finish-btn]');

    let currentIndex = 1;
    const totalSteps = navItems.length;

    // Initialize stepper
    updateStepper();

    // Navigation handlers
    prevBtn.addEventListener('click', goToPrevStep);
    nextBtn.addEventListener('click', goToNextStep);
    finishBtn.addEventListener('click', finishStepper);
    navItems.forEach((item) => {
        const data = JSON.parse(item.getAttribute('data-stepper-nav-item'));
        item.addEventListener('click', () => goToStep(data.index));
    });

    function goToStep(index) {
        currentIndex = index;
        updateStepper();
    }

    function goToPrevStep() {
        if (currentIndex > 1) {
            currentIndex--;
            updateStepper();
        }
    }

    function goToNextStep() {
        if (currentIndex < totalSteps) {
            currentIndex++;
            updateStepper();
        }
    }

    function finishStepper() {
        alert('Carbon footprint calculation complete!');
    }

    function updateStepper() {
        // Update nav items
        navItems.forEach((item, index) => {
            const stepNumber = index + 1;
            const circle = item.querySelector('span span:first-child');

            // Reset all steps
            circle.classList.remove('stepper-completed', 'stepper-active');
            circle.classList.add('bg-gray-200', 'text-gray-700');

            // Current step
            if (stepNumber === currentIndex) {
                circle.classList.add('stepper-active');
                circle.classList.remove('bg-gray-200', 'text-gray-700');
            }
            // Completed steps
            else if (stepNumber < currentIndex) {
                circle.classList.add('stepper-completed');
                circle.classList.remove('bg-gray-200', 'text-gray-700');
            }
        });

        // Update content visibility
        contentItems.forEach((item, index) => {
            const stepNumber = index + 1;
            item.style.display = stepNumber === currentIndex ? 'block' : 'none';
        });

        // Update button visibility
        prevBtn.style.display = currentIndex > 1 ? 'flex' : 'none';
        nextBtn.style.display = currentIndex < totalSteps ? 'flex' : 'none';
        finishBtn.style.display = currentIndex === totalSteps ? 'flex' : 'none';
    }
});

// Vehicle Template (hidden)
const vehicleTemplate = document.createElement('template');
vehicleTemplate.innerHTML = `
<div class="vehicle-mpg-container vehicle-item space-y-2">
    <div class="flex gap-2">
    <select class="select select-bordered flex-1 vehicle-fuel-type">
        <option value="gasoline">Gasoline</option>
        <option value="diesel">Diesel</option>
        <option value="electric">Electric</option>
    </select>
    <button type="button" class="focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-2 py-1 me-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900" 
        onclick="deleteVehicle(this.closest('div.vehicle-item'))"
    >
        X
    </button>
    </div>
    
    <div class="input-group">
    <input type="number" class="input input-bordered w-full vehicle-distance" placeholder="15,600">
    <span class="input-group-addon">kms/yr</span>
    </div>
    
    <div class="space-y-1">
    <div class="flex justify-between text-sm">
        <span>Fuel Efficiency</span>
        <span class="vehicle-mpg-value">22</span>
    </div>
    <input type="range" min="10" max="115" value="22" step="1" class="w-full range range-primary vehicle-mpg">
    <div class="flex justify-between text-xs">
        <span>10</span>
        <span>25</span>
        <span>40</span>
        <span>55</span>
        <span>70</span>
        <span>85</span>
        <span>100</span>
        <span>115</span>
    </div>
    </div>
</div>
`;

// Add Vehicle
function addVehicle() {
    const addingVehicleContainer = document.getElementById('vehicles-container')
    const vehicleChildNode = vehicleTemplate.content.cloneNode(true)
    addingVehicleContainer.appendChild(vehicleChildNode);

    // Vehicle sliders
    setupSlider('.vehicle-mpg', '.vehicle-mpg-value', (slider, value) => {
        return parseFloat(value).toFixed(1);
    });
}

function deleteVehicle(el) {
    const locatingVehicleItem = el
    locatingVehicleItem.remove()
}

//Shopping Form Toggle
document.addEventListener('DOMContentLoaded', function () {
    const simpleForm = document.getElementById('shoppingSimple');
    const advancedForm = document.getElementById('shoppingAdvanced');
    const btnToAdvanced = document.getElementById('btnToAdvanced');
    const btnToSimple = document.getElementById('btnToSimple');

    function syncForms(fromForm, toForm) {
        const fromInputs = fromForm.querySelectorAll('input');
        fromInputs.forEach(input => {
            if (!input.id) return; // Ignore inputs without an ID
            const matching = toForm.querySelector(`#${input.id}`);
            if (matching) matching.value = input.value;
        });
    }

    btnToAdvanced.addEventListener('click', function () {
        syncForms(simpleForm, advancedForm);
        simpleForm.classList.add('hidden');
        advancedForm.classList.remove('hidden');
        btnToAdvanced.classList.add('hidden');
        btnToSimple.classList.remove('hidden');
    });

    btnToSimple.addEventListener('click', function () {
        syncForms(advancedForm, simpleForm);
        advancedForm.classList.add('hidden');
        simpleForm.classList.remove('hidden');
        btnToSimple.classList.add('hidden');
        btnToAdvanced.classList.remove('hidden');
    });
});


// Update slider values in real-time
function setupSlider(sliderClass, valueClass, formatter) {
    document.querySelectorAll(sliderClass).forEach(slider => {
        const valueElement = slider.closest(`${sliderClass}-container`)
            .querySelector(valueClass);

        slider.addEventListener('input', function () {
            valueElement.textContent = formatter(slider, this.value);
        });
    });
}

// Clean Energy sliders
setupSlider('.clean-energy-slider', '.clean-energy-value', (slider, value) => {
    return parseFloat(value).toFixed(1) + "%";
});

// Water Usage sliders
setupSlider('.water-usage-slider', '.water-value', (slider, value) => {
    return parseFloat(value).toFixed(1) + "%";
});

// Food sliders
setupSlider('.food-slider', '.food-value', (slider, value) => {
    return parseFloat(value).toFixed(1) + "x";
});

// Shopping sliders
setupSlider('.shopping-slider', '.shopping-value', (slider, value) => {
    const multiplier = parseFloat(value);
    const baseValues = {
        'Goods': 1311,
        'Services': 2413
    };
    const category = slider.closest('.shopping-category').querySelector('h4 span').textContent;
    const amount = Math.round(baseValues[category] * multiplier);
    return `$${amount.toLocaleString()}`;
});

