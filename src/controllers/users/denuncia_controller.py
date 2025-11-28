from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)


denunia_bp = Blueprint("denuncias", __name__, url_prefix="/denuncias")

@denunia_bp.route("/", methods=["GET", "POST"])
def form_denuncia():
    if request.method == "POST":
        data = request.form.to_dict()
        
        print(data)
        
        return render_template("success.html")

    return render_template("formulario_denuncia.html")


@denunia_bp.route("/success", methods=["GET"])
def page_success():
    return render_template("success.html")