import os
import views
from flask import Flask
from .views.home import home
instance_path = os.path.abspath(os.path.join(os.getcwd(), 'instance'))

app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)
app.config.from_object('reimisite.config')
app.config.from_pyfile('config.py')

if 'APP_SETTINGS' in os.environ:
    app.config.from_envvar('APP_SETTINGS')

app.register_blueprint(home);
