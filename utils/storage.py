import os
from flask import current_app, send_from_directory, abort

def get_upload_folder():
    return current_app.config.get('UPLOAD_FOLDER') or os.path.join(current_app.root_path, 'uploads', 'documents')

def safe_join_upload(filename):
    base = os.path.abspath(get_upload_folder())
    path = os.path.abspath(os.path.join(base, filename))
    if not path.startswith(base):
        raise ValueError("Invalid file path")
    return path

def serve_file(filename):
    folder = get_upload_folder()
    # validate path
    try:
        _ = safe_join_upload(filename)
    except Exception:
        abort(403)
    return send_from_directory(folder, filename, as_attachment=False)