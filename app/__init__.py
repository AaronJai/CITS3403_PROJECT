from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
import os
from app.config import Config

# Initialize extensions outside of create_app to avoid circular imports
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'error'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.blueprints import main
    app.register_blueprint(main)
    
    return app
    
# Import models here to avoid circular imports
from app import models