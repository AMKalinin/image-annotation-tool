from flask import Blueprint

bp = Blueprint('task_edit', __name__, static_folder='static', static_url_path='/task_edit/static', template_folder='templates', url_prefix='/task_edit')

from app.task_edit import routes