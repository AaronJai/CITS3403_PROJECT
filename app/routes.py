from app import app, db
from flask import redirect, render_template, request, url_for, flash, session
import re
from app.constants import nav_items
from app.forms import LoginForm, SignupForm, ChangePasswordForm, ShareForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.email_utils import send_confirmation_email, send_password_reset_email

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
            # Check if user has confirmed their email
            if not user.confirmed:
                flash('Please confirm your email address before logging in.', 'warning')
                return redirect(url_for('inactive', email=user.email))
            
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
    if 'user_id' in session:
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
    if 'user_id' in session:
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