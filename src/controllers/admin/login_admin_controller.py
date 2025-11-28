from flask import (
    Blueprint,
    render_template
)

from src.models.Vitima_model import Vitima
from src.models.Ofesor_model import Ofesor
from src.models.Denuncia_model import Denuncia

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/", methods=["GET"])
def index_page():
    return render_template("index.html")

@admin_bp.route("/login", methods=["GET", "POST"])
def login_admin():
    return render_template("login_adm.html")