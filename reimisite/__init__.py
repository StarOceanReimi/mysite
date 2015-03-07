import os
from .views.home import home
from flask import Flask

instance_path = os.path.abspath('/home/reimi/rs_project/reimisite_root/instance')
app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)
app.config.from_object('reimisite.config')
app.config.from_pyfile('config.py')
if 'APP_SETTINGS' in os.environ:
    app.config.from_envvar('APP_SETTINGS')

app.register_blueprint(home)
