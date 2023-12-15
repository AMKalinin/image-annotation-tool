import os

#from app import const


basedir = os.path.abspath(os.path.dirname(__file__))



class BaseConfig:
    SECRET_KEY               = '91d640b663270b95f8345354d4499c06d86803e1934295384ea932e89a81'   
    CSRF_ENABLED             = True                    

    # UPLOAD_FOLDER            = 'uploads' #const.path.UPLOAD_FOLDER.value
    ALLOWED_EXTENSIONS       = {'PNG','png', 'jpg', 'jpeg', 'tiff', 'tif'}
    SQLALCHEMY_DATABASE_URI  = os.environ.get('DATABASE_URL') or \
                                'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    FLASK_ADMIN_SWATCH = 'cerulean'
    DEBUG = False


class DebugConfig(BaseConfig):
    DEBUG                    = True


class TestConfig(BaseConfig):
    TESTING                    = True