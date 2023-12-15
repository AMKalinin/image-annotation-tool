from flask import Blueprint

bp = Blueprint('projects_tab', __name__, static_folder='static', static_url_path='/projects_tab/static', template_folder='templates', url_prefix='/projects')

from app.projects_tab import routes