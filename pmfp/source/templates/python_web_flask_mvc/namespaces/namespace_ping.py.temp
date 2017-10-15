from flask_restplus import Namespace, Resource, fields

api = Namespace('ping', description='ping-pong related operations')


@api.doc('get_pong')
@api.route('/')
class Ping(Resource):
    @api.doc('get_pong')
    def get(self):
        return {'msg': 'pong'}


__all__ = ["api"]
