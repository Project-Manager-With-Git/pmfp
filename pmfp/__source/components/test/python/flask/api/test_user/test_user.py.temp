import sys
import json
import unittest
from pathlib import Path
try:
    from test.test_api._core import Core
except:
    path = str(
        Path(__file__).absolute().parent.parent
    )
    if path not in sys.path:
        sys.path.append(path)
    from _core import Core


class UserTest(Core):

    def test_get(self):
        rv = self.client.get('/api/user/1')
        print(rv)
        result = json.loads(rv.data)
        assert "name" in result.keys()

    def test_update(self):
        rv = self.client.put(
            '/api/user/1',
            data=json.dumps({
                "age": 30
            }),
            content_type='application/json'
        )
        rv = self.client.get('/api/user/1')
        result = json.loads(rv.data)
        age = result["age"]
        assert age == 30

    def test_delete(self):
        rv = self.client.get('/api/user/1')
        result = json.loads(rv.data)
        assert "name" in result.keys()

        rv = self.client.delete('/api/user/1')
        result = json.loads(rv.data)
        assert  result["msg"]== "删除成功"

        rv = self.client.get('/api/user/1')
        assert rv.status_code == 401
        result = json.loads(rv.data)
        assert  result["msg"]== "未找到用户"

    def test_create(self):
        rv = self.client.get('/api/user')
        result = json.loads(rv.data)
        assert result["user-count"] == 4
        rv = self.client.post(
            '/api/user',
             data=json.dumps({
                 "name":"hsz",
                "age": 12
            }),
            content_type='application/json')
        result = json.loads(rv.data)
        uid = result["uid"]
        rv = self.client.get(f'/api/user')
        result = json.loads(rv.data)
        assert result["user-count"] == 5
        rv = self.client.get(f'/api/user/{uid}')
        result = json.loads(rv.data)
        assert result["name"] == "hsz"
        assert result["age"] == 12


def user_suite():
    suite = unittest.TestSuite()
    suite.addTest(UserTest("test_get"))
    suite.addTest(UserTest("test_update"))
    suite.addTest(UserTest("test_delete"))
    suite.addTest(UserTest("test_create"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = user_suite()
    runner.run(test_suite)
