from flask import (request, url_for, redirect, make_response, 
                   session, jsonify, flash)
from flask_login import login_required
import time

from app.general import bp
from app.utils import utils


availability_dict = {}

@bp.route('/')
@login_required
@utils.access_required()
def home():
    return redirect(url_for('projects_tab.projects'))

@bp.route('/task_icon/<project_name>/<task_index>')
@login_required
@utils.access_required(roles=['any_no_log'])
def task_icon(project_name, task_index):
    img = utils.get_task_icon(project_name, task_index)
    return make_response(img)

@bp.route('/task_tail/<project_name>/<task_index>/<x>/<y>/<z>')
@login_required
@utils.access_required(roles=['any_no_log'])
def task_tail(project_name, task_index, x, y, z):
    img = utils.get_task_tile(project_name, task_index, x, y, z)
    return make_response(img)

@bp.route('/get_img_info/<project_name>/<task_index>', methods=['POST'])
@login_required
@utils.access_required(roles=['any_no_log'])
def get_img_info(project_name, task_index):
    data = utils.parse_project_task(project_name, task_index)
    return jsonify(data)

@bp.route('/change_status/<project_name>/<task_index>', methods = ['POST'])
@bp.route('/change_status', methods = ['POST'])
@login_required
@utils.access_required()
def change_status(project_name=None, task_index=None):
    if project_name == None:
        project_name = session.get('project_name')
        task_index = session.get('task_index')
    if request.form['button'] == '>>':
        flag = 1
    elif request.form['button'] == '<<':
        flag = -1
    if not utils.change_status(project_name, task_index, flag):
        flash('Действие невозможно, вы не имеете прав')
        return redirect(url_for('tasks_tab.tasks')+'#flash_msg')
    return redirect(url_for('tasks_tab.tasks', project_name=project_name))

@bp.route('/availability_check', methods=['POST'])
@utils.access_required()
def availability_check():
    user = utils.get_user_info()
    data = request.json
    if not ava_check(data, user):
        flash('Действие невозможно, задача открыта другим пользователем')
        return url_for('tasks_tab.tasks')+'#flash_msg'
    else:
        return jsonify({'norm': 123})

def ava_check(data, user):
    if data['prj_tsk'] in availability_dict:
        if availability_dict[data['prj_tsk']][0] == user['id']:
            availability_dict.update({ data['prj_tsk']:[user['id'], time.time()] })
        elif (time.time()- availability_dict[data['prj_tsk']][1] > 16):
            availability_dict.update({ data['prj_tsk']:[user['id'], time.time()] })
        else:
            return False
    else:
        availability_dict.update({ data['prj_tsk']:[user['id'], time.time()] })
    return True
