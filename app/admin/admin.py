from flask_login import current_user

import os.path as op

from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.base import AdminIndexView


class MyAdminView(AdminIndexView):
    def is_visible(self):
        return False

    def is_accessible(self):
        return (current_user.is_authenticated and current_user.user_role == 1)


class MyModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.user_role == 1)


class Folder_projects(FileAdmin):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.user_role == 1)


class Folder_logs(FileAdmin):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.user_role == 1)

def add_admin(app, db):
    admin = Admin(app, template_mode='bootstrap3',name='Web Labeling', index_view=MyAdminView())
    from app import models
    admin.add_view(MyModelView(models.User, db.session, name='Users'))
    admin.add_view(Folder_projects('projects', '/projects_d/', name='Projects'))
    # path = op.join(op.dirname(__file__), 'logs')
    admin.add_view(Folder_logs('logs', '/logs/', name='LOGS'))
