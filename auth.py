from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def team_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You must log in to access this page.", "danger")
            return redirect(url_for("login"))
        if current_user.role.value not in ["attorney", "manager", "staff", "superuser"]:
            flash("Access denied.", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated_function