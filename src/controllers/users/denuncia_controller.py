import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from datetime import datetime

from src.models.Vitima_model import Vitima
from src.models.Ofensor_model import Ofesor
from src.models.Denuncia_model import Denuncia
from src.models.Denuncia_anexos_model import DenunciaAnexos

from src.settings.extensions import db

from src.utils.utils import allowed_file, get_file_type, generate_unique_filename

denuncia_bp = Blueprint("denuncias", __name__, url_prefix="/denuncias") 

@denuncia_bp.route("/formulario", methods=["GET", "POST"])
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
        
        
        data_hoje = datetime.today()
        
        obj_denuncia = Denuncia(
            categoria=data.get("tipo_situacao"),
            frequencia=data.get("frequencia"),
            data=data.get("data_ocorrencia"),
            testemunha=data.get("testemunhas"),
            nomes_testemunhas=data.get("nome_testemunhas"),
            descricao_do_fato=data.get("descricaoFatos"),
            vitima_id=obj_vitima.id,
            ofesor_id=obj_ofensor.id,
            data_public=data_hoje
        )

        db.session.add(obj_denuncia)
        db.session.commit()
        
        arquivos = request.files.getlist("arquivos")
        
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        
        os.makedirs(upload_folder, exist_ok=True)
        
        for arquivo in arquivos:
            if arquivo and arquivo.filename != "":
                if allowed_file(arquivo.filename, current_app.config["ALLOWED_EXTENSIONS"]):
                    original_name = arquivo.filename
                    filename = generate_unique_filename(arquivo.filename)
                    
                    file_path = os.path.join(upload_folder, filename)
                    
                    arquivo.save(file_path)
                    
                    obj_anexos = DenunciaAnexos(
                        obj_denuncia.id,
                        file_path=filename,
                        file_type=get_file_type(filename),
                        original_name=original_name   
                    )

                    db.session.add(obj_anexos)
        
        db.session.commit()

        return render_template("success.html")

    return render_template("formulario_denuncia.html")


@denuncia_bp.route("/success", methods=["GET"])
def page_success():
    return render_template("success.html")
