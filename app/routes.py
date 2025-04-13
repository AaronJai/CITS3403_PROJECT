from app import app
from flask import redirect, render_template, request, url_for


@app.route('/')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/add_data')
def add_data():
    return render_template('add_data.html', active_page='add_data')

@app.route('/view_data')
def view_data():
    return render_template('view_data.html', active_page='view_data')

@app.route('/share')
def share():
    return render_template('share.html', active_page='share')

@app.route('/facts')
def facts():
    return render_template('facts.html', active_page='facts')

@app.route('/profile')
def profile():
    return render_template('profile.html')