import os

import jinja2
from flask import Flask
from . import pages


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        PAGESPATH = './texts' #todo: ask user for path
    )
    #https://stackoverflow.com/questions/13598363/how-to-dynamically-select-template-directory-to-be-used-in-flask

    add_texts_to_jinja_templates_path = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader([app.config['PAGESPATH'], './templates'])])
    app.jinja_loader = add_texts_to_jinja_templates_path

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(pages.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
