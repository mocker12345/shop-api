import urllib2

from app.models import Category
from test import TestCase
from app import db
import unittest

class test_category(TestCase):
    # def test_add_category(self):
    #     category = Category(name='rancongjie')
    #     db.session.add(category)
    #     db.session.commit()
    #     assert category in db.session

    # def test_update_category(self):
    #     category = db.session.query(Category).get(1)
    #     category.name = '222'
    #     db.session.add(category)
    #     db.session.commit()
    #     assert category in db.session

    def test_category_view(self):
        response = urllib2.urlopen(self.get_server_url() + '/category')
        self.assertEqual(response.code, 200)
