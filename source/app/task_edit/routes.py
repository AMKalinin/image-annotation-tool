from flask import render_template, request, url_for, redirect, session, flash
from flask_login import login_required


from urllib.parse import unquote

from app.task_edit import bp
from app.general.routes import ava_check 
from app.utils import utils


@bp.route('/<project_name>/<task_index>')
@login_required
@utils.access_required(roles=['admin', 'marker'])
def task_edit(project_name, task_index):
    if utils.check_status_done(project_name, task_index):
        flash('Действие невозможно, задача закрыта')
        return redirect(url_for('tasks_tab.tasks')+'#flash_msg')
    task_status = utils.get_projects_task_status(project_name, task_index)
    type_mask = 0
    masks_list = utils.parse_project_task_masks(project_name, task_index)
    classes_list = utils.parse_project_classes(project_name)
    user = utils.get_user_info()
    data = {'prj_tsk': project_name+'_'+task_index}
    session['task_index'] = task_index
    if not ava_check(data, user):
        flash('Действие невозможно, задача открыта другим пользователем')
        return redirect(url_for('tasks_tab.tasks')+'#flash_msg')
    else:
        return render_template("task_edit/task_edit.html", 
                                title='Edit', 
                                project_name=project_name, 
                                task_index=task_index, 
                                masks_list=masks_list,
                                classes_list=classes_list,
                                type_mask = type_mask,
                                task_status = task_status,
                                user=user)

@bp.route('/change_task', methods = ['POST'])
@login_required
@utils.access_required(roles=['admin', 'marker'])
def change_task():
    type_mask = 0
    data = request.json
    project_name = unquote(data['projectName'])
    task_index = data['taskIndex']
    points = data['points']
    mask_type = data['type']
    class_code = data['code']
    utils.save_shape(project_name, task_index, points, mask_type, class_code)
    mask = utils.parse_project_task_masks(project_name, task_index)[-1]
    classes_list = utils.parse_project_classes(project_name)
    return render_template('maska.html',
                            project_name=project_name, 
                            task_index=task_index,
                            mask=mask,
                            classes_list=classes_list,
                            type_mask = type_mask)


@bp.route('/change_class_code', methods = ['POST'])
@login_required
@utils.access_required(roles=['admin', 'marker'])
def change_class_code():
    data = request.json
    project_name = unquote(data['projectName'])
    task_index = data['taskIndex']
    mask_id = data['maskID']
    class_code = data['code']
    utils.change_mask_code(project_name, task_index, mask_id, class_code)
    return redirect(url_for('.task_edit', 
                            project_name=project_name, 
                            task_index=task_index))

@utils.access_required(roles=['admin', 'marker'])
@bp.route('/delete_mask', methods = ['POST'])
def delete_mask():
    data = request.json
    project_name = unquote(data['projectName'])
    task_index = data['taskIndex']
    mask_id = data['maskID']
    utils.delete_mask(project_name, task_index, mask_id)
    return redirect(url_for('.task_edit', 
                            project_name=project_name, 
                            task_index=task_index))

@bp.route('/change_mask_point', methods = ['POST'])
@utils.access_required(roles=['admin', 'marker'])
def change_mask_point():
    data = request.json
    project_name = unquote(data['projectName'])
    task_index = data['taskIndex']
    mask_id = data['maskID']
    points = data['points']
    utils.change_mask_points(project_name, task_index, mask_id, points)
    return redirect(url_for('.task_edit', 
                            project_name=project_name, 
                            task_index=task_index))
