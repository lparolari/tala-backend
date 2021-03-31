from flask import Blueprint, Response
from flask import jsonify, request, redirect, url_for, current_app
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
from ..analyzer.analyze import get_anomalies_list, get_left, read_meeting_from_csv
import os


bp = Blueprint('anomalies', __name__, url_prefix='/anomalies')


ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_files(files):
    for f in files:
        if f.filename == '':
            return jsonify({"errors": ["file is empty"]}), 409
        if not allowed_file(f.filename):
            return jsonify({"errors": ["file type not allowed"]}), 409
    return None


def save_files(files, filenames):
    for f, fn in zip(files, filenames):
        f.save(fn)


@bp.route('/left', methods=['POST'])
def anomalies_left():
    upload_folder = current_app.config['UPLOAD_FOLDER']

    files = request.files.getlist("file[]")
    filenames = [os.path.join(
        upload_folder, secure_filename(f.filename)) for f in files]

    # check file constraints
    checks = check_files(files)
    if checks is not None:
        return checks

    # save files
    save_files(files, filenames)

    return {"anomalies": get_anomalies_list([read_meeting_from_csv(filename) for filename in filenames], get_left)}


@ bp.after_request
def after_request(response):
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
