# for static structures, mappings, etc.

nav_items = [
    {"name": "Dashboard", "endpoint": "main.dashboard", "icon": "dashboard.svg"},
    {"name": "Add Data", "endpoint": "main.add_data", "icon": "add_data.svg"},
    {"name": "View Data", "endpoint": "main.view_data", "icon": "view_data.svg"},
    {"name": "Share", "endpoint": "main.share", "icon": "share.svg"},
    {"name": "Facts", "endpoint": "main.facts", "icon": "facts.svg"},
]

# Emission factors (in kg CO2e)
EMISSION_FACTORS = {
    'vehicle': {
        'gasoline': 2.34,  # kg CO₂e per litre
        'diesel': 2.69,    # kg CO₂e per litre
        'electric': 0.68   # kg CO₂e per kWh
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
        'electricity_kwh': 0.68,      
        'electricity_dollar': 0.33,
        'natural_gas_therm': 0.181, 
        'natural_gas_m3': 0.038,     
        'natural_gas_dollar': 4.08, 
        'heating_oil_litre': 0.671,
        'heating_oil_dollar': 1.46, 
        'water_usage': 0.00046,      
        'construction': 0.42         
    },
    'food': {
        'meat_fish_eggs': 4.05,       
        'grains_baked_goods': 0.23,   
        'dairy': 0.95,                
        'fruits_vegetables': 0.35,    
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