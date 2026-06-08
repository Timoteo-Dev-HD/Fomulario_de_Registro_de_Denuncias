from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    url_for,
    redirect,
    jsonify,
    Response,
    current_app
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from datetime import date, datetime
from sqlalchemy import extract
    
import csv
import io

from src.models.Vitima_model import Vitima
from src.models.Ofensor_model import Ofesor
from src.models.Denuncia_model import Denuncia, StatusEnum
from src.models.Usuario_model import Usuario

from src.settings.extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/", methods=["GET"])
def index_page():
    return render_template("index.html")

@admin_bp.route("/login", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        #data = request.form.to_dict()
        
        email = request.form.get("email")
        senha = request.form.get("password")

        user_obj = (
            db.session.query(Usuario)
            .filter_by(email=email, senha=senha)
            .first()
        )

        if not user_obj:
            flash("Usuário ou senha inválidos", "error")
            return render_template("login_adm.html")

        # 🔑 FLASK-LOGIN
        login_user(user_obj)
                
        return redirect(url_for("admin.index_page"))

    
    return render_template("login_adm.html")

@admin_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login_admin"))

# ============== Painel ADM ====================

@admin_bp.route('/painel', methods=['GET', 'POST'])
@login_required
def painel():
    denuncias = (
        db.session.query(Denuncia)
        .order_by(Denuncia.data.desc())
        .all()
    )
    denuncias_dict = [d.to_dict() for d in denuncias]
    return render_template("painel_denuncias.html", denuncias=denuncias_dict)




@admin_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    try:     
        # Variaveis pegar todas as denuncias.
        qtd_denuncias = len(Denuncia.query.all())
        
        # Variaveis que pegar as denuncias de hoje.
        data_hoje = date.today()
        denuncias_do_dia = len(db.session.query(Denuncia).filter(Denuncia.data_public == data_hoje).all())
        
        # Variavel que pegar casos que estão em anaálise.
        denuncias_em_analise =len(db.session.query(Denuncia).filter(Denuncia.status == StatusEnum.EM_ANALISE.value).all())
    
        # print(qtd_denuncias)
        # print(data_hoje)
        # print(denuncias_do_dia)
        # print(denuncias_em_analise)
                
        return render_template("dashboard.html",
            qtd_denuncias=qtd_denuncias,
            denuncias_em_analise=denuncias_em_analise,
            denuncias_do_dia=denuncias_do_dia,                      
        )
    except Exception as e:
        return jsonify({"error": str(e)})

@admin_bp.route("/filter", methods=["POST"])
@login_required
def filter_dashboard():
    try:
        if request.method == "POST":
            data = request.form.to_dict()
            # print(data)
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@admin_bp.route("/filter/quantidade_status", methods=["GET"])
@login_required
def quatidade_status():
    try:
        qtd_recebida = db.session.query(Denuncia).filter(Denuncia.status == StatusEnum.PENDENTE.value).count()
        qtd_em_analise = db.session.query(Denuncia).filter(Denuncia.status == StatusEnum.EM_ANALISE.value).count()
        qtd_suspenso = db.session.query(Denuncia).filter(Denuncia.status == StatusEnum.SUSPENSO.value).count()
        qtd_encerrada = db.session.query(Denuncia).filter(Denuncia.status == StatusEnum.FINALIZADO.value).count()

        return jsonify({
            "pendente": qtd_recebida,
            "em_analise": qtd_em_analise,
            "suspenso": qtd_suspenso,
            "encerrada": qtd_encerrada
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
# @admin_bp.route("/denuncia/<int:id>/finalizar", methods=["POST"])
# @login_required
# def finalizar_denuncia(id):
#     print("CHEGOU NA ROTA FINALIZAR")
#     print("ID RECEBIDO:", id)

#     denuncia = Denuncia.query.get_or_404(id)

#     print("STATUS ANTES:", denuncia.status)

#     denuncia.status = "finalizado"

#     db.session.commit()

#     print("STATUS DEPOIS:", denuncia.status)

#     return jsonify({
#         "sucesso": True,
#         "novo_status": denuncia.status
#     }), 200


@admin_bp.route("/denuncia/<int:id>/atualizar", methods=["POST"])
@login_required
def atualizar_denuncia(id):
    denuncia = Denuncia.query.get_or_404(id)

    data = request.get_json()

    status = data.get("status")

    status_permitidos = [item.value for item in StatusEnum]

    if status not in status_permitidos:
        return jsonify({
            "sucesso": False,
            "mensagem": "Status inválido."
        }), 400

    denuncia.status = status

    denuncia.depoimento_vitima = data.get("depoimento_vitima")
    denuncia.depoimento_acusado = data.get("depoimento_acusado")
    denuncia.depoimento_testemunha = data.get("depoimento_testemunha")
    denuncia.depoimento_admin = data.get("depoimento_admin")

    db.session.commit()

    return jsonify({
        "sucesso": True,
        "mensagem": "Denúncia atualizada com sucesso.",
        "novo_status": denuncia.status
    }), 200
    
    
@admin_bp.route("/meses-denuncias")
@login_required
def meses_denuncias():
    
    meses = []
    mes = None
    for i in range(1, 13):
        qtd = db.session.query(Denuncia).filter(
            extract('month', Denuncia.data_public) == i
        ).count()
        meses.append(qtd)
        
    return jsonify({
        "Jan": meses[0] or 0,
        "Fev": meses[1] or 0,
        "Mar": meses[2] or 0,
        "Abr": meses[3] or 0,
        "Mai": meses[4] or 0,
        "Jun": meses[5] or 0,
        "Jul": meses[6] or 0,
        "Ago": meses[7] or 0,
        "Set": meses[8] or 0,
        "Out": meses[9] or 0,
        "Nov": meses[10] or 0,
        "Dez": meses[11] or 0     
    })
    

@admin_bp.route("/exportar/csv")
@login_required
def exportar_csv():
    denuncias = Denuncia.query.order_by(Denuncia.data.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Categoria", "Data", "Status", "Severidade",
                     "Vítima", "Ofensor", "Descrição"])
    for d in denuncias:
        writer.writerow([
            d.id, d.categoria, d.data, d.status, d.severidade,
            d.vitima.nome, d.ofesor.nome, d.descricao_do_fato
        ])
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=denuncias.csv"}
    )

@admin_bp.route("/exportar/excel")
@login_required
def exportar_excel():
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment

    wb = Workbook()
    ws = wb.active
    ws.title = "Denúncias"

    headers = ["ID", "Categoria", "Data", "Status", "Severidade",
               "Vítima", "Ofensor", "Descrição"]
    ws.append(headers)

    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    for d in Denuncia.query.order_by(Denuncia.data.desc()).all():
        ws.append([
            d.id, d.categoria, str(d.data) if d.data else "",
            d.status, d.severidade,
            d.vitima.nome if d.vitima else "",
            d.ofesor.nome if d.ofesor else "",
            d.descricao_do_fato
        ])

    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 12
    ws.column_dimensions["D"].width = 12
    ws.column_dimensions["E"].width = 10
    ws.column_dimensions["F"].width = 22
    ws.column_dimensions["G"].width = 22
    ws.column_dimensions["H"].width = 40

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return Response(
        output.read(),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=denuncias.xlsx"}
    )