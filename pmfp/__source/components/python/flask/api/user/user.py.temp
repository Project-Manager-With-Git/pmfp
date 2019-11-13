from flask import jsonify, current_app, request
from flask.views import MethodView
from model import get_table
from data_schema import get_schema
User = get_table("User")
User_Schema = get_schema("user")


class UserAPI(MethodView):

    def get(self, uid):
        try:
            u = User.get(User.id == uid)
        except User.DoesNotExist as dn:
            return jsonify({
                "msg": "未找到用户",
            }), 401

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }), 500
        else:
            return jsonify(u.to_dict())

    def put(self, uid):
        try:
            u = User.get(User.id == uid)
        except User.DoesNotExist as dn:
            return jsonify({
                "msg": "未找到用户",
            }), 401

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }), 500
        else:
            insert = request.json
            u_dict = u.to_dict()
            for k, v in insert.items():
                try:
                    if v != u_dict[k]:
                        setattr(u, k, v)
                except Exception as e:
                    return jsonify({
                        "msg": "参数错误",
                        "error": str(e)
                    }), 401
                u.save()
                return jsonify({
                    "msg": "更新成功"
                })

    def delete(self, uid):
        try:
            u = User.get(User.id == uid)
        except User.DoesNotExist as dn:
            return jsonify({
                "msg": "未找到用户",
            }), 401

        except Exception as e:
            return jsonify({
                "msg": "执行错误",
            }), 500
        else:
            u.delete_instance()
            return jsonify({
                "msg": "删除成功",
            })


user_view = UserAPI.as_view('user_api')

__all__ = ["user_view"]
