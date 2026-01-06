from flask import (
    render_template,
    session,    
    request,
    jsonify,
    flash,
    url_for,
    redirect
)
from flask_login import (
    login_required
)

from src.controllers.admin.login_admin_controller import admin_bp


@admin_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    pass