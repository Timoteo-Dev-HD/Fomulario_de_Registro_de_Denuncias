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
    current_app,
    send_from_directory,
    abort
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from datetime import date, datetime
from sqlalchemy import extract, or_
    
import csv
import io
import os

from src.models.Vitima_model import Vitima
from src.models.Ofensor_model import Ofesor
from src.models.Denuncia_model import Denuncia, StatusEnum
from src.models.Denuncia_anexos_model import DenunciaAnexos
from src.models.Denuncia_historico_model import DenunciaHistorico
from src.models.Usuario_model import Usuario

from src.settings.extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

PAINEL_DEFAULT_PER_PAGE = 10
PAINEL_MAX_PER_PAGE = 50
PRAZO_PENDENTE_DIAS = 7

STATUS_OPTIONS = [
    ("", "Todos"),
    (StatusEnum.PENDENTE.value, "Pendente"),
    (StatusEnum.EM_ANALISE.value, "Em análise"),
    (StatusEnum.SUSPENSO.value, "Suspenso"),
    (StatusEnum.FINALIZADO.value, "Finalizado"),
]

SORT_OPTIONS = [
    ("recentes", "Mais recentes"),
    ("antigas", "Mais antigas"),
    ("status", "Status"),
    ("categoria", "Categoria"),
]


def _parse_date(value):
    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _safe_export_value(value):
    text = "" if value is None else str(value)

    if text.startswith(("=", "+", "-", "@")):
        return f"'{text}"

    return text


def _get_painel_filters():
    per_page = request.args.get("per_page", PAINEL_DEFAULT_PER_PAGE, type=int)
    per_page = min(max(per_page, 5), PAINEL_MAX_PER_PAGE)

    return {
        "q": (request.args.get("q") or "").strip(),
        "status": request.args.get("status") or "",
        "evidencias": request.args.get("evidencias") or "",
        "data_inicio": request.args.get("data_inicio") or "",
        "data_fim": request.args.get("data_fim") or "",
        "sort": request.args.get("sort") or "recentes",
        "per_page": per_page,
    }


def _apply_painel_filters(query, filtros):
    search = filtros["q"]
    status = filtros["status"]
    evidencias = filtros["evidencias"]
    data_inicio = _parse_date(filtros["data_inicio"])
    data_fim = _parse_date(filtros["data_fim"])

    if search:
        term = f"%{search}%"
        query = query.filter(or_(
            Denuncia.categoria.ilike(term),
            Denuncia.descricao_do_fato.ilike(term),
            Vitima.nome.ilike(term),
            Ofesor.nome.ilike(term),
        ))

    if status in [item.value for item in StatusEnum]:
        query = query.filter(Denuncia.status == status)

    if evidencias == "com":
        query = query.filter(Denuncia.anexos.any())
    elif evidencias == "sem":
        query = query.filter(~Denuncia.anexos.any())

    if data_inicio:
        query = query.filter(Denuncia.data >= data_inicio)

    if data_fim:
        query = query.filter(Denuncia.data <= data_fim)

    return query


def _apply_painel_sort(query, sort):
    if sort == "antigas":
        return query.order_by(Denuncia.data_public.asc(), Denuncia.id.asc())

    if sort == "status":
        return query.order_by(Denuncia.status.asc(), Denuncia.data_public.desc(), Denuncia.id.desc())

    if sort == "categoria":
        return query.order_by(Denuncia.categoria.asc(), Denuncia.data_public.desc(), Denuncia.id.desc())

    return query.order_by(Denuncia.data_public.desc(), Denuncia.id.desc())


def _build_page_url(page, query_params):
    params = query_params.copy()
    params["page"] = page
    return url_for("admin.painel", **params)


def _build_page_links(pagination, query_params):
    links = []

    for page in pagination.iter_pages(left_edge=1, left_current=2, right_current=2, right_edge=1):
        if page is None:
            links.append({"page": None, "url": None, "active": False})
        else:
            links.append({
                "page": page,
                "url": _build_page_url(page, query_params),
                "active": page == pagination.page,
            })

    return links


def _painel_query_params(filtros):
    query_params = {}

    for key, value in filtros.items():
        if key == "per_page" and value == PAINEL_DEFAULT_PER_PAGE:
            continue

        if value not in (None, ""):
            query_params[key] = value

    return query_params


def _painel_summary():
    return {
        "total": Denuncia.query.count(),
        "pendentes": Denuncia.query.filter(Denuncia.status == StatusEnum.PENDENTE.value).count(),
        "em_analise": Denuncia.query.filter(Denuncia.status == StatusEnum.EM_ANALISE.value).count(),
        "finalizadas": Denuncia.query.filter(Denuncia.status == StatusEnum.FINALIZADO.value).count(),
    }


def _record_change(denuncia, campo, old_value, new_value):
    old_text = "" if old_value is None else str(old_value)
    new_text = "" if new_value is None else str(new_value)

    if old_text == new_text:
        return

    user_id = int(current_user.get_id()) if current_user and current_user.get_id() else None

    db.session.add(DenunciaHistorico(
        denuncia_id=denuncia.id,
        usuario_id=user_id,
        campo=campo,
        valor_anterior=old_text,
        valor_novo=new_text
    ))


@admin_bp.route("/", methods=["GET"])
def index_page():
    return render_template("index.html")

@admin_bp.route("/login", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        senha = request.form.get("password") or ""

        user_obj = (
            db.session.query(Usuario)
            .filter_by(email=email)
            .first()
        )

        if not user_obj:
            flash("Usuário ou senha inválidos", "error")
            return render_template("login_adm.html")

        if user_obj.is_legacy_password(senha):
            user_obj.set_password(senha)
            db.session.commit()
        elif not user_obj.check_password(senha):
            flash("Usuário ou senha inválidos", "error")
            return render_template("login_adm.html")

        login_user(user_obj)
                
        return redirect(url_for("admin.index_page"))

    
    return render_template("login_adm.html")

@admin_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login_admin"))

# ============== Painel ADM ====================

@admin_bp.route('/painel', methods=['GET'])
@login_required
def painel():
    page = request.args.get("page", 1, type=int)
    filtros = _get_painel_filters()
    query_params = _painel_query_params(filtros)

    query = (
        Denuncia.query
        .join(Vitima, Denuncia.vitima_id == Vitima.id)
        .join(Ofesor, Denuncia.ofesor_id == Ofesor.id)
    )
    query = _apply_painel_filters(query, filtros)
    query = _apply_painel_sort(query, filtros["sort"])

    pagination = query.paginate(
        page=max(page, 1),
        per_page=filtros["per_page"],
        error_out=False
    )
    denuncias_dict = [d.to_dict() for d in pagination.items]

    return render_template(
        "painel_denuncias.html",
        denuncias=denuncias_dict,
        pagination=pagination,
        page_links=_build_page_links(pagination, query_params),
        previous_url=_build_page_url(pagination.prev_num, query_params) if pagination.has_prev else None,
        next_url=_build_page_url(pagination.next_num, query_params) if pagination.has_next else None,
        filtros=filtros,
        resumo=_painel_summary(),
        total_filtrado=pagination.total,
        status_options=STATUS_OPTIONS,
        sort_options=SORT_OPTIONS,
        prazo_pendente_dias=PRAZO_PENDENTE_DIAS,
    )


@admin_bp.route("/anexos/<int:anexo_id>", methods=["GET"])
@login_required
def visualizar_anexo(anexo_id):
    anexo = DenunciaAnexos.query.get_or_404(anexo_id)
    filename = os.path.basename(anexo.file_path)

    if not filename:
        abort(404)

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=False,
        download_name=anexo.original_name
    )




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

    data = request.get_json(silent=True) or {}

    status = data.get("status") or denuncia.status

    status_permitidos = [item.value for item in StatusEnum]

    if status not in status_permitidos:
        return jsonify({
            "sucesso": False,
            "mensagem": "Status inválido."
        }), 400

    responsavel = (data.get("responsavel") or "").strip() or None

    campos = {
        "Status": ("status", status),
        "Responsável": ("responsavel", responsavel),
        "Depoimento da vítima": ("depoimento_vitima", data.get("depoimento_vitima")),
        "Depoimento do acusado": ("depoimento_acusado", data.get("depoimento_acusado")),
        "Depoimento das testemunhas": ("depoimento_testemunha", data.get("depoimento_testemunha")),
        "Observações da administração": ("depoimento_admin", data.get("depoimento_admin")),
    }

    for label, (attr, new_value) in campos.items():
        old_value = getattr(denuncia, attr)
        _record_change(denuncia, label, old_value, new_value)
        setattr(denuncia, attr, new_value)

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
    

@admin_bp.route("/denuncia/<int:id>/exportar/csv")
@login_required
def exportar_denuncia_csv(id):
    denuncia = Denuncia.query.get_or_404(id)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Categoria", "Data", "Status", "Severidade", "Responsável",
        "Vítima", "Telefone", "Email", "Ofensor", "Descrição"
    ])
    writer.writerow([
        _safe_export_value(denuncia.id),
        _safe_export_value(denuncia.categoria),
        _safe_export_value(denuncia.data),
        _safe_export_value(denuncia.status),
        _safe_export_value(denuncia.severidade),
        _safe_export_value(denuncia.responsavel),
        _safe_export_value(denuncia.vitima.nome if denuncia.vitima else ""),
        _safe_export_value(denuncia.vitima.telefone if denuncia.vitima else ""),
        _safe_export_value(denuncia.vitima.email if denuncia.vitima else ""),
        _safe_export_value(denuncia.ofesor.nome if denuncia.ofesor else ""),
        _safe_export_value(denuncia.descricao_do_fato),
    ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=denuncia_{denuncia.id}.csv"}
    )


@admin_bp.route("/exportar/csv")
@login_required
def exportar_csv():
    denuncias = Denuncia.query.order_by(Denuncia.data.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Categoria", "Data", "Status", "Severidade",
                     "Responsável", "Vítima", "Ofensor", "Descrição"])
    for d in denuncias:
        writer.writerow([
            _safe_export_value(d.id),
            _safe_export_value(d.categoria),
            _safe_export_value(d.data),
            _safe_export_value(d.status),
            _safe_export_value(d.severidade),
            _safe_export_value(d.responsavel),
            _safe_export_value(d.vitima.nome if d.vitima else ""),
            _safe_export_value(d.ofesor.nome if d.ofesor else ""),
            _safe_export_value(d.descricao_do_fato)
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
               "Responsável", "Vítima", "Ofensor", "Descrição"]
    ws.append(headers)

    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    for d in Denuncia.query.order_by(Denuncia.data.desc()).all():
        ws.append([
            _safe_export_value(d.id),
            _safe_export_value(d.categoria),
            _safe_export_value(str(d.data) if d.data else ""),
            _safe_export_value(d.status),
            _safe_export_value(d.severidade),
            _safe_export_value(d.responsavel),
            _safe_export_value(d.vitima.nome if d.vitima else ""),
            _safe_export_value(d.ofesor.nome if d.ofesor else ""),
            _safe_export_value(d.descricao_do_fato)
        ])

    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 12
    ws.column_dimensions["D"].width = 12
    ws.column_dimensions["E"].width = 10
    ws.column_dimensions["F"].width = 22
    ws.column_dimensions["G"].width = 22
    ws.column_dimensions["H"].width = 22
    ws.column_dimensions["I"].width = 40

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return Response(
        output.read(),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=denuncias.xlsx"}
    )
