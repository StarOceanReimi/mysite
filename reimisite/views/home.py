from flask import Blueprint, render_template
import json
import os

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('home/index.html')

@home.route('/popularimages')
def popular_images():

    return os.listdir(os.path.abspath("/home/reimi/hentai/comics"))
    
if __name__ == "__main__":
    print popular_images()
