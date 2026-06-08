from flask import (
    Blueprint,    
    request,
    jsonify,
    flash,
    url_for,
    redirect
)
from flask_login import (
    login_required
)


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
