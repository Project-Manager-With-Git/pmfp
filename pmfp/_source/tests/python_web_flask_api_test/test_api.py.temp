import json
import unittest
from test.get_app import app


def setUpModule():
    print("setUpModule")


def tearDownModule():
    print("tearUpModule")


class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_ping(self):
        rv = self.client.get('/api/test/ping/')
        self.assertEqual(json.loads(rv.data)["msg"], 'pong')

    def test_catlist(self):
        rv = self.client.get('/api/test/cat/')
        self.assertListEqual(json.loads(rv.data), [
            {
                "id": "1",
                "name": "hello"
            },
            {
                "id": "2",
                "name": "kitty"
            }
        ])

    def test_cat(self):
        rv = self.client.get('/api/test/cat/1')
        self.assertDictEqual(json.loads(rv.data),
                             {
            "id": "1",
            "name": "hello"
        })


def add_suite():
    suite = unittest.TestSuite()
    suite.addTest(ApiTest("test_ping"))
    suite.addTest(ApiTest("test_cat"))
    suite.addTest(ApiTest("test_catlist"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = add_suite()
    runner.run(test_suite)
