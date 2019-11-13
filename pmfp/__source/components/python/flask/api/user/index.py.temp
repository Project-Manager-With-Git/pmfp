from flask import jsonify, current_app, request
from flask.views import MethodView
from model import get_table
from data_schema import get_schema
User = get_table("User")
User_Schema = get_schema("user")


class UserIndexAPI(MethodView):

    def get(self):
        count = User.select().count()
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

        return jsonify(result)

    def post(self):
        insert = request.json

        try:
            User_Schema(insert)
        except Exception as e:
            return jsonify({
                "msg": "参数错误",
                "error": str(e)
            }), 401
        else:
            uid = User.insert(insert).execute()
            return jsonify({
                "msg": "插入成功",
                "uid": uid
            })


user_index_view = UserIndexAPI.as_view('user_index_api')

__all__ = ["user_index_view"]
