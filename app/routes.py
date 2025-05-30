from app import db
from app.blueprints import main
from flask import redirect, render_template, request, url_for, flash, session, flash, jsonify
import re
from app.constants import nav_items
from app.forms import VehicleForm, PublicTransitSimpleForm, PublicTransitAdvancedForm
from app.forms import AirTravelSimpleForm, AirTravelAdvancedForm, HomeEnergyForm
from app.forms import FoodForm, ShoppingSimpleForm, ShoppingAdvancedForm, CarbonFootprintForm
from app.models import User, CarbonFootprint, Travel, Vehicle, Home, Food, Shopping, Emissions, Share, Message
from app.processing_layer import CarbonFootprintCalculator
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, SignupForm, ChangePasswordForm, ShareForm, ResetPasswordRequestForm, ResetPasswordForm, DeleteAccountForm, EditNameForm, EditEMailForm
from app.email_utils import send_confirmation_email, send_password_reset_email, send_email_update_confirmation
from app.controllers import (
    process_travel_data,
    process_vehicles_data,
    process_home_data,
    process_food_data,
    process_shopping_data,
    delete_user_and_data
)

@main.route('/')
@login_required
def dashboard():
    user_data = CarbonFootprint.query.filter_by(user_id=current_user.id).first()
    is_new_user = user_data is None  # User is new if no data exists
    locked = is_new_user  # Lock the page if the user is new

    if locked:
        return redirect(url_for('main.add_data', new_user='true'))

    return render_template('dashboard.html', 
                          active_page='dashboard', 
                          nav_items=nav_items,
                          first_name=current_user.first_name,
                          last_name=current_user.last_name,
                          email=current_user.email,
                          is_new_user=is_new_user,
                          locked=locked)

@main.route('/add_data', methods=['GET', 'POST'])
@login_required
def add_data():
    user = current_user
    
    # Check if user is new (has no data)
    user_data = CarbonFootprint.query.filter_by(user_id=current_user.id).first()
    is_new_user = user_data is None

    # Show message for new users only on GET requests
    if is_new_user and request.method == 'GET':
        flash("Please add your data to unlock the Dashboard and View Data features.", "info")

    # Instantiate all forms - do this only once
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
    
    # Process POST request
    if request.method == 'POST' and 'calculate_footprint' in request.form:
        try:
            # Get the active mode for travel and shopping sections
            travel_mode = request.form.get('travel_mode', 'simple')
            shopping_mode = request.form.get('shopping_mode', 'simple')

            # Validate forms based on which mode is active
            forms_to_validate = [home_energy, food]
            if travel_mode == 'simple':
                forms_to_validate.extend([public_transit_simple, air_travel_simple])
            else:
                forms_to_validate.extend([public_transit_advanced, air_travel_advanced])

            if shopping_mode == 'simple':
                forms_to_validate.append(shopping_simple)
            else:
                forms_to_validate.append(shopping_advanced)
                
            # Check if all forms are valid
            is_valid = all(form.validate() for form in forms_to_validate)

            if is_valid:
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
                return redirect(url_for('main.view_data'))
            else:
                # Show form validation errors
                for form in forms_to_validate:
                    for field, errors in form.errors.items():
                        for error in errors:
                            flash(f"{field}: {error}", "danger")
                flash("There were errors in your submission. Please correct them and try again.", "danger")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")

    # Render the template with forms (for both GET and failed POST)
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
        shopping_advanced=shopping_advanced,
        is_new_user=is_new_user
    )

@main.route('/view_data')
@login_required
def view_data():
    user_data = CarbonFootprint.query.filter_by(user_id=current_user.id).first()
    locked = user_data is None  # Lock the page if the user is new

    if locked:
        return redirect(url_for('main.add_data', new_user='true'))

    # Leader Board
    shared_with_me_raw = []

    # Current user's own data
    emission = Emissions.query.filter_by(user_id=current_user.id).order_by(Emissions.calculated_at.desc()).first()
    shared_with_me_raw.append({
        'name': f"{current_user.first_name} {current_user.last_name}",
        'email': current_user.email,
        'carbon_footprint_value': float(emission.total_emissions) if emission else float('inf'),
        'carbon_footprint': f"{emission.total_emissions:.2f} CO2eq" if emission else "N/A"
    })

    # Data shared by other users
    shared_entries = Share.query.filter_by(to_user_id=current_user.id).all()
    for entry in shared_entries:
        sender = User.query.get(entry.from_user_id)
        if sender:
            sender_emission = Emissions.query.filter_by(user_id=sender.id).order_by(Emissions.calculated_at.desc()).first()
            if sender_emission:
                shared_with_me_raw.append({
                    'name': f"{sender.first_name} {sender.last_name}",
                    'email': sender.email,
                    'carbon_footprint_value': float(sender_emission.total_emissions),
                    'carbon_footprint': f"{sender_emission.total_emissions:.2f} CO2eq"
                })

    # Sort and rank users
    shared_with_me_sorted = sorted(shared_with_me_raw, key=lambda x: x['carbon_footprint_value'])
    for i, user in enumerate(shared_with_me_sorted, start=1):
        user['rank'] = i

    return render_template('view_data.html',
                           active_page='view_data',
                           nav_items=nav_items,
                           first_name=current_user.first_name,
                           last_name=current_user.last_name,
                           email=current_user.email,
                           locked=locked,
                           shared_with_me=shared_with_me_sorted)

@main.route('/api/compare_emissions')
@login_required
def compare_emissions():
    target_email = request.args.get('email')
    other_user = User.query.filter_by(email=target_email).first()
    if not other_user:
        return jsonify({'error': 'User not found'}), 404

    your_emission = Emissions.query.filter_by(user_id=current_user.id).order_by(Emissions.calculated_at.desc()).first()
    other_emission = Emissions.query.filter_by(user_id=other_user.id).order_by(Emissions.calculated_at.desc()).first()

    if not your_emission or not other_emission:
        return jsonify({'error': 'Missing emission data'}), 400

    def get_grouped_data(emission):
        return [
            emission.car_emissions + emission.public_transit_emissions + emission.air_travel_emissions,  # Travel
            emission.meat_emissions + emission.dairy_emissions + emission.fruits_vegetables_emissions + emission.cereals_emissions + emission.snacks_emissions,  # Food
            emission.electricity_emissions + emission.natural_gas_emissions + emission.heating_fuels_emissions + emission.water_emissions + emission.construction_emissions,  # Home
            emission.furniture_emissions + emission.clothing_emissions + emission.other_goods_emissions + emission.services_emissions  # Shopping
        ]

    return jsonify({
        'your_emissions': get_grouped_data(your_emission),
        'other_emissions': get_grouped_data(other_emission),
        'other_name': f"{other_user.first_name} {other_user.last_name}"
    })

@main.route('/api/emissions', methods=['GET'])
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

@main.route('/api/dashboard_metrics', methods=['GET'])
@login_required
def get_dashboard_metrics():
    """
    Returns all dashboard metrics (percentages, saved, emitted, isBelow, etc.) for the current user.
    """
    emissions = Emissions.query.filter_by(user_id=current_user.id).order_by(Emissions.calculated_at.desc()).first()
    if not emissions:
        return jsonify({'error': 'No emissions data found'}), 404

    GOALS = {
        'total': 12.3,
        'travel': 2.9,
        'home': 3.5,
        'food': 3.1,
        'shopping': 2.8
    }
    AU_AVG = 15.01  # Australian average household emissions

    # Calculate category totals
    travel = (emissions.car_emissions or 0.0) + (emissions.public_transit_emissions or 0.0) + (emissions.air_travel_emissions or 0.0)
    home = (emissions.electricity_emissions or 0.0) + (emissions.natural_gas_emissions or 0.0) + (emissions.heating_fuels_emissions or 0.0) + (emissions.water_emissions or 0.0) + (emissions.construction_emissions or 0.0)
    food = (emissions.meat_emissions or 0.0) + (emissions.dairy_emissions or 0.0) + (emissions.fruits_vegetables_emissions or 0.0) + (emissions.cereals_emissions or 0.0) + (emissions.snacks_emissions or 0.0)
    shopping = (emissions.furniture_emissions or 0.0) + (emissions.clothing_emissions or 0.0) + (emissions.other_goods_emissions or 0.0) + (emissions.services_emissions or 0.0)
    total = emissions.total_emissions or 0.0

    def calc_metrics(actual, goal):
        percentage = (actual / goal) * 100 if goal else 0
        is_below = actual <= goal
        saved = max(AU_AVG - actual, 0)
        return {
            'percentage': round(percentage),
            'saved': round(saved, 2),
            'emitted': round(actual, 2),
            'isBelow': is_below
        }

    return jsonify({
        'total': calc_metrics(total, GOALS['total']),
        'travel': calc_metrics(travel, GOALS['travel']),
        'home': calc_metrics(home, GOALS['home']),
        'food': calc_metrics(food, GOALS['food']),
        'shopping': calc_metrics(shopping, GOALS['shopping']),
        'goals': GOALS,
        'au_average': AU_AVG
    })

@main.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    user_data = CarbonFootprint.query.filter_by(user_id=current_user.id).first()
    is_new_user = user_data is None

    form = ShareForm()
    search_results = None

    if form.validate_on_submit():
        search_email = form.search_email.data.strip()
        search_results = User.query.filter_by(email=search_email).first()
        if not search_results:
            flash('No user found with that email address.', 'warning')
        else:
            flash('User found!', 'success')

    if request.method == 'POST' and 'share_email' in request.form:
        target_email = request.form.get('share_email').strip()
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

        return redirect(url_for('main.share'))

    # Users current_user shared to
    sharing_records = Share.query.filter_by(from_user_id=current_user.id).all()
    sharing_with = []
    for share_record in sharing_records:
        target = db.session.get(User, share_record.to_user_id)

        # Check if message read or not
        has_unread = Message.query.filter_by(
            sender_id=target.email,
            receiver_id=current_user.email,
            is_read=False
        ).count() > 0

        sharing_with.append({
            'name': f"{target.first_name} {target.last_name}",
            'email': target.email,
            'shared_date': share_record.shared_date.strftime("%B %d, %Y"),
            'has_unread': has_unread
        })


    # Users who shared with current_user
    received_records = Share.query.filter_by(to_user_id=current_user.id).all()
    shared_with_me_raw = []
    for share in received_records:
        sender = db.session.get(User, share.from_user_id)
        emission = Emissions.query.filter_by(user_id=sender.id).order_by(Emissions.calculated_at.desc()).first()
        shared_with_me_raw.append({
            'name': f"{sender.first_name} {sender.last_name}",
            'email': sender.email,
            'carbon_footprint_value': float(emission.total_emissions) if emission else float('inf'),
            'carbon_footprint': f"{emission.total_emissions:.2f} CO2eq" if emission else "N/A"
        })

    # Add current user to the leaderboard
    emission = Emissions.query.filter_by(user_id=current_user.id).order_by(Emissions.calculated_at.desc()).first()
    shared_with_me_raw.append({
        'name': f"{current_user.first_name} {current_user.last_name}",
        'email': current_user.email,
        'carbon_footprint_value': float(emission.total_emissions) if emission else float('inf'),
        'carbon_footprint': f"{emission.total_emissions:.2f} CO2eq" if emission else "N/A"
    })

    shared_with_me_sorted = sorted(shared_with_me_raw, key=lambda x: x['carbon_footprint_value'])
    for i, user in enumerate(shared_with_me_sorted, start=1):
        user['rank'] = i

    # Viewing other user's data
    view_email = request.args.get('view_email')
    selected_name = selected_email = None
    travel_pct = food_pct = home_pct = shopping_pct = total_emission = 0

    if view_email:
        target_user = User.query.filter_by(email=view_email).first()
        if target_user:
            selected_name = f"{target_user.first_name} {target_user.last_name}"
            selected_email = target_user.email
            emission = Emissions.query.filter_by(user_id=target_user.id).order_by(Emissions.calculated_at.desc()).first()

            if emission and emission.total_emissions:
                total_emission = emission.total_emissions
                travel = (emission.car_emissions or 0) + (emission.air_travel_emissions or 0) + (emission.public_transit_emissions or 0)
                food = (emission.meat_emissions or 0) + (emission.dairy_emissions or 0) + (emission.fruits_vegetables_emissions or 0) + \
                       (emission.cereals_emissions or 0) + (emission.snacks_emissions or 0)
                home = (emission.electricity_emissions or 0) + (emission.natural_gas_emissions or 0) + (emission.heating_fuels_emissions or 0) + \
                       (emission.water_emissions or 0) + (emission.construction_emissions or 0)
                shopping = (emission.clothing_emissions or 0) + (emission.furniture_emissions or 0) + (emission.other_goods_emissions or 0) + \
                           (emission.services_emissions or 0)
                travel_pct = round((travel / total_emission) * 100) if total_emission else 0
                food_pct = round((food / total_emission) * 100) if total_emission else 0
                home_pct = round((home / total_emission) * 100) if total_emission else 0
                shopping_pct = round((shopping / total_emission) * 100) if total_emission else 0

    return render_template('share.html',
                           active_page='share',
                           nav_items=nav_items,
                           first_name=current_user.first_name,
                           last_name=current_user.last_name,
                           email=current_user.email,
                           form=form,
                           search_results=search_results,
                           shared_with_me=shared_with_me_sorted,
                           sharing_with=sharing_with,
                           selected_name=selected_name,
                           selected_email=selected_email,
                           travel_pct=travel_pct,
                           food_pct=food_pct,
                           home_pct=home_pct,
                           shopping_pct=shopping_pct,
                           total_emission=total_emission,
                           is_new_user=is_new_user)

@main.route('/api/emissions/<email>', methods=['GET'])
@login_required
def get_user_emissions(email):
    user = db.session.get(User, email) if isinstance(email, int) else User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    emissions = Emissions.query.filter_by(user_id=user.id).order_by(Emissions.calculated_at.desc()).first()
    if not emissions:
        return jsonify({'error': 'No emissions data'}), 404

    total = emissions.total_emissions or 0.0

    travel = (emissions.car_emissions or 0.0) + (emissions.public_transit_emissions or 0.0) + (emissions.air_travel_emissions or 0.0)
    food = (emissions.meat_emissions or 0.0) + (emissions.dairy_emissions or 0.0) + \
           (emissions.fruits_vegetables_emissions or 0.0) + (emissions.cereals_emissions or 0.0) + (emissions.snacks_emissions or 0.0)
    home = (emissions.electricity_emissions or 0.0) + (emissions.natural_gas_emissions or 0.0) + \
           (emissions.heating_fuels_emissions or 0.0) + (emissions.water_emissions or 0.0) + (emissions.construction_emissions or 0.0)
    shopping = (emissions.furniture_emissions or 0.0) + (emissions.clothing_emissions or 0.0) + \
               (emissions.other_goods_emissions or 0.0) + (emissions.services_emissions or 0.0)

    GOALS = {
        'total': 12.3,
        'travel': 2.9,
        'home': 3.5,
        'food': 3.1,
        'shopping': 2.8
    }

    # Calculate percentages based on goals rather than total emissions
    # This ensures consistency with how the dashboard displays percentages
    travel_pct = round((travel / GOALS['travel']) * 100) if travel else 0
    food_pct = round((food / GOALS['food']) * 100) if food else 0
    home_pct = round((home / GOALS['home']) * 100) if home else 0
    shopping_pct = round((shopping / GOALS['shopping']) * 100) if shopping else 0

    return jsonify({
        'name': f'{user.first_name} {user.last_name}',
        'email': user.email,
        'travel_pct': travel_pct,
        'food_pct': food_pct,
        'home_pct': home_pct,
        'shopping_pct': shopping_pct,
        'total_emissions': total
    })

@main.route('/api/emissions_summary')
@login_required
def get_emissions_summary():
    emissions = Emissions.query.filter_by(user_id=current_user.id).order_by(Emissions.calculated_at.desc()).first()
    if not emissions:
        return jsonify({'error': 'No emissions data found'}), 404

    # Calculate totals for each category
    car = emissions.car_emissions or 0
    air = emissions.air_travel_emissions or 0
    transit = emissions.public_transit_emissions or 0
    travel_total = car + air + transit

    electricity = emissions.electricity_emissions or 0
    natural_gas = emissions.natural_gas_emissions or 0
    heating_fuel = emissions.heating_fuels_emissions or 0
    water = emissions.water_emissions or 0
    construction = emissions.construction_emissions or 0
    home_total = electricity + natural_gas + heating_fuel + water + construction

    meat = emissions.meat_emissions or 0
    dairy = emissions.dairy_emissions or 0
    fruit_veg = emissions.fruits_vegetables_emissions or 0
    cereals = emissions.cereals_emissions or 0
    snacks = emissions.snacks_emissions or 0
    food_total = meat + dairy + fruit_veg + cereals + snacks

    furniture = emissions.furniture_emissions or 0
    clothing = emissions.clothing_emissions or 0
    other_goods = emissions.other_goods_emissions or 0
    services = emissions.services_emissions or 0
    shopping_total = furniture + clothing + other_goods + services

    def safe_pct(value, total):
        return round((value / total) * 100, 2) if total else 0

    return jsonify({
        'travelTotal': travel_total,
        'homeTotal': home_total,
        'foodTotal': food_total,
        'shoppingTotal': shopping_total,

        'travel': {
            'carPct': safe_pct(car, travel_total),
            'airPct': safe_pct(air, travel_total),
            'transitPct': safe_pct(transit, travel_total),
        },
        'home': {
            'electricityPct': safe_pct(electricity, home_total),
            'naturalGasPct': safe_pct(natural_gas, home_total),
            'heatingFuelPct': safe_pct(heating_fuel, home_total),
            'waterPct': safe_pct(water, home_total),
            'constructionPct': safe_pct(construction, home_total),
        },
        'food': {
            'meatPct': safe_pct(meat, food_total),
            'dairyPct': safe_pct(dairy, food_total),
            'fruitVegPct': safe_pct(fruit_veg, food_total),
            'cerealsPct': safe_pct(cereals, food_total),
            'snacksPct': safe_pct(snacks, food_total),
        },
        'shopping': {
            'furniturePct': safe_pct(furniture, shopping_total),
            'clothingPct': safe_pct(clothing, shopping_total),
            'otherGoodsPct': safe_pct(other_goods, shopping_total),
            'servicesPct': safe_pct(services, shopping_total),
        }
    })

@main.route('/api/share', methods=['POST'])
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

@main.route('/stop_share', methods=['POST'])
@login_required
def stop_share():
    receiver_email = request.form['receiver_email']
    receiver = User.query.filter_by(email=receiver_email).first()

    if not receiver:
        flash('User not found.', 'warning')
        return redirect(url_for('main.share'))

    share = Share.query.filter_by(from_user_id=current_user.id, to_user_id=receiver.id).first()
    if share:
        db.session.delete(share)
        db.session.commit()
        flash('Stopped sharing successfully.', 'success')
    else:
        flash('Sharing record not found.', 'warning')

    return redirect(url_for('main.share'))

@main.route('/chat', methods=['POST'])
def chat():
    print("Received POST /chat request")
    print("Headers:", dict(request.headers))
    print("Raw body:", request.data)

    try:
        data = request.get_json(force=True)
        print("Parsed JSON:", data)
    except Exception as e:
        print("Failed to parse JSON:", str(e))
        return jsonify(success=False, error="Failed to parse JSON"), 400

    # Extract recipient email and message content
    to_email = data.get('to')
    content = data.get('message')
    print("To:", to_email)
    print("Message:", content)

    # Validate the presence of required fields
    if not to_email or not content:
        print("Incomplete data")
        return jsonify(success=False, error="Missing data"), 400

    # Save the new message to the database
    new_msg = Message(
        sender_id=current_user.email,
        receiver_id=to_email,
        content=content
    )
    db.session.add(new_msg)
    db.session.commit()

    print("Message saved successfully!")
    return jsonify(success=True)

@main.route('/chat/<email>', methods=['GET'])
@login_required
def chat_history(email):

    # Load message history
    messages = Message.query.filter(
        ((Message.sender_id == current_user.email) & (Message.receiver_id == email)) |
        ((Message.sender_id == email) & (Message.receiver_id == current_user.email))
    ).order_by(Message.timestamp).all()

    # mark messages sent by the other
    unread_msgs = Message.query.filter_by(sender_id=email, receiver_id=current_user.email, is_read=False).all()
    for msg in unread_msgs:
        msg.is_read = True
    db.session.commit()

    return jsonify([
        {
            'sender': msg.sender_id,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M')
        } for msg in messages
    ])

@main.route('/facts')
@login_required
def facts():
    # Check if user is new (has no data)
    user_data = CarbonFootprint.query.filter_by(user_id=current_user.id).first()
    is_new_user = user_data is None
    
    return render_template('facts.html', 
                          active_page='facts', 
                          nav_items=nav_items,
                          first_name=current_user.first_name,
                          last_name=current_user.last_name,
                          email=current_user.email,
                          is_new_user=is_new_user)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Check if user is new (has no data)
    user_data = CarbonFootprint.query.filter_by(user_id=current_user.id).first()
    is_new_user = user_data is None
    
    form = ChangePasswordForm()
    delete_form = DeleteAccountForm()
    name_form = EditNameForm()
    email_form = EditEMailForm()

    email_form.original_email.data = current_user.email

    if email_form.submit_email.data and email_form.validate_on_submit():
        submitted_original_email = request.form.get('original_email')
        if email_form.email.data != current_user.email:
            current_user.unconfirmed_email = email_form.email.data #stores email temporarily 
            # current_user.confirmed = False
            db.session.commit()
            send_email_update_confirmation(current_user, email_form.email.data)
            flash('Email updated. Please confirm your new email address.', 'info')
        else:
            flash("Please enter a valid Email address", "error")
        return redirect(url_for('main.profile'))
    
    if email_form.submit_email.data and not email_form.validate():
        for field, errors in email_form.errors.items():
            for error in errors:
                flash(f"{email_form[field].label.text}: {error}", "error")
        return redirect(url_for('main.profile'))
    
    if name_form.submit_name.data and name_form.validate_on_submit():
        current_user.first_name = name_form.first_name.data
        current_user.last_name = name_form.last_name.data
        db.session.commit()
        flash('Name updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html', 
                          nav_items=nav_items,
                          first_name=current_user.first_name,
                          last_name=current_user.last_name,
                          email=current_user.email,
                          form=form,
                          delete_form=delete_form,
                          name_form = name_form,
                          email_form = email_form,
                          is_new_user=is_new_user)

@main.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
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
                return redirect(url_for('main.inactive', email=user.email))
            
            # Login user with Flask-Login
            login_user(user, remember=form.remember_me.data if hasattr(form, 'remember_me') else False)
            
            # Redirect to next page if specified, otherwise dashboard
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
                
            flash('Logged in successfully!', 'success')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'error')
            # Redirect to the login page instead of rendering template directly
            return redirect(url_for('main.login'))
            
    return render_template('auth/login.html', active_page='login', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = SignupForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists', 'error')
            return redirect(url_for('main.signup'))
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
            return redirect(url_for('main.inactive', email=new_user.email))
            
    # If form validation failed, redirect with errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "error")
        return redirect(url_for('main.signup'))
        
    return render_template('auth/signup.html', active_page='signup', form=form)

@main.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.login'))

@main.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Check if current password is correct
        if not current_user.check_password(form.current_password.data):
            flash("Current password is incorrect.", "error")
            return redirect(url_for('main.profile'))
        
        # Set new password and save to database
        current_user.set_password(form.new_password.data)
        db.session.commit()
        
        flash("Password updated successfully!", "success")
        return redirect(url_for('main.profile'))
    else:
        # Form validation failed
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "error")
        
        return redirect(url_for('main.profile'))

@main.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = current_user._get_current_object()
        logout_user()
        delete_user_and_data(user)
        flash('Your account and all related data has been deleted.', 'success')
    return redirect(url_for('main.login'))

# New routes for email verification
@main.route('/inactive')
def inactive():
    email = request.args.get('email', '')
    return render_template('auth/inactive.html', email=email)

@main.route('/resend_confirmation', methods=['POST'])
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
    
    return redirect(url_for('main.inactive', email=email))

@main.route('/confirm_email/<token>')
def confirm_email(token):
    user = User.verify_email_token(token)
    if not user:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('main.login'))
    if user.confirmed:
        flash('Account already confirmed. Please log in.', 'info')
        return redirect(url_for('main.login'))
    user.confirmed = True
    db.session.commit()
    flash('Account confirmed! Please log in.', 'success')
    return redirect(url_for('main.login'))

@main.route('/confirm_new_email/<token>')
def confirm_new_email(token):
    data = User.verify_email_update_token(token)
    if not data:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('main.profile'))
    user = db.session.get(User, data.get('user_id'))
    new_email = data.get('new_email')
    if not user or not new_email:
        flash('Invalid confirmation data.', 'error')
        return redirect(url_for('main.profile'))
    # Check if the new email is already taken
    if User.query.filter_by(email=new_email).first():
        flash('This email is already in use.', 'error')
        return redirect(url_for('main.profile'))
    user.email = new_email
    user.unconfirmed_email = None
    db.session.commit()
    flash('Your email address has been updated and confirmed!', 'success')
    return redirect(url_for('main.profile'))

# Password reset functionality
@main.route('/confirm_email', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        # Always show the same message whether the email exists or not
        flash('If the email exists, a password reset link has been sent.', 'info')
        return redirect(url_for('main.login'))
    
    return render_template('auth/confirm_email.html', form=form)

@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        flash('The reset link is invalid or has expired.', 'error')
        return redirect(url_for('main.login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been reset. Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('auth/change_password.html', form=form)
