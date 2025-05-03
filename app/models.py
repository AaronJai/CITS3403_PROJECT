# Database models (ORM)
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Database Model for User (Single Row within our DB)
class User(db.Model):
    # class variables
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # store password_hash instead of plain text password for security
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class CarbonFootprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.id'), nullable=True)
    shopping_id = db.Column(db.Integer, db.ForeignKey('shopping.id'), nullable=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=True)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=True)
    emissions = db.relationship('Emissions', backref='carbon_footprint', lazy=True)
    
    travel = db.relationship('Travel', uselist=False, backref='carbon_footprint')
    home = db.relationship('Home', uselist=False, backref='carbon_footprint')
    food = db.relationship('Food', uselist=False, backref='carbon_footprint')
    shopping = db.relationship('Shopping', uselist=False, backref='carbon_footprint')

    

class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_transit_distance = db.Column(db.Float, default=0.0)
    air_travel_distance = db.Column(db.Float, default=0.0)
    # Advanced public transit fields
    bus_kms = db.Column(db.Float, default=0.0)
    transit_rail_kms = db.Column(db.Float, default=0.0)
    commuter_rail_kms = db.Column(db.Float, default=0.0)
    intercity_rail_kms = db.Column(db.Float, default=0.0)
    # Advanced air travel fields
    short_flights = db.Column(db.Integer, default=0)
    medium_flights = db.Column(db.Integer, default=0)
    long_flights = db.Column(db.Integer, default=0)
    extended_flights = db.Column(db.Integer, default=0)
    vehicles = db.relationship('Vehicle', backref='travel', lazy=True)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.id'), nullable=False)
    fuel_type = db.Column(db.String(20), nullable=False)
    distance = db.Column(db.Float, default=0.0)
    fuel_efficiency = db.Column(db.Float, default=0.0)

class Shopping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_multiplier = db.Column(db.Float, default=0.0)
    services_multiplier = db.Column(db.Float, default=0.0)
    furniture_appliances = db.Column(db.Float, default=0.0)
    clothing = db.Column(db.Float, default=0.0)
    entertainment = db.Column(db.Float, default=0.0)
    office_supplies = db.Column(db.Float, default=0.0)
    personal_care = db.Column(db.Float, default=0.0)
    services_food = db.Column(db.Float, default=0.0)
    education = db.Column(db.Float, default=0.0)
    communication = db.Column(db.Float, default=0.0)
    loan = db.Column(db.Float, default=0.0)
    transport = db.Column(db.Float, default=0.0)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meat_fish_eggs = db.Column(db.Float, default=0.0)
    grains_baked_goods = db.Column(db.Float, default=0.0)
    dairy = db.Column(db.Float, default=0.0)
    fruits_vegetables = db.Column(db.Float, default=0.0)
    snacks_drinks = db.Column(db.Float, default=0.0)

class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    electricity = db.Column(db.Float, default=0.0)
    electricity_unit = db.Column(db.String(10))
    electricity_frequency = db.Column(db.String(10))
    clean_energy_percentage = db.Column(db.Float, default=0.0)
    natural_gas = db.Column(db.Float, default=0.0)
    natural_gas_unit = db.Column(db.String(10))
    natural_gas_frequency = db.Column(db.String(10))
    heating_oil = db.Column(db.Float, default=0.0)
    heating_oil_unit = db.Column(db.String(10))
    heating_oil_frequency = db.Column(db.String(10))
    living_space = db.Column(db.Float, default=0.0)
    water_usage = db.Column(db.Float, default=0.0)

class Emissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carbon_footprint_id = db.Column(db.Integer, db.ForeignKey('carbon_footprint.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_emissions = db.Column(db.Float, default=0.0)
    car_emissions = db.Column(db.Float, default=0.0)
    air_travel_emissions = db.Column(db.Float, default=0.0)
    public_transit_emissions = db.Column(db.Float, default=0.0)
    water_emissions = db.Column(db.Float, default=0.0)
    heating_fuels_emissions = db.Column(db.Float, default=0.0)
    construction_emissions = db.Column(db.Float, default=0.0)
    electricity_emissions = db.Column(db.Float, default=0.0)
    natural_gas_emissions = db.Column(db.Float, default=0.0)
    meat_emissions = db.Column(db.Float, default=0.0)
    dairy_emissions = db.Column(db.Float, default=0.0)
    fruits_vegetables_emissions = db.Column(db.Float, default=0.0)
    cereals_emissions = db.Column(db.Float, default=0.0)
    snacks_emissions = db.Column(db.Float, default=0.0)
    clothing_emissions = db.Column(db.Float, default=0.0)
    furniture_emissions = db.Column(db.Float, default=0.0)
    other_goods_emissions = db.Column(db.Float, default=0.0)
    services_emissions = db.Column(db.Float, default=0.0)

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_date = db.Column(db.DateTime, default=datetime.utcnow)

