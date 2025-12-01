from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from src.models.Vitima_model import Vitima
from src.models.Ofesor_model import Ofesor
from src.models.Denuncia_model import Denuncia

from src.settings.extensions import db

from src.utils.utils import validar_telefone, validar_email

denunia_bp = Blueprint("denuncias", __name__, url_prefix="/denuncias") 

@denunia_bp.route("/formulario", methods=["GET", "POST"])
def form_denuncia():
    if request.method == "POST":
        data = request.form.to_dict()
        
        obj_vitima = Vitima(
            nome=data.get("nome"),
            idade=data.get("idade"),
            telefone=data.get("telefone"),
            email=data.get("email"),
            setor_cargo=data.get("setor")
        )
        
        db.session.add(obj_vitima)
        
        obj_ofensor = Ofesor(
            nome=data.get("nomeOfensor"),
            setor_cargo=data.get("setorOfensor"),
            descricao=data.get("descricaoOfensor")
        )
        
        db.session.add(obj_ofensor)
        db.session.commit()
        
        obj_denuncia = Denuncia(
            categoria=data.get("tipo_situacao"),
            frequencia=data.get("frequencia"),
            data=data.get("data_ocorrencia"),
            testemunha=data.get("testemunhas"),
            nomes_testemunhas=data.get("nome_testemunhas"),
            descricao_do_fato=data.get("descricaoFatos"),
            vitima_id=obj_vitima.id,
            ofesor_id=obj_ofensor.id
        )

        db.session.add(obj_denuncia)
        db.session.commit()
        
        return render_template("success.html")

    return render_template("formulario_denuncia.html")


@denunia_bp.route("/success", methods=["GET"])
def page_success():
    return render_template("success.html")