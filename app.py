from flask import (
    Flask,
    render_template
)
from flask_login import (
    LoginManager
)

from src.settings.config import Config
from src.settings.extensions import db, csrf
import os

app = Flask(
    __name__,
    template_folder="src/views/templates",
    static_folder="src/views/static"
)
app.config.from_object(Config)

db.init_app(app=app)
csrf.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "admin.login_admin"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Models para importa o metadata
from src.models import Usuario_model
from src.models import Vitima_model
from src.models import Ofensor_model
from src.models import Denuncia_model
from src.models import Denuncia_anexos_model

# Import Controllers

from src.controllers.admin.login_admin_controller import admin_bp
from src.controllers.users.denuncia_controller import denuncia_bp


# Register Routes

app.register_blueprint(admin_bp) 
app.register_blueprint(denuncia_bp)


# Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario_model.Usuario, int(user_id))

# Main
@app.route("/", methods=["GET"])
def index():
    return render_template("indexUser.html")


if __name__ == "__main__":
    app.run(debug=True)