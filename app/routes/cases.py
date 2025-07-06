from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime

from app import db
from app.models.case import Case, CaseType, CaseStatus
from app.models.client import Client
from app.models.user import User
from app.forms.case import CaseForm, CaseSearchForm

# Create the blueprint
cases = Blueprint('cases', __name__)

@cases.route('/')
@login_required
def index():
    """Display list of cases with search and filter options"""
    search_form = CaseSearchForm(request.args)

    # Build query
    query = Case.query

    # Apply filters if provided
    if request.args.get('keywords'):
        keywords = f"%{request.args.get('keywords')}%"
        query = query.filter(or_(
            Case.title.ilike(keywords),
            Case.case_number.ilike(keywords),
            Case.description.ilike(keywords)
        ))

    if request.args.get('case_type') and request.args.get('case_type') != '':
        query = query.filter(Case.type == request.args.get('case_type'))

    if request.args.get('status') and request.args.get('status') != '':
        query = query.filter(Case.status == request.args.get('status'))

    # Get all cases
    cases = query.order_by(Case.created_at.desc()).all()

    return render_template('cases/index.html',
                           cases=cases,
                           search_form=search_form,
                           now=datetime.utcnow())


@cases.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new case"""
    form = CaseForm()

    # Populate select fields
    form.client_id.choices = [(c.id, c.name) for c in Client.query.order_by('name').all()]
    form.lead_attorney_id.choices = [(u.id, u.name) for u in User.query.filter(
        or_(User.role == 'attorney', User.role == 'admin')
    ).order_by('name').all()]

    if form.validate_on_submit():
        case = Case(
            title=form.title.data,
            case_number=form.case_number.data,
            type=form.type.data,
            status=form.status.data,
            description=form.description.data,
            court_name=form.court_name.data,
            judge_name=form.judge_name.data,
            opposing_counsel=form.opposing_counsel.data,
            filing_date=form.filing_date.data,
            hearing_date=form.hearing_date.data,
            hourly_rate=form.hourly_rate.data,
            retainer_amount=form.retainer_amount.data,
            client_id=form.client_id.data,
            lead_attorney_id=form.lead_attorney_id.data
        )

        db.session.add(case)
        db.session.commit()

        flash(f'Case "{case.title}" has been created successfully.', 'success')
        return redirect(url_for('cases.view', id=case.id))

    return render_template('cases/create.html', form=form, now=datetime.utcnow())


@cases.route('/<int:id>')
@login_required
def view(id):
    """View a specific case"""
    case = Case.query.get_or_404(id)
    return render_template('cases/view.html', case=case, now=datetime.utcnow())


@cases.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a case"""
    case = Case.query.get_or_404(id)
    form = CaseForm(obj=case)

    # Populate select fields
    form.client_id.choices = [(c.id, c.name) for c in Client.query.order_by('name').all()]
    form.lead_attorney_id.choices = [(u.id, u.name) for u in User.query.filter(
        or_(User.role == 'attorney', User.role == 'admin')
    ).order_by('name').all()]

    if form.validate_on_submit():
        form.populate_obj(case)
        db.session.commit()

        flash(f'Case "{case.title}" has been updated successfully.', 'success')
        return redirect(url_for('cases.view', id=case.id))

    return render_template('cases/edit.html', form=form, case=case, now=datetime.utcnow())


@cases.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a case"""
    case = Case.query.get_or_404(id)
    title = case.title

    db.session.delete(case)
    db.session.commit()

    flash(f'Case "{title}" has been deleted.', 'success')
    return redirect(url_for('cases.index'))


# API endpoints for AJAX calls
@cases.route('/api/cases')
@login_required
def api_cases():
    """Return JSON list of cases for AJAX calls"""
    query = Case.query

    # Apply filters
    if request.args.get('status'):
        query = query.filter(Case.status == request.args.get('status'))

    if request.args.get('type'):
        query = query.filter(Case.type == request.args.get('type'))

    cases_list = [case.to_dict() for case in query.all()]
    return jsonify({'cases': cases_list})