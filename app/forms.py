from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SearchField
from wtforms import IntegerField, FloatField, SelectField, RadioField, BooleanField, FormField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange, Optional
import re

def password_check(form, field):
    """Custom validator to check password complexity"""
    password = field.data
    
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter")
    
    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one number")
    
    if not re.search(r"[@$!%*?&]", password):
        raise ValidationError("Password must contain at least one special character (@$!%*?&)")

class LoginForm(FlaskForm):
    """Form for user login"""
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    """Form for user registration"""
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long"),
        password_check
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Sign Up')

class ShareForm(FlaskForm):
    """Form for searching users by email"""
    search_email = EmailField('Search by email', validators=[
        Email(message="Please enter a valid email address")
    ])
    submit = SubmitField('Search')

class ChangePasswordForm(FlaskForm):
    """Form for changing user password"""
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message="Please enter your current password")
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long"),
        password_check
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message="Passwords must match")
    ])
    submit = SubmitField('Save')

# Carbon Footprint Forms

class VehicleForm(FlaskForm):
    """Form for vehicle data entry"""
    fuel_type = SelectField('Fuel Type', choices=[
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric')
    ])
    distance = FloatField('Distance', validators=[NumberRange(min=0)], default=15600)
    fuel_efficiency = FloatField('Fuel Efficiency', validators=[NumberRange(min=10, max=115)], default=22)

class PublicTransitSimpleForm(FlaskForm):
    """Simple form for public transit"""
    distance = FloatField('Distance', validators=[NumberRange(min=0)], default=368)

class PublicTransitAdvancedForm(FlaskForm):
    """Advanced form for public transit"""
    bus_miles = FloatField('Bus', validators=[NumberRange(min=0)], default=130)
    transit_rail_miles = FloatField('Transit Rail', validators=[NumberRange(min=0)], default=97)
    commuter_rail_miles = FloatField('Commuter Rail', validators=[NumberRange(min=0)], default=65)
    intercity_rail_miles = FloatField('Inter-city Rail', validators=[NumberRange(min=0)], default=32)

class AirTravelSimpleForm(FlaskForm):
    """Simple form for air travel"""
    distance = FloatField('Distance', validators=[NumberRange(min=0)], default=3300)

class AirTravelAdvancedForm(FlaskForm):
    """Advanced form for air travel"""
    short_flights = IntegerField('Short Flights (<400 kms)', validators=[NumberRange(min=0)], default=3)
    medium_flights = IntegerField('Medium Flights (400-1500 kms)', validators=[NumberRange(min=0)], default=2)
    long_flights = IntegerField('Long Flights (1500-3000 kms)', validators=[NumberRange(min=0)], default=0)
    extended_flights = IntegerField('Extended Flights (>3000 kms)', validators=[NumberRange(min=0)], default=0)

class HomeEnergyForm(FlaskForm):
    """Form for home energy usage"""
    electricity = FloatField('Electricity', validators=[NumberRange(min=0)], default=1350)
    electricity_unit = SelectField('Unit', choices=[('$', '$'), ('kWh', 'kWh')])
    electricity_frequency = SelectField('Frequency', choices=[('/yr', '/yr'), ('/mo', '/mo')])
    clean_energy_percentage = FloatField('Clean Energy %', validators=[NumberRange(min=0, max=100)], default=31)
    
    natural_gas = FloatField('Natural Gas', validators=[NumberRange(min=0)], default=590)
    natural_gas_unit = SelectField('Unit', choices=[('$', '$'), ('therms', 'therms'), ('m³', 'm³')])
    natural_gas_frequency = SelectField('Frequency', choices=[('/yr', '/yr'), ('/mo', '/mo')])
    
    heating_oil = FloatField('Heating Oil & Other Fuels', validators=[NumberRange(min=0)], default=260)
    heating_oil_unit = SelectField('Unit', choices=[('$', '$'), ('litres', 'litres')])
    heating_oil_frequency = SelectField('Frequency', choices=[('/yr', '/yr'), ('/mo', '/mo')])
    
    living_space = FloatField('Living Space Area', validators=[NumberRange(min=0)], default=1850)
    water_usage = FloatField('Water Usage', validators=[NumberRange(min=0, max=300)], default=100)

class FoodForm(FlaskForm):
    """Form for food consumption data"""
    meat_fish_eggs = FloatField('Meat, Fish, Eggs', validators=[NumberRange(min=0.01, max=3)], default=2.3)
    grains_baked_goods = FloatField('Grains & Baked Goods', validators=[NumberRange(min=0.01, max=3)], default=3.9)
    dairy = FloatField('Dairy', validators=[NumberRange(min=0.01, max=3)], default=2.1)
    fruits_vegetables = FloatField('Fruits and Vegetables', validators=[NumberRange(min=0.01, max=3)], default=3.4)
    snacks_drinks = FloatField('Snacks, Drinks, etc.', validators=[NumberRange(min=0.01, max=3)], default=3.2)

class ShoppingSimpleForm(FlaskForm):
    """Simple form for shopping data"""
    goods_multiplier = FloatField('Goods', validators=[NumberRange(min=0.0001, max=3)], default=1)
    services_multiplier = FloatField('Services', validators=[NumberRange(min=0.0001, max=3)], default=1)

class ShoppingAdvancedForm(FlaskForm):
    """Advanced form for shopping data"""
    # Goods
    furniture_appliances = FloatField('Furniture & Appliances', validators=[NumberRange(min=0)], default=362)
    clothing = FloatField('Clothing', validators=[NumberRange(min=0)], default=391)
    entertainment = FloatField('Entertainment', validators=[NumberRange(min=0)], default=54)
    office_supplies = FloatField('Office Supplies', validators=[NumberRange(min=0)], default=37)
    personal_care = FloatField('Personal Care', validators=[NumberRange(min=0)], default=56)
    
    # Services
    services_food = FloatField('Food', validators=[NumberRange(min=0)], default=196)
    education = FloatField('Education', validators=[NumberRange(min=0)], default=22)
    communication = FloatField('Communication', validators=[NumberRange(min=0)], default=46)
    loan = FloatField('Loan', validators=[NumberRange(min=0)], default=82)
    transport = FloatField('Transport', validators=[NumberRange(min=0)], default=113)

class CarbonFootprintForm(FlaskForm):
    """Main form that combines all sections"""
    # Hidden field for csrf token only
    calculate_footprint = HiddenField()
    
    # The individual form objects will be passed separately in the template
    # so we don't need to include them here
    submit = SubmitField('Calculate Footprint')