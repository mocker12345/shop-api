import hashlib
import random
from functools import wraps

import httplib2
from json import dumps

import time
from flask import json

from app import models

from . import land

from flask import request

from flask import jsonify


@models.validate_json
@land.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    username = req['username']
    password = req['password'].encode()
    data_key = "fdjf,jkgfkl"
    b = password + chr(163) + chr(172) + chr(161) + chr(163) + data_key
    c = bytearray(b)
    md5 = hashlib.md5()
    md5.update(c)
    password = md5.hexdigest()
    h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
    data = {'login_name': username, "password": password, "org_name": "qcqh_sakura"}
    urlstr = "https://ucbetapi.101.com/v0.93/tokens"
    response, content = h.request(urlstr, 'POST', dumps(data), headers={'Content-Type': 'application/json'})
    content = json.loads(content)
    return jsonify(content)


def valid_header(header):
    auth_header = header.get('Authorization')
    method = request.method
    host = "0.0.0.0:8000"
    uri = request.path
    info = str(auth_header).split(',')
    access_token = info[0].split('=')[1].replace('\"', '')
    mac = info[2].split('=')[1].replace('\"', '') + '='
    nonce = info[1].split('=')[1].replace('\"', '')
    data = {'mac': mac, 'nonce': nonce, 'http_method': method, 'request_uri': uri, "host": host}
    h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
    urlstr = "https://ucbetapi.101.com/v0.93/tokens/" + access_token + "/actions/valid"
    response, content = h.request(urlstr, 'POST', dumps(data), headers={'Content-Type': 'application/json'})
    content = json.loads(content)
    if 'message' in content:
        return content, 401
    else:
        return content, 200


def valid_token():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                return jsonify({'code': 401, 'errors': "is not login"}), 401
            else:
                content, status = valid_header(request.headers)
                if status == 401:
                    return jsonify(content), 401

            return f(*args, **kw)

        return wrapper

    return decorator
