from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    url_for,
    redirect
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from datetime import date, datetime

from src.models.Vitima_model import Vitima
from src.models.Ofesor_model import Ofesor
from src.models.Denuncia_model import Denuncia
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
        denuncias_em_analise =len(db.session.query(Denuncia).filter(Denuncia.status == "Em análise").all())
    
        print(qtd_denuncias)
        print(data_hoje)
        print(denuncias_do_dia)
        print(denuncias_em_analise)
                
        return render_template("dashboard.html",
            qtd_denuncias=qtd_denuncias,
            denuncias_em_analise=denuncias_em_analise,
            denuncias_do_dia=denuncias_do_dia                       
        )
    except Exception as e:
        return e

@admin_bp.route("/filter", methods=["POST"])
def filter_dashboard():
    pass
    # try:     
    #     data = request.form.to_dict()
    #     print(data)
        
    #     # Variaveis pegar todas as denuncias.
    #     qtd_denuncias = len(Denuncia.query.all())
        
    #     # Variaveis que pegar as denuncias de hoje.
    #     data_hoje = date.today()
    #     denuncias_do_dia = db.session.query(Denuncia).filter(Denuncia.data_public == data_hoje).all()
        
    #     # Variavel que pegar casos que estão em anaálise.
    #     denuncias_em_analise = db.session.query(Denuncia).filter(Denuncia.status == data["status"]).all()
        
        
            
    #     return render_template("dashboard.html",
    #         qtd_denuncias=qtd_denuncias,
    #         denuncias_em_analise=denuncias_em_analise,
    #         denuncias_do_dia=denuncias_do_dia                       
    #     )
    # except Exception as e:
    #     return e
    