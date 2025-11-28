from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory, abort, render_template_string, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from models import db, User, UserRole, Case, Client, Document, CalendarEvent, Note, Template, PersonEntity
from forms import SignUpForm, LoginForm, CaseForm, ClientForm, CalendarEventForm,  TemplateForm, GenerateDocumentForm, DocumentForm, PartyForm
import datetime
from datetime import timedelta
from werkzeug.utils import secure_filename
import os
from services.custom_fields import attach_custom_fields_to_form, get_custom_fields_for, save_custom_field_values
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# inside app.py after app = Flask(...)
from cms.cases import cases_bp
app.register_blueprint(cases_bp)
# Add similar for documents blueprint or services

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Ensure super user exists ---
def create_superuser():
    with app.app_context():
        super_email = "admin@lawfirm.com"
        super_name = "Super User"
        super_password = "supersecret"
        superuser = User.query.filter_by(email=super_email).first()
        if not superuser:
            su = User(
                name=super_name,
                email=super_email,
                role=UserRole.superuser,
                is_active=True
            )
            su.set_password(super_password)
            db.session.add(su)
            db.session.commit()

@app.before_request
def setup():
    db.create_all()
    create_superuser()

# --- Routes ---
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email is already registered.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            role=UserRole.pending
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration submitted. Await super user approval.', 'info')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Awaiting super user approval.', 'warning')
                return redirect(url_for('login'))
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('team_dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    import datetime
    today = datetime.date.today()
    # Get start of week (Monday)
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)

    # Get events for the current week
    week_start_dt = datetime.datetime.combine(start_of_week, datetime.time.min)
    week_end_dt = datetime.datetime.combine(end_of_week, datetime.time.max)
    weekly_events = CalendarEvent.query.filter(
        CalendarEvent.event_datetime >= week_start_dt,
        CalendarEvent.event_datetime <= week_end_dt
    ).order_by(CalendarEvent.event_datetime.asc()).all()
    return render_template('dashboard.html',
        user=current_user,
        weekly_events=weekly_events,
        timedelta=timedelta,
        week_days=[start_of_week + datetime.timedelta(days=i) for i in range(7)],
    )

from auth import team_required

@app.route('/team_dashboard')
@team_required
def team_dashboard():
    # You can pass real data for recent cases, events, etc.
    return render_template('team_dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

# --- Superuser approval ---
@app.route('/approve', methods=['GET', 'POST'])
@login_required
def approve_users():
    if not current_user.is_superuser():
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    pending_users = User.query.filter_by(role=UserRole.pending).all()
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        role = request.form.get('role')
        user = User.query.get(user_id)
        if user and role in UserRole.__members__ and role != 'superuser':
            user.role = UserRole[role]
            user.is_active = True
            db.session.commit()
            flash(f'User {user.name} approved as {role}.', 'success')
        return redirect(url_for('approve_users'))
    return render_template('approve.html', pending_users=pending_users, roles=[r for r in UserRole if r != UserRole.superuser and r != UserRole.pending])

@app.route('/settings')
@login_required
def settings():
    # You can restrict to certain roles if needed
    return render_template('settings.html', user=current_user)

@app.route('/admin/search_users')
@login_required
def search_users():
    if not current_user.is_superuser():
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    query = request.args.get('q', '')
    users = User.query.filter(
        db.or_(
            User.name.ilike(f"%{query}%"),
            User.email.ilike(f"%{query}%"),
            User.id == query if query.isdigit() else False
        )
    ).all()
    return render_template('admin_dashboard.html', users=users)
#--- Cases Module ---
@app.route('/cases')
@login_required
def cases_list():
    search = request.args.get('search', '').strip()
    query = Case.query
    if search:
        query = query.filter(Case.style.ilike(f"%{search}%") | Case.case_number.ilike(f"%{search}%"))
    cases = query.all()
    return render_template('cases_list.html', cases=cases, search=search)

@app.route('/cases/<int:case_id>')
@login_required
def case_detail(case_id):
    case = Case.query.get_or_404(case_id)
    # Pass related info as needed
    return render_template('case_detail.html', case=case)


@app.route('/cases/create', methods=['GET', 'POST'])
@login_required
def case_create():
    form = CaseForm()
    # populate client/user choices
    form.client_id.choices = [(c.id, c.name) for c in Client.query.order_by(Client.name).all()]
    form.user_id.choices = [(u.id, u.name) for u in User.query.order_by(User.name).all()]

    # Get custom fields metadata and attach dynamic fields to the form (no owner yet)
    custom_fields = get_custom_fields_for('case')
    attach_custom_fields_to_form(form, target='case', owner=None)

    if form.validate_on_submit():
        # create the Case first so it has an id for storing custom values
        new_case = Case()
        form.populate_obj(new_case)
        db.session.add(new_case)
        db.session.commit()  # now new_case.id exists

        # Persist custom field values for the new case
        save_custom_field_values(new_case, 'case', custom_fields, form)
        db.session.commit()  # commit custom field values

        flash('Case created.', 'success')
        return redirect(url_for('cases_list'))  # adjust endpoint name as needed
    return render_template('case_form.html', form=form, custom_fields=custom_fields, case=None)

@app.route('/cases/<int:case_id>/edit', methods=['GET', 'POST'])
@login_required
def case_edit(case_id):
    case = Case.query.get_or_404(case_id)
    form = CaseForm(obj=case)
    # populate client/user choices
    form.client_id.choices = [(c.id, c.name) for c in Client.query.order_by(Client.name).all()]
    form.user_id.choices = [(u.id, u.name) for u in User.query.order_by(User.name).all()]

    # Get custom fields and attach to form, passing the existing case so fields get pre-populated
    custom_fields = get_custom_fields_for('case')
    attach_custom_fields_to_form(form, target='case', owner=case)

    if form.validate_on_submit():
        form.populate_obj(case)
        # Save custom field values for this case (owner already has id)
        save_custom_field_values(case, 'case', custom_fields, form)
        db.session.commit()
        flash('Case updated.', 'success')
        return redirect(url_for('case_detail', case_id=case.id))  # adjust endpoint as needed

    return render_template('case_form.html', form=form, custom_fields=custom_fields, case=case)
@app.route('/cases/<int:case_id>/delete', methods=['POST'])
@login_required
def case_delete(case_id):
    case = Case.query.get_or_404(case_id)
    db.session.delete(case)
    db.session.commit()
    flash('Case deleted.', 'info')
    return redirect(url_for('cases_list'))

@app.route('/people_entity')
@login_required
def people_entity_list():
    people_entity = PersonEntity.query.all()
    return render_template('people_entity_list.html', people_entity=people_entity)

@app.route('/people_entity/create', methods=['GET', 'POST'])
@login_required
def people_entity_create():
    form = PartyForm()
    if form.validate_on_submit():
        new_people_entity = Client(
            name=form.name.data,
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(new_people_entity)
        db.session.commit()
        flash('Client created!', 'success')
        return redirect(url_for('people_entity_list'))
    return render_template('people_entity_form.html', form=form)

@app.route('/people_entity/<int:people_entity_id>/edit', methods=['GET', 'POST'])
@login_required
def people_entity_edit(client_id):
    people_entity = PersonEntity.query.get_or_404(client_id)
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        form.populate_obj(people_entity)
        db.session.commit()
        flash('Updated!', 'success')
        return redirect(url_for('people_entity'))
    return render_template('people_entity_form.html', form=form, client=client)

@app.route('/people_entity/<int:people_entity_id>/delete', methods=['POST'])
@login_required
def people_entity_delete(client_id):
    people_entity = PersonEntity.query.get_or_404(client_id)
    db.session.delete(people_entity)
    db.session.commit()
    flash('Data deleted.', 'info')
    return redirect(url_for('people_entity_list'))

@app.route('/clients/<int:client_id>')
@login_required
def client_detail(client_id):
    client = Client.query.get_or_404(client_id)
    cases = client.cases
    documents = client.documents
    return render_template('people_entity_detail.html', client=client, cases=cases, documents=documents)

@app.route('/documents')
@login_required
def documents_list():
    sort = request.args.get('sort', 'recently_added')
    query = Document.query

    if sort == 'recently_viewed':
        query = query.order_by(Document.last_viewed_at.desc().nullslast())
    elif sort == 'recently_added':
        query = query.order_by(Document.uploaded_at.desc())
    elif sort == 'client_alpha':
        query = query.join(Client).order_by(Client.name.asc())
    elif sort == 'case_alpha':
        query = query.join(Case).order_by(Case.style.asc())
    elif sort == 'name_alpha':
        query = query.order_by(Document.filename.asc())

    documents = query.all()
    return render_template('documents_list.html', documents=documents, sort=sort)

@app.route('/documents/create', methods=['GET', 'POST'])
@login_required
def document_create():
    form = DocumentForm()
    form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]
    form.case_id.choices = [(c.id, c.style) for c in Case.query.all()]
    if form.validate_on_submit():
        # handle file upload as needed
        doc = Document(
            filename=form.filename.data,
            client_id=form.client_id.data or None,
            case_id=form.case_id.data or None,
            uploaded_at=datetime.utcnow()
        )
        db.session.add(doc)
        db.session.commit()
        flash('Document created!', 'success')
        return redirect(url_for('documents_list'))
    return render_template('document_form.html', form=form)

@app.route('/documents/<int:doc_id>/edit', methods=['GET', 'POST'])
@login_required
def document_edit(doc_id):
    doc = Document.query.get_or_404(doc_id)
    form = DocumentForm(obj=doc)
    form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]
    form.case_id.choices = [(c.id, c.style) for c in Case.query.all()]
    if form.validate_on_submit():
        form.populate_obj(doc)
        db.session.commit()
        flash('Document updated!', 'success')
        return redirect(url_for('documents_list'))
    return render_template('document_form.html', form=form, doc=doc)

@app.route('/documents/<int:doc_id>/delete', methods=['POST'])
@login_required
def document_delete(doc_id):
    doc = Document.query.get_or_404(doc_id)
    db.session.delete(doc)
    db.session.commit()
    flash('Document deleted.', 'info')
    return redirect(url_for('documents_list'))

@app.route('/documents/<int:doc_id>')
@login_required
def document_detail(doc_id):
    doc = Document.query.get_or_404(doc_id)
    return render_template('document_detail.html', doc=doc)

@app.route('/notes')
@login_required
def notes_list():
    search = request.args.get('search', '').strip()
    user_id = request.args.get('user_id', type=int)
    client_id = request.args.get('client_id', type=int)
    case_id = request.args.get('case_id', type=int)

    query = Note.query

    if search:
        query = query.filter(Note.note.ilike(f"%{search}%"))
    if user_id:
        query = query.filter(Note.user_id == user_id)
    if client_id:
        query = query.filter(Note.client_id == client_id)
    if case_id:
        query = query.filter(Note.case_id == case_id)

    notes = query.order_by(Note.created_at.desc()).all()

    users = User.query.all()
    clients = Client.query.all()
    cases = Case.query.all()

    return render_template(
        'notes_list.html',
        notes=notes,
        search=search,
        user_id=user_id,
        client_id=client_id,
        case_id=case_id,
        users=users,
        clients=clients,
        cases=cases
    )

@app.route('/notes/create', methods=['GET', 'POST'])
@login_required
def note_create():
    form = NoteForm()
    form.user_id.choices = [(u.id, u.name) for u in User.query.all()]
    form.case_id.choices = [(c.id, c.style) for c in Case.query.all()]
    form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]
    form.event_id.choices = [(e.id, e.title) for e in CalendarEvent.query.all()]
    form.document_id.choices = [(d.id, d.filename) for d in Document.query.all()]
    if form.validate_on_submit():
        note = Note(
            note=form.note.data,
            date_made=form.date_made.data,
            user_id=form.user_id.data,
            case_id=form.case_id.data or None,
            client_id=form.client_id.data or None,
            event_id=form.event_id.data or None,
            document_id=form.document_id.data or None
        )
        db.session.add(note)
        db.session.commit()
        flash('Note created!', 'success')
        return redirect(url_for('notes_list'))
    return render_template('note_form.html', form=form)

@app.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def note_edit(note_id):
    note = Note.query.get_or_404(note_id)
    form = NoteForm(obj=note)
    form.user_id.choices = [(u.id, u.name) for u in User.query.all()]
    form.case_id.choices = [(c.id, c.style) for c in Case.query.all()]
    form.client_id.choices = [(c.id, c.name) for c in Client.query.all()]
    form.event_id.choices = [(e.id, e.title) for e in CalendarEvent.query.all()]
    form.document_id.choices = [(d.id, d.filename) for d in Document.query.all()]
    if form.validate_on_submit():
        form.populate_obj(note)
        db.session.commit()
        flash('Note updated!', 'success')
        return redirect(url_for('notes_list'))
    return render_template('note_form.html', form=form, note=note)

@app.route('/notes/<int:note_id>/delete', methods=['POST'])
@login_required
def note_delete(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted.', 'info')
    return redirect(url_for('notes_list'))

@app.route('/notes/<int:note_id>')
@login_required
def note_detail(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('note_detail.html', note=note)

@app.route('/calendar')
@login_required
def calendar_month():
    # Get current month info
    today = datetime.now()
    year, month = today.year, today.month

    # Get all events for the current month
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime.datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    events = CalendarEvent.query.filter(CalendarEvent.event_datetime >= start, CalendarEvent.event_datetime < end).all()

    # Organize events by day
    from collections import defaultdict
    events_by_day = defaultdict(list)
    for event in events:
        day = event.event_datetime.day
        events_by_day[day].append(event)

    import calendar as pycal
    month_days = pycal.monthcalendar(year, month)  # list of weeks, each week is a list of day numbers (0 means blank)

    return render_template(
        'calendar_month.html',
        year=year,
        month=month,
        month_days=month_days,
        events_by_day=events_by_day
    )


@app.route('/calendar/events')
@login_required
def events_list():
    events = CalendarEvent.query.order_by(CalendarEvent.event_datetime.asc()).all()
    return render_template('events_list.html', events=events)

from datetime import datetime

@app.route('/calendar/events/create', methods=['GET', 'POST'])
@login_required
def event_create():
    form = CalendarEventForm(request.form)
    # ... set choices if needed ...
    if request.method == 'POST' and form.validate():
        # Combine event date/time
        event_dt_str = f"{form.event_year.data}-{form.event_month.data}-{form.event_day.data} {form.event_hour.data}:{form.event_minute.data}"
        event_datetime = datetime.strptime(event_dt_str, "%Y-%m-%d %H:%M")
        # Combine deadline date/time if deadline is set
        deadline_datetime = None
        if form.deadline.data:
            deadline_dt_str = f"{form.deadline_year.data}-{form.deadline_month.data}-{form.deadline_day.data} {form.deadline_hour.data}:{form.deadline_minute.data}"
            deadline_datetime = datetime.strptime(deadline_dt_str, "%Y-%m-%d %H:%M")

        event = CalendarEvent(
            name=form.name.data,
            event_datetime=event_datetime,
            deadline=form.deadline.data,
            deadline_datetime=deadline_datetime,
            # ... other fields ...
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created!', 'success')
        return redirect(url_for('events_list'))
    return render_template('event_form.html', form=form)
@app.route('/calendar/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def event_edit(event_id):
    event = CalendarEvent.query.get_or_404(event_id)
    form = CalendarEventForm(obj=event)
    form.case_id.choices = [(0, '')] + [(c.id, c.style) for c in Case.query.all()]
    form.client_id.choices = [(0, '')] + [(c.id, c.name) for c in Client.query.all()]
    form.document_id.choices = [(0, '')] + [(d.id, d.filename) for d in Document.query.all()]
    form.user_id.choices = [(0, '')] + [(u.id, u.name) for u in User.query.all()]
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        flash('Event updated!', 'success')
        return redirect(url_for('events_list'))
    return render_template('event_form.html', form=form, event=event)

@app.route('/calendar/events/<int:event_id>/delete', methods=['POST'])
@login_required
def event_delete(event_id):
    event = CalendarEvent.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'info')
    return redirect(url_for('events_list'))

@app.route('/calendar/events/<int:event_id>')
@login_required
def event_detail(event_id):
    event = CalendarEvent.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

# Add upload folder config (near app.config lines)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads', 'documents')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Template management routes ---
@app.route('/documents/templates')
@login_required
def templates_list():
    templates = Template.query.order_by(Template.created_at.desc()).all()
    return render_template('templates_list.html', templates=templates)

@app.route('/documents/templates/create', methods=['GET', 'POST'])
@login_required
def template_create():
    form = TemplateForm()
    if form.validate_on_submit():
        t = Template(name=form.name.data, content=form.content.data)
        db.session.add(t)
        db.session.commit()
        flash('Template saved.', 'success')
        return redirect(url_for('templates_list'))
    return render_template('template_form.html', form=form)

@app.route('/documents/templates/<int:template_id>/edit', methods=['GET', 'POST'])
@login_required
def template_edit(template_id):
    t = Template.query.get_or_404(template_id)
    form = TemplateForm(obj=t)
    if form.validate_on_submit():
        t.name = form.name.data
        t.content = form.content.data
        db.session.commit()
        flash('Template updated.', 'success')
        return redirect(url_for('templates_list'))
    return render_template('template_form.html', form=form, template=t)

# --- Generate a document from a template and a case ---
@app.route('/documents/generate', methods=['GET', 'POST'])
@login_required
def documents_generate():
    form = GenerateDocumentForm()
    # populate choices
    form.template_id.choices = [(t.id, t.name) for t in Template.query.order_by(Template.name).all()]
    form.case_id.choices = [(c.id, c.style) for c in Case.query.order_by(Case.created_at.desc()).all()]

    if form.validate_on_submit():
        template = Template.query.get_or_404(form.template_id.data)
        case = Case.query.get_or_404(form.case_id.data)
        client = case.client if hasattr(case, 'client') else None
        # Render template content using Jinja2
        try:
            rendered = render_template_string(template.content, case=case, client=client, user=current_user, today=datetime.utcnow().date(), now=datetime.utcnow())
        except Exception as e:
            flash(f'Error rendering template: {e}', 'danger')
            return render_template('generate_document.html', form=form)

        # Save file
        base_name = secure_filename(form.filename.data)
        if not base_name:
            base_name = f"{template.name}_{case.id}_{int(datetime.utcnow().timestamp())}"
        filename = f"{base_name}.html"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(rendered)

        # Create Document record
        doc = Document(
            filename=filename,
            filepath=os.path.relpath(filepath, start=os.path.dirname(__file__)),
            client_id=client.id if client else None,
            case_id=case.id,
            uploaded_at=datetime.utcnow()
        )
        db.session.add(doc)
        db.session.commit()
        flash('Document generated and saved.', 'success')
        return redirect(url_for('document_detail', doc_id=doc.id))

    return render_template('generate_document.html', form=form)

@app.route('/documents/<int:doc_id>/preview')
@login_required
def document_preview(doc_id):
    doc = Document.query.get_or_404(doc_id)

    # Ensure we have a filepath
    if not getattr(doc, 'filepath', None):
        flash('No file available to preview.', 'warning')
        return redirect(url_for('document_detail', doc_id=doc.id))

    # Determine upload base directory
    base_folder = app.config.get('UPLOAD_FOLDER') or os.path.join(os.path.dirname(__file__), 'uploads', 'documents')
    # Resolve absolute paths to prevent directory traversal
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), doc.filepath))
    base_abs = os.path.abspath(base_folder)

    # Security check: only allow files inside the upload folder
    if not file_path.startswith(base_abs):
        abort(403)

    try:
        with open(file_path, 'r', encoding='utf-8') as fh:
            content = fh.read()
    except Exception as e:
        flash(f'Could not read file: {e}', 'danger')
        return redirect(url_for('document_detail', doc_id=doc.id))

    # Render the HTML content inside a page
    return render_template('document_preview.html', doc=doc, content=content)

# --- Bulk document generation (paste this into app.py near other document routes) ---
# Required imports (add these to the top of app.py if they aren't already present):
# import os
# from werkzeug.utils import secure_filename
# from flask import render_template_string, current_app
# from datetime import datetime
# from forms import BulkGenerateForm
# from models import Template, Case, Document
#
# Note: Ensure app.config['UPLOAD_FOLDER'] is set (see earlier suggestions). The route below
# expects Document.filepath to store a path relative to the repo/app directory.

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


@app.route('/documents/bulk_generate', methods=['GET', 'POST'])
@login_required
def documents_bulk_generate():
    """
    Bulk generate documents for a selected case.
    Page shows checkboxes for each doc type in DOC_TYPE_CHOICES and a case selector.
    After generation, created Document records are saved and user is redirected to documents list.
    """
    form = BulkGenerateForm()

    # populate choices
    form.case_id.choices = [(c.id, f"{c.style} ({c.case_number})") for c in Case.query.order_by(Case.created_at.desc()).all()]
    form.doc_types.choices = DOC_TYPE_CHOICES

    if form.validate_on_submit():
        case = Case.query.get_or_404(form.case_id.data)
        client = getattr(case, 'client', None)
        selected = form.doc_types.data or []

        if not selected:
            flash('Please select at least one document type to generate.', 'warning')
            return render_template('bulk_generate.html', form=form)

        # ensure upload folder exists
        base_upload_folder = app.config.get('UPLOAD_FOLDER') or os.path.join(os.path.dirname(__file__), 'uploads', 'documents')
        os.makedirs(base_upload_folder, exist_ok=True)

        generated_docs = []
        for doc_type in selected:
            label = dict(DOC_TYPE_CHOICES).get(doc_type, doc_type)

            # Try to use a Template whose name contains the label (case-insensitive). Fallback to default.
            template_obj = None
            try:
                template_obj = Template.query.filter(Template.name.ilike(f"%{label}%")).first()
            except Exception:
                template_obj = None

            content_src = template_obj.content if template_obj else DEFAULT_TEMPLATES.get(doc_type, f"<p>{label} for {{ case.style }}</p>")

            # Render template content (Jinja2)
            try:
                rendered = render_template_string(content_src, case=case, client=client, user=current_user, today=datetime.utcnow().date(), now=datetime.utcnow())
            except Exception as e:
                flash(f"Error rendering {label}: {e}", 'danger')
                continue

            # Build filename and save file
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

            # Create Document DB record
            relpath = os.path.relpath(filepath, start=os.path.dirname(__file__))
            doc = Document(
                filename=filename,
                filepath=relpath,
                client_id=client.id if client else None,
                case_id=case.id,
                uploaded_at=datetime.utcnow()
            )
            db.session.add(doc)
            generated_docs.append(doc)

        # commit all created documents
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error saving documents to DB: {e}", 'danger')
            return render_template('bulk_generate.html', form=form)

        flash(f"Generated {len(generated_docs)} document(s).", 'success')
        return redirect(url_for('documents_list'))

    return render_template('bulk_generate.html', form=form)

# Add/merge these constants into your app (near DOC_TYPE_CHOICES / DEFAULT_TEMPLATES)

# Document types available for generation (add these to your existing list)
DOC_TYPE_CHOICES.extend([
    ('notice_of_appearance', 'Notice of Appearance (Criminal)'),
    ('written_plea_not_guilty', 'Written Plea of Not Guilty (Criminal)'),
    ('demand_for_discovery', 'Demand for Discovery (Criminal)'),
    ('blank_motion', 'Blank Motion (Criminal - bare bones)'),
    ('petition_for_administration', 'Petition for Administration (Estate)'),
    ('letter_of_representation', 'Letter of Representation (Personal Injury)'),
])

# Default templates for the new document types. The generator will try to find a Template row
# by name that matches the label; otherwise it uses these fallbacks.
DEFAULT_TEMPLATES.update({
    'notice_of_appearance': """<!doctype html>
<html><head><meta charset="utf-8"><title>Notice of Appearance - {{ case.case_number }}</title></head>
<body>
<h2>NOTICE OF APPEARANCE</h2>
<p>IN THE MATTER OF: <strong>{{ case.style }}</strong></p>
<p>Case No.: {{ case.case_number }}</p>
<p>Judge: {{ case.judge or 'N/A' }}</p>
<p>TO: The Clerk of the Court and all parties of record:</p>
<p>Please take notice that {{ user.name if user else 'Counsel' }} of {{ client.name if client else 'Client' }} appears as counsel for {{ case.defendant or client.name or 'the Defendant' }} in the above-captioned matter.</p>
<p>Date: {{ today }}</p>
<hr>
<p>Sincerely,</p>
<p>{{ user.name if user else 'Attorney' }}</p>
</body></html>
""",

    'written_plea_not_guilty': """<!doctype html>
<html><head><meta charset="utf-8"><title>Plea of Not Guilty - {{ case.case_number }}</title></head>
<body>
<h2>WRITTEN PLEA OF NOT GUILTY</h2>
<p>Case: {{ case.style }} ({{ case.case_number }})</p>
<p>Defendant: {{ case.defendant or client.name if client else 'Defendant' }}</p>
<p>I, the undersigned, on behalf of the defendant, hereby enter a plea of <strong>NOT GUILTY</strong> to the charges in this matter.</p>
<p>Charges: {{ case.charges or 'See case file' }}</p>
<p>Date retained: {{ case.retained_date or 'N/A' }}</p>
<p>Date: {{ today }}</p>
<hr>
<p>Respectfully submitted,</p>
<p>{{ user.name if user else 'Attorney' }}</p>
</body></html>
""",

    'demand_for_discovery': """<!doctype html>
<html><head><meta charset="utf-8"><title>Demand for Discovery - {{ case.case_number }}</title></head>
<body>
<h2>DEMAND FOR DISCOVERY</h2>
<p>To: Prosecutor / State Counsel</p>
<p>Re: {{ case.style }} — Case No. {{ case.case_number }}</p>
<p>Pursuant to applicable rules, the defense demands disclosure of all discoverable materials, including but not limited to:</p>
<ul>
  <li>Police reports and incident reports</li>
  <li>Witness statements</li>
  <li>Scientific and laboratory reports</li>
  <li>Prior criminal records</li>
  <li>Any exculpatory evidence (Brady)</li>
</ul>
<p>Defendant: {{ case.defendant or client.name if client else 'Defendant' }}<br>Date: {{ today }}</p>
<hr>
<p>{{ user.name if user else 'Defense Counsel' }}</p>
</body></html>
""",

    'blank_motion': """<!doctype html>
<html><head><meta charset="utf-8"><title>Motion - {{ case.case_number }}</title></head>
<body>
<h2>MOTION</h2>
<p>IN THE CIRCUIT/UNITED STATES DISTRICT COURT</p>
<p>Case: {{ case.style }} • Case No. {{ case.case_number }}</p>
<p>COMES NOW the undersigned counsel and respectfully moves the Court to [describe relief requested].</p>
<h3>Grounds</h3>
<p>[Insert grounds / facts / legal authority here]</p>
<h3>Conclusion</h3>
<p>Wherefore, the defense respectfully requests that the Court grant the relief requested above.</p>
<p>Date: {{ today }}</p>
<p>{{ user.name if user else 'Attorney' }}</p>
</body></html>
""",

    'petition_for_administration': """<!doctype html>
<html><head><meta charset="utf-8"><title>Petition for Administration - {{ case.case_number or case.probate_case_number }}</title></head>
<body>
<h2>PETITION FOR ADMINISTRATION</h2>
<p>IN THE PROBATE COURT FOR: {{ case.court or '_____' }}</p>
<p>Decedent: {{ case.decedent_name or 'Decedent' }}</p>
<p>Petitioner: {{ client.name if client else 'Petitioner' }}</p>
<p>Estate Value: {{ case.estate_value or 'Unknown' }}</p>
<p>Relief sought: administration of decedent's estate and appointment of executor/administrator.</p>
<p>Date of death: {{ case.date_of_death or 'N/A' }}</p>
<hr>
<p>Respectfully submitted,</p>
<p>{{ user.name if user else 'Attorney' }}</p>
</body></html>
""",

    'letter_of_representation': """<!doctype html>
<html><head><meta charset="utf-8"><title>Letter of Representation - {{ case.case_number }}</title></head>
<body>
<h2>LETTER OF REPRESENTATION</h2>
<p>Date: {{ today }}</p>
<p>To: {{ client.name if client else 'Client' }}</p>
<p>Re: Representation in {{ case.style }} • Case No. {{ case.case_number }}</p>
<p>Dear {{ client.name if client else 'Client' }},</p>
<p>This letter confirms that {{ user.name if user else 'Attorney' }} represents you with respect to the above-referenced matter arising from the incident on {{ case.accident_date or 'N/A' }} at {{ case.accident_location or 'N/A' }}.</p>
<p>We will be handling medical records, insurance communications, and settlement negotiations. Please direct all inquiries and other attorneys to our office.</p>
<p>Sincerely,</p>
<p>{{ user.name if user else 'Attorney' }}</p>
</body></html>
""",
})

# Helper to render and save a generated HTML document for a case
def generate_and_save_document(case, doc_type_slug, label=None, template_obj=None, current_user=None):
    """
    Renders and saves a document for `case`.
    - doc_type_slug: key from DOC_TYPE_CHOICES / DEFAULT_TEMPLATES
    - label: human label used to search for Template rows (optional)
    - template_obj: optional Template instance to use (skip DB lookup)
    Returns Document instance (not committed) or None on error.
    """
    from flask import render_template_string
    import os
    from werkzeug.utils import secure_filename
    from datetime import datetime

    client = getattr(case, 'client', None)

    label = label or dict(DOC_TYPE_CHOICES).get(doc_type_slug, doc_type_slug.replace('_', ' ').title())

    # prefer passed-in template_obj; otherwise try to find Template row by label match
    if not template_obj:
        try:
            template_obj = Template.query.filter(Template.name.ilike(f"%{label}%")).first()
        except Exception:
            template_obj = None

    content_src = template_obj.content if template_obj else DEFAULT_TEMPLATES.get(doc_type_slug, f"<p>{label} for {{ case.style }}</p>")

    try:
        rendered = render_template_string(content_src, case=case, client=client, user=current_user, today=datetime.utcnow().date(), now=datetime.utcnow())
    except Exception as e:
        # calling code should flash or log the error
        return None

    # ensure upload folder exists
    base_upload_folder = app.config.get('UPLOAD_FOLDER') or os.path.join(os.path.dirname(__file__), 'uploads', 'documents')
    os.makedirs(base_upload_folder, exist_ok=True)

    safe_case = secure_filename(case.case_number or case.style) or f"case_{case.id}"
    base_name = f"{safe_case}_{doc_type_slug}_{int(datetime.utcnow().timestamp())}"
    filename = f"{base_name}.html"
    filepath = os.path.join(base_upload_folder, filename)
    with open(filepath, 'w', encoding='utf-8') as fh:
        fh.write(rendered)

    relpath = os.path.relpath(filepath, start=os.path.dirname(__file__))
    doc = Document(
        filename=filename,
        filepath=relpath,
        client_id=client.id if client else None,
        case_id=case.id,
        uploaded_at=datetime.utcnow()
    )
    db.session.add(doc)
    # Note: do not commit here; caller may batch-commit.
    return doc

@app.route('/documents/generate_for_case/<int:case_id>', methods=['GET', 'POST'])
@login_required
def documents_generate_for_case(case_id):
    """
    Single-case generator page.
    Shows the appropriate document types for the case type and offers checkboxes to generate them.
    """
    from forms import BulkGenerateForm  # reuse bulk form but with case preselected
    case = Case.query.get_or_404(case_id)
    client = getattr(case, 'client', None)

    # build a filtered list of doc choices depending on case.case_type
    # mapping of case_type -> list of doc_type_slugs (order matters)
    type_map = {
        'criminal': ['notice_of_appearance', 'written_plea_not_guilty', 'demand_for_discovery', 'blank_motion'],
        'estate': ['petition_for_administration'],
        'personal_injury': ['letter_of_representation'],
        # fallback/general: allow all, or choose subset
        'other': ['letter_of_representation', 'blank_motion'],
        None: ['letter_of_representation', 'blank_motion'],
    }
    choices = type_map.get(case.case_type, type_map.get('other'))

    form = BulkGenerateForm()  # contains case_id and doc_types
    # set the form choices
    form.case_id.choices = [(case.id, f"{case.style} ({case.case_number})")]
    form.doc_types.choices = [(slug, dict(DOC_TYPE_CHOICES).get(slug, slug.replace('_',' ').title())) for slug in choices]

    if form.validate_on_submit():
        selected = form.doc_types.data or []
        if not selected:
            flash('Please select at least one document to generate.', 'warning')
            return render_template('generate_for_case.html', form=form, case=case)
        generated = []
        for slug in selected:
            doc = generate_and_save_document(case, slug, current_user=current_user)
            if doc:
                generated.append(doc)
            else:
                flash(f'Error generating {slug}.', 'danger')
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving generated documents: {e}', 'danger')
            return render_template('generate_for_case.html', form=form, case=case)

        flash(f'Generated {len(generated)} document(s).', 'success')
        return redirect(url_for('document_detail', doc_id=generated[0].id) if len(generated)==1 else url_for('documents_list'))

    return render_template('generate_for_case.html', form=form, case=case)

@app.route('/documents/preview_template/<template_slug>')
@login_required
def documents_preview_template(template_slug):
    """
    Preview the default or Template content for a slug. Optional case_id query param to render with data.
    """
    case_id = request.args.get('case_id', type=int)
    case = Case.query.get(case_id) if case_id else None
    client = getattr(case, 'client', None) if case else None

    # try find Template by matching label text
    label = dict(DOC_TYPE_CHOICES).get(template_slug, template_slug)
    template_obj = None
    try:
        template_obj = Template.query.filter(Template.name.ilike(f"%{label}%")).first()
    except Exception:
        template_obj = None

    content_src = template_obj.content if template_obj else DEFAULT_TEMPLATES.get(template_slug, f"<p>{label}</p>")
    from flask import render_template_string
    rendered = render_template_string(content_src, case=case, client=client, user=current_user, today=datetime.utcnow().date(), now=datetime.utcnow())
    return render_template('document_preview.html', doc={'filename': f'Preview-{template_slug}.html'}, content=rendered)

if __name__ == "__main__":
    app.run(debug=True)