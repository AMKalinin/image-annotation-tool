from flask import Blueprint

bp = Blueprint('auth', __name__, static_folder='static',static_url_path='/auth/static', template_folder='templates')

from app.auth import routes