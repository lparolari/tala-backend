from flask import Flask
from flask_cors import CORS
import os


def load_config(app, test_config):
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


def ensure_instance_folder(app):
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    load_config(app, test_config)
    ensure_instance_folder(app)

    return app
