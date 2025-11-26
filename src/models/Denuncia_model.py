from src.settings.extensions import db

class Denuncia(db.Model):
    
    __tablename__ = "denuncias"
    
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(255), nullable=False)
    frequencia = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Date, nullable=False)
    testemunha = db.Column(db.String(10), nullable=False)
    descricao_do_fato = db.Column(db.Text, nullable=False)
    
    def __init__(self, categoria, frequencia, data, testemunha, descricao_do_fato):
        self.categoria = categoria
        self.frequencia = frequencia
        self.data = data
        self.testemunha = testemunha
        self.descricao_do_fato = descricao_do_fato
        
    def __repr__(self):
        return f"Denuncia: {self.id}"