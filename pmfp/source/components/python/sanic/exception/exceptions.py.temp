from sanic.response import json
from sanic.exceptions import NotFound, ServerError
from .method import excep


@excep.register(NotFound)
async def ignore_404s(request, exception):
    return json({"msg": "source not found"}, status=404)


@excep.register(ServerError)
async def ignore_500s(request, exception):
    return json({"msg": "unknown server error"}, status=500)


__all__ = ["ignore_404s", "ignore_500s"]
