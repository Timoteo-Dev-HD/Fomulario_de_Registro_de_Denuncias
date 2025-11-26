from flask import Flask

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

# Routes do Controllers



if __name__ == "__main__":
    app.run(debug=True)