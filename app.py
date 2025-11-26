from flask import Flask

from src.settings.config import Config
from src.settings.extesions import db

app = Flask(
    __name__,
    template_folder="src/views/templates",
    static_folder="src/views/static"
)
app.config.from_object(Config)

db.init_app(app=app)

from src.models import *





if __name__ == "__main__":
    app.run(debug=True)