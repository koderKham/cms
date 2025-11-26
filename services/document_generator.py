import os
from datetime import datetime
from flask import current_app, render_template_string
from werkzeug.utils import secure_filename
from models import Template, Document, db

# Default templates can be extended; keep them small here and refer to DEFAULT_TEMPLATES in app if present.
DEFAULT_TEMPLATES = {
    # keys: 'notice_of_appearance', 'written_plea_not_guilty', etc.
}

def allowed_filename(name):
    return bool(name) and '/' not in name and '\\' not in name

def render_template_for_case(slug, case, user=None):
    """Return rendered HTML string for slug using Template DB override if present."""
    label = slug.replace('_', ' ').title()
    template_obj = None
    try:
        template_obj = Template.query.filter(Template.name.ilike(f"%{label}%")).first()
    except Exception:
        template_obj = None

    if template_obj and template_obj.content:
        src = template_obj.content
    else:
        src = DEFAULT_TEMPLATES.get(slug, f"<p>{label} for {{ case.style }}</p>")

    rendered = render_template_string(src, case=case, client=getattr(case, 'client', None), user=user, today=datetime.utcnow().date(), now=datetime.utcnow())
    return rendered

def save_rendered_document(rendered_html, case, filename_base=None):
    """Write file to disk and create Document DB object (uncommitted)."""
    base_upload_folder = current_app.config.get('UPLOAD_FOLDER')
    os.makedirs(base_upload_folder, exist_ok=True)

    safe_case = secure_filename(case.case_number or case.style) or f"case_{case.id}"
    timestamp = int(datetime.utcnow().timestamp())
    filename_base = filename_base or f"{safe_case}_{timestamp}"
    filename = f"{secure_filename(filename_base)}.html"
    filepath = os.path.join(base_upload_folder, filename)

    with open(filepath, 'w', encoding='utf-8') as fh:
        fh.write(rendered_html)

    relpath = os.path.relpath(filepath, start=os.path.dirname(current_app.root_path))
    doc = Document(
        filename=filename,
        filepath=relpath,
        client_id=getattr(case, 'client_id', None),
        case_id=case.id,
        uploaded_at=datetime.utcnow()
    )
    db.session.add(doc)
    # do not commit here
    return doc

def generate_documents_for_case(case, slugs, user=None):
    """
    Takes a Case and list of slugs, renders, saves and returns list of Document objects (uncommitted).
    Caller should commit DB after successful generation.
    """
    generated = []
    for slug in slugs:
        rendered = render_template_for_case(slug, case, user=user)
        filename_base = f"{slug}"
        doc = save_rendered_document(rendered, case, filename_base=filename_base)
        generated.append(doc)
    return generated