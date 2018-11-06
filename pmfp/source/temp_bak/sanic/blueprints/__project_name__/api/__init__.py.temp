from sanic import Blueprint
from .sample_source import SimpleView


apis = Blueprint('api', url_prefix='/api')
apis.add_route(SimpleView.as_view(), '/simple')
