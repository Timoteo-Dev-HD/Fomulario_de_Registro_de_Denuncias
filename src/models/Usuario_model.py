from flask_login import UserMixin

from src.settings.extensions import db

class Usuario(db.Model, UserMixin):
    
    __tablename__ = "usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
    
    def __repr__(self):
        return f"User: {self.nome} - {self.email} - {self.senha}"