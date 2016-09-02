from flask_testing import TestCase as Base
from app import create_app, db


class TestCase(Base):
    def create_app(self):
        app = create_app()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()
