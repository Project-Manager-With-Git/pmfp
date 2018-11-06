from sanic.views import HTTPMethodView
from sanic.response import json


class SimpleView(HTTPMethodView):

    def get(self, request):
        return json({"message": 'I am get method'})

    def post(self, request):
        return json({"message": 'I am post method'})

    def put(self, request):
        return json({"message": 'I am put method'})

    def patch(self, request):
        return json({"message": 'I am patch method'})

    def delete(self, request):
        return json({"message": 'I am delete method'})
