from src.settings.extensions import db

class Vitima(db.Model):
    
    __tablename__ = "vitimas"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    setor_cargo = db.Column(db.String(255), nullable=False)
    genero = db.Column(db.String(25), nullable=False)
    
    denuncias = db.relationship("Denuncia", back_populates="vitima")
    
    def __init__(self, nome, matricula, idade, telefone, email, setor_cargo, genero):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone
        self.email = email
        self.setor_cargo = setor_cargo
        self.genero = genero
        
    def __repr__(self):
        return f"Vitima: {self.nome}"