from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import logging
from logging.handlers import RotatingFileHandler

from config import DebugConfig
from app.admin import admin

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_class=DebugConfig):
    from app.utils import utils
    utils.check_create_structure_folder()
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp
    from app.general import bp as general_bp
    from app.projects_tab import bp as projects_tab_bp
    from app.tasks_tab import bp as tasks_tab_bp
    from app.task_edit import bp as task_edit_bp
    from app.task_view import bp as task_view_bp


    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(general_bp)
    app.register_blueprint(projects_tab_bp)
    app.register_blueprint(tasks_tab_bp)
    app.register_blueprint(task_edit_bp)
    app.register_blueprint(task_view_bp)

    admin.add_admin(app, db)

    

    if not app.debug and not app.testing:
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=100*10240,
                                       backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)-25s %(levelname)-6s %(message)s'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('app startup')

    return app
