from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    url_for,
    redirect
)

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
        data = request.form.to_dict()
        
        email_user = data["email"]
        senha_user = data["password"]
        
        user_obj = db.session.query(Usuario).filter(Usuario.email == email_user and Usuario.senha == senha_user).first()
        
        if not user_obj:
            flash("Usuário não existe no sistema...", "error")
            return render_template("login_adm.html")

        session["nomeUser"] = user_obj.nome
        session["emailUser"] = user_obj.email
        session["senhaUser"] = user_obj.senha
                
        return redirect(url_for("admin.index_page"))

    
    return render_template("login_adm.html")

@admin_bp.route("/logout", methods=["GET"])
def logout():
    pass

# ============== Painel ADM ====================

@admin_bp.route('/painel', methods=['GET', 'POST'])
def painel():
    denuncias = (
        db.session.query(Denuncia)
        .order_by(Denuncia.data.desc())
        .all()
    )
    denuncias_dict = [d.to_dict() for d in denuncias]
    return render_template("painel_denuncias.html", denuncias=denuncias_dict)
