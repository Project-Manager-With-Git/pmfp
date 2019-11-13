from flask import jsonify, current_app, request
from flask.views import MethodView


class IndexAPI(MethodView):

    def get(self):
        result = {
            "description": "测试api",
            "links": [
                {
                    "uri": "/user",
                    "method": "GET",
                    "description": "用户信息总览"
                }
            ]
        }
        return jsonify(result,)


index_view = IndexAPI.as_view('index_api')

__all__ = ["index_view"]
