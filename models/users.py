from db import db

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullalble = False)
    token = db.Column(db.String, nullable = False)
    
    def __init__(self, name, token):
        self.name = name
        self.token = token