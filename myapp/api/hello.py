from flask import Blueprint, jsonify, make_response


bp = Blueprint('hello', __name__)


@bp.route('/')
def hello():
    return make_response(jsonify("world"))


@bp.after_request
def after_request(response):
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
