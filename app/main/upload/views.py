import datetime
import random
from flask import json, jsonify, make_response
from qiniu import put_data, Auth

from app.main.login.views import valid_token
from . import upload
from flask import request


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@upload.route('/uptoken/', methods=['GET'])
def upload_token():
    access_key = 'KwiWX_tDNWUafhJmsaOvbCeImLUFjnez0nuJEdt3'
    secret_key = '69U1YTlBlHJKMqMD_xJ3I56b0OkdUhvHgtMmeVvt'
    q = Auth(access_key, secret_key)
    bucket_name = 'qiniuimage'
    uptoken = q.upload_token(bucket_name)
    resp = make_response(jsonify({'uptoken': uptoken}))
    return resp


@upload.route('/upload', methods=['POST'])
@valid_token()
def upload():
    fs = request.files['file']
    key = gen_rnd_filename() + fs.filename
    base_url = 'http://oce6f0hwv.bkt.clouddn.com/'
    uptoken = json.loads(upload_token().data)
    ret, info = put_data(uptoken['uptoken'], key, fs.stream)
    return_name = ret['key']
    return jsonify({'success': True, 'image_url': base_url + return_name})
