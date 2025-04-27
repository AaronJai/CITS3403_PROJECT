from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i_love_matcha'

from app import routes
from app import models