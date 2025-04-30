from app import app, db
from flask import redirect, render_template, request, url_for, flash, session, flash
import re
from app.constants import nav_items
from app.forms import LoginForm, SignupForm, ChangePasswordForm, ShareForm
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

@app.route('/add_data')
def add_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('add_data.html', 
                          active_page='add_data', 
                          nav_items=nav_items,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          email=user.email)

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
            # Redirect to the login page instead of rendering template directly
            return redirect(url_for('login'))
            
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
            return redirect(url_for('signup'))
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
            
    # If form validation failed, redirect with errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "error")
        return redirect(url_for('signup'))
        
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