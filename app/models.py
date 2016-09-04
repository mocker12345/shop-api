import datetime
from functools import wraps

from flask import Flask, jsonify
from flask import abort
from flask import request
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from marshmallow import ValidationError
from marshmallow import fields
from sqlalchemy import Column, Integer, Numeric, String
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.mysql import MEDIUMTEXT

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/ran1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Article(db.Model):
    __tablename__ = 'article'
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(255), nullable=False, unique=True)
    content = Column(MEDIUMTEXT, nullable=False)
    good = Column(db.Integer, nullable=False, default=0)
    cover_url = Column(db.String(255), nullable=False)
    summary = Column(db.VARCHAR(400), nullable=True, default=None)
    category = Column(db.Integer, nullable=False)
    create_time = Column(db.DATETIME, default=datetime.datetime, nullable=False)

    def __init__(self, title, content, good, cover_url, summary, category, create_time):
        self.title = title
        self.content = content
        self.good = good
        self.cover_url = cover_url
        self.summary = summary
        self.category = category
        self.create_time = create_time

    def __repr__(self):
        return '<Article %r>' % self.title

    @staticmethod
    def get_article_child(article_id):
        child = relations_schema.dump(Relation.query.filter_by(parent=article_id).all())
        child = [child_schema.dump(Article.query.get(i['child'])).data for i in child.data]
        return child

    @staticmethod
    def get_article_price(article_id):
        price = prices_schema.dump(Price.query.filter_by(article_id=article_id))
        for i in price.data:
            i['price'] = str(i['price'])
        return price


class Relation(db.Model):
    __tablename__ = 'relation'

    id = Column(db.Integer, primary_key=True)
    parent = Column(db.Integer, nullable=False)
    child = Column(db.Integer, nullable=False)


class ChildSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'summary', 'cover_url', 'category')


class PriceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'site_name', 'price', 'site_url')


class ArticleSchema(ma.Schema):
    def must_not_be_blank(data):
        if not data:
            raise ValidationError('data not allow blank')

    id = fields.Int(dump_only=True)
    title = fields.Str(validate=must_not_be_blank, required=True)
    content = fields.Str(validate=must_not_be_blank, required=True)
    cover_url = fields.Str(validate=must_not_be_blank, required=True)
    category = fields.Int(required=True)
    summary = fields.Str(validate=must_not_be_blank,required=True)

    class Meta:
        fields = ('id', 'title', 'content', 'good', 'cover_url',
                  'summary', 'category', 'create_time', 'children', 'price')


prices_schema = PriceSchema(many=True)

child_schema = ChildSchema()


class RelationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'parent', 'child')


relations_schema = RelationSchema(many=True)


class CategorySchema(ma.Schema):
    def must_not_be_blank(data):
        if not data:
            raise ValidationError('data not allow blank')

    name = fields.Str(validate=must_not_be_blank, required=True)
    id = fields.Int(dump_only=True)

    class Meta:
        type_ = 'categorys'


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name



class CommoditySchema(ma.Schema):
    def must_not_be_blank(data):
        if not data:
            raise ValidationError('data not allow blank')

    id = fields.Int(dump_only=True)
    title = fields.Str(validate=must_not_be_blank, required=True)
    cover_url = fields.Str(validate=must_not_be_blank, required=True)
    price = fields.Number(validate=must_not_be_blank, required=True)
    summary = fields.Str(required=False)
    buy_url = fields.Str(validate=must_not_be_blank, required=True)

    class Meta:
        type_ = 'commoditys'


class Commodity(db.Model):
    __tablename__ = 'commodity'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    cover_url = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    summary = Column(String(255), nullable=True, default=None)
    buy_url = Column(String(255), nullable=False)

    def __init__(self, title, cover_url, price, summary, buy_url):
        self.title = title
        self.cover_url = cover_url
        self.price = price
        self.summary = summary
        self.buy_url = buy_url

    def __repr__(self):
        return '<Commodity %r>' % self.title


class Price(db.Model):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    site_name = Column(String(255))
    price = Column(Numeric(10, 2))
    site_url = Column(String(255))
    article_id = Column(Integer)

    def __init__(self, site_name, price, site_url, article_id):
        self.site_name = site_name
        self.site_url = site_url
        self.article_id = article_id
        self.price = price

    def __repr__(self):
        return '<Price %r>' % self.price


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        if request.get_json() is None:
            msg = "must be a valid json"
            return jsonify({'code':400,"error": msg}), 400
        return f(*args, **kw)

    return wrapper


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            data, errors = schema.load(request.get_json())
            if errors:
                return jsonify({'code': 400, 'errors': errors}), 400
            return f(*args, **kw)

        return wrapper

    return decorator


def set_pagination(limit, offset, schema):
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
    pagination = schema.query.order_by().paginate(offset, per_page=limit, error_out=False)
    return pagination, offset


if __name__ == "__main__":
    db.create_all()
