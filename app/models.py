from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    cep = db.Column(db.String(20), nullable=True)
    complemento = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)


class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nome_usuario = db.Column(db.String(100), nullable=False)
    produtos = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), nullable=False, default='realizado')
    data_criacao = db.Column(db.DateTime, nullable=False)
