from app import app, db
from flask import redirect, render_template, request, url_for, flash, session, flash, jsonify
import re
from app.constants import nav_items
from app.forms import LoginForm, SignupForm, ChangePasswordForm, ShareForm
from app.forms import VehicleForm, PublicTransitSimpleForm, PublicTransitAdvancedForm
from app.forms import AirTravelSimpleForm, AirTravelAdvancedForm, HomeEnergyForm
from app.forms import FoodForm, ShoppingSimpleForm, ShoppingAdvancedForm, CarbonFootprintForm
from app.models import User

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
    
    # Create primary form with CSRF token
    form = CarbonFootprintForm()
    
    # Create form instances
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
            # Process vehicle data
            # Here you would extract the vehicle data from the form
            
            # Process travel data based on active mode
            if travel_mode == 'simple':
                # Validate and process simple travel form
                if public_transit_simple.validate() and air_travel_simple.validate():
                    public_transit_distance = public_transit_simple.distance.data
                    air_travel_distance = air_travel_simple.distance.data
                    # Process simple travel data
            else:
                # Validate and process advanced travel form
                if public_transit_advanced.validate() and air_travel_advanced.validate():
                    bus_kms = public_transit_advanced.bus_kms.data
                    transit_rail_kms = public_transit_advanced.transit_rail_kms.data
                    commuter_rail_kms = public_transit_advanced.commuter_rail_kms.data
                    intercity_rail_kms = public_transit_advanced.intercity_rail_kms.data
                    
                    short_flights = air_travel_advanced.short_flights.data
                    medium_flights = air_travel_advanced.medium_flights.data
                    long_flights = air_travel_advanced.long_flights.data
                    extended_flights = air_travel_advanced.extended_flights.data
                    # Process advanced travel data
            
            # Home energy data is always required and has only one form
            if home_energy.validate():
                # Process home energy data
                pass
            
            # Food data is always required and has only one form
            if food.validate():
                # Process food data
                pass
            
            # Process shopping data based on active mode
            if shopping_mode == 'simple':
                # Validate and process simple shopping form
                if shopping_simple.validate():
                    goods_multiplier = shopping_simple.goods_multiplier.data
                    services_multiplier = shopping_simple.services_multiplier.data
                    # Process simple shopping data
            else:
                # Validate and process advanced shopping form
                if shopping_advanced.validate():
                    # Goods
                    furniture_appliances = shopping_advanced.furniture_appliances.data
                    clothing = shopping_advanced.clothing.data
                    entertainment = shopping_advanced.entertainment.data
                    office_supplies = shopping_advanced.office_supplies.data
                    personal_care = shopping_advanced.personal_care.data
                    
                    # Services
                    services_food = shopping_advanced.services_food.data
                    education = shopping_advanced.education.data
                    communication = shopping_advanced.communication.data
                    loan = shopping_advanced.loan.data
                    transport = shopping_advanced.transport.data
                    # Process advanced shopping data
            
            # Here you would save the form data to the database
            # And calculate the carbon footprint based on the collected data
            
            flash('Your carbon footprint has been calculated and saved!', 'success')
            return redirect(url_for('view_data'))
            
    return render_template('add_data.html', 
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
                          shopping_advanced=shopping_advanced)

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