import json

from app.models import Article, Category
from . import category
from flask import jsonify
from app import db
from flask import request
import app.models as models

categorys_schema = models.CategorySchema(many=True)
category_schema = models.CategorySchema()


@category.route('/category/<int:category_id>', methods=['PUT'])
@models.validate_json
@models.validate_schema(category_schema)
def api_category_by_id(category_id):
    if request.method == 'PUT':
        category = db.session.query(Category).get(category_id)
        req = request.get_json()
        category.name = req['name']
        db.session.add(category)
        db.session.commit()

        result = json.loads(api_category_all().data)
        return jsonify({'success': True, 'data': result['data']})


@category.route('/category/<int:category_id>', methods=['DELETE'])
def api_delete_category(category_id):
    if request.method == 'DELETE':
        category = db.session.query(Category).get(category_id)
        db.session.delete(category)
        try:
            article = db.session.query(Article).filter_by(category=category_id).all()
            for i in article:
                i.category = 0
                db.session.add(i)
            db.session.commit()
        except Exception, e:
            return e.message
        result = json.loads(api_category_all().data)
        return jsonify({'success': True, 'data':result['data']})


@category.route('/category', methods=['GET'])
def api_category_all():
    categorys = db.session.query(Category).all()
    result = categorys_schema.dump(categorys)
    return jsonify({'data': result.data})


@category.route('/category', methods=['POST'])
@models.validate_json
@models.validate_schema(category_schema)
def api_category_add():
    if request.method == 'POST':
        req = request.get_json()
        category = Category(name=req['name'])
        db.session.add(category)
        db.session.commit()
        result = json.loads(api_category_all().data)
        return jsonify({'success': True, 'data': result['data']})
