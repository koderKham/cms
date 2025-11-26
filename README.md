# cms_v2 — Law Firm CMS (starter)

This repository is an adaptable content-management system for law practice management. The structure is modular and designed for iterative development.

Quick start
1. Create a Python virtualenv and install requirements:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure environment (optional) — create a `.env`:
   ```
   SECRET_KEY=your_secret
   DATABASE_URL=sqlite:///cms.db
   ```

3. Initialize DB (dev quick-start):
   ```
   export FLASK_APP=app.py
   flask db init    # only first time
   flask db migrate -m "Initial"
   flask db upgrade
   ```

4. Run:
   ```
   python app.py
   ```

Architecture notes
- Blueprints: cms/cases.py, cms/documents.py, etc. for route organization.
- Services: services/document_generator.py contains business logic for document generation.
- Templates stored in `templates/`. DB Template model allows overriding default templates.
- Uploads live in `uploads/documents/`.

Next features you may add
- Background job worker for batch generation and PDF conversion (Celery/RQ).
- Role-based permissions & audit trail (who created/edited documents).
- Document versioning and comments.
- Integration with external calendaring (Google Calendar), billing, e-signatures.
