from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.models.document import Document
from app.forms.document import DocumentForm
import os

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/')
@login_required
def index():
    Document.query.order_by(Document.uploaded_at.desc()).all()
    doc = Document.query.order_by(Document.uploaded_at.desc()).all()
    return render_template('documents/index.html', doc=doc)

@documents_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = DocumentForm()
    if form.validate_on_submit():
        # Handle file upload
        file = form.file.data
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        # Only one association allowed
        associations = [form.person_id.data, form.case_id.data, form.event_id.data]
        if sum(1 for x in associations if x) != 1:
            flash('Associate the document with exactly one of Person, Case, or Event.', 'danger')
            return render_template('documents/add.html', form=form)
        doc = Document(
            title=form.title.data,
            description=form.description.data,
            file_path=filename,
            person_id=form.person_id.data if form.person_id.data else None,
            case_id=form.case_id.data if form.case_id.data else None,
            event_id=form.event_id.data if form.event_id.data else None,
        )
        db.session.add(doc)
        db.session.commit()
        flash('Document uploaded.', 'success')
        return redirect(url_for('documents.index'))
    return render_template('documents/add.html', form=form)

@documents_bp.route('/<int:id>')
@login_required
def view(id):
    doc = Document.query.get_or_404(id)
    return render_template('documents/view.html', doc=doc)

@documents_bp.route('/<int:id>/download')
@login_required
def download(id):
    doc = Document.query.get_or_404(id)
    upload_dir = os.path.join(current_app.root_path, 'uploads')
    return send_from_directory(upload_dir, doc.file_path, as_attachment=True)

# Add edit and delete routes as needed
@documents_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    doc = Document.query.get_or_404(id)
    form = DocumentForm(obj=doc)
    if form.validate_on_submit():
        # Only one association allowed
        associations = [form.person_id.data, form.case_id.data, form.event_id.data]
        if sum(1 for x in associations if x) != 1:
            flash('Associate the document with exactly one of Person, Case, or Event.', 'danger')
            return render_template('documents/edit.html', form=form, doc=doc)
        doc.title = form.title.data
        doc.description = form.description.data
        doc.person_id = form.person_id.data if form.person_id.data else None
        doc.case_id = form.case_id.data if form.case_id.data else None
        doc.event_id = form.event_id.data if form.event_id.data else None
        # If a new file is uploaded, replace it
        if form.file.data:
            from werkzeug.utils import secure_filename
            import os
            file = form.file.data
            filename = secure_filename(file.filename)
            upload_dir = os.path.join(current_app.root_path, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            doc.file_path = filename
        db.session.commit()
        flash('Document updated!', 'success')
        return redirect(url_for('documents.view', id=doc.id))
    return render_template('documents/edit.html', form=form, doc=doc)

@documents_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    doc = Document.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(doc)
        db.session.commit()
        flash('Document deleted.', 'success')
        return redirect(url_for('documents.index'))
    return render_template('documents/delete.html', doc=doc)