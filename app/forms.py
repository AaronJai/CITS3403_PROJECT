from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
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