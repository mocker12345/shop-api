from app.models import Article, Category
from . import category
from flask import json
from flask import jsonify
from app import db
from flask import abort
from flask import request
import app.models as models

category_schema = models.CategorySchema(many=True)


@category.route('/category/<category_id>', methods=['PUT', 'DELETE'])
def api_category_by_id(category_id):
    try:
        int_id = int(category_id)
    except:
        abort(400)
    category = db.session.query(Category).get(int_id)
    if category is None:
        abort(404)
    if request.method == 'DELETE':
        db.session.delete(category)
        try:
            article = db.session.query(Article).filter_by(category=int_id).all()
            for i in article:
                i.category = 0
                db.session.add(i)
            db.session.commit()
        except Exception, e:
            return e.message
        return jsonify({'success': True})
    if request.method == 'PUT':
        req = request.get_json()
        category.name = req['name']
        try:
            db.session.add(category)
            db.session.commit()
        except Exception, e:
            return e.message
        return jsonify({'success': True})


@category.route('/category', methods=['GET'])
def api_category_all():
    categorys = db.session.query(Category).all()
    result = category_schema.dump(categorys)
    print result.data
    return jsonify({'data': result.data})


@category.route('/category', methods=['POST'])
def api_category_add():
    if request.method == 'POST':
        req = request.get_json()
        category = Category(name=req['name'])
        db.session.add(category)
        db.session.commit()
        result = json.loads(api_category_all().data)
        return jsonify({'success': True, 'data': result['data']})
