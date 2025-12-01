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
    
    def __init__(self, categoria, frequencia, data, testemunha, nomes_testemunhas, descricao_do_fato, vitima_id, ofesor_id):
        self.categoria = categoria
        self.frequencia = frequencia
        self.data = data
        self.testemunha = testemunha
        self.nomes_testemunhas = nomes_testemunhas
        self.descricao_do_fato = descricao_do_fato
        self.vitima_id = vitima_id
        self.ofesor_id = ofesor_id
        
    def __repr__(self):
        return f"Denuncia: {self.id}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "categoria": self.categoria,
            "frequencia": self.frequencia,
            "data": self.data.strftime("%d/%m/%Y") if self.data else None,
            "testemunha": self.testemunha,
            "nomes_testemunhas": self.nomes_testemunhas,
            "descricao_do_fato": self.descricao_do_fato,

            # --- Dados da vítima ---
            "vitima": {
                "id": self.vitima.id,
                "nome": self.vitima.nome,
                "idade": self.vitima.idade,
                "telefone": self.vitima.telefone,
                "email": self.vitima.email,
                "setor_cargo": self.vitima.setor_cargo
            } if self.vitima else None,

            # --- Dados do ofensor ---
            "ofensor": {
                "id": self.ofesor.id,
                "nome": self.ofesor.nome,
                "setor_cargo": self.ofesor.setor_cargo,
                "descricao": self.ofesor.descricao
            } if self.ofesor else None,
        }
