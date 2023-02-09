from Server.instance import server
from ma import ma
from db import db

from controllers.users import Users

api = server.api
app = server.app

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Users, '/get/user')


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    server.run()

