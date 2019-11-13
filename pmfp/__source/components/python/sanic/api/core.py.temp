from sanic import Blueprint
from sanic.views import HTTPMethodView


class APIView:
    def __init__(self, name='restapi', url_prefix="/api", app=None):
        self.restapi = Blueprint(name, url_prefix=url_prefix)
        if app:
            self.init_app(app)

    def register(self, url):
        def wrap(clz):
            if not issubclass(clz, HTTPMethodView):
                raise AttributeError("must HTTPMethodView's subclass")
            self.restapi.add_route(clz.as_view(), url)
            return clz
        return wrap

    def init_app(self, app):
        app.blueprint(self.restapi)


restapi = APIView()
__all__ = ["restapi", "APIView"]
