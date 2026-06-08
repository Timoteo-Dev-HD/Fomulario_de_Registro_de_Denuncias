from src.settings.extensions import db

class Ofesor(db.Model):
    
    __tablename__ = "ofesors"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    setor_cargo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    
    denuncias = db.relationship("Denuncia", back_populates="ofesor")
    
    def __init__(self, nome, setor_cargo, descricao):
        self.nome = nome
        self.setor_cargo = setor_cargo
        self.descricao = descricao
        
    def __repr__(self):
        return f"Ofesor: {self.nome}"