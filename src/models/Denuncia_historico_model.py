from datetime import datetime

from src.settings.extensions import db


class DenunciaHistorico(db.Model):

    __tablename__ = "denuncias_historico"

    id = db.Column(db.Integer, primary_key=True)
    denuncia_id = db.Column(db.Integer, db.ForeignKey("denuncias.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    campo = db.Column(db.String(80), nullable=False)
    valor_anterior = db.Column(db.Text, nullable=True)
    valor_novo = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    denuncia = db.relationship("Denuncia", back_populates="historicos")
    usuario = db.relationship("Usuario")

    def __init__(self, denuncia_id, usuario_id, campo, valor_anterior, valor_novo):
        self.denuncia_id = denuncia_id
        self.usuario_id = usuario_id
        self.campo = campo
        self.valor_anterior = valor_anterior
        self.valor_novo = valor_novo

    def __repr__(self):
        return f"Historico Denuncia: {self.denuncia_id} - {self.campo}"
