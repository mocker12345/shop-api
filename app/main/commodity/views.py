from app.models import Commodity
from . import commodity
from flask import json
from flask import jsonify
from app import db
from flask import abort
from flask import request
import app.models as models

commodity_Schema = models.CommoditySchema(many=True)


@commodity.route('/commodity', methods=['GET'])
def api_commodity_all():
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None:
        limit = 8
    else:
        try:
            limit = int(limit)
        except Exception, e:
            abort(400)
    if offset is None:
        offset = 1
    else:
        try:
            offset = int(offset)
        except Exception, e:
            abort(400)
    pagination = Commodity.query.order_by().paginate(offset, per_page=limit, error_out=False)
    total_num = pagination.pages
    commodity = pagination.items
    for i in commodity:
        i.price = str(i.price)
    # print commodity
    result = commodity_Schema.dump(commodity)
    return jsonify({'data': result.data, 'total_page': total_num, 'offset': offset})


@commodity.route('/commodity', methods=['POST'])
def api_commodity_add():
    req = request.get_json()
    insert = Commodity(title=req['title'], cover_url=req['cover_url'], price=req['price'],
                       summary=['summary'], buy_url=req['buy_url'])
    db.session.add(insert)
    try:
        db.session.commit()
    except Exception, e:
        abort(500)
    commoditys = json.loads(api_commodity_all().data)
    print (commoditys)
    return jsonify({'success': True, 'data': commoditys['data']})


@commodity.route('/commodity/<commodity_id>', methods=['PUT', 'DELETE'])
def api_commodity_by_id(commodity_id):
    try:
        int_id = int(commodity_id)
    except:
        abort(400)
    commodity = db.session.query(Commodity).get(int_id)
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
    if request.method == 'PUT':
        req = request.get_json()
        for i in req.keys():
            commodity.__setattr__(i, req[i])
        try:
            db.session.add(commodity)
            db.session.commit()
        except:
            abort(500)
        return jsonify({'success': True})
