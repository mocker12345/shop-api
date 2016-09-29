from flask_testing import TestCase as Base
from app import create_app


class TestCase(Base):
    def create_app(self):
        return create_app("testing")


