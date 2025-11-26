from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from datetime import datetime

from models import db, Case, Client, Document, Template
from forms import BulkGenerateForm

from flask import render_template_string

documents_bulk_bp = Blueprint('documents_bulk_bp', __name__)

# Document types we expose on the bulk-generate page (slug, label)
DOC_TYPE_CHOICES = [
    ('letter_to_client', 'Letter to Client'),
    ('letter_to_insurance', 'Letter to Insurance Company'),
    ('letter_to_opposing', 'Letter to Opposing Counsel'),
    ('general_letter', 'General Letter'),
    ('motion', 'Motion'),
    ('demand', 'Demand'),
    ('notice', 'Notice'),
    ('billing', 'Billing'),
]

# Default fallback templates (simple HTML) used if no Template by name is found
DEFAULT_TEMPLATES = {
    'letter_to_client': """<!doctype html><html><body>
<h1>Letter to Client - {{ case.style }}</h1>
<p>Client: {{ client.name if client else 'N/A' }}</p>
<p>Case Number: {{ case.case_number }}</p>
<p>Judge: {{ case.judge }}</p>
<p>Parties: {{ case.parties }}</p>
<p>Date: {{ today }}</p>
<hr>
<p>Dear {{ client.name if client else 'Client' }},</p>
<p>[Insert letter body here]</p>
</body></html>""",
    'letter_to_insurance': """<!doctype html><html><body>
<h1>Letter to Insurance Company - {{ case.style }}</h1>
<p>To: [Insurance Company]</p>
<p>Case: {{ case.case_number }} - {{ case.style }}</p>
<p>Date: {{ today }}</p>
<hr>
<p>[Insert letter body]</p>
</body></html>""",
    'letter_to_opposing': """<!doctype html><html><body>
<h1>Letter to Opposing Counsel - {{ case.style }}</h1>
<p>Opponent: {{ case.parties }}</p>
<p>Case Number: {{ case.case_number }}</p>
<hr>
<p>[Insert letter body]</p>
</body></html>""",
    'general_letter': """<!doctype html><html><body>
<h1>General Letter - {{ case.style }}</h1>
<p>Date: {{ today }}</p>
<hr>
<p>[Insert content]</p>
</body></html>""",
    'motion': """<!doctype html><html><body>
<h1>Motion - {{ case.style }}</h1>
<p>Judge: {{ case.judge }}</p>
<p>Case Number: {{ case.case_number }}</p>
<hr>
<p>[Motion text here]</p>
</body></html>""",
    'demand': """<!doctype html><html><body>
<h1>Demand Letter - {{ case.style }}</h1>
<p>[Demand details]</p>
</body></html>""",
    'notice': """<!doctype html><html><body>
<h1>Notice - {{ case.style }}</h1>
<p>[Notice details]</p>
</body></html>""",
    'billing': """<!doctype html><html><body>
<h1>Billing Statement - {{ case.style }}</h1>
<p>Client: {{ client.name if client else 'N/A' }}</p>
<p>Date: {{ today }}</p>
<hr>
<p>[Billing details]</p>
</body></html>""",
}


@documents_bulk_bp.route('/bulk_generate', methods=['GET', 'POST'])
@login_required
def documents_bulk_generate():
    """
    Bulk generate documents for a selected case.
    URL (after registering blueprint with url_prefix='/documents'):
      /documents/bulk_generate
    """
    form = BulkGenerateForm()

    # populate case choices
    form.case_id.choices = [(c.id, f"{c.style} ({c.case_number})") for c in Case.query.order_by(Case.created_at.desc()).all()]
    # set doc type choices for checkbox list
    form.doc_types.choices = DOC_TYPE_CHOICES

    if form.validate_on_submit():
        case = Case.query.get_or_404(form.case_id.data)
        client = getattr(case, 'client', None)
        selected_types = form.doc_types.data or []

        if not selected_types:
            flash('Please select at least one document type to generate.', 'warning')
            return render_template('bulk_generate.html', form=form)

        # Ensure upload folder exists
        base_upload_folder = current_app.config.get('UPLOAD_FOLDER') or os.path.join(os.path.dirname(__file__), '..', 'uploads', 'documents')
        os.makedirs(base_upload_folder, exist_ok=True)

        generated = []
        for doc_type in selected_types:
            label = dict(DOC_TYPE_CHOICES).get(doc_type, doc_type)

            # Try to find a Template with a name that matches the intended label (case-insensitive)
            template_obj = None
            try:
                template_obj = Template.query.filter(Template.name.ilike(f"%{label}%")).first()
            except Exception:
                template_obj = None

            if template_obj:
                content_src = template_obj.content
            else:
                content_src = DEFAULT_TEMPLATES.get(doc_type, f"<p>{label} for {{ case.style }}</p>")

            # Render using Jinja2 (flask render_template_string is fine here)
            try:
                rendered = render_template_string(content_src, case=case, client=client, user=current_user, today=datetime.utcnow().date(), now=datetime.utcnow())
            except Exception as e:
                flash(f"Error rendering {label}: {e}", 'danger')
                continue

            # Create filename
            safe_case = secure_filename(case.case_number or case.style) or f"case_{case.id}"
            base_name = f"{safe_case}_{doc_type}_{int(datetime.utcnow().timestamp())}"
            filename = f"{base_name}.html"
            filepath = os.path.join(base_upload_folder, filename)
            try:
                with open(filepath, 'w', encoding='utf-8') as fh:
                    fh.write(rendered)
            except Exception as e:
                flash(f"Failed to write file for {label}: {e}", 'danger')
                continue

            # create Document DB record
            relpath = os.path.relpath(filepath, start=os.path.dirname(__file__))
            doc = Document(
                filename=filename,
                filepath=relpath,
                client_id=client.id if client else None,
                case_id=case.id,
                uploaded_at=datetime.utcnow()
            )
            db.session.add(doc)
            generated.append(doc)

        # commit all generated documents
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error saving documents to DB: {e}", 'danger')
            return render_template('bulk_generate.html', form=form)

        flash(f"Generated {len(generated)} document(s).", 'success')
        # redirect to documents home (documents blueprint is named documents_bp)
        return redirect(url_for('documents_bp.documents_list'))

    return render_template('bulk_generate.html', form=form)