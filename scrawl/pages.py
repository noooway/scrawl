import os
from flask import (
    current_app,
    Blueprint, render_template, request,
    redirect, url_for, safe_join, flash
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
        # todo: security
        content = request.form['content']
        print(content)
        fullpath = safe_join(path, filename)
        with open(fullpath, 'w') as f:
            f.write(content)
    pages = get_pages(path)
    current_page = filename
    fullpath = safe_join(path, filename)
    with open(fullpath, 'r') as f:
        content = f.read()
    return render_template('base.html', pages=pages, content=content)


@bp.route('/create_page', methods=['POST'])
def create_page():
    # todo: security;
    # http://lucumr.pocoo.org/2010/12/24/common-mistakes-as-web-developer/
    pagename = request.form['page_name']
    path = current_app.config['PAGESPATH']
    fullpath = safe_join(path, pagename)
    with open(fullpath, "a+") as f:
        create_text = '<div id="content">\n Scrawl! \n</div>'
        f.write(create_text)
    return redirect(url_for('pages.render_page', filename=pagename))


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
