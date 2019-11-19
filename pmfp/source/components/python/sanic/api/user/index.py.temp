from sanic.response import json
from sanic.views import HTTPMethodView

from model import get_table
from data_schema import get_schema
from ..core import restapi


User = get_table("User")
User_Schema = get_schema("user")


@restapi.register("/user")
class UserIndexAPI(HTTPMethodView):

    async def get(self, request):
        count_query = User.select()
        count = await request.app.db_manager.count(count_query)
        result = {
            "description": "测试api,User总览",
            "user-count": count,
            "links": [
                {
                    "uri": "/user",
                    "method": "POST",
                    "description": "创建一个新用户"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "GET",
                    "description": "用户号为<id>的用户信息"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "PUT",
                    "description": "更新用户号为<id>用户信息"
                },
                {
                    "uri": "/user/<int:uid>",
                    "method": "DELETE",
                    "description": "删除用户号为<id>用户"
                },
            ]
        }

        return json(result,ensure_ascii=False)

    async def post(self, request):
        insert = request.json
        try:
            User_Schema(insert)
        except Exception as e:
            return json({
                "msg": "参数错误",
                "error": str(e)
            },ensure_ascii=False), 401
        else:
            uid = await request.app.db_manager.create(User,**insert)
            return json({
                "msg": "插入成功",
                "uid": uid
            },ensure_ascii=False)


__all__ = ["UserIndexAPI"]
