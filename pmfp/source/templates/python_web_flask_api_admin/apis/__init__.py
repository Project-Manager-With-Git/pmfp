from flask_restplus import Api
from .namespace_ping import api as ping
from .namespace_cat import api as cat
api = Api(
    title='Test Api',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(ping, path='/api/test/ping')
api.add_namespace(cat, path='/api/test/cat')
