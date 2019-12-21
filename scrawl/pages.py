import os
from flask import (
    Blueprint, render_template, request,
    current_app
)


bp = Blueprint('pages', __name__)


@bp.route('/')
def index():
    path = current_app.config['PAGESPATH']
    pages = get_pages_tree(path)
    current_page = 'default.html'
    return render_template(current_page, pages=pages)


@bp.route('/pages/<path:filename>', methods=('GET', 'POST'))
def render_page(filename):
    path = current_app.config['PAGESPATH']
    if request.method == 'POST':
        content = request.form['content']
        # todo: avoid template language altogether; use divs.
        # todo: move template wrapping to separate function
        template = """
        {{% extends 'base.html' %}}

        {{% block content %}}
        {content}
        {{% endblock %}}
        """
        print(template.format(content=content))
        # todo: use system separator
        fullpath = '/'.join([path, filename])
        with open(fullpath, 'w') as f:
            f.write(template.format(content=content))
    pages = get_pages_tree(path)
    current_page = filename
    return render_template(current_page, pages=pages)


def get_pages_tree(path):
    #https://stackoverflow.com/questions/10961378/how-to-generate-an-html-directory-list-using-python
    #https://stackoverflow.com/questions/44271535/generating-a-recursive-sitemap-with-relative-href-links
    tree = dict(name=os.path.basename(path), children=[])
    lst = os.listdir(path)
    for name in lst:
        fullname = os.path.join(path, name)
        relpath = "/".join(fullname.strip("/").split('/')[2:]) #todo: simplify
        if os.path.isdir(fullname):
            tree['children'].append(get_pages_tree(fullname))
        else:
            tree['children'].append({"name":name, "relpath":relpath})
    return tree
