from flask import Blueprint, render_template
from flask_login import login_required

cases_bp = Blueprint('cases_bp', __name__, template_folder='templates')

@cases_bp.route('/cases')
@login_required
def cases_list():
    # placeholder implementation - replace with your real view
    return render_template('cases_list.html', cases=[])