import hashlib


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
    a = bytearray(data_key)
    data_pwd = bytearray(password)
    size_key = len(a)
    size_pwd = len(data_pwd)
    data = bytearray(size_key + 4 + size_pwd)
    i = 0
    for item in data_pwd:
        data[i] = item
        i += 1

    add = bytearray([163, 172, 161, 163])
    for item in add:
        data[i] = item
        i += 1
    for item in a:
        data[i] = item
        i += 1
    m = hashlib.md5()
    m.update(data)
    password = m.hexdigest()

    h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
    data = {'login_name': username, "password": password, "org_name": "qcqh_sakura"}
    urlstr = "https://ucbetapi.101.com/v0.93/tokens"
    response, content = h.request(urlstr, 'POST', dumps(data), headers={'Content-Type': 'application/json'});
    content = json.loads(content)
    return jsonify(content)
