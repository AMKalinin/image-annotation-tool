from os import path as Path
from jinja2 import Template
from xml.sax.saxutils import escape

class VocWriter:
    def __init__(self, imageDir, annotationDir, imageName, w, h, depth=3, database='Unknown', segmented=1):
        myxml = open('app/utils/create_format/VOC/templates/annotation.xml').read()
        
        self.annotation_template = Template(myxml)
        
        self.imageDir = imageDir        
        self.annotationDir = annotationDir
        self.imageName = imageName


        self.template_parameters = {
            'width': w,
            'height': h,
            'depth': depth,
            'database': escape(database),
            'segmented': segmented,
            'objects': []
        }


    def addBndBox(self, name, points, pose='Unspecified', truncated=0, difficult=0):
        self.template_parameters['objects'].append({
            'name': escape(name),
            'pose': escape(pose),
            'truncated': truncated,
            'difficult': difficult,
            'xmin': min(points, key=lambda x:x[0])[0],
            'ymin': min(points, key=lambda x:x[1])[1],
            'xmax': max(points, key=lambda x:x[0])[0],
            'ymax': max(points, key=lambda x:x[1])[1]
        })
            
    def addPolygon(self, name, points, pose='Unspecified', truncated=0, difficult=0):
        self.template_parameters['objects'].append({
            'name': escape(name),
            'pose': escape(pose),
            'truncated': truncated,
            'difficult': difficult,
            'points_p': points,
            'xmin': min(points, key=lambda x:x[0])[0],
            'ymin': min(points, key=lambda x:x[1])[1],
            'xmax': max(points, key=lambda x:x[0])[0],
            'ymax': max(points, key=lambda x:x[1])[1]
        })

    def addPoint(self, name, points, pose='Unspecified', truncated=0, difficult=0):
        self.template_parameters['objects'].append({
            'name': escape(name),
            'pose': escape(pose),
            'truncated': truncated,
            'difficult': difficult,
            'point_p': points,
            'xmin': min(points, key=lambda x:x[0])[0],
            'ymin': min(points, key=lambda x:x[1])[1],
            'xmax': max(points, key=lambda x:x[0])[0],
            'ymax': max(points, key=lambda x:x[1])[1]
        })

    def addLine(self, name, points, pose='Unspecified', truncated=0, difficult=0):
        self.template_parameters['objects'].append({
            'name': escape(name),
            'pose': escape(pose),
            'truncated': truncated,
            'difficult': difficult,
            'points_l': points,
            'xmin': min(points, key=lambda x:x[0])[0],
            'ymin': min(points, key=lambda x:x[1])[1],
            'xmax': max(points, key=lambda x:x[0])[0],
            'ymax': max(points, key=lambda x:x[1])[1]
        })
    
    def addCircle(self, name, points, pose='Unspecified', truncated=0, difficult=0):
        cx = points[0][0]
        cy = points[0][1]
        r = ((points[0][0]-points[1][0])**2 + (points[0][1]-points[1][1])**2)**0.5
        self.template_parameters['objects'].append({
            'name': escape(name),
            'pose': escape(pose),
            'truncated': truncated,
            'difficult': difficult,
            'points_c': [cx, cy, r],
            'xmin': cx - r,
            'ymin': cy - r,
            'xmax': cx + r,
            'ymax': cy + r
        })

    def save(self):
        imagePath = Path.join(self.imageDir, self.imageName)
        _ = self.template_parameters
        _['filename'] = escape(Path.basename(self.imageName))
        _['folder'] = escape(Path.basename(Path.abspath(self.imageDir)))
        _['path'] = escape(Path.abspath(imagePath))
        
        annotationName = Path.splitext(self.imageName)[0] + '.xml'
        annotationPath = Path.join(self.annotationDir, annotationName)
        with open(annotationPath, 'w') as file:
            content = self.annotation_template.render(**self.template_parameters)
            file.write(content)