from app.models import Travel, Vehicle, Home, Food, Shopping, CarbonFootprint, Emissions, Share
from flask import request
from app import db

def process_travel_data(mode, pts, pta, ats, ata):
    travel = Travel()
    if mode == 'simple':
        travel.public_transit_distance = pts.distance.data
        travel.air_travel_distance = ats.distance.data
    else:
        travel.bus_kms = pta.bus_kms.data
        travel.transit_rail_kms = pta.transit_rail_kms.data
        travel.commuter_rail_kms = pta.commuter_rail_kms.data
        travel.intercity_rail_kms = pta.intercity_rail_kms.data
        travel.short_flights = ata.short_flights.data
        travel.medium_flights = ata.medium_flights.data
        travel.long_flights = ata.long_flights.data
        travel.extended_flights = ata.extended_flights.data
    return travel

def process_vehicles_data(travel_id):
    vehicles = []
    valid_fuel_types = ['gasoline', 'diesel', 'electric']
    i = 0
    while True:
        fuel_type = request.form.get(f'vehicle-fuel_type{i}')
        distance = request.form.get(f'vehicle-distance{i}')
        efficiency = request.form.get(f'vehicle-fuel_efficiency{i}')
        if not fuel_type or fuel_type not in valid_fuel_types:
            break
        vehicles.append(Vehicle(
            travel_id=travel_id,
            fuel_type=fuel_type,
            distance=distance,
            fuel_efficiency=efficiency
        ))
        i += 1
    return vehicles

def process_home_data(form):
    return Home(
        electricity=form.electricity.data,
        electricity_unit=form.electricity_unit.data,
        electricity_frequency=form.electricity_frequency.data,
        clean_energy_percentage=form.clean_energy_percentage.data,
        natural_gas=form.natural_gas.data,
        natural_gas_unit=form.natural_gas_unit.data,
        natural_gas_frequency=form.natural_gas_frequency.data,
        heating_oil=form.heating_oil.data,
        heating_oil_unit=form.heating_oil_unit.data,
        heating_oil_frequency=form.heating_oil_frequency.data,
        living_space=form.living_space.data,
        water_usage=form.water_usage.data
    )

def process_food_data(form):
    return Food(
        meat_fish_eggs=form.meat_fish_eggs.data,
        grains_baked_goods=form.grains_baked_goods.data,
        dairy=form.dairy.data,
        fruits_vegetables=form.fruits_vegetables.data,
        snacks_drinks=form.snacks_drinks.data
    )

def process_shopping_data(mode, simple_form, advanced_form):
    shopping = Shopping()
    if mode == 'simple':
        shopping.goods_multiplier = simple_form.goods_multiplier.data
        shopping.services_multiplier = simple_form.services_multiplier.data
    else:
        shopping.furniture_appliances = advanced_form.furniture_appliances.data
        shopping.clothing = advanced_form.clothing.data
        shopping.entertainment = advanced_form.entertainment.data
        shopping.office_supplies = advanced_form.office_supplies.data
        shopping.personal_care = advanced_form.personal_care.data
        shopping.services_food = advanced_form.services_food.data
        shopping.education = advanced_form.education.data
        shopping.communication = advanced_form.communication.data
        shopping.loan = advanced_form.loan.data
        shopping.transport = advanced_form.transport.data
    return shopping

def delete_user_and_data(user):
    footprints = CarbonFootprint.query.filter_by(user_id=user.id).all()
    for fp in footprints:
        Emissions.query.filter_by(carbon_footprint_id=fp.id).delete()
        if fp.travel_id:
            Vehicle.query.filter_by(travel_id=fp.travel_id).delete()
            Travel.query.filter_by(id=fp.travel_id).delete()
        if fp.home_id:
            Home.query.filter_by(id=fp.home_id).delete()
        if fp.food_id:
            Food.query.filter_by(id=fp.food_id).delete()
        if fp.shopping_id:
            Shopping.query.filter_by(id=fp.shopping_id).delete()
    CarbonFootprint.query.filter_by(user_id=user.id).delete()
    Share.query.filter(
        (Share.from_user_id == user.id) |
        (Share.to_user_id == user.id)
    ).delete()
    db.session.delete(user)
    db.session.commit()
