from flask import Blueprint

bp = Blueprint('tasks_tab', __name__, static_folder='static', static_url_path='/tasks_tab/static', template_folder='templates', url_prefix='/tasks')

from app.tasks_tab import routes