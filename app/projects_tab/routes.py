from flask import render_template, request, url_for, redirect, flash, send_file
from flask_login import login_required

from werkzeug.utils import secure_filename


import pathlib, tempfile

from app import current_app
from app.projects_tab import bp
from app.utils import utils

availability_dict = {}

@bp.route('/')
@login_required
@utils.access_required()
def projects():
    project_list = utils.parse_projects_folder()
    classes_list = utils.get_all_classes()
    user = utils.get_user_info()
    return render_template("projects_tab/projects_tab.html", 
                            title='Projects', 
                            projects_list=project_list, 
                            classes_list=classes_list,
                            user = user)

@bp.route('/upload', methods=['POST'])
@login_required
@utils.access_required(roles=['admin'])
def upload():
    if request.method =='POST':
        file_list = request.files.getlist('projectImg')
        filter_files(file_list)
        project_name = request.form['projectName']
        if request.form['projectName'][-1]==' ':
            project_name = request.form['projectName'][:-1]
        codes_list = fill_code_list(request)
        if utils.check_project(project_name):                       # Лучше сделать во время проверки формы 
            flash('Проект с таким именем существует')               # 
            return redirect(url_for('.projects')+'#flash_msg')  #   
        utils.create_project(project_name,
                                request.form['projectDescription'], 
                                codes_list, 
                                file_list)
        current_app.logger.info(f'new project ({project_name})')
        flash('Проект создан')  
    return redirect(url_for('.projects')+'#flash_msg')

@bp.route('/uploadBased', methods=['POST'])
@login_required
@utils.access_required(roles=['admin'])
def upload_based():
    if request.method =='POST':
        file_list = request.files.getlist('projectImg')
        filter_files(file_list)
        project_name = request.form['projectName']
        if request.form['projectName'][-1]==' ':
            project_name = request.form['projectName'][:-1]
        codes_list = fill_code_list(request)
        if utils.check_project(project_name):                       # Лучше сделать во время проверки формы 
            flash('Файл с таким именем существует')                 # 
            return redirect(url_for('.projects')+'#flash_msg')  #   
        based = request.form['projectBase']
        utils.create_project_based(project_name,
                                request.form['projectDescription'], 
                                codes_list, 
                                file_list,
                                request.form['projectBase'])
        current_app.logger.info(f'new project {project_name}.hdf5 based {based}.hdf5')
    return redirect(url_for('.projects'))

@bp.route('/export_ds/<projectName>/<format_data>')
@utils.access_required()
def export_ds(projectName, format_data):
    with tempfile.TemporaryDirectory() as tmp:
        pth_dir = pathlib.Path(tmp)
        file_path = utils.create_export_project(projectName, annotation=[format_data], img=False, folder = pth_dir)
        return send_file(file_path, as_attachment=True)  

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

def filter_files(file_list):
    file_list.reverse()
    for img in file_list:
            if not allowed_file(secure_filename(img.filename)):
                file_list.remove(img)
    
def fill_code_list(req):
    codes_list = []
    for key in req.form:
        if key[:5] =='check':
            codes_list.append(request.form[key].split(':')[1])
    return codes_list
