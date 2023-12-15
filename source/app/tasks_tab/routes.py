from flask import render_template, request, session
from flask_login import login_required

from app.tasks_tab import bp
from app.utils import utils


availability_dict = {}

@bp.route('/')
@bp.route('/<string:project_name>')
@login_required
@utils.access_required()
def tasks(project_name=None):
    user = utils.get_user_info()
    if project_name != None:
        session['project_name'] = project_name
    elif 'project_name' in session:
        project_name = session.get('project_name')
    else:
        return render_template("tasks_tab/tasks_tab.html", title='Tasks', user = user)
    # tasks_list = utils.parse_project_tasks(project_name)
    path = utils.build_project_path(project_name)
    project_descriptoin = utils.get_project_description(path)
    tasks_list = utils.parse_project_tasks_range(project_name, 0, 'left')
    tasks_list.extend(utils.parse_project_tasks_range(project_name, 0, 'right'))
    return render_template("tasks_tab/tasks_tab.html", 
                            title='Tasks',
                            project_name=project_name, 
                            description=project_descriptoin,
                            tasks_list=tasks_list,
                            user = user)

@bp.route('/get_tasks', methods=['POST'])
@login_required
@utils.access_required()
def get_tasks():
    if request.method =='POST':
        data = request.json
        project_name = session.get('project_name')
        page = data['page']
        status = data['status']
        tasks_list = utils.parse_project_tasks_range(project_name, page, status)
    return render_template('tasks_tab/tasks_create.html', 
                           project_name=project_name,
                           tasks_list=tasks_list)