from flask import Blueprint, render_template, request, redirect, url_for, flash
import os

# Define the blueprint
documents_bp = Blueprint('documents', __name__, template_folder='templates', static_folder='static')

# Simulated in-memory storage (replace with database in production)
documents = []
recently_viewed = []

# Route to display the index page with recently viewed documents
@documents_bp.route('/documents/', methods=['GET', 'POST'])
def index():
    document_types = ['Notice', 'Motion', 'Letter', 'Court Document', 'Other']
    cases = [
        {'id': 1, 'name': 'Case A'},
        {'id': 2, 'name': 'Case B'},
        {'id': 3, 'name': 'Case C'}
    ]

    if request.method == 'POST':
        # Handle file upload
        file = request.files.get('file')
        case_id = request.form.get('case')
        document_type = request.form.get('document_type')

        if file and case_id and document_type:
            document = {
                'filename': file.filename,
                'case_id': int(case_id),
                'document_type': document_type
            }
            documents.insert(0, document)  # Add to the beginning of the list to ensure it's recent
            flash(f"Document '{file.filename}' uploaded successfully!", 'success')
            return redirect(url_for('documents.index'))
        else:
            flash("Please provide all required fields.", 'danger')

    return render_template('documents/index.html', cases=cases, documents=documents, document_types=document_types)

# Route to handle document upload
@documents_bp.route('/documents/upload', methods=['GET', 'POST'])
def upload():
    categories = ['Court Document', 'Invoice', 'Letter', 'Contract', 'Report']  # Example categories
    if request.method == 'POST':
        # Process uploaded file
        file = request.files.get('file')
        category = request.form.get('category')

        if file and category:
            # Simulate saving the document (replace with actual file storage logic)
            document = {
                'filename': file.filename,
                'category': category
            }
            documents.append(document)

            # Redirect to index page
            flash(f"Document '{file.filename}' uploaded successfully!", 'success')
            return redirect(url_for('documents.index'))
        else:
            flash("Please provide both a file and a category.", 'danger')

    return render_template('documents/upload.html', categories=categories)

# Route to view a specific document
@documents_bp.route('/documents/view/<filename>')
def view(filename):
    # Simulated logic for viewing a document
    for doc in documents:
        if doc['filename'] == filename:
            # Add document to recently viewed (if not already there)
            if doc not in recently_viewed:
                recently_viewed.insert(0, doc)  # Add to the start of the list
            # Limit recently viewed list to 10 items
            if len(recently_viewed) > 10:
                recently_viewed.pop()
            return render_template('documents/view.html', document=doc)
    flash(f"Document '{filename}' not found.", 'danger')
    return redirect(url_for('documents.index'))