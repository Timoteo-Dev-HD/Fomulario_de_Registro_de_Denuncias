from flask import (
    Flask,
    render_template
)

from src.settings.config import Config
from src.settings.extensions import db

app = Flask(
    __name__,
    template_folder="src/views/templates",
    static_folder="src/views/static"
)
app.config.from_object(Config)

db.init_app(app=app)

# Models para importa o metadata
from src.models import Usuario_model
from src.models import Vitima_model
from src.models import Ofesor_model
from src.models import Denuncia_model

# Import Controllers

from src.controllers.admin.login_admin_controller import admin_bp
from src.controllers.users.denuncia_controller import denunia_bp


# Register Routes

app.register_blueprint(admin_bp) 
app.register_blueprint(denunia_bp)




@app.route("/", methods=["GET"])
def index():
    return render_template("indexUser.html")


if __name__ == "__main__":
    app.run(debug=True)