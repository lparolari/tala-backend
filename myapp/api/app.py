from flask import Flask
from flask_cors import CORS
import os

from .anomalies import bp as anomalies_bp
from .hello import bp as hello_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['UPLOAD_FOLDER'] = '/tmp'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)

    app.register_blueprint(anomalies_bp)
    app.register_blueprint(hello_bp)

    return app
