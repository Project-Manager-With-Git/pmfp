from flask_restplus import Namespace, Resource, fields
from model.peewee_models import Cat as CatModel
api = Namespace('cats', description='Cats related operations')

cat = api.model('Cat', {
    'id': fields.String(required=True, description='The cat identifier'),
    'name': fields.String(required=True, description='The cat name'),
})


@api.route('/')
class CatList(Resource):
    @api.doc('list_cats')
    @api.marshal_list_with(cat)
    def get(self):
        '''List all cats'''
        return [i.to_dict() for i in CatModel.select()]


@api.route('/<id>')
@api.param('id', 'The cat identifier')
@api.response(404, 'Cat not found')
class Cat(Resource):
    @api.doc('get_cat')
    @api.marshal_with(cat)
    def get(self, id):
        '''Fetch a cat given its identifier'''
        try:
            cat = CatModel.get(CatModel.id == int(id))
        except Exception as e:
            print(type(e))
            api.abort(404)
        else:
            return cat.to_dict()


__all__ = ["api"]
