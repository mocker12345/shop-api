import hashlib
from functools import wraps

import httplib2
from json import dumps

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


def valid_header(auth_header):
    info = auth_header.splite(';')
    access_token = info[0].splite('=')[1]
    mac = info[2].splite('=')[1]
    nonce = info[1].splite('=')[1]
    data = {'mac':mac,'nonce':nonce}



def valid_token():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                return jsonify({'code': 401, 'errors': "is not login"}), 401
            else:
                valid_header(auth_header)
            return f(*args, **kw)

        return wrapper

    return decorator
