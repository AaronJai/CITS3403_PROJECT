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
    distance = FloatField('Distance', validators=[NumberRange(min=0), Optional()])
    fuel_efficiency = FloatField('Fuel Efficiency', validators=[NumberRange(min=0, max=35), Optional()])

class PublicTransitSimpleForm(FlaskForm):
    """Simple form for public transit"""
    distance = FloatField('Distance', validators=[NumberRange(min=0), Optional()])

class PublicTransitAdvancedForm(FlaskForm):
    """Advanced form for public transit"""
    bus_kms = FloatField('Bus', validators=[NumberRange(min=0), Optional()])
    transit_rail_kms = FloatField('Transit Rail', validators=[NumberRange(min=0), Optional()])
    commuter_rail_kms = FloatField('Commuter Rail', validators=[NumberRange(min=0), Optional()])
    intercity_rail_kms = FloatField('Inter-city Rail', validators=[NumberRange(min=0), Optional()])

class AirTravelSimpleForm(FlaskForm):
    """Simple form for air travel"""
    distance = FloatField('Distance', validators=[NumberRange(min=0), Optional()])

class AirTravelAdvancedForm(FlaskForm):
    """Advanced form for air travel"""
    short_flights = IntegerField('Short Flights (<400 kms)', validators=[NumberRange(min=0), Optional()])
    medium_flights = IntegerField('Medium Flights (400-1500 kms)', validators=[NumberRange(min=0), Optional()])
    long_flights = IntegerField('Long Flights (1500-3000 kms)', validators=[NumberRange(min=0), Optional()])
    extended_flights = IntegerField('Extended Flights (>3000 kms)', validators=[NumberRange(min=0), Optional()])

class HomeEnergyForm(FlaskForm):
    """Form for home energy usage"""
    electricity = FloatField('Electricity', validators=[NumberRange(min=0), Optional()])
    electricity_unit = SelectField('Unit', choices=[('$', '$'), ('kWh', 'kWh')])
    electricity_frequency = SelectField('Frequency', choices=[('/yr', '/yr'), ('/mo', '/mo')])
    clean_energy_percentage = FloatField('Clean Energy %', validators=[NumberRange(min=0, max=100)], default=31)
    
    natural_gas = FloatField('Natural Gas', validators=[NumberRange(min=0), Optional()])
    natural_gas_unit = SelectField('Unit', choices=[('$', '$'), ('therms', 'therms'), ('m³', 'm³')])
    natural_gas_frequency = SelectField('Frequency', choices=[('/yr', '/yr'), ('/mo', '/mo')])
    
    heating_oil = FloatField('Heating Oil & Other Fuels', validators=[NumberRange(min=0), Optional()])
    heating_oil_unit = SelectField('Unit', choices=[('$', '$'), ('litres', 'litres')])
    heating_oil_frequency = SelectField('Frequency', choices=[('/yr', '/yr'), ('/mo', '/mo')])
    
    living_space = FloatField('Living Space Area', validators=[NumberRange(min=0), Optional()])
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
    furniture_appliances = FloatField('Furniture & Appliances', validators=[NumberRange(min=0), Optional()])
    clothing = FloatField('Clothing', validators=[NumberRange(min=0), Optional()])
    entertainment = FloatField('Entertainment', validators=[NumberRange(min=0), Optional()])
    office_supplies = FloatField('Office Supplies', validators=[NumberRange(min=0), Optional()])
    personal_care = FloatField('Personal Care', validators=[NumberRange(min=0), Optional()])
    
    # Services
    services_food = FloatField('Food', validators=[NumberRange(min=0), Optional()])
    education = FloatField('Education', validators=[NumberRange(min=0), Optional()])
    communication = FloatField('Communication', validators=[NumberRange(min=0), Optional()])
    loan = FloatField('Loan', validators=[NumberRange(min=0), Optional()])
    transport = FloatField('Transport', validators=[NumberRange(min=0), Optional()])

# Dictionary of default values for fields, to be used when placeholders are needed
DEFAULT_VALUES = {
    'vehicle': {
        'distance': '12100',
        'fuel_efficiency': '22',
    },
    'public_transit_simple': {
        'distance': '368',
    },
    'public_transit_advanced': {
        'bus_kms': '130',
        'transit_rail_kms': '97',
        'commuter_rail_kms': '65',
        'intercity_rail_kms': '32',
    },
    'air_travel_simple': {
        'distance': '3300',
    },
    'air_travel_advanced': {
        'short_flights': '3',
        'medium_flights': '2',
        'long_flights': '0',
        'extended_flights': '0',
    },
    'home_energy': {
        'electricity': '1350',
        'natural_gas': '590',
        'heating_oil': '260',
        'living_space': '1850',
    },
    'shopping_advanced': {
        'furniture_appliances': '362',
        'clothing': '391',
        'entertainment': '54',
        'office_supplies': '37',
        'personal_care': '56',
        'services_food': '196',
        'education': '22',
        'communication': '46',
        'loan': '82',
        'transport': '113',
    }
}

class CarbonFootprintForm(FlaskForm):
    """Main form that combines all sections"""
    # Hidden field for csrf token only
    calculate_footprint = HiddenField()
    
    # The individual form objects will be passed separately in the template
    # so we don't need to include them here
    submit = SubmitField('Calculate Footprint')

class ResetPasswordRequestForm(FlaskForm):
    """Form for requesting a password reset"""
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address")
    ])
    submit = SubmitField('Send Reset Link')

class ResetPasswordForm(FlaskForm):
    """Form for resetting password"""
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long"),
        password_check
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message="Passwords must match")
    ])
    submit = SubmitField('Reset Password')

