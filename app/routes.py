from app import app, db
from flask import redirect, render_template, request, url_for, flash, session
from app.constants import nav_items
from app.forms import LoginForm, SignupForm
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

@app.route('/share')
def share():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('share.html', 
                          active_page='share', 
                          nav_items=nav_items,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          email=user.email)

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

@app.route('/profile/')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('profile.html', 
                          nav_items=nav_items,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          email=user.email)

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