from src.settings.extensions import db

class Denuncia(db.Model):
    
    __tablename__ = "denuncias"
    
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(255), nullable=False)
    frequencia = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Date, nullable=False)
    testemunha = db.Column(db.String(10), nullable=False)
    nomes_testemunhas = db.Column(db.Text(), nullable=True)
    descricao_do_fato = db.Column(db.Text, nullable=False)
    
    vitima_id = db.Column(db.Integer, db.ForeignKey("vitimas.id"), nullable=False)
    ofesor_id = db.Column(db.Integer, db.ForeignKey("ofesors.id"), nullable=False)
    
    vitima = db.relationship("Vitima", back_populates="denuncias")
    ofesor = db.relationship("Ofesor", back_populates="denuncias")
    
    def __init__(self, categoria, frequencia, data, testemunha, nomes_testemunhas, descricao_do_fato):
        self.categoria = categoria
        self.frequencia = frequencia
        self.data = data
        self.testemunha = testemunha
        self.nomes_testemunhas = nomes_testemunhas
        self.descricao_do_fato = descricao_do_fato
        
    def __repr__(self):
        return f"Denuncia: {self.id}"