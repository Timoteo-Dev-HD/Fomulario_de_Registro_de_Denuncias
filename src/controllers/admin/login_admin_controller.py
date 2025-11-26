from flask import (
    Blueprint,
    render_template
)



admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def login_admin():
    return render_template("login_adm.html")