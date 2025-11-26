from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Case, Client, User
from forms import CaseForm

cases_bp = Blueprint('cases_bp', __name__, template_folder='templates')

@cases_bp.route('/cases')
@login_required
def cases_list():
    q = request.args.get('q', '')
    if q:
        cases = Case.query.filter(Case.style.ilike(f'%{q}%')).order_by(Case.created_at.desc()).all()
    else:
        cases = Case.query.order_by(Case.created_at.desc()).all()
    return render_template('cases_list.html', cases=cases, q=q)

@cases_bp.route('/cases/new', methods=['GET', 'POST'])
@login_required
def case_create():
    form = CaseForm()
    # populate client/user choices
    form.client_id.choices = [(c.id, c.name) for c in Client.query.order_by(Client.name).all()]
    form.user_id.choices = [(u.id, u.name) for u in User.query.order_by(User.name).all()]

    if form.validate_on_submit():
        case = Case()
        form.populate_obj(case)
        db.session.add(case)
        db.session.commit()
        flash('Case created.', 'success')
        return redirect(url_for('cases_bp.cases_list'))
    return render_template('case_form.html', form=form, case=None)

@cases_bp.route('/cases/<int:case_id>/edit', methods=['GET', 'POST'])
@login_required
def case_edit(case_id):
    case = Case.query.get_or_404(case_id)
    form = CaseForm(obj=case)
    form.client_id.choices = [(c.id, c.name) for c in Client.query.order_by(Client.name).all()]
    form.user_id.choices = [(u.id, u.name) for u in User.query.order_by(User.name).all()]

    if form.validate_on_submit():
        form.populate_obj(case)
        db.session.commit()
        flash('Case updated.', 'success')
        return redirect(url_for('cases_bp.cases_list'))
    return render_template('case_form.html', form=form, case=case)

@cases_bp.route('/cases/<int:case_id>')
@login_required
def case_detail(case_id):
    case = Case.query.get_or_404(case_id)
    return render_template('case_detail.html', case=case)