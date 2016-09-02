from flask import jsonify
from flask import Flask
from sqlalchemy.exc import IntegrityError
from . import error

app = Flask(__name__)


@error.app_errorhandler(404)
def not_found(e):
    return jsonify({'error': 404, 'message': 'not found'}), 404


@error.app_errorhandler(400)
def not_valid(e):
    return jsonify({'error': 400, 'message': 'Parameter is not valid'}), 400


# class repeat(Exception):
#     pass
#
#
# @main_b.app_errorhandler(repeat)
# def is_repeat(e):
#     respones = dict(error=400, message='Name repetition')
#     return jsonify(respones)

@error.app_errorhandler(500)
def not_server_error(e):
    return jsonify({'error': 500, 'message': 'Unkown server error'})


@error.app_errorhandler(IntegrityError)
def valid_exist(e):
    return jsonify({'error': 4000, 'message': 'name is exist'})
