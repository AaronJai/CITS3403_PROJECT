from app import app, db
from flask import redirect, render_template, request, url_for, flash, session, flash, jsonify
import re
from app.constants import nav_items
from app.forms import LoginForm, SignupForm, ChangePasswordForm, ShareForm
from app.forms import VehicleForm, PublicTransitSimpleForm, PublicTransitAdvancedForm
from app.forms import AirTravelSimpleForm, AirTravelAdvancedForm, HomeEnergyForm
from app.forms import FoodForm, ShoppingSimpleForm, ShoppingAdvancedForm, CarbonFootprintForm
from app.models import User, CarbonFootprint, Travel, Vehicle, Home, Food, Shopping, Emissions
from app.processing_layer import CarbonFootprintCalculator

@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', 
                          active_page='dashboard', 
                          nav_items=nav_items,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          email=user.email)

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    # Instantiate all forms
    form = CarbonFootprintForm()
    vehicle_form = VehicleForm(prefix='vehicle')
    public_transit_simple = PublicTransitSimpleForm(prefix='public_transit_simple')
    public_transit_advanced = PublicTransitAdvancedForm(prefix='public_transit_advanced')
    air_travel_simple = AirTravelSimpleForm(prefix='air_travel_simple')
    air_travel_advanced = AirTravelAdvancedForm(prefix='air_travel_advanced')
    home_energy = HomeEnergyForm(prefix='home_energy')
    food = FoodForm(prefix='food')
    shopping_simple = ShoppingSimpleForm(prefix='shopping_simple')
    shopping_advanced = ShoppingAdvancedForm(prefix='shopping_advanced')

    if request.method == 'POST':
        # Get the active mode for travel and shopping sections
        travel_mode = request.form.get('travel_mode', 'simple')
        shopping_mode = request.form.get('shopping_mode', 'simple')

        # Process form submission
        if 'calculate_footprint' in request.form:

            is_valid = home_energy.validate() and food.validate()
            if travel_mode == 'simple':
                is_valid &= public_transit_simple.validate() and air_travel_simple.validate()
            else:
                is_valid &= public_transit_advanced.validate() and air_travel_advanced.validate()

            if shopping_mode == 'simple':
                is_valid &= shopping_simple.validate()
            else:
                is_valid &= shopping_advanced.validate()

            if not is_valid:
                flash("There were errors in your submission. Please correct them and try again.", "danger")
                return render_template(
                    'add_data.html',
                    active_page='add_data',
                    nav_items=nav_items,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    form=form,
                    vehicle_form=vehicle_form,
                    public_transit_simple=public_transit_simple,
                    public_transit_advanced=public_transit_advanced,
                    air_travel_simple=air_travel_simple,
                    air_travel_advanced=air_travel_advanced,
                    home_energy=home_energy,
                    food=food,
                    shopping_simple=shopping_simple,
                    shopping_advanced=shopping_advanced
                )

            calc = CarbonFootprintCalculator(Emissions())

            # Process and save data
            travel = process_travel_data(
                travel_mode,
                public_transit_simple,
                public_transit_advanced,
                air_travel_simple,
                air_travel_advanced
            )
            calc.calculate_travel(travel_mode, travel)

            db.session.add(travel)
            db.session.flush()

            vehicles = process_vehicles_data(travel.id)
            for vehicle in vehicles:
                db.session.add(vehicle)
            calc.calculate_vehicles(vehicles)

            home = process_home_data(home_energy)
            calc.calculate_home(home)

            food_data = process_food_data(food)
            calc.calculate_food(food_data)

            shopping = process_shopping_data(shopping_mode, shopping_simple, shopping_advanced)
            calc.calculate_shopping(shopping_mode, shopping)

            db.session.add_all([home, food_data, shopping])
            db.session.flush()

            footprint = CarbonFootprint(
                user_id=user.id,
                travel_id=travel.id,
                home_id=home.id,
                food_id=food_data.id,
                shopping_id=shopping.id
            )
            db.session.add(footprint)
            db.session.flush()

            calc.calculate_total_emissions()
            calc.emission.carbon_footprint_id = footprint.id
            calc.emission.user_id = user.id
            db.session.add(calc.emission)
            db.session.commit()

            flash('Your carbon footprint has been calculated and saved!', 'success')
            return redirect(url_for('view_data'))

    return render_template(
        'add_data.html',
        active_page='add_data',
        nav_items=nav_items,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        form=form,
        vehicle_form=vehicle_form,
        public_transit_simple=public_transit_simple,
        public_transit_advanced=public_transit_advanced,
        air_travel_simple=air_travel_simple,
        air_travel_advanced=air_travel_advanced,
        home_energy=home_energy,
        food=food,
        shopping_simple=shopping_simple,
        shopping_advanced=shopping_advanced
    )

def process_travel_data(mode, pts:PublicTransitSimpleForm, pta:PublicTransitAdvancedForm, ats:AirTravelSimpleForm, ata:AirTravelAdvancedForm):
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
    """
    Process vehicle form data and return a list of Vehicle objects.
    """
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

def process_home_data(form:HomeEnergyForm):
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

def process_food_data(form:FoodForm):
    return Food(
        meat_fish_eggs=form.meat_fish_eggs.data,
        grains_baked_goods=form.grains_baked_goods.data,
        dairy=form.dairy.data,
        fruits_vegetables=form.fruits_vegetables.data,
        snacks_drinks=form.snacks_drinks.data
    )

def process_shopping_data(mode, simple_form:ShoppingSimpleForm, advanced_form:ShoppingAdvancedForm):
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



@app.route('/view_data')
def view_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('view_data.html', 
                          active_page='view_data', 
                          nav_items=nav_items,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          email=user.email)

@app.route('/share', methods=['GET', 'POST'])
def share():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    form = ShareForm()
    search_results = None
    
    if form.validate_on_submit():
        search_email = form.search_email.data
        search_results = User.query.filter_by(email=search_email).first()
        if not search_results:
            flash('No user found with that email address.', 'warning')
        else:
            flash('User found!', 'success')
    
    # Placeholder data for shared with me and currently sharing with
    # This would be replaced with actual database queries in the full implementation
    shared_with_me = [
        {'name': 'Jane Doe', 'email': 'jane@example.com', 'carbon_footprint': '120 CO2eq'},
        {'name': 'John Smith', 'email': 'john@example.com', 'carbon_footprint': '95 CO2eq'},
    ]
    
    sharing_with = [
        {'name': 'Mike Johnson', 'email': 'mike@example.com', 'shared_date': 'April 22, 2025'},
        {'name': 'Sarah Williams', 'email': 'sarah@example.com', 'shared_date': 'April 20, 2025'},
    ]
    
    return render_template('share.html', 
                          active_page='share', 
                          nav_items=nav_items,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          email=user.email,
                          form=form,
                          search_results=search_results,
                          shared_with_me=shared_with_me,
                          sharing_with=sharing_with)

@app.route('/facts')
def facts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('facts.html', 
                          active_page='facts', 
                          nav_items=nav_items,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          email=user.email)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    form = ChangePasswordForm()
    
    return render_template('profile.html', 
                          nav_items=nav_items,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          email=user.email,
                          form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Find user with matching email
        user = User.query.filter_by(email=email).first()
        
        # Verify password if user exists
        if user and user.check_password(password):
            # Store user ID in session
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
            
    return render_template('auth/login.html', active_page='login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    form = SignupForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists', 'error')
        else:
            # Create new user
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data
            )
            new_user.set_password(form.password.data)
            
            # Add to database
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('auth/signup.html', active_page='signup', form=form)

@app.route('/logout')
def logout():
    # Remove user_id from session
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))
    
    form = ChangePasswordForm()
    user = User.query.get(session['user_id'])
    
    if form.validate_on_submit():
        # Check if current password is correct
        if not user.check_password(form.current_password.data):
            flash("Current password is incorrect.", "error")
            return redirect(url_for('profile'))
        
        # Set new password and save to database
        user.set_password(form.new_password.data)
        db.session.commit()
        
        flash("Password updated successfully!", "success")
        return redirect(url_for('profile'))
    else:
        # Form validation failed
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "error")
        
        return redirect(url_for('profile'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    print("Deleting user account")
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('login'))