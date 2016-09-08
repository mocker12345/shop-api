from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cache import Cache

db = SQLAlchemy()
ma = Marshmallow()
config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': '127.0.0.1',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': '',
    'CACHE_REDIS_PASSWORD': ''
}
cache = Cache()

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@180.76.132.102/sakura'
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app,config={'CACHE_TYPE': 'redis'})
    from main.article import article
    from main.category import category
    from main.commodity import commodity
    from main.upload import upload
    from main import error
    app.register_blueprint(article)
    app.register_blueprint(category)
    app.register_blueprint(commodity)
    app.register_blueprint(upload)
    app.register_blueprint(error)
    return app
