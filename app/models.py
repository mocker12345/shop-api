import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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


class Relation(db.Model):
    __tablename__ = 'relation'

    id = Column(db.Integer, primary_key=True)
    parent = Column(db.Integer, nullable=False)
    child = Column(db.Integer, nullable=False)


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'good', 'cover_url',
                  'summary', 'category', 'create_time', 'children', 'price')


class PriceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'site_name', 'price', 'site_url')


class ChildSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'summary', 'cover_url', 'category')


class RelationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'parent', 'child')


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class CommoditySchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'cover_url', 'price', 'summary', 'buy_url')


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


if __name__ == "__main__":
    db.create_all()
