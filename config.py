import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@180.76.132.102/sakura'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/ran1'


config = {
    'dev': DevConfig,
    'testing': TestingConfig
}
