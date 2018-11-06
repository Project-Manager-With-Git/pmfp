from flask import Blueprint
from .index import index_view
from .user import (
    user_view,
    user_index_view
)

restapi = Blueprint('restapi', __name__, url_prefix='/api')
restapi.add_url_rule('/', view_func=index_view)
restapi.add_url_rule('/user', view_func=user_index_view)
restapi.add_url_rule('/user/<int:uid>', view_func=user_view)

__all__ = ["main"]
