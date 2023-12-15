from flask import Blueprint

bp = Blueprint('general', __name__, static_folder='static', static_url_path='/general/static', template_folder='templates')

from app.general import routes