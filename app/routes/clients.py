from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime

from app import db
from app.models.client import Client, ClientType
from app.forms.client import ClientForm, ClientSearchForm

# Create the blueprint
clients = Blueprint('clients', __name__)


@clients.route('/')
@login_required
def index():
    """Display list of clients with search and filter options"""
    search_form = ClientSearchForm(request.args)

    # Build query
    query = Client.query

    # Apply filters if provided
    if request.args.get('keywords'):
        keywords = f"%{request.args.get('keywords')}%"
        query = query.filter(or_(
            Client.name.ilike(keywords),
            Client.email.ilike(keywords),
            Client.phone.ilike(keywords),
            Client.company_name.ilike(keywords)
        ))

    if request.args.get('client_type') and request.args.get('client_type') != '':
        query = query.filter(Client.client_type == request.args.get('client_type'))

    if request.args.get('is_active') and request.args.get('is_active') != '':
        is_active = request.args.get('is_active') == '1'
        query = query.filter(Client.is_active == is_active)

    # Sort by most recently updated by default
    query = query.order_by(Client.updated_at.desc())

    # Get all clients
    clients_list = query.all()

    return render_template('clients/index.html',
                           clients=clients_list,
                           search_form=search_form,
                           now=datetime.utcnow())


@clients.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new client"""
    form = ClientForm()

    if form.validate_on_submit():
        client = Client(
            name=form.name.data,
            client_type=form.client_type.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            postal_code=form.postal_code.data,
            country=form.country.data,
            date_of_birth=form.date_of_birth.data,
            ssn_last_four=form.ssn_last_four.data,
            company_name=form.company_name.data,
            industry=form.industry.data,
            tax_id=form.tax_id.data,
            website=form.website.data,
            notes=form.notes.data,
            referral_source=form.referral_source.data,
            is_active=form.is_active.data
        )

        db.session.add(client)
        db.session.commit()

        flash(f'Client "{client.name}" has been created successfully.', 'success')
        return redirect(url_for('clients.view', id=client.id))

    return render_template('clients/create.html', form=form, now=datetime.utcnow())


@clients.route('/<int:id>')
@login_required
def view(id):
    """View a specific client"""
    client = Client.query.get_or_404(id)

    # Get active cases for this client
    from app.models.case import Case
    cases = Case.query.filter_by(client_id=client.id).order_by(Case.updated_at.desc()).all()

    return render_template('clients/view.html', client=client, cases=cases, now=datetime.utcnow())


@clients.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a client"""
    client = Client.query.get_or_404(id)
    form = ClientForm(obj=client)

    if form.validate_on_submit():
        form.populate_obj(client)
        client.updated_at = datetime.utcnow()
        db.session.commit()

        flash(f'Client "{client.name}" has been updated successfully.', 'success')
        return redirect(url_for('clients.view', id=client.id))

    return render_template('clients/edit.html', form=form, client=client, now=datetime.utcnow())


@clients.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a client"""
    client = Client.query.get_or_404(id)

    # Check if client has any cases
    if client.cases.count() > 0:
        flash(
            f'Cannot delete client "{client.name}" because they have associated cases. Please delete cases first or deactivate the client instead.',
            'danger')
        return redirect(url_for('clients.view', id=client.id))

    name = client.name
    db.session.delete(client)
    db.session.commit()

    flash(f'Client "{name}" has been deleted.', 'success')
    return redirect(url_for('clients.index'))


@clients.route('/<int:id>/toggle-status', methods=['POST'])
@login_required
def toggle_status(id):
    """Toggle active status of a client"""
    client = Client.query.get_or_404(id)
    client.is_active = not client.is_active
    status_text = "activated" if client.is_active else "deactivated"

    db.session.commit()
    flash(f'Client "{client.name}" has been {status_text}.', 'success')
    return redirect(url_for('clients.view', id=client.id))


# API endpoints for AJAX calls
@clients.route('/api/clients')
@login_required
def api_clients():
    """Return JSON list of clients for AJAX calls"""
    query = Client.query

    # Apply filters
    if request.args.get('is_active'):
        is_active = request.args.get('is_active') == 'true'
        query = query.filter(Client.is_active == is_active)

    if request.args.get('type'):
        query = query.filter(Client.client_type == request.args.get('type'))

    clients_list = [client.to_dict() for client in query.all()]
    return jsonify({'clients': clients_list})