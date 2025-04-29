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
        window.scrollTo({
            top: 0,
            behavior: 'smooth' // Smooth scrolling for better UX
        });
    }

    function goToPrevStep() {
        if (currentIndex > 1) {
            currentIndex--;
            updateStepper();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
    }

    function goToNextStep() {
        if (currentIndex < totalSteps) {
            currentIndex++;
            updateStepper();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
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

            const headerImageContainer = document.getElementById('stepper-header-image-container');
            if (headerImageContainer) {
                const newSrc = headerImageContainer.getAttribute(`data-step-${currentIndex}`);
                if (newSrc) {
                    headerImageContainer.style.backgroundImage = `url(${newSrc})`;
                    headerImageContainer.classList.remove('animate-bg-slide-down');
                    void headerImageContainer.offsetWidth; // Force reflow to restart animation
                    headerImageContainer.classList.add('animate-bg-slide-down');
                }
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
    addVehicle();
    addVehicle();
});

// Vehicle Template (hidden)
const vehicleTemplate = document.createElement('template');
vehicleTemplate.innerHTML = `
<div class="vehicle-mpg-container vehicle-item space-y-2 pb-4 border-b border-gray-300 last:border-b-0">
    <div class="flex gap-2">
    <select class="select select-bordered flex-1 vehicle-fuel-type">
        <option value="gasoline">Gasoline</option>
        <option value="diesel">Diesel</option>
        <option value="electric">Electric</option>
    </select>
    <button type="button" class="focus:outline-none cursor-pointer text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-2 py-1 me-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900" 
        onclick="deleteVehicle(this.closest('div.vehicle-item'))"
    >
        X
    </button>
    </div>
    
    <div class="input-group flex items-center space-x-2">
    <input type="number" class="w-full p-2 border border-gray-300 rounded-md vehicle-distance" placeholder="15,600">
    <span class="input-group-addon">kms/yr</span>
    </div>
    
    <div class="space-y-1">
    <div class="flex justify-between text-sm">
        <span>Fuel Efficiency (L/100km or kWh/100km)</span>
        <span class="vehicle-mpg-value">7</span>
    </div>
    <input type="range" min="0" max="35" value="7" step="1" class="w-full range range-primary vehicle-mpg">
    <div class="flex justify-between text-xs">
        <span>0</span>
        <span>5</span>
        <span>10</span>
        <span>15</span>
        <span>20</span>
        <span>25</span>
        <span>30</span>
        <span>35</span>
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

//Public Transport and Air Travel Form Toggle
const simpleForm = document.getElementById('simple-form');
const advancedForm = document.getElementById('advanced-form');
const showSimpleBtn = document.getElementById('show-simple');
const showAdvancedBtn = document.getElementById('show-advanced');

function setActiveButton(activeBtn, inactiveBtn) {
    activeBtn.classList.remove('bg-transparent', 'text-primary', 'hover:bg-primary/10');
    activeBtn.classList.add('bg-primary', 'text-white', 'hover:bg-primary/90');
    inactiveBtn.classList.remove('bg-primary', 'text-white', 'hover:bg-primary/90');
    inactiveBtn.classList.add('bg-transparent', 'text-primary', 'hover:bg-primary/10');
}

showSimpleBtn.addEventListener('click', () => {
    simpleForm.classList.remove('hidden');
    advancedForm.classList.add('hidden');
    setActiveButton(showSimpleBtn, showAdvancedBtn);
});

showAdvancedBtn.addEventListener('click', () => {
    advancedForm.classList.remove('hidden');
    simpleForm.classList.add('hidden');
    setActiveButton(showAdvancedBtn, showSimpleBtn);
});



//Shopping Form Toggle
document.addEventListener('DOMContentLoaded', function () {
    const simpleFormShopping = document.getElementById('shoppingSimple');
    const advancedFormShopping = document.getElementById('shoppingAdvanced');
    const showSimpleBtnShopping = document.getElementById('show-simple-shopping');
    const showAdvancedBtnShopping = document.getElementById('show-advanced-shopping');

    function syncForms(fromForm, toForm) {
        const fromInputs = fromForm.querySelectorAll('input');
        fromInputs.forEach(input => {
            if (!input.id) return; // Ignore inputs without an ID
            const matching = toForm.querySelector(`#${input.id}`);
            if (matching) matching.value = input.value;
        });
    }

    showSimpleBtnShopping.addEventListener('click', () => {
        syncForms(advancedFormShopping, simpleFormShopping);
        simpleFormShopping.classList.remove('hidden');
        advancedFormShopping.classList.add('hidden');
        setActiveButton(showSimpleBtnShopping, showAdvancedBtnShopping);
    });

    showAdvancedBtnShopping.addEventListener('click', () => {
        syncForms(simpleFormShopping, advancedFormShopping);
        advancedFormShopping.classList.remove('hidden');
        simpleFormShopping.classList.add('hidden');
        setActiveButton(showAdvancedBtnShopping, showSimpleBtnShopping);
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
    return parseFloat(value).toFixed(1) + "% of similar households";
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

