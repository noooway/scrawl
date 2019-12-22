import os
from flask import (
    Blueprint, render_template, request,
    current_app
)


bp = Blueprint('pages', __name__)


@bp.route('/')
def index():
    path = current_app.config['PAGESPATH']
    pages = get_pages(path)
    return render_template('base.html', pages=pages)


@bp.route('/pages/<path:filename>', methods=('GET', 'POST'))
def render_page(filename):
    path = current_app.config['PAGESPATH']
    if request.method == 'POST':
        content = request.form['content']
        print(content)
        fullpath = os.path.join(path, filename)
        with open(fullpath, 'w') as f:
            f.write(content)
    pages = get_pages(path)
    current_page = filename
    fullpath = os.path.join(path, filename)
    with open(fullpath, 'r') as f:
        content = f.read()
    return render_template('base.html', pages=pages, content=content)


def get_pages(path):
    pages = []
    dircontent = os.listdir(path)
    for name in dircontent:
        fullname = os.path.join(path, name)
        if os.path.isdir(fullname):
            pass
        else:
            pages.append(name)
    return pages
