import io
import math
import numpy as np
import h5py

from sqlalchemy.orm import Session
from fastapi import UploadFile

from PIL import Image
Image.MAX_IMAGE_PIXELS = 933120000

from app import crud
from app.schemas.task import TaskBase


class ProjectWorker():
    def __init__(self, project_name:str) -> None:
        self.project_name:str = project_name
        self.project_path:str = self.build_path() 
        self.tile = {'width': 256,
                     'height': 256}
        self.min_size = {'width': 1000,
                         'height': 1000}

    def build_path(self) -> str:
        path = f'projects/{self.project_name}.hdf'
        return path

    def create_project(self,db:Session, images:list[UploadFile]) -> None:
        with h5py.File(self.project_path, 'w-') as hdf:
            self.add_tasks(db, hdf, images)

    def add_tasks(self,db, hdf:h5py.File, images:list[UploadFile]):
        for index, image in enumerate(images):
            self.add_task(db, hdf, image, index)

    def add_task(self,db:Session, hdf:h5py.File, image:UploadFile, index:int):
        img = Image.open(image.file)
        task_folder = hdf.create_group(str(index))
        count_layers = self.get_count_layers(img.size[0], img.size[1])
        task = TaskBase(id=index,
                        project_name=self.project_name,
                        file_name=image.filename,
                        width=img.size[0],
                        height=img.size[1],
                        layers_count=count_layers,
                        status='OK')
        self.add_task_db(db, task_in=task)  
        
        for i in range(count_layers):
            self.create_layer(task_folder, i, img)

        img_icon = img.resize((100,100))
        task_folder.create_dataset('img_icon', data=np.asarray(img_icon, dtype='uint8'))  

    def add_task_db(self, db:Session, task_in:TaskBase):
        crud.task.create(db, task_in)

    def get_count_layers(self, w:int, h:int) -> int:
        col_layer = 0
        while w>self.min_size['width'] or h>self.min_size['height']:
            col_layer += 1
            w /= 2
            h /= 2
        if col_layer == 0:
            col_layer = 1
        return col_layer
    
    def create_layer(self, 
                     task_folder:h5py.Group, 
                     layer_index:int, 
                     img:Image):
        desc = 2
        width = int(img.size[0]/(desc**layer_index))
        height = int(img.size[1]/(desc**layer_index))
        img = img.resize((width, height))
        layer = task_folder.create_group(f"layer_{layer_index}")
        for sampl_h in range(math.ceil(height/self.tile['height'])):
            for sampl_w in range(math.ceil(width/self.tile['width'])):
                start_p, end_p = self.calculate_tile_position(sampl_h, sampl_w, width, height)
                sample = img.crop((start_p[0],start_p[1], end_p[0], end_p[1]))
                layer.create_dataset(f'{sampl_w}:{sampl_h}', data=np.asarray(sample, dtype='uint8'))
        

    def calculate_tile_position(self, sampl_h:int, sampl_w:int,
                                width:int, height:int) -> tuple[list[int]]:
        start_p = [sampl_w*self.tile['width'], sampl_h*self.tile['height']]
        end_p = [(sampl_w+1)*self.tile['width'], (sampl_h+1)*self.tile['height']]
        if ((sampl_w+1)*self.tile['width']) > width:
            end_p[0] = width
        if ((sampl_h+1)*self.tile['height']) > height:
            end_p[1] = height
        return start_p, end_p
    
    def image_data2byte(self, data:np.ndarray) -> bytes:
        image = Image.fromarray(data)
        buf = io.BytesIO()
        image.save(buf, format='png')
        byte_encode = buf.getvalue()
        return byte_encode

    def get_task_icon(self, task_id:int) -> bytes:
        with h5py.File(self.project_path, 'r') as hdf:
            task = hdf.get(str(task_id))
            data = np.array(task.get('img_icon'))
            byte_encode = self.image_data2byte(data)
        return byte_encode

    def get_task_tail(self, task_id:int, layer:int, x:int, y:int) -> bytes:
        with h5py.File(self.project_path, 'r') as hdf:
            task = hdf.get(str(task_id))
            layer = task.get('layer_' + str(layer))
            data = np.array(layer.get(f'{str(x)}:{str(y)}'))
            byte_encode = self.image_data2byte(data)
        return byte_encode