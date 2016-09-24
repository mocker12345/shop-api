import urllib2

from app.models import Category
from test import TestCase
from app import db
import unittest

class test_category(TestCase):
    def test_category_get(self):
        response = urllib2.urlopen(self.get_server_url() + '/category')
        self.assertEqual(response.code, 200)
