from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Root route - redirects to dashboard if logged in, otherwise to login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard route - requires authentication"""
    # Get counts for dashboard stats
    try:
        from app.models.case import Case, CaseStatus
        open_cases_count = Case.query.filter_by(status=CaseStatus.OPEN).count()
    except:
        open_cases_count = 0

    return render_template('dashboard.html',
                           now=datetime.utcnow(),
                           open_cases_count=open_cases_count)

# Remove placeholder routes and let module blueprints handle their own index routes.
# If you want, you can keep routes here that redirect to the proper module index:

@main.route('/cases')
@login_required
def cases():
    return redirect(url_for('cases.index'))

@main.route('/clients')
@login_required
def clients():
    return redirect(url_for('clients.index'))

@main.route('/calendar')
@login_required
def calendar():
    return redirect(url_for('calendar.index'))

@main.route('/documents')
@login_required
def documents():
    return redirect(url_for('documents.index'))

@main.route('/billing')
@login_required
def billing():
    return redirect(url_for('billing.index'))

@main.route('/settings')
@login_required
def settings():
    return redirect(url_for('settings.index'))