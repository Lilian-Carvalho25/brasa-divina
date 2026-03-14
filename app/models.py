from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    cep = db.Column(db.String(20), nullable=True)
    complemento = db.Column(db.String(100), nullable=True)
