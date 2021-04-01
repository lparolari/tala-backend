from flask import Blueprint, Response
from flask import jsonify, make_response, request, current_app
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
from ..analyzer.analyze import get_anomalies_list, get_left, get_joined, read_meeting_from_csv
import os
import ntpath


bp = Blueprint('anomalies', __name__)


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


@bp.route('/anomalies', methods=['POST'])
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

    # get analysis type
    analysis_type = request.args.get('analysis_type')
    if analysis_type not in ["Left", "Joined"]:
        analysis_type = "Left"

    # set the analysis function
    analysis_f = get_left if analysis_type == "Left" else get_joined

    # load dfs
    dfs = [read_meeting_from_csv(filename) for filename in filenames]

    # collect anomalies
    anomalies = zip(get_anomalies_list(dfs, analysis_f), filenames)
    anomalies = filter(lambda a: not (a[0] == {}), anomalies)
    anomalies = map(
        lambda a: {**a[0], "filename": ntpath.basename(a[1])}, anomalies)
    anomalies = list(anomalies)

    return make_response(jsonify(anomalies))


@bp.after_request
def after_request(response):
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
