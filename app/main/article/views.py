import datetime
from flask import jsonify
from flask import abort
from flask import request
import app.models as models
from app import db
from app.models import Article, Relation, Price
from . import article

article_schema = models.ArticleSchema()
articles_schema = models.ArticleSchema(many=True)
child_schema = models.ChildSchema()
relations_schema = models.RelationSchema(many=True)
relation_schema = models.RelationSchema()
prices_schema = models.PriceSchema(many=True)


@article.route('/article/<article_id>', methods=['GET', 'PUT', 'DELETE'])
def api_article_by_id(article_id):
    try:
        int_id = int(article_id)
    except:
        abort(400)
    article = Article.query.get(int_id)
    if article is None:
        abort(404)
    if request.method == 'DELETE':
        article = db.session.query(Article).get(int_id)
        price = db.session.query(Price).filter_by(article_id=int_id).all()
        relation = db.session.query(Relation).filter_by(parent=int_id).all()
        print article
        print price
        print relation
        db.session.delete(article)
        if len(price) != 0:
            for i in price:
                db.session.delete(i)
        if len(relation) != 0:
            for i in relation:
                db.session.delete(i)
        try:
            db.session.commit()
        except Exception, e:
            return e.message
        return jsonify({"success": True})
    if request.method == 'GET':
        child = relations_schema.dump(Relation.query.filter_by(parent=int_id).all())
        if len(child.data) is not 0:
            child = [child_schema.dump(Article.query.get(i['child'])).data for i in child.data]
            article.children = child
            # print article.children
            # print child
            # print(child_schema.jsonify())
            # a = Article.query.get(7)
            # a.children = []
            # a.price = []
            # article.children = [article_schema.dump(a).data]
        else:
            child = []
            article.children = child
        price = prices_schema.dump(Price.query.filter_by(article_id=int_id))
        if len(price.data) is 0:
            article.price = []
        else:
            for i in price.data:
                i['price'] = str(i['price'])
            article.price = price.data
        return article_schema.jsonify(article)
    if request.method == 'PUT':
        req = request.get_json()

        if not req:
            abort(400)
        if 'title' in req and type(req['title']) != unicode:
            abort(400)
        if 'content' in req and type(req['content']) is not unicode:
            abort(400)
        if 'cover_url' in req and type(req['cover_url']) != unicode:
            abort(400)
        old_price = db.session.query(Price).filter_by(article_id=req['id']).all()
        if old_price is not None:
            for i in old_price:
                db.session.delete(i)
            db.session.commit()

        # old_children = Relation.query.filter_by(parent=req['id']).all()
        old_children = db.session.query(Relation).filter_by(parent=req['id']).all()
        if old_children is not None:
            for i in old_children:
                db.session.delete(i)
            db.session.commit()
        if 'price' in req and len(req['price']) != 0:

            price = req['price']
            for i in price:
                price = Price(article_id=req['id'], site_url=i['site_url'],
                              site_name=i['site_name'], price=i['price'])
                db.session.add(price)
            try:
                db.session.commit()
            except Exception, e:
                return e.message
        if 'children' in req and len(req['children']) != 0:
            children = req['children']
            for i in children:
                child = Relation(parent=req['id'], child=i['id'])
                db.session.add(child)
            try:
                db.session.commit()
            except Exception, e:
                return e.message

        return jsonify({"success": True})


@article.route('/article', methods=['GET', 'POST'])
def api_articles():
    if request.method == 'GET':
        limit = request.args.get('limit')
        offset = request.args.get('offset')

        if limit is None:
            limit = 12
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
        pagination = Article.query.order_by(Article.create_time.desc()).paginate(offset, per_page=limit,
                                                                                 error_out=False)
        articles = pagination.items
        pages_num = pagination.pages
        for i in articles:
            i.price = []
            i.children = []
        result = articles_schema.dump(articles)
        return jsonify({'data': result.data, 'total_page': pages_num, 'offset': offset})
    if request.method == 'POST':
        req = request.get_json()
        if not req:
            abort(400)
        if 'title' in req and type(req['title']) != unicode:
            abort(400)
        if 'content' in req and type(req['content']) is not unicode:
            abort(400)
        if 'cover_url' in req and type(req['cover_url']) != unicode:
            abort(400)

        insert = Article(title=req['title'], content=req['content'],
                         good="0", cover_url=req['cover_url'],
                         category=req['category'],
                         create_time=datetime.datetime.now(),
                         summary=req['summary'])
        db.session.add(insert)
        try:
            db.session.commit()
            article_id = insert.id
        except Exception, e:
            return e
        if 'price' in req and len(req['price']) != 0:
            price = req['price']
            # article = Article.query.filter_by(title=req['title']).first()
            # print article
            # article_id = article.id
            for i in price:
                insert = Price(site_name=i['site_name'],
                               price=i['price'],
                               site_url=i['site_url'],
                               article_id=article_id)
                db.session.add(insert)
            try:
                db.session.commit()
            except Exception, e:
                return e.message
        if 'children' in req and len(req['children']) != 0:
            child = req['children']
            for i in child:
                insert = Relation(parent=article_id, child=i['id'])
                db.session.add(insert)
            try:
                db.session.commit()
            except Exception, e:
                return e
        return jsonify({"success": True})
