from turtle import title
from flask import Flask, Blueprint
from flask_restplus import Api

class Server():
    def __init__(self):
        self.app = Flask('auth_poc_api')
        self.blueprint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(self.blueprint, doc='/doc', title='auth_doc_backend')
        self.app.register_blueprint(self.blueprint)

        # __sqlalchemy_database_uri = 'mysql+pymysql://' + 'root' + ':' + '123' + '@' + '127.0.0.1' + ':' + '3007' + '/' + 'auth_poc_db'

        # self.app.config['SQLALCHEMY_DATABASE_URI'] = __sqlalchemy_database_uri

        self.book_name_space = self.book_name_space()

    def book_name_space(self):
        return self.api.namespace(name='Books', description='books related operation', path='/')

    def run(self):
        self.app.run(
            port=5000,
            debug=True,
            host='localhost'
        )

server = Server()