from app import app
from flask import redirect, render_template, request, url_for, flash, session
from app.constants import nav_items
from app.forms import LoginForm, SignupForm

# Temporary users array to simulate database storage
# This will be cleared when server restarts
users = [
    {
        'id': 1,
        'first_name': 'Demo',
        'last_name': 'User',
        'email': 'demo@example.com',
        'password': 'password123'  # In a real app, this would be hashed
    }
]

# Temporary current user variable
current_user = None

@app.route('/')
def dashboard():
    return render_template('dashboard.html', 
                          active_page='dashboard', 
                          nav_items=nav_items,
                          first_name=current_user['first_name'] if current_user else '',
                          last_name=current_user['last_name'] if current_user else '',
                          email=current_user['email'] if current_user else '')

@app.route('/add_data')
def add_data():
    return render_template('add_data.html', 
                          active_page='add_data', 
                          nav_items=nav_items,
                          first_name=current_user['first_name'] if current_user else '',
                          last_name=current_user['last_name'] if current_user else '',
                          email=current_user['email'] if current_user else '')

@app.route('/view_data')
def view_data():
    return render_template('view_data.html', 
                          active_page='view_data', 
                          nav_items=nav_items,
                          first_name=current_user['first_name'] if current_user else '',
                          last_name=current_user['last_name'] if current_user else '',
                          email=current_user['email'] if current_user else '')

@app.route('/share')
def share():
    return render_template('share.html', 
                          active_page='share', 
                          nav_items=nav_items,
                          first_name=current_user['first_name'] if current_user else '',
                          last_name=current_user['last_name'] if current_user else '',
                          email=current_user['email'] if current_user else '')

@app.route('/facts')
def facts():
    return render_template('facts.html', 
                          active_page='facts', 
                          nav_items=nav_items,
                          first_name=current_user['first_name'] if current_user else '',
                          last_name=current_user['last_name'] if current_user else '',
                          email=current_user['email'] if current_user else '')

@app.route('/profile')
def profile():
    return render_template('profile.html', 
                          nav_items=nav_items,
                          first_name=current_user['first_name'] if current_user else '',
                          last_name=current_user['last_name'] if current_user else '',
                          email=current_user['email'] if current_user else '')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Find user with matching email and password
        found_user = next((user for user in users if user['email'] == email and user['password'] == password), None)
        
        if found_user:
            # Set current user
            current_user = found_user
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
            
    return render_template('auth/login.html', active_page='login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Check if email already exists
        if any(user['email'] == form.email.data for user in users):
            flash('Email already exists', 'error')
        else:
            # Create new user
            new_user = {
                'id': len(users) + 1,
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'email': form.email.data,
                'password': form.password.data  # In a real app, this would be hashed
            }
            users.append(new_user)
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('auth/signup.html', active_page='signup', form=form)

@app.route('/logout')
def logout():
    global current_user
    current_user = None
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))