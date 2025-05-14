from flask import Blueprint

main = Blueprint('main', __name__)

# Import routes at the end to avoid circular imports
from app import routes