from app import app, db
from flask import redirect, render_template, request, url_for, flash, session, flash, jsonify
import re
from app.constants import nav_items
from app.forms import VehicleForm, PublicTransitSimpleForm, PublicTransitAdvancedForm
from app.forms import AirTravelSimpleForm, AirTravelAdvancedForm, HomeEnergyForm
from app.forms import FoodForm, ShoppingSimpleForm, ShoppingAdvancedForm, CarbonFootprintForm
from app.models import User, CarbonFootprint, Travel, Vehicle, Home, Food, Shopping, Emissions, Share
from app.processing_layer import CarbonFootprintCalculator
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, SignupForm, ChangePasswordForm, ShareForm, ResetPasswordRequestForm, ResetPasswordForm, DeleteAccountForm
from app.email_utils import send_confirmation_email, send_password_reset_email

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', 
                          active_page='dashboard', 
                          nav_items=nav_items,
                          first_name=current_user.first_name,
                          last_name=current_user.last_name,
                          email=current_user.email)

@app.route('/add_data', methods=['GET', 'POST'])
@login_required
def add_data():
    user = current_user

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
@login_required
def view_data():
    return render_template('view_data.html', 
                          active_page='view_data', 
                          nav_items=nav_items,
                          first_name=current_user.first_name,
                          last_name=current_user.last_name,
                          email=current_user.email)


@app.route('/api/emissions', methods=['GET'])
@login_required
def get_emissions():
    """
    Fetch the latest Emissions record for the logged-in user.
    Returns JSON with emission fields.
    """
    emissions = Emissions.query.filter_by(user_id=current_user.id).order_by(Emissions.calculated_at.desc()).first()
    if not emissions:
        return jsonify({'error': 'No emissions data found'}), 404

    return jsonify({
        'car_emissions': emissions.car_emissions or 0.0,
        'public_transit_emissions': emissions.public_transit_emissions or 0.0,
        'air_travel_emissions': emissions.air_travel_emissions or 0.0,
        'electricity_emissions': emissions.electricity_emissions or 0.0,
        'natural_gas_emissions': emissions.natural_gas_emissions or 0.0,
        'heating_fuels_emissions': emissions.heating_fuels_emissions or 0.0,
        'water_emissions': emissions.water_emissions or 0.0,
        'construction_emissions': emissions.construction_emissions or 0.0,
        'meat_emissions': emissions.meat_emissions or 0.0,
        'dairy_emissions': emissions.dairy_emissions or 0.0,
        'fruits_vegetables_emissions': emissions.fruits_vegetables_emissions or 0.0,
        'cereals_emissions': emissions.cereals_emissions or 0.0,
        'snacks_emissions': emissions.snacks_emissions or 0.0,
        'furniture_emissions': emissions.furniture_emissions or 0.0,
        'clothing_emissions': emissions.clothing_emissions or 0.0,
        'other_goods_emissions': emissions.other_goods_emissions or 0.0,
        'services_emissions': emissions.services_emissions or 0.0,
        'total_emissions': emissions.total_emissions or 0.0
    })



@app.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    form = ShareForm()
    search_results = None
    
    if form.validate_on_submit():
        search_email = form.search_email.data
        search_results = User.query.filter_by(email=search_email).first()
        if not search_results:
            flash('No user found with that email address.', 'warning')
        else:
            flash('User found!', 'success')
    
    if request.method == 'POST' and 'share_email' in request.form:
        target_email = request.form.get('share_email')
        to_user = User.query.filter_by(email=target_email).first()

        if not to_user:
            flash('User not found', 'warning')
        elif current_user.id == to_user.id:
            flash('Cannot share with yourself.', 'error')
        else:
            existing = Share.query.filter_by(from_user_id=current_user.id, to_user_id=to_user.id).first()
            if existing:
                flash('You have already shared with this user.', 'warning')
            else:
                new_share = Share(from_user_id=current_user.id, to_user_id=to_user.id)
                db.session.add(new_share)
                db.session.commit()
                flash('Shared successfully!', 'success')

        return redirect(url_for('share'))

    sharing_records = Share.query.filter_by(from_user_id=current_user.id).all()
    sharing_with = []
    for share in sharing_records:
        target = User.query.get(share.to_user_id)
        sharing_with.append({
            'name': f"{target.first_name} {target.last_name}",
            'email': target.email,
            'shared_date': share.shared_date.strftime("%B %d, %Y")
        })
    received_records = Share.query.filter_by(to_user_id=current_user.id).all()
    shared_with_me = []
    for share in received_records:
        sender = User.query.get(share.from_user_id)
        footprint = CarbonFootprint.query.filter_by(user_id=sender.id).first()
        if footprint:
            emission = Emissions.query.filter_by(carbon_footprint_id=footprint.id).first()
        else:
            emission = None
        shared_with_me.append({
        'name': f"{sender.first_name} {sender.last_name}",
        'email': sender.email,
        'carbon_footprint': f"{emission.total_emissions:.2f} CO2eq" if emission is not None else "N/A"
    })
    view_email = request.args.get('view_email')
    if view_email:
        target_user = User.query.filter_by(email=view_email).first()
        selected_footprint = CarbonFootprint.query.filter_by(user_id=target_user.id).first()
        selected_name = f"{target_user.first_name} {target_user.last_name}"
        selected_email = target_user.email
    else:
        selected_footprint = CarbonFootprint.query.filter_by(user_id=current_user.id).first()
        selected_name = f"{current_user.first_name} {current_user.last_name}"
        selected_email = current_user.email 

    emission = Emissions.query.filter_by(carbon_footprint_id=selected_footprint.id).first() if selected_footprint else None
    if emission:
        travel = (
            (emission.car_emissions or 0) +
            (emission.air_travel_emissions or 0) +
            (emission.public_transit_emissions or 0)
        )
        food = (
            (emission.meat_emissions or 0) +
            (emission.dairy_emissions or 0) +
            (emission.fruits_vegetables_emissions or 0) +
            (emission.cereals_emissions or 0) +
            (emission.snacks_emissions or 0)
        )
        home = (
            (emission.electricity_emissions or 0) +
            (emission.natural_gas_emissions or 0) +
            (emission.heating_fuels_emissions or 0) +
            (emission.water_emissions or 0)
        )
        shopping = (
            (emission.clothing_emissions or 0) +
            (emission.furniture_emissions or 0) +
            (emission.other_goods_emissions or 0) +
            (emission.services_emissions or 0)
        )

        total = travel + food + home + shopping
        total_emission = round(total, 2)
        travel_pct = round((travel / total) * 100) if total else 0
        food_pct = round((food / total) * 100) if total else 0
        home_pct = round((home / total) * 100) if total else 0
        shopping_pct = round((shopping / total) * 100) if total else 0
    else:
        travel_pct = food_pct = home_pct = shopping_pct = 0
        total_emission = 0 

    return render_template('share.html', 
                          active_page='share', 
                          nav_items=nav_items,
                          first_name=current_user.first_name,
                          last_name=current_user.last_name,
                          email=current_user.email,
                          form=form,
                          search_results=search_results,
                          shared_with_me=shared_with_me,
                          sharing_with=sharing_with,
                          selected_footprint=selected_footprint,
                          selected_name=selected_name,  
                          selected_email = selected_email,
                          travel_pct=travel_pct,
                          food_pct=food_pct,
                          home_pct=home_pct,
                          shopping_pct=shopping_pct,
                          total_emission=total_emission)

@app.route('/api/share', methods=['POST'])
@login_required
def api_share():
    data = request.get_json()
    target_email = data.get('email')

    to_user = User.query.filter_by(email=target_email).first()

    if not to_user:
        return jsonify({'error': 'User not found'}), 404

    # Cannot share with yourself
    if current_user.id == to_user.id:
        return jsonify({'error': 'Cannot share with yourself'}), 400

    # Check if already shared
    existing = Share.query.filter_by(from_user_id=current_user.id, to_user_id=to_user.id).first()
    if existing:
        return jsonify({'error': 'Already shared with this user'}), 400

    # Create new share record
    new_share = Share(from_user_id=current_user.id, to_user_id=to_user.id)
    db.session.add(new_share)
    db.session.commit()
    
    return jsonify({'success': True}), 200

@app.route('/stop_share', methods=['POST'])
@login_required
def stop_share():
    receiver_email = request.form['receiver_email']
    receiver = User.query.filter_by(email=receiver_email).first()

    if not receiver:
        flash('User not found.', 'warning')
        return redirect(url_for('share'))

    share = Share.query.filter_by(from_user_id=current_user.id, to_user_id=receiver.id).first()
    if share:
        db.session.delete(share)
        db.session.commit()
        flash('Stopped sharing successfully.', 'success')
    else:
        flash('Sharing record not found.', 'warning')

    return redirect(url_for('share'))

@app.route('/facts')
@login_required
def facts():
    return render_template('facts.html', 
                          active_page='facts', 
                          nav_items=nav_items,
                          first_name=current_user.first_name,
                          last_name=current_user.last_name,
                          email=current_user.email)

@app.route('/profile')
@login_required
def profile():
    form = ChangePasswordForm()
    delete_form = DeleteAccountForm()
    
    return render_template('profile.html', 
                          nav_items=nav_items,
                          first_name=current_user.first_name,
                          last_name=current_user.last_name,
                          email=current_user.email,
                          form=form,
                          delete_form=delete_form,)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Find user with matching email
        user = User.query.filter_by(email=email).first()
        
        # Verify password if user exists
        if user and user.check_password(password):
            # Check if user has confirmed their email
            if not user.confirmed:
                flash('Please confirm your email address before logging in.', 'warning')
                return redirect(url_for('inactive', email=user.email))
            
            # Login user with Flask-Login
            login_user(user, remember=form.remember_me.data if hasattr(form, 'remember_me') else False)
            
            # Redirect to next page if specified, otherwise dashboard
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard')
                
            flash('Logged in successfully!', 'success')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'error')
            # Redirect to the login page instead of rendering template directly
            return redirect(url_for('login'))
            
    return render_template('auth/login.html', active_page='login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = SignupForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists', 'error')
            return redirect(url_for('signup'))
        else:
            # Create new user
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                confirmed=False
            )
            new_user.set_password(form.password.data)
            
            # Add to database
            db.session.add(new_user)
            db.session.commit()
            
            # Send confirmation email
            send_confirmation_email(new_user)
            
            flash('Thanks for registering! Please check your email to confirm your account.', 'success')
            return redirect(url_for('inactive', email=new_user.email))
            
    # If form validation failed, redirect with errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "error")
        return redirect(url_for('signup'))
        
    return render_template('auth/signup.html', active_page='signup', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Check if current password is correct
        if not current_user.check_password(form.current_password.data):
            flash("Current password is incorrect.", "error")
            return redirect(url_for('profile'))
        
        # Set new password and save to database
        current_user.set_password(form.new_password.data)
        db.session.commit()
        
        flash("Password updated successfully!", "success")
        return redirect(url_for('profile'))
    else:
        # Form validation failed
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "error")
        
        return redirect(url_for('profile'))

#helper function to delete any related data to user 
def delete_user_and_data(user):
    # Delete emissions and footprint-related models
    footprints = CarbonFootprint.query.filter_by(user_id=user.id).all()
    for fp in footprints:
        # Delete emissions first
        Emissions.query.filter_by(carbon_footprint_id=fp.id).delete()

        # Delete linked travel and vehicles
        if fp.travel_id:
            Vehicle.query.filter_by(travel_id=fp.travel_id).delete()
            Travel.query.filter_by(id=fp.travel_id).delete()

        # Delete other linked models
        if fp.home_id:
            Home.query.filter_by(id=fp.home_id).delete()
        if fp.food_id:
            Food.query.filter_by(id=fp.food_id).delete()
        if fp.shopping_id:
            Shopping.query.filter_by(id=fp.shopping_id).delete()

    # Delete the footprints
    CarbonFootprint.query.filter_by(user_id=user.id).delete()

    # Delete share records (both sent and received)
    Share.query.filter(
        (Share.from_user_id == user.id) |
        (Share.to_user_id == user.id)
    ).delete()

    # Finally, delete the user
    db.session.delete(user)
    db.session.commit()

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = current_user._get_current_object()
        logout_user()
        delete_user_and_data(user)
        flash('Your account and all related data has been deleted.', 'success')
    return redirect(url_for('login'))

# New routes for email verification
@app.route('/inactive')
def inactive():
    email = request.args.get('email', '')
    return render_template('auth/inactive.html', email=email)

@app.route('/resend_confirmation', methods=['POST'])
def resend_confirmation():
    email = request.form.get('email')
    if not email:
        email = request.args.get('email')
    
    if email:
        user = User.query.filter_by(email=email).first()
        if user and not user.confirmed:
            send_confirmation_email(user)
            flash('A new confirmation email has been sent.', 'success')
        else:
            flash('Email could not be sent.', 'error')
    
    return redirect(url_for('inactive', email=email))

@app.route('/confirm_email/<token>')
def confirm_email(token):
    user = User.verify_email_token(token)
    if not user:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('login'))
    
    user.confirmed = True
    db.session.commit()
    flash('Account confirmed! Please log in.', 'success')
    return redirect(url_for('login'))

# Password reset functionality
@app.route('/confirm_email', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        # Always show the same message whether the email exists or not
        flash('If the email exists, a password reset link has been sent.', 'info')
        return redirect(url_for('login'))
    
    return render_template('auth/confirm_email.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        flash('The reset link is invalid or has expired.', 'error')
        return redirect(url_for('login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been reset. Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/change_password.html', form=form)