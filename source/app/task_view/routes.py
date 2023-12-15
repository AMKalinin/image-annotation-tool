from flask import render_template, request, url_for, redirect, session, flash
from flask_login import login_required

from app.task_view import bp
from app.utils import utils


@bp.route('/')
@bp.route('/<project_name>/<task_index>')
@login_required
@utils.access_required()
def view(project_name=None, task_index=None):
    user = utils.get_user_info()
    if project_name != None:
        if task_index != None:
            masks_list = utils.parse_project_task_masks(project_name, task_index)
    elif ('project_name' in session):
        project_name = session.get('project_name')
        task_index = '0'
        masks_list = utils.parse_project_task_masks(project_name, task_index)
    else:
        return render_template("task_view/view_tab.html", 
                                title='View',
                                project_name=project_name,
                                task_index=task_index,
                                user=user)
    path = utils.build_project_path(project_name)
    all_task = utils.get_project_alltasks(path)
    session['task_index'] = task_index
    task_status = utils.get_projects_task_status(project_name, task_index)
    task_index = int(task_index)
    return render_template("task_view/view_tab.html", 
                                title='View',
                                project_name=project_name,
                                task_index=task_index,
                                masks_list=masks_list,
                                user=user,
                                max_index = all_task-1,
                                task_status = task_status)

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