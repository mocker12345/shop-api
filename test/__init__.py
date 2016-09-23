import urllib2

from flask_testing import LiveServerTestCase
from app import create_app, db
from app.models import Category


class TestCase(LiveServerTestCase):
    def create_app(self):
        return create_app("testing")
