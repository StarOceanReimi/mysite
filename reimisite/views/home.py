from flask import Blueprint, render_template, Response
import json
import os
import shutil
import urllib
import random

home = Blueprint('home', __name__, template_folder="../templates", \
                 static_folder="../static")

IMAGEPATH ='/home/reimi/rs_project/reimisite_root/reimisite/static/images/shared'
SERVER_IMAGEPATH = '/static/images/shared'

@home.route('/')
def index():
    return render_template('home/index.html')

join = os.path.join

def _get_relative_imagepath_onserver(dirname):
    return os.path.join(SERVER_IMAGEPATH, dirname)

def _get_imagepath_onserver(dirname):
    return os.path.join(IMAGEPATH, dirname)

def _clear_server_imagepath():
    alldirs = _list_dir_with_parentpath(IMAGEPATH)
    for filename in alldirs:
        if os.path.isdir(filename):
            shutil.rmtree(filename)
        else:
            os.remove(filename)

def _clear_imageapth_onserver(dirname):
    imagepath_onserver = _get_imagepath_onserver(dirname)
    if os.path.exists(imagepath_onserver):
        shutil.rmtree(imagepath_onserver)
    return imagepath_onserver

def _new_imagepath_onserver(dirname):
    imagepath_onserver = _get_imagepath_onserver(dirname)
    if not os.path.exists(imagepath_onserver):
        os.mkdir(imagepath_onserver)
    return imagepath_onserver

def _list_dir_with_parentpath(dirname, f=True):
    """f is for a filter func or a boolean value
       if f is a functiion, it has to accept an 
       argument which represent each file's name
       in the directory[dirname]
    """
    if callable(f):
        return [join(dirname, d) for d in os.listdir(dirname) if f(join(dirname, d))]
    else:
        return [join(dirname, d) for d in os.listdir(dirname) if bool(f)]
    
def _copy_dir_to_dir(dest, src):
    for filename in _list_dir_with_parentpath(src):
        shutil.copy(filename, dest)

def _random_copy_from_hentai():
    ori = "/home/reimi/hentai/comics"
    available_dirs = _list_dir_with_parentpath(ori, lambda x:os.path.isdir(x))
    random_index = random.randint(0, len(available_dirs)-1)
    picked = available_dirs[random_index] 
    picked_basename = os.path.basename(picked)
    new_dir_for_picked = _new_imagepath_onserver(picked_basename)
    _copy_dir_to_dir(new_dir_for_picked, picked)


@home.route('/popularimages')
def popular_images():
    shared_images_dirs = _list_dir_with_parentpath(IMAGEPATH, lambda x: os.path.isdir(x))
    dir_basenames = map(lambda x: os.path.basename(x), shared_images_dirs)
    random_index = random.randint(0, len(dir_basenames)-1)
    basename = dir_basenames[random_index]
    shared_images_dir = shared_images_dirs[random_index]
    #picked_basename are pathname, x is filename, and a url path need to be
    #escaped so use urllib.quote
    picked_links = map(lambda x: urllib.quote(\
                       _get_relative_imagepath_onserver(\
                       join(basename, x))),\
                       os.listdir(shared_images_dir))
    picked_links = sorted(picked_links)
    response_json = json.dumps([dict(src=link, title=basename, dest="#",\
                            desc="Hentai Collection! Which I love! Haha")\
                            for link in picked_links])
    return Response(response_json, mimetype="application/json")

if __name__ == "__main__":
    print popular_images()
