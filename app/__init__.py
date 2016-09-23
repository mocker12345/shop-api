from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import config

# from models import db
# from models import ma
# from models import app

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/ran1'
    db.init_app(app)
    ma.init_app(app)
    from main.article import article
    from main.category import category
    from main.commodity import commodity
    from main.upload import upload
    from main import error
    from main.login import land
    app.register_blueprint(land)
    app.register_blueprint(article)
    app.register_blueprint(category)
    app.register_blueprint(commodity)
    app.register_blueprint(upload)
    app.register_blueprint(error)
    return app
