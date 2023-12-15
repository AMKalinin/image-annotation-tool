from flask import flash, request, redirect, session, current_app
from flask_login import current_user

import time

import math

from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = 933120000

import io

import os
import h5py
from mpi4py import MPI

import re
import time
import numpy as np
from copy import deepcopy
from functools import wraps

from app.utils import const
from app.models import Role

import pathlib, tempfile
import shutil 
from app.utils.create_format.VOC.voc_writer import VocWriter
from app.utils.create_format.COCO.coco_writer import COCODataAnnotation, COCODataCategories, COCODataImage, COCODataWriter


def build_project_path(project_name):
    return  f'{const.path.PROJECTS_FOLDER.value}/{project_name}{const.hdfs.POSTFIX.value}'

def build_logs_path(file_name):
    return  f'{const.path.LOGS_FOLDER.value}/{file_name}'

def add_project_atrr(hdf, name, description, classes, count_img):
    hdf.attrs[const.hdfs.NAME.value] = name
    hdf.attrs[const.hdfs.DESCRIPTION.value] = description
    hdf.attrs[const.hdfs.CLASSES.value] = classes
    hdf.attrs[const.hdfs.TASK_COUNT.value] = count_img
    hdf.attrs[const.hdfs.DONE_COUNT.value] = 0
    hdf.attrs[const.hdfs.TO_CHECK_COUNT.value] = 0

def get_count_layers(w, h):
    col_layer = 0
    while w>1000 or h>1000:
        col_layer += 1
        w /= 2
        h /= 2
    if col_layer == 0:
        col_layer = 1
    return col_layer

def add_task_and_attr(hdf, image, index):
    img = Image.open(image)
    task_folder = hdf.create_group(str(index))

    w = img.size[0]
    h = img.size[1]
    count_layers = get_count_layers(w,h)

    task_folder.attrs[const.tasks.FILE_NAME.value] = image.filename
    task_folder.attrs[const.tasks.WIDTH.value] = w
    task_folder.attrs[const.tasks.HEIGHT.value] = h
    task_folder.attrs[const.tasks.COUNT.value] = 0
    task_folder.attrs[const.tasks.LAYERS_COUNT.value] = count_layers
    task_folder.attrs[const.tasks.STATUS.value] = const.tasks.TO_DO.value

    for i in range(count_layers):
        if i == 0:
            desc = 1
        else:
            desc = 2
        width = int(img.size[0]/(desc))
        height = int(img.size[1]/(desc))
        img = img.resize((width, height))
        
        layer = task_folder.create_group(f"layer_{i}")
        for sampl_h in range(math.ceil(height/256)):
            for sampl_w in range(math.ceil(width/256)):
                start_p = [sampl_w*256, sampl_h*256]
                end_p = [(sampl_w+1)*256, (sampl_h+1)*256]
                if ((sampl_w+1)*256) > width:
                    end_p[0] = width
                if ((sampl_h+1)*256) > height:
                    end_p[1] = height
                sample = img.crop((start_p[0],start_p[1], end_p[0], end_p[1]))
                layer.create_dataset(f'{sampl_w}:{sampl_h}', data=np.asarray(sample, dtype='uint8'))
    
    img_icon = img.resize((100,100))
    task_folder.create_dataset('img_icon', data=np.asarray(img_icon, dtype='uint8'))         

def create_project(name, description, classes, images_list):
    project_path = build_project_path(name)
    try:
        with h5py.File(project_path, 'w-', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
            add_project_atrr(hdf, name,description, classes, len(images_list))
            for image in images_list:
                add_task_and_attr(hdf, image, images_list.index(image))
    except FileExistsError:
        print('Файл существует') 


def rewrite_task_and_attr(hdf_new, hdf_old, id, classes):
    task_folder = hdf_new.create_group(str(id))
    task_folder.attrs[const.tasks.FILE_NAME.value] = hdf_old[str(id)].attrs[const.tasks.FILE_NAME.value]
    task_folder.attrs[const.tasks.WIDTH.value] = hdf_old[str(id)].attrs[const.tasks.WIDTH.value]
    task_folder.attrs[const.tasks.HEIGHT.value] = hdf_old[str(id)].attrs[const.tasks.HEIGHT.value]
    task_folder.attrs[const.tasks.COUNT.value] = 0
    task_folder.attrs[const.tasks.LAYERS_COUNT.value] = hdf_old[str(id)].attrs[const.tasks.LAYERS_COUNT.value]
    task_folder.attrs[const.tasks.STATUS.value] = const.tasks.TO_DO.value

    count_m = hdf_old[str(id)].attrs[const.tasks.COUNT.value]

    i = 0
    for id_polygon in range(count_m):
        cclas = attrs_get_class(hdf_old[str(id)].attrs[str(id_polygon)])
        if cclas in classes:
            task_folder.attrs[str(id_polygon-i)] = hdf_old[str(id)].attrs[str(id_polygon)]
            task_folder.attrs[const.tasks.COUNT.value] += 1 
        else:
            i += 1   
    
    task_folder.create_dataset('img_icon', data=hdf_old[str(id)]['img_icon']) 

    for i in range(task_folder.attrs[const.tasks.LAYERS_COUNT.value]):
        layer = task_folder.create_group(f"layer_{i}")

        task_old = hdf_old.get(str(id))
        layer_old = task_old.get('layer_' + str(i))
        for key in layer_old.keys():
            layer.create_dataset(key, data=layer_old.get(key))

def create_project_based(name, description, classes, images_list, base):
    project_path = build_project_path(name)
    base_path = build_project_path(base)
    try:
        with h5py.File(project_path, 'w-') as hdf_new:
            add_project_atrr(hdf_new, name,description, classes, len(images_list))
            with h5py.File(base_path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf_old:
                count = hdf_old.attrs[const.hdfs.TASK_COUNT.value]
                hdf_new.attrs[const.hdfs.TASK_COUNT.value] = len(images_list) + count
                for id in range(count):
                    rewrite_task_and_attr(hdf_new, hdf_old, id, classes)
            for image in images_list:
                add_task_and_attr(hdf_new, image, images_list.index(image)+count)
    except FileExistsError:
        print('Файл существует') 


def get_project_name(path):
    name = re.search(r'[/][^/]*\.hdf', path).group(0)
    return name[1:-4]

def get_project_description(path):
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        description = hdf.attrs[const.hdfs.DESCRIPTION.value]
    return description

def get_project_alltasks(path):
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        alltasks = hdf.attrs[const.hdfs.TASK_COUNT.value]
    return alltasks

def get_project_donetasks(path):
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        donetasks = hdf.attrs[const.hdfs.DONE_COUNT.value]
    return donetasks

def get_project_to_check_tasks(path):
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        to_check_tasks = hdf.attrs[const.hdfs.TO_CHECK_COUNT.value]
    return to_check_tasks

def get_project_lastupdate(path):
    lastupdate = os.path.getmtime(path)
    return lastupdate

def get_projects_task_status(project_name, task_index):
    path = build_project_path(project_name)
    with h5py.File(path, 'r+', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        current_status = hdf[task_index].attrs[const.tasks.STATUS.value]
    return current_status

def check_status_done(project_name, task_index):
    return const.tasks.DONE.value == get_projects_task_status(project_name, task_index)

def parse_projects_folder():
    project_name_list = os.listdir(const.path.PROJECTS_FOLDER.value)
    info_dict = {'name': '',
                'description': '',
                'task':{'all': None,
                      'done': None},
                'last_update':''}
    project_info_list = []
    try:
        for project in project_name_list:
            path = f'{const.path.PROJECTS_FOLDER.value}/{project}'
            info_dict['name'] = get_project_name(path)
            info_dict['description'] = get_project_description(path)
            info_dict['task']['all'] = get_project_alltasks(path)
            info_dict['task']['done'] = get_project_donetasks(path)
            info_dict['last_update'] = time.ctime(get_project_lastupdate(path))
            project_info_list.append(deepcopy(info_dict))
    except:
        current_app.logger.warning('Ошибка при чтении проекта')
    return project_info_list

def parse_project_task(project_name, task_index):
    path = build_project_path(project_name)
    info_dict = {'index': None,
                'status': '',
                'file_name': '',
                'width': 0,
                'height':0,
                'layers':0 }
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        info_dict['index'] = task_index
        task_status = hdf[str(task_index)].attrs[const.tasks.STATUS.value]
        info_dict['status'] = task_status

        info_dict['file_name'] = hdf[str(task_index)].attrs[const.tasks.FILE_NAME.value]
        info_dict['width'] = int(hdf[str(task_index)].attrs[const.tasks.WIDTH.value])
        info_dict['height'] = int(hdf[str(task_index)].attrs[const.tasks.HEIGHT.value])
        info_dict['layers'] = int(hdf[str(task_index)].attrs[const.tasks.LAYERS_COUNT.value])
    return info_dict


def parse_project_tasks(project_name):
    path = build_project_path(project_name)
    task_count = int(get_project_alltasks(path))
    info_dict = {'index': None,
                'status': '',
                'file_name': '',
                'width': 0,
                'height':0 }
    task_info_list = []
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        for task_index in range(task_count):
            info_dict['index'] = task_index
            task_status = hdf[str(task_index)].attrs[const.tasks.STATUS.value]
            info_dict['status'] = task_status

            info_dict['file_name'] = hdf[str(task_index)].attrs[const.tasks.FILE_NAME.value]
            info_dict['width'] = hdf[str(task_index)].attrs[const.tasks.WIDTH.value]
            info_dict['height'] = hdf[str(task_index)].attrs[const.tasks.HEIGHT.value]

            task_info_list.append(info_dict.copy())
    return task_info_list

def parse_project_tasks_range(project_name, page, status, count=20):
    path = build_project_path(project_name)
    task_count = int(get_project_alltasks(path))
    task_done = int(get_project_donetasks(path))
    task_check = int(get_project_to_check_tasks(path))

    start = count*page
    end = start+count
    if status == 'right':
        status = [const.tasks.TO_CHECK.value]
        if end > task_check:
            end = task_check
    if status == 'left':
        status = [const.tasks.IN_PROGRESS.value, const.tasks.TO_DO.value]
        if end > task_count - (task_done + task_check):
            end = task_count - (task_done + task_check)

    info_dict = {'index': None,
                'status': ''}
    task_info_list = []

    needed_index = 0
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        for task_index in range(task_count):
            task_status = hdf[str(task_index)].attrs[const.tasks.STATUS.value]
            if task_status in status:
                if needed_index in range(start, end):
                    info_dict['index'] = task_index
                    info_dict['status'] = task_status
                    task_info_list.append(info_dict.copy())
                needed_index += 1
            if len(task_info_list) == (end - start):
                break
    return task_info_list

def get_task_icon(project_name, task_index):
    path = build_project_path(project_name)
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        task = hdf.get(task_index)
        data = np.array(task.get('img_icon'))
        image = Image.fromarray(data)
        buf = io.BytesIO()
        image.save(buf, format='png')
        byte_encode = buf.getvalue()
    return byte_encode

def get_task_tile(project_name, task_index, x, y, z):
    path = build_project_path(project_name)
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        task = hdf.get(task_index)
        layer = task.get('layer_' + z)
        data = np.array(layer.get(f'{str(x)}:{str(y)}'))
        image = Image.fromarray(data)
        buf = io.BytesIO()
        image.save(buf, format='png')
        byte_encode = buf.getvalue()
    return byte_encode

def pointslist_from_str(str):
    points = [[int(pnt.split(', ')[0]),int(pnt.split(', ')[1])]  for pnt in  re.findall(r'[0-9]{1,10}, [0-9]{1,10}', str)]
    return points

def save_shape(project_name, task_index, points, mask_type, class_code):
    path = build_project_path(project_name)
    with h5py.File(path, 'r+', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        mask_name = str(hdf[task_index].attrs[const.tasks.COUNT.value])
        hdf[task_index].attrs[mask_name] =f'{mask_type};{class_code};{points}'
        hdf[task_index].attrs[const.tasks.COUNT.value] +=  1
        # hdf[task_index].attrs[const.tasks.STATUS.value] = const.tasks.IN_PROGRESS.value

def parse_project_task_masks(project_name, task_index):
    result_list_masks = []
    path = build_project_path(project_name)
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        mask_count = hdf[task_index].attrs[const.tasks.COUNT.value]
        for i in [str(x) for x in range(mask_count)]:
            if attrs_get_class(hdf[task_index].attrs[i]) == '000':
                clr = '#c0c0c0'
            else:
                clr = get_codenamecolor([attrs_get_class(hdf[task_index].attrs[i])])[0][3]
            mask_info = {'name': i,
                        'type': attrs_get_type(hdf[task_index].attrs[i]),
                        'class_code':attrs_get_class(hdf[task_index].attrs[i]),
                        'points': attrs_get_points(hdf[task_index].attrs[i]),
                        'color': clr
                        }
            mask_info.update({'class_name':get_name(int(mask_info['class_code']))})
            result_list_masks.append(mask_info.copy())
    return result_list_masks

def attrs_get_type(attrs):
    return attrs.split(';')[0]

def attrs_get_class(attrs):
    return attrs.split(';')[1]

def attrs_get_points(attrs):
    return attrs.split(';')[2]

def get_all_classes():
    bases = [(x, y) for x, y in zip(const.bases.unique_id(),
                                    const.bases.name())]
    classes = [(x, y, z) for x,y,z in zip(const.classes.base(), 
                                        const.classes.code(), 
                                        const.classes.name())]
    result = []
    for base in bases:
        tmp = []
        for class_ in classes:
            if class_[0] == base[0]:
                tmp.append( [class_[2], str(class_[1])])
        result.append({'base_name':base[1],
                        'class_name':tmp.copy()})
    return result

def change_status(project_name, task_index, flag):
    path = build_project_path(project_name)
    with h5py.File(path, 'r+', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        currentStatus = hdf[task_index].attrs[const.tasks.STATUS.value]
        if flag == 1:
            if ((currentStatus == const.tasks.TO_DO.value) or \
                (currentStatus == const.tasks.IN_PROGRESS.value)) and (current_user.user_role in [1, 2]):
                hdf[task_index].attrs[const.tasks.STATUS.value] = const.tasks.TO_CHECK.value
                hdf.attrs[const.hdfs.TO_CHECK_COUNT.value] += 1
            elif (currentStatus == const.tasks.TO_CHECK.value) and (current_user.user_role in [1, 3]):
                hdf[task_index].attrs[const.tasks.STATUS.value] = const.tasks.DONE.value
                hdf.attrs[const.hdfs.DONE_COUNT.value] += 1
                hdf.attrs[const.hdfs.TO_CHECK_COUNT.value] -= 1
            else:
                return False
        if flag == -1:
            if (currentStatus == const.tasks.TO_CHECK.value) and (current_user.user_role in [1, 2, 3]):
                hdf[task_index].attrs[const.tasks.STATUS.value] = const.tasks.IN_PROGRESS.value
                hdf.attrs[const.hdfs.TO_CHECK_COUNT.value] -= 1
            else:
                return False
        return True

def change_mask_code(project_name, task_index, mask_id, class_code):
    path = build_project_path(project_name)
    with h5py.File(path, 'r+', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        triple = hdf[task_index].attrs[mask_id].split(';')
        hdf[task_index].attrs[mask_id]= f'{triple[0]};{class_code};{triple[2]}'

def change_mask_points(project_name, task_index, mask_id, points):
    path = build_project_path(project_name)
    with h5py.File(path, 'r+', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        triple = hdf[task_index].attrs[mask_id].split(';')
        hdf[task_index].attrs[mask_id]= f'{triple[0]};{triple[1]};{points}'

def delete_mask(project_name, task_index, mask_id):
    path = build_project_path(project_name)
    with h5py.File(path, 'r+', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        hdf[task_index].attrs.__delitem__(mask_id)
        hdf[task_index].attrs[const.tasks.COUNT.value] -=  1
        for i in range(hdf[task_index].attrs[const.tasks.COUNT.value]+1):
            if i > int(mask_id):
                value = hdf[task_index].attrs[str(i)]
                hdf[task_index].attrs.__delitem__(str(i))
                hdf[task_index].attrs[str(i-1)] = value

def ispoints(attr):
    if (    attr != const.tasks.COUNT.value and 
            attr != const.tasks.STATUS.value and 
            attr != const.aerial.SOURCE.value and
            attr != const.aerial.ALTITUDE.value and
            attr != const.aerial.LATITUDE.value and
            attr != const.aerial.LONGITUDE.value and
            attr != const.aerial.SUN.value and
            attr != const.aerial.SPATIAL.value and
            attr != const.aerial.SIZE.value and
            attr != const.aerial.DATE.value and
            attr != const.aerial.TIME.value  and
            attr != const.tasks.HEIGHT.value and
            attr != const.tasks.WIDTH.value and 
            attr != const.tasks.LAYERS_COUNT.value and
            attr != const.tasks.FILE_NAME.value):
            return True
    return False

def get_codenamecolor(classes_list=None):
    codenamecolor = []
    codes = const.classes.code()
    names = const.classes.name()
    colors = const.classes.color()
    code_colors = const.classes.code_color()
    for code, name, color, code_colors in zip(codes, names, colors, code_colors):
        if classes_list == None:
            codenamecolor.append((code, name, color, code_colors))
        elif str(code) in classes_list:
            codenamecolor.append((code, name, color, code_colors))
    return codenamecolor

def parse_project_classes(project_name):
    path = build_project_path(project_name)
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        classes_codes = [x for x in hdf.attrs[const.hdfs.CLASSES.value]]
    classes_list = get_codenamecolor(classes_codes)
    return classes_list

def get_name(code):
    for triple in get_codenamecolor():
        if triple[0] == code:
            return triple[1]

def get_code(classes_codes, name):
    for triple in get_codenamecolor(classes_codes):
        if triple[1] == name:
            return triple[0]

def get_color(classes_codes, code):
    for triple in get_codenamecolor(classes_codes):
        if triple[0] == code:
            return triple[2]
    #if triple[0] == '000':
    if code == 0:
        return 5
    
def access_required(roles=['any']):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if ('any_no_log' in roles):
                a = 1
            elif ('any' in roles):
                current_app.logger.info(f'user:{current_user.email} role:{current_user.user_role} from:{request.referrer} in:{request.base_url}')
            elif (current_user.user_role == 1) and ('admin' in roles):
                current_app.logger.info(f'user:{current_user.email} role:{current_user.user_role} from:{request.referrer} in:{request.base_url}')
            elif (current_user.user_role == 2) and ('marker' in roles):
                current_app.logger.info(f'user:{current_user.email} role:{current_user.user_role} from:{request.referrer} in:{request.base_url}')
            elif (current_user.user_role == 3) and ('inspector' in roles):
                current_app.logger.info(f'user:{current_user.email} role:{current_user.user_role} from:{request.referrer} in:{request.base_url}')
            else: 
                current_app.logger.info(f'user:{current_user.email} role:{current_user.user_role} from:{request.referrer} in:{request.base_url}')
                flash('Действие невозможно, так как ваш аккаунт не имеет к этому доступа')
                if request.method == 'POST':
                    request.form.to_dict()  
                return redirect(request.referrer+'#flash_msg')
                
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def get_user_info():
    role = Role.query.get(current_user.user_role).role_name
    if 'project_name' in session:
        project_name = session.get('project_name')
    else:
        project_name = None
    user = {'name':current_user.email,
            'role': role,
            'project_name': project_name,
            'id': current_user.id}
    return user

def check_create_structure_folder():
    if not os.path.exists(const.path.LOGS_FOLDER.value):
                os.mkdir(const.path.LOGS_FOLDER.value)
    if not os.path.exists(const.path.PROJECTS_FOLDER.value):
                os.mkdir(const.path.PROJECTS_FOLDER.value)

def check_project(project_name):
    path = build_project_path(project_name)
    return os.path.exists(path)

def create_folder_with_img(path_dir, project_name):
    img_dir = path_dir / 'img_dir'
    os.mkdir(img_dir)
    path = build_project_path(project_name)
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        alltasks = hdf.attrs[const.hdfs.TASK_COUNT.value]
        for task_index in range(alltasks):
            file_name = hdf[str(task_index)].attrs[const.tasks.FILE_NAME.value].split('.')[0]+'.png'
            col_width_tile = math.ceil(hdf[str(task_index)].attrs[const.tasks.WIDTH.value]/256)
            col_height_tile = math.ceil(hdf[str(task_index)].attrs[const.tasks.HEIGHT.value]/256)
            
            layer = hdf[str(task_index)].get('layer_0')
            res_img = np.zeros((256, hdf[str(task_index)].attrs[const.tasks.WIDTH.value], 3), dtype='uint8')
            for sampl_h in range(col_height_tile):
                tile_string = np.array(layer.get(f'0:{str(sampl_h)}'))
                for sampl_w in range(1, col_width_tile):
                    data = np.array(layer.get(f'{str(sampl_w)}:{str(sampl_h)}'))
                    tile_string = np.hstack((tile_string, data))
                if sampl_h == 0 :
                    res_img += tile_string
                else:
                    res_img = np.vstack((res_img, tile_string))
            image = Image.fromarray(res_img)
            image.save(img_dir / file_name)
    return img_dir

def create_COCO_annotation(task, data_writer, project_name, img):
    if img:
        file_name = task['file_name'].split('.')[0]+'.png'
    else:
        file_name = task['file_name']
    image = COCODataImage(file_name=file_name, height=int(task['height']), width=int(task['width']))
    data_writer.add_image(image)
    mask_list = parse_project_task_masks(project_name, str(task['index']))
    for mask in mask_list:
        segmentation = matr2spisok(pointslist_from_str(mask['points']))
        name_class = get_name(int(mask['class_code']))
        if not name_class:
            name_class = 'class not select'
        annot = COCODataAnnotation(False, file_name, segmentation, name_class)
        data_writer.add_annotation(annot)

def create_folder_with_COCO(path_dir, project_name, task_info_list, img):
    annotation_coco = path_dir / 'annotation_coco'
    os.mkdir(annotation_coco)
    categories = COCODataCategories()
    project_classes_list = parse_project_classes(project_name)
    categories.add_category(code=0, category_name='class not select')
    for cls in project_classes_list:
        categories.add_category(code=int(cls[0]), category_name=cls[1],super_category_name=get_name(int(str(cls[0])[0])*100))

    data_writer = COCODataWriter(categories)
    for task in task_info_list:
        create_COCO_annotation(task, data_writer, project_name, img)
    annotation_name = project_name + '.json'
    data_writer.write_data(annotation_coco / annotation_name )

def create_folder_with_VOC(path_dir, task_info_list, project_name, img, img_dir):
    annotation_voc = path_dir / 'annotation_voc'
    os.mkdir(annotation_voc)
    for task in task_info_list:
        if img:
            file_name = task['file_name'].split('.')[0]+'.png'
        else:
            file_name = task['file_name']
        writer = VocWriter(img_dir, annotation_voc, file_name, w=task['width'], h=task['height'])

        mask_list = parse_project_task_masks(project_name, str(task['index']))
        for mask in mask_list:
            points = pointslist_from_str(mask['points'])
            if mask['type'] in ['rect']:
                writer.addBndBox(mask['class_code'], points)
            elif mask['type'] == 'polygon':
                writer.addPolygon(mask['class_code'], points)
            elif mask['type'] == 'line':
                writer.addLine(mask['class_code'], points)
            elif mask['type'] == 'point':
                writer.addPoint(mask['class_code'], points)
            if mask['type'] in ['circle']:
                writer.addCircle(mask['class_code'], points)

        writer.save()

def create_folder_with_PNG(path_dir, project_name):
    annotation_png = path_dir / 'annotation_png'
    os.mkdir(annotation_png)

    path = build_project_path(project_name)
    with h5py.File(path, 'r', driver='mpio', comm=MPI.COMM_WORLD) as hdf:
        alltasks = hdf.attrs[const.hdfs.TASK_COUNT.value]
        for task_index in range(alltasks):
            file_name = hdf[str(task_index)].attrs[const.tasks.FILE_NAME.value].split('.')[0]+'.png'
            w = hdf[str(task_index)].attrs[const.tasks.WIDTH.value]
            h = hdf[str(task_index)].attrs[const.tasks.HEIGHT.value]
            
            image = Image.new('RGB', (w, h))
            draw = ImageDraw.Draw(image)
            mask_list = parse_project_task_masks(project_name, str(task_index))
            for mask in mask_list:
                points = pointslist_from_str(mask['points'])
                points_tuple = tuple([tuple(el) for el in points])
                if mask['type'] in ['rect']:
                    draw.rectangle([points_tuple[0], points_tuple[2]], fill=mask['color'])
                elif mask['type'] == 'polygon':
                    draw.polygon(points_tuple, fill=mask['color'])
                elif mask['type'] == 'line':
                    draw.line(points_tuple, fill=mask['color'], width=3)
                elif mask['type'] == 'point':
                    draw.ellipse([points_tuple[0][0]-1, points_tuple[0][1]-1, points_tuple[0][0]+1,points_tuple[0][1]+1], fill=mask['color'])
                elif mask['type'] == 'circle':
                    r = ((points_tuple[0][0]-points_tuple[1][0])**2 + (points_tuple[0][1]-points_tuple[1][1])**2)**0.5
                    draw.ellipse([points_tuple[0][0]-r, 
                                points_tuple[0][1]-r, 
                                points_tuple[0][0]+r, 
                                points_tuple[0][1]+r], 
                                fill=mask['color'])
            image.save(annotation_png / file_name)

def create_export_project(project_name, annotation, img = False, folder=None):
    task_info_list = parse_project_tasks(project_name)
    with tempfile.TemporaryDirectory() as tmp:
        pth_dir = pathlib.Path(tmp)
        path_dir = pth_dir / project_name
        os.mkdir(path_dir)
        if img:
            img_dir = create_folder_with_img(path_dir, project_name)
        else:
            img_dir = 'None'
        if 'coco' in annotation:
            create_folder_with_COCO(path_dir, project_name, task_info_list, img)

        if 'voc' in annotation:
            create_folder_with_VOC(path_dir, task_info_list, project_name, img, img_dir)
        
        if 'png' in annotation:
            create_folder_with_PNG(path_dir, project_name)
        
        if folder:
            output_path = folder / project_name
        else:
            output_path = project_name
            
        return shutil.make_archive(output_path, 'zip', pth_dir)


def matr2spisok(matr):
    answer = []
    for el in matr:
        for e in el:
            answer.append(e)
    return answer