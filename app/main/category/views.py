import json

from app.models import Article, Category
from . import category
from flask import jsonify
from flask import abort
from app import db
from flask import request
import app.models as models

categorys_schema = models.CategorySchema(many=True)
category_schema = models.CategorySchema()
articles_schema = models.ArticleSchema(many=True)


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

@category.route('/category/<int:category_id>/articles',methods=['GET'])
def api_get_articles_by_category(category_id):
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None:
        limit = 18
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
    pagination = Article.query.filter_by(category=category_id)\
        .order_by(Article.create_time.desc()).paginate(offset, per_page=limit, error_out=False)
    articles = pagination.items
    pages_num = pagination.pages
    for i in articles:
            i.price = []
            i.children = []
    result = articles_schema.dump(articles)
    return jsonify({'data': result.data, 'total_page': pages_num, 'offset': offset})