from flask import Blueprint

bp = Blueprint('task_view', __name__, static_folder='static', static_url_path='/task_view/static', template_folder='templates',url_prefix='/view')

from app.task_view import routes