from test import TestCase


class test_category(TestCase):
    def test_category_get(self):
        response = self.client.get('/category')
        self.assertEquals(response.json, dict(success=True, data=response.json['data']))


class test_article(TestCase):
    def test_article_get(self):
        response = self.client.get('/article?limit=12&offset=1')
        self.assertEqual(response.json, dict(data=response.json['data'], offset=1, total_page=1))


class test_commodity(TestCase):
    def test_commodity(self):
        response = self.client.get('/commodity')
        self.assertEqual(response.json, dict(data=response.json['data'], offset=1, total_page=1))
