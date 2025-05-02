from app.models import CarbonFootprint, Travel, Vehicle, Home, Food, Shopping, Emissions

# Emission factors (in kg CO2e)
EMISSION_FACTORS = {
    'vehicle': {
        'gasoline': 0.008887,  
        'diesel': 0.010135,    
        'electric': 0.066667  
    },
    'public_transit': {
        'simple': 0.036661,    
        'bus': 0.064622,      
        'transit_rail': 0.025476, 
        'commuter_rail': 0.039768, 
        'intercity_rail': 0.017398 
    },
    'air_travel': {
        'simple': 0.087489,   
        'short': 0.2,          
        'medium': 0.15,        
        'long': 0.12,          
        'extended': 0.11       
    },
    'home': {
        'electricity_kwh': 0.4,      
        'electricity_dollar': 0.008,
        'natural_gas_therm': 0.181, 
        'natural_gas_m3': 0.038,     
        'natural_gas_dollar': 0.006,
        'heating_oil_litre': 0.00268,
        'heating_oil_dollar': 0.001, 
        'water_usage': 0.00113,      
        'construction': 0.05         
    },
    'food': {
        'meat_fish_eggs': 4.8,       
        'grains_baked_goods': 1.5,   
        'dairy': 3.2,                
        'fruits_vegetables': 0.9,    
        'snacks_drinks': 2.0         
    },
    'shopping': {
        'goods_base': 1311,          
        'services_base': 2413,       
        'furniture_appliances': 0.5, 
        'clothing': 0.6,             
        'entertainment': 0.4,        
        'office_supplies': 0.7,      
        'personal_care': 0.5,        
        'services_food': 0.3,        
        'education': 0.2,            
        'communication': 0.25,       
        'loan': 0.15,                
        'transport': 0.35            
    }
}

class CarbonFootprintCalculator:
    """
    Class to calculate carbon footprint based on various factors and update Emissions model.
    """

    def __init__(self, emission: Emissions):
        self.emission = emission

    def calculate_travel(self, mode: str, travel: Travel):
        """
        Process travel data and calculate emissions for public transit and air travel.
        Updates self.emission.public_transit_emissions and self.emission.air_travel_emissions.
        Returns a tuple of (Travel instance, emissions dict).
        """
        emissions = {'public_transit': 0.0, 'air_travel': 0.0}

        if mode == 'simple':
            # Simple mode: distances in miles
            emissions['public_transit'] = (travel.public_transit_distance * EMISSION_FACTORS['public_transit']['simple']) / 1000
            emissions['air_travel'] = (travel.air_travel_distance * EMISSION_FACTORS['air_travel']['simple']) / 1000
        else:
            # Advanced mode: distances in km, convert to miles for public transit emission factors
            public_transit_emissions = (
                (travel.bus_kms / 1.60934) * EMISSION_FACTORS['public_transit']['bus'] +
                (travel.transit_rail_kms / 1.60934) * EMISSION_FACTORS['public_transit']['transit_rail'] +
                (travel.commuter_rail_kms / 1.60934) * EMISSION_FACTORS['public_transit']['commuter_rail'] +
                (travel.intercity_rail_kms / 1.60934) * EMISSION_FACTORS['public_transit']['intercity_rail']
            )
            emissions['public_transit'] = public_transit_emissions / 1000

            # Air travel: use km directly
            air_travel_emissionss = (
                travel.short_flights * 400 * EMISSION_FACTORS['air_travel']['short'] +
                travel.medium_flights * 1000 * EMISSION_FACTORS['air_travel']['medium'] +
                travel.long_flights * 2250 * EMISSION_FACTORS['air_travel']['long'] +
                travel.extended_flights * 4000 * EMISSION_FACTORS['air_travel']['extended']
            )
            emissions['air_travel'] = air_travel_emissionss / 1000

        self.emission.public_transit_emissions = emissions['public_transit']
        self.emission.air_travel_emissions = emissions['air_travel']
        return emissions

    def calculate_vehicles(self, vehicles: list[Vehicle]):
        """
        Process vehicle data and calculate emissions.
        Updates self.emission.car_emissions.
        Returns car emissions in metric tons CO2e.
        """
        car_emissions = 0.0
        for vehicle in vehicles:
            fuel_type = vehicle.fuel_type
            distance = float(vehicle.distance) if vehicle.distance else 0.0
            efficiency = float(vehicle.fuel_efficiency) if vehicle.fuel_efficiency else 0.0
            if fuel_type and distance and efficiency:
                vehicle_emissions = distance * EMISSION_FACTORS['vehicle'][fuel_type]
                car_emissions += vehicle_emissions / 1000  # Convert kg to metric tons

        self.emission.car_emissions = car_emissions
        return car_emissions

    def calculate_home(self, home: Home):
        """
        Process home energy data and calculate emissions.
        Updates self.emission.electricity_emissions, natural_gas_emissions, heating_fuels_emissions,
        water_emissions, and construction_emissions.
        Returns a tuple of (Home instance, emissions dict).
        """
        emissions = {
            'electricity': 0.0,
            'natural_gas': 0.0,
            'heating_fuels': 0.0,
            'water': 0.0,
            'construction': 0.0
        }
        # Electricity
        factor = EMISSION_FACTORS['home']['electricity_kwh'] if home.electricity_unit == 'kWh' else EMISSION_FACTORS['home']['electricity_dollar']
        freq_factor = 1 if home.electricity_frequency == '/yr' else 12
        clean_energy_factor = 1 - (home.clean_energy_percentage / 100)
        emissions['electricity'] = (home.electricity * factor * freq_factor * clean_energy_factor) / 1000

        # Natural Gas
        if home.natural_gas_unit == 'therms':
            factor = EMISSION_FACTORS['home']['natural_gas_therm']
        elif home.natural_gas_unit == 'm³':
            factor = EMISSION_FACTORS['home']['natural_gas_m3']
        else:  # $
            factor = EMISSION_FACTORS['home']['natural_gas_dollar']
        freq_factor = 1 if home.natural_gas_frequency == '/yr' else 12
        emissions['natural_gas'] = (home.natural_gas * factor * freq_factor) / 1000

        # Heating Oil
        factor = EMISSION_FACTORS['home']['heating_oil_litre'] if home.heating_oil_unit == 'litres' else EMISSION_FACTORS['home']['heating_oil_dollar']
        freq_factor = 1 if home.heating_oil_frequency == '/yr' else 12
        emissions['heating_fuels'] = (home.heating_oil * factor * freq_factor) / 1000

        # Water Usage
        emissions['water'] = (home.water_usage * 365 * EMISSION_FACTORS['home']['water_usage']) / 1000

        # Construction (based on living space)
        emissions['construction'] = (home.living_space * EMISSION_FACTORS['home']['construction']) / 1000

        self.emission.electricity_emissions = emissions['electricity']
        self.emission.natural_gas_emissions = emissions['natural_gas']
        self.emission.heating_fuels_emissions = emissions['heating_fuels']
        self.emission.water_emissions = emissions['water']
        self.emission.construction_emissions = emissions['construction']
        return emissions

    def calculate_food(self, food: Food):
        """
        Process food data and calculate emissions.
        Updates self.emission.meat_emissions, dairy_emissions, fruits_vegetables_emissions,
        cereals_emissions, and snacks_emissions.
        Returns a tuple of (Food instance, emissions dict).
        """
        emissions = {
            'meat': (food.meat_fish_eggs * 365 * EMISSION_FACTORS['food']['meat_fish_eggs']) / 1000,
            'cereals': (food.grains_baked_goods * 365 * EMISSION_FACTORS['food']['grains_baked_goods']) / 1000,
            'dairy': (food.dairy * 365 * EMISSION_FACTORS['food']['dairy']) / 1000,
            'fruits_vegetables': (food.fruits_vegetables * 365 * EMISSION_FACTORS['food']['fruits_vegetables']) / 1000,
            'snacks': (food.snacks_drinks * 365 * EMISSION_FACTORS['food']['snacks_drinks']) / 1000
        }

        self.emission.meat_emissions = emissions['meat']
        self.emission.dairy_emissions = emissions['dairy']
        self.emission.fruits_vegetables_emissions = emissions['fruits_vegetables']
        self.emission.cereals_emissions = emissions['cereals']
        self.emission.snacks_emissions = emissions['snacks']
        return emissions

    def calculate_shopping(self, mode: str, shopping: Shopping):
        """
        Process shopping data and calculate emissions.
        Updates self.emission.furniture_emissions, clothing_emissions, other_goods_emissions,
        and services_emissions.
        Returns a tuple of (Shopping instance, emissions dict).
        """
        emissions = {
            'furniture': 0.0,
            'clothing': 0.0,
            'other_goods': 0.0,
            'services': 0.0
        }
        if mode == 'simple':
            # Split goods_base evenly across furniture, clothing, other_goods
            goods_emission = shopping.goods_multiplier * EMISSION_FACTORS['shopping']['goods_base']
            emissions['furniture'] = (goods_emission / 3) / 1000
            emissions['clothing'] = (goods_emission / 3) / 1000
            emissions['other_goods'] = (goods_emission / 3) / 1000
            emissions['services'] = (shopping.services_multiplier * EMISSION_FACTORS['shopping']['services_base']) / 1000
        else:
            # Goods emissions
            emissions['furniture'] = (shopping.furniture_appliances * EMISSION_FACTORS['shopping']['furniture_appliances']) / 1000
            emissions['clothing'] = (shopping.clothing * EMISSION_FACTORS['shopping']['clothing']) / 1000
            emissions['other_goods'] = (
                (shopping.entertainment * EMISSION_FACTORS['shopping']['entertainment']) +
                (shopping.office_supplies * EMISSION_FACTORS['shopping']['office_supplies']) +
                (shopping.personal_care * EMISSION_FACTORS['shopping']['personal_care'])
            ) / 1000
            # Services emissions
            emissions['services'] = (
                (shopping.services_food * EMISSION_FACTORS['shopping']['services_food']) +
                (shopping.education * EMISSION_FACTORS['shopping']['education']) +
                (shopping.communication * EMISSION_FACTORS['shopping']['communication']) +
                (shopping.loan * EMISSION_FACTORS['shopping']['loan']) +
                (shopping.transport * EMISSION_FACTORS['shopping']['transport'])
            ) / 1000

        self.emission.furniture_emissions = emissions['furniture']
        self.emission.clothing_emissions = emissions['clothing']
        self.emission.other_goods_emissions = emissions['other_goods']
        self.emission.services_emissions = emissions['services']
        return emissions

    def calculate_total_emissions(self):
        """
        Calculate total emissions as the sum of all individual fields.
        Updates self.emission.total_emissions.
        Returns total emissions in metric tons CO2e.
        """
        total_emissions = (
            (self.emission.car_emissions or 0.0) +
            (self.emission.public_transit_emissions or 0.0) +
            (self.emission.air_travel_emissions or 0.0) +
            (self.emission.electricity_emissions or 0.0) +
            (self.emission.natural_gas_emissions or 0.0) +
            (self.emission.heating_fuels_emissions or 0.0) +
            (self.emission.water_emissions or 0.0) +
            (self.emission.construction_emissions or 0.0) +
            (self.emission.meat_emissions or 0.0) +
            (self.emission.dairy_emissions or 0.0) +
            (self.emission.fruits_vegetables_emissions or 0.0) +
            (self.emission.cereals_emissions or 0.0) +
            (self.emission.snacks_emissions or 0.0) +
            (self.emission.furniture_emissions or 0.0) +
            (self.emission.clothing_emissions or 0.0) +
            (self.emission.other_goods_emissions or 0.0) +
            (self.emission.services_emissions or 0.0)
        )
        self.emission.total_emissions = total_emissions
        return total_emissions