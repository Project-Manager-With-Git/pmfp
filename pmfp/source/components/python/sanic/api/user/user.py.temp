from sanic.response import json
from sanic.views import HTTPMethodView
from model import get_table
from data_schema import get_schema
from ..core import restapi
User = get_table("User")
User_Schema = get_schema("user")


@restapi.register('/user/<uid:int>')
class UserAPI(HTTPMethodView):

    async def get(self, request, uid):
        try:
            u = await request.app.db_manager.get(User, id=uid)
        except User.DoesNotExist as dn:
            return json({
                "msg": "未找到用户",
            }, status=401, ensure_ascii=False)

        except Exception as e:
            return json({
                "msg": "执行错误",
            }, status=500, ensure_ascii=False)
        else:
            if u:
                return json(u.to_dict(), ensure_ascii=False)
            else:
                return json({
                    "msg": "未找到用户",
                }, status=401, ensure_ascii=False)

    async def put(self, request, uid):
        try:
            u = await request.app.db_manager.get(User, id=uid)
        except User.DoesNotExist as dn:
            return json({
                "msg": "未找到用户",
            }, status=401, ensure_ascii=False)

        except Exception as e:
            return json({
                "msg": "执行错误",
            }, status=500, ensure_ascii=False)
        else:
            if not u:
                return json({
                    "msg": "未找到用户",
                }, status=401, ensure_ascii=False)
            insert = request.json
            u_dict = u.to_dict()
            for k, v in insert.items():
                try:
                    if v != u_dict[k]:
                        setattr(u, k, v)
                except Exception as e:
                    return json({
                        "msg": "参数错误",
                        "error": str(e)
                    }, status=401, ensure_ascii=False)
                await request.app.db_manager.update(u)
                return json({
                    "msg": "更新成功"
                }, ensure_ascii=False)

    async def delete(self, request, uid):
        try:
            u = await request.app.db_manager.get(User, id=uid)
        except User.DoesNotExist as dn:
            return json({
                "msg": "未找到用户",
            }, status=401, ensure_ascii=False)

        except Exception as e:
            return json({
                "msg": "执行错误",
                "error": str(type(e))
            }, status=500, ensure_ascii=False)
        else:
            if not u:
                return json({
                    "msg": "未找到用户",
                }, status=401, ensure_ascii=False)
            await request.app.db_manager.delete(u)
            return json({
                "msg": "删除成功",
            }, ensure_ascii=False)


__all__ = ["UserAPI"]
