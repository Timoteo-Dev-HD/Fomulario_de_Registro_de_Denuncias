from flask import Blueprint, Response
from flask_login import login_required
from src.models.Denuncia_model import Denuncia

import csv, io

exportar_bp = Blueprint("export", __name__, url_prefix="/export")

@exportar_bp.route("/exportar/csv")
@login_required
def exportar_csv():
    denuncias = Denuncia.query.order_by(Denuncia.data.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeçalho
    writer.writerow(["ID", "Categoria", "Data", "Status", "Severidade",
                     "Vítima", "Ofensor", "Descrição"])
    
    # Dados
    for d in denuncias:
        writer.writerow([
            d.id, d.categoria, d.data, d.status, d.severidade,
            d.vitima.nome, d.ofesor.nome, d.descricao_do_fato
        ])
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=denuncias.csv"}
    )
    
@exportar_bp.route("/exportar/excel", methods=["GET"])
def exportar_excel():
    ...