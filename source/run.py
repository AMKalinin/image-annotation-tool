from app import create_app
from config import BaseConfig

app = create_app(config_class=BaseConfig)
if __name__ == '__main__':
    app.run(host='0.0.0.0')
