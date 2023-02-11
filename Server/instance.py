from turtle import title
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restplus import Api

class Server():
    def __init__(self):
        self.app = Flask('auth_poc_api')
        CORS(self.app, origins='*')
        self.blueprint = Blueprint('api', __name__, url_prefix='/api')
        self.api = Api(self.blueprint, doc='/doc', title='auth_doc_backend')
        self.app.register_blueprint(self.blueprint)

    def run(self):
        self.app.run(
            port=5000,
            debug=True,
            host='localhost'
        )

server = Server()