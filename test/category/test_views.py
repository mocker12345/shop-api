from test import TestCase
from app.models import Category, db


class test_category(TestCase):
    def test_add_category(self):
        category = Category(name='666')
        db.session.add(category)
        db.session.commit()
        assert category in db.session

    def test_update_category(self):
        category = db.session.query(Category).get(5)
        category.name = '222'
        db.session.add(category)
        db.session.commit()
        assert category in db.session
