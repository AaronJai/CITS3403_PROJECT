// Function for stepper navigation, vehicle addition, and slider functionality for the carbon footprint calculator
document.addEventListener('DOMContentLoaded', function () {
    const stepper = document.querySelector('[data-stepper]');
    const navItems = document.querySelectorAll('[data-stepper-nav-item]');
    const contentItems = document.querySelectorAll('[data-stepper-content-item]');
    const prevBtn = document.querySelector('[data-stepper-back-btn]');
    const nextBtn = document.querySelector('[data-stepper-next-btn]');
    const finishBtn = document.querySelector('[data-stepper-finish-btn]');
    const form = document.querySelector('form');

    // Prevent form submission on Enter key press
    form.addEventListener('keypress', function (e) {
        // Check if Enter key is pressed
        if (e.key === 'Enter') {
            // Prevent default form submission
            e.preventDefault();
        }
    });

    // Track which mode is active for each section
    let isTravelSimpleMode = true;
    let isShoppingSimpleMode = true;

    // Add hidden fields to track active modes
    const travelModeField = document.createElement('input');
    travelModeField.setAttribute('type', 'hidden');
    travelModeField.setAttribute('name', 'travel_mode');
    travelModeField.setAttribute('value', 'simple');
    form.appendChild(travelModeField);

    const shoppingModeField = document.createElement('input');
    shoppingModeField.setAttribute('type', 'hidden');
    shoppingModeField.setAttribute('name', 'shopping_mode');
    shoppingModeField.setAttribute('value', 'simple');
    form.appendChild(shoppingModeField);

    // Handle form submission and use placeholder values as defaults
    form.addEventListener('submit', function (e) {
        // Before submitting, apply placeholder values to empty fields
        applyPlaceholdersToEmptyFields();
        // Now log the form values for debugging
        logFormValues();
    });

    // Function to apply placeholder values to empty fields
    function applyPlaceholdersToEmptyFields() {
        // Find all inputs with placeholder attributes
        const inputFields = document.querySelectorAll('input[placeholder]');
        inputFields.forEach(input => {
            if (input.value.trim() === '' && input.placeholder) {
                // Remove commas from placeholders before using them as values
                input.value = input.placeholder.replace(/,/g, '');
            }
        });

        // Handle vehicles specifically
        const vehicleItems = document.querySelectorAll('.vehicle-item');
        vehicleItems.forEach((vehicle, index) => {
            const distanceField = vehicle.querySelector('.vehicle-distance');
            if (distanceField && distanceField.value.trim() === '' && distanceField.placeholder) {
                distanceField.value = distanceField.placeholder.replace(/,/g, '');
            }
        });
    }

    let currentIndex = 1;
    const totalSteps = navItems.length;

    // Read the step parameter from the URL and set the initial step
    const urlParams = new URLSearchParams(window.location.search);
    const stepParam = urlParams.get('step');
    if (stepParam && !isNaN(stepParam) && stepParam >= 1 && stepParam <= totalSteps) {
        currentIndex = parseInt(stepParam);
    }

    // Initialize stepper with the correct step
    updateStepper();
    // Initialize stepper
    updateStepper();

    // Navigation handlers
    prevBtn.addEventListener('click', goToPrevStep);
    nextBtn.addEventListener('click', goToNextStep);

    // Add logging to the finish button click
    finishBtn.addEventListener('click', function () {
        // Apply placeholders before logging and submitting
        applyPlaceholdersToEmptyFields();
        logFormValues();
        finishStepper();
    });

    function logFormValues() {
        console.log('========== FORM SUBMISSION VALUES ==========');
        console.log('Active Travel Mode:', travelModeField.value);
        console.log('Active Shopping Mode:', shoppingModeField.value);

        // Log all input values
        const allInputs = form.querySelectorAll('input, select, textarea');
        const formData = {};

        allInputs.forEach(input => {
            // Skip submit buttons
            if (input.type !== 'submit') {
                formData[input.name] = input.value;
            }
        });

        // Log by category
        console.log('--- Travel Data ---');

        // Enhanced vehicle logging with details
        const vehicleItems = document.querySelectorAll('.vehicle-item');
        console.log(`Vehicles: ${vehicleItems.length}`);
        vehicleItems.forEach((vehicle, index) => {
            const fuelType = vehicle.querySelector('.vehicle-fuel-type').value;
            const distance = vehicle.querySelector('.vehicle-distance').value;
            const fuelEfficiency = vehicle.querySelector('.vehicle-mpg').value;

            console.log(`  Vehicle #${index + 1}:`);
            console.log(`    Type: ${fuelType}`);
            console.log(`    Distance: ${distance || 'Not specified'} kms/yr`);
            console.log(`    Fuel Efficiency: ${fuelEfficiency} ${fuelType === 'electric' ? 'kWh/100km' : 'L/100km'}`);
        });

        // Log simple travel data
        if (travelModeField.value === 'simple') {
            console.log('Public Transit (simple):', formData['public_transit_simple-distance']);
            console.log('Air Travel (simple):', formData['air_travel_simple-distance']);
        } else {
            // Log advanced travel data
            console.log('Bus kms:', formData['public_transit_advanced-bus_kms']);
            console.log('Transit Rail kms:', formData['public_transit_advanced-transit_rail_kms']);
            console.log('Commuter Rail kms:', formData['public_transit_advanced-commuter_rail_kms']);
            console.log('Intercity Rail kms:', formData['public_transit_advanced-intercity_rail_kms']);
            console.log('Short Flights:', formData['air_travel_advanced-short_flights']);
            console.log('Medium Flights:', formData['air_travel_advanced-medium_flights']);
            console.log('Long Flights:', formData['air_travel_advanced-long_flights']);
            console.log('Extended Flights:', formData['air_travel_advanced-extended_flights']);
        }

        console.log('--- Home Energy Data ---');
        console.log('Electricity:', formData['home_energy-electricity']);
        console.log('Electricity Unit:', formData['home_energy-electricity_unit']);
        console.log('Electricity Frequency:', formData['home_energy-electricity_frequency']);
        console.log('Clean Energy Percentage:', formData['home_energy-clean_energy_percentage']);
        console.log('Natural Gas:', formData['home_energy-natural_gas']);
        console.log('Natural Gas Unit:', formData['home_energy-natural_gas_unit']);
        console.log('Natural Gas Frequency:', formData['home_energy-natural_gas_frequency']);
        console.log('Heating Oil:', formData['home_energy-heating_oil']);
        console.log('Heating Oil Unit:', formData['home_energy-heating_oil_unit']);
        console.log('Heating Oil Frequency:', formData['home_energy-heating_oil_frequency']);
        console.log('Living Space:', formData['home_energy-living_space']);
        console.log('Water Usage:', formData['home_energy-water_usage']);

        console.log('--- Food Data ---');
        console.log('Meat/Fish/Eggs:', formData['food-meat_fish_eggs']);
        console.log('Grains/Baked Goods:', formData['food-grains_baked_goods']);
        console.log('Dairy:', formData['food-dairy']);
        console.log('Fruits/Vegetables:', formData['food-fruits_vegetables']);
        console.log('Snacks/Drinks:', formData['food-snacks_drinks']);

        console.log('--- Shopping Data ---');
        if (shoppingModeField.value === 'simple') {
            console.log('Goods Multiplier:', formData['shopping_simple-goods_multiplier']);
            console.log('Services Multiplier:', formData['shopping_simple-services_multiplier']);
        } else {
            // Goods
            console.log('Furniture & Appliances:', formData['shopping_advanced-furniture_appliances']);
            console.log('Clothing:', formData['shopping_advanced-clothing']);
            console.log('Entertainment:', formData['shopping_advanced-entertainment']);
            console.log('Office Supplies:', formData['shopping_advanced-office_supplies']);
            console.log('Personal Care:', formData['shopping_advanced-personal_care']);

            // Services
            console.log('Services Food:', formData['shopping_advanced-services_food']);
            console.log('Education:', formData['shopping_advanced-education']);
            console.log('Communication:', formData['shopping_advanced-communication']);
            console.log('Loan:', formData['shopping_advanced-loan']);
            console.log('Transport:', formData['shopping_advanced-transport']);
        }
        console.log('===========================================');
    }

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
        isTravelSimpleMode = true;
        travelModeField.setAttribute('value', 'simple');
    });

    showAdvancedBtn.addEventListener('click', () => {
        advancedForm.classList.remove('hidden');
        simpleForm.classList.add('hidden');
        setActiveButton(showAdvancedBtn, showSimpleBtn);
        isTravelSimpleMode = false;
        travelModeField.setAttribute('value', 'advanced');
    });

    //Shopping Form Toggle
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
        isShoppingSimpleMode = true;
        shoppingModeField.setAttribute('value', 'simple');
    });

    showAdvancedBtnShopping.addEventListener('click', () => {
        syncForms(simpleFormShopping, advancedFormShopping);
        advancedFormShopping.classList.remove('hidden');
        simpleFormShopping.classList.add('hidden');
        setActiveButton(showAdvancedBtnShopping, showSimpleBtnShopping);
        isShoppingSimpleMode = false;
        shoppingModeField.setAttribute('value', 'advanced');
    });
});

// Vehicle addition and deletion
let vehicleIndex = 0;

function addVehicle() {
    const container = document.getElementById('vehicles-container');
    const clone = vehicleTemplate.content.cloneNode(true);

    // Set proper name attributes based on index
    const inputs = clone.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.name = `${input.name}${vehicleIndex}`;
    });

    container.appendChild(clone);
    vehicleIndex++;

    // Reattach sliders for new elements
    setupSlider('.vehicle-mpg', '.vehicle-mpg-value', (slider, value) => {
        return parseFloat(value).toFixed(1);
    });
}


function deleteVehicle(el) {
    const locatingVehicleItem = el
    locatingVehicleItem.remove()
}

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

