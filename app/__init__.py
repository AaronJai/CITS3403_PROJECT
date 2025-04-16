from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.secret_key = '9f6b2f3c4d1e7a2b57cf5e2d8a7b3f7a'

from app import routes
from app import models