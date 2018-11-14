from sanic.response import json
from sanic.views import HTTPMethodView
from .core import restapi


@restapi.register("/")
class IndexAPI(HTTPMethodView):

    async def get(self, request):
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
        return json(result,ensure_ascii=False)


__all__ = ["IndexAPI"]
