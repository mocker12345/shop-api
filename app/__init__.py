from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models import db
from models import ma
from models import app

def create_app():

    # app = Flask(__name__)
    # # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@180.76.132.102/sakura'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/ran1'
    db.init_app(app)
    ma.init_app(app)
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
