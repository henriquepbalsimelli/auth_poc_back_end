from flask import request
from flask_restplus import Resource, fields


class Users(Resource):
    def get(self, id = 1, token = 'token', name='name'):
        user = {
            'id': id,
            'token': token,
            'name': name
        }
        return user