import datetime

from app.main.login.views import valid_token
from app.models import Commodity
from . import commodity
from flask import json
from flask import jsonify
from app import db
from flask import abort
from flask import request
import app.models as models

commoditys_schema = models.CommoditySchema(many=True)
commodity_schema = models.CommoditySchema()


@commodity.route('/commodity', methods=['GET'])
def api_commodity_all():
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    pagination, offset = models.set_pagination(limit, offset, Commodity)
    total_num = pagination.pages
    commodity = pagination.items
    for i in commodity:
        i.price = str(i.price)
    result = commoditys_schema.dump(commodity)
    return jsonify({'data': result.data, 'total_page': total_num, 'offset': offset})


@commodity.route('/commodity/<int:commodity_id>', methods=['GET'])
def api_get_by_id(commodity_id):
    commodity = db.session.query(Commodity).get(commodity_id)
    if commodity is None:
        abort(404)
    return commodity_schema.jsonify(commodity)


@commodity.route('/commodity', methods=['POST'])
@valid_token()
@models.validate_json
@models.validate_schema(commodity_schema)
def api_commodity_add():
    req = request.get_json()
    insert = Commodity(title=req['title'], cover_url=req['cover_url'], price=req['price'], summary=req['summary'],
                       buy_url=req['buy_url'], create_time=datetime.datetime.now())
    db.session.add(insert)
    db.session.commit()
    commoditys = json.loads(api_commodity_all().data)
    return jsonify({'success': True, 'data': commoditys['data']})


@commodity.route('/commodity/<int:commodity_id>', methods=['DELETE'])
@valid_token()
def api_delete_commodity(commodity_id):
    commodity = db.session.query(Commodity).get(commodity_id)
    if commodity is None:
        abort(404)
    if request.method == 'DELETE':
        db.session.delete(commodity)
        try:
            db.session.commit()
        except Exception, e:
            abort(500)
        commoditys = json.loads(api_commodity_all().data)
        return jsonify({'success': True, 'data': commoditys['data']})


@commodity.route('/commodity/<int:commodity_id>', methods=['PUT'])
@valid_token()
@models.validate_json
@models.validate_schema(commodity_schema)
def api_commodity_by_id(commodity_id):
    if request.method == 'PUT':
        commodity = db.session.query(Commodity).get(commodity_id)
        if commodity is None:
            abort(404)
        req = request.get_json()
        for i in req.keys():
            commodity.__setattr__(i, req[i])
        try:
            db.session.add(commodity)
            db.session.commit()
        except:
            abort(500)
        return jsonify({'success': True})
