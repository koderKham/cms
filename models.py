# Full models.py with added case-type specific nullable columns
import enum
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class UserRole(enum.Enum):
    superuser = "superuser"
    manager = "manager"
    attorney = "attorney"
    staff = "staff"
    client = "client"
    pending = "pending"  # default for new signups

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.pending, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def is_superuser(self):
        return self.role == UserRole.superuser

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(200), nullable=False)               # Style/Name
    case_number = db.Column(db.String(100), unique=True, nullable=False)
    judge = db.Column(db.String(100), nullable=True)
    filed_date = db.Column(db.Date, nullable=True)
    case_type = db.Column(db.String(100), nullable=True)            # 'personal_injury','criminal','estate','other'

    # Generic / parties
    parties = db.Column(db.Text, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', backref='cases')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cases', lazy=True))

    # -----------------------
    # Personal Injury fields
    # -----------------------
    injuries = db.Column(db.Text, nullable=True)                   # injuries summary / medical notes
    accident_date = db.Column(db.Date, nullable=True)
    accident_location = db.Column(db.String(255), nullable=True)
    treating_physicians = db.Column(db.Text, nullable=True)
    medical_record_refs = db.Column(db.Text, nullable=True)        # references to records / file ids
    lost_wages = db.Column(db.String(100), nullable=True)          # stored as string for currency or note
    insurance_info = db.Column(db.Text, nullable=True)             # insurer, policy number, claim number
    settlement_amount = db.Column(db.String(100), nullable=True)

    # -----------------------
    # Criminal fields
    # -----------------------
    jurisdiction = db.Column(db.String(32), nullable=True)         # 'state' or 'federal' or NULL
    defendant = db.Column(db.String(200), nullable=True)
    co_defendants = db.Column(db.Boolean, nullable=True)
    retained_date = db.Column(db.Date, nullable=True)
    charges = db.Column(db.Text, nullable=True)                    # charges / allegations (text)
    arresting_agency = db.Column(db.String(200), nullable=True)
    case_status = db.Column(db.String(100), nullable=True)         # e.g., 'open','plea','dismissed','closed'

    # -----------------------
    # Probate / Estate Planning fields
    # -----------------------
    decedent_name = db.Column(db.String(200), nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)
    will_present = db.Column(db.Boolean, nullable=True)
    executor_name = db.Column(db.String(200), nullable=True)
    beneficiaries = db.Column(db.Text, nullable=True)              # JSON or newline-separated list
    estate_value = db.Column(db.String(100), nullable=True)       # string for currency
    probate_case_number = db.Column(db.String(100), nullable=True)

    # -----------------------
    # Other / generic matter fields
    # -----------------------
    matter_description = db.Column(db.Text, nullable=True)
    opposing_party = db.Column(db.String(200), nullable=True)
    priority = db.Column(db.String(50), nullable=True)             # e.g., 'low','medium','high'
    court = db.Column(db.String(200), nullable=True)

    # Relationships
    notes = db.relationship('Note', backref='case', lazy=True, cascade="all, delete-orphan")
    documents = db.relationship('Document', backref='case', lazy=True, cascade="all, delete-orphan")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=True)
    # ... other fields ...


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='notes')


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_viewed_at = db.Column(db.DateTime)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=True)
    client = db.relationship('Client', backref='documents')


class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    time_length = db.Column(db.String(50), nullable=True)
    deadline = db.Column(db.Boolean, default=False)
    deadline_datetime = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=True)
    case = db.relationship('Case', backref='calendar_events')

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    client = db.relationship('Client', backref='calendar_events')

    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=True)
    document = db.relationship('Document', backref='calendar_events')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref='calendar_events')

    event_datetime = db.Column(db.DateTime, nullable=False)


class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Add these classes into your models.py (near other SQLAlchemy models)

import json
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

# Custom Field metadata (one per field)
class CustomField(db.Model):
    __tablename__ = 'custom_field'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)      # internal name
    slug = Column(String(120), nullable=False, unique=True)  # stable key used in templates & storage
    label = Column(String(200), nullable=False)     # shown to users
    target = Column(String(50), nullable=False)     # 'case' or 'client' (can extend)
    field_type = Column(String(50), nullable=False) # 'text','textarea','select','radio','checkbox','date','number','boolean'
    options = Column(Text, nullable=True)           # JSON or newline list for choices (for select/radio/checkbox)
    required = Column(Boolean, default=False)
    help_text = Column(Text, nullable=True)
    order = Column(Integer, default=100)
    visible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_options_list(self):
        """Return options as list of (value,label) tuples."""
        if not self.options:
            return []
        # try JSON first (list or dict)
        try:
            parsed = json.loads(self.options)
            if isinstance(parsed, dict):
                # dict of value:label
                return [(k, v) for k, v in parsed.items()]
            if isinstance(parsed, list):
                # list of strings or [value,label] pairs
                out = []
                for item in parsed:
                    if isinstance(item, list) and len(item) >= 2:
                        out.append((str(item[0]), str(item[1])))
                    else:
                        out.append((str(item), str(item)))
                return out
        except Exception:
            # fallback: newline-separated values
            lines = [l.strip() for l in self.options.splitlines() if l.strip()]
            return [(v, v) for v in lines]
        return []

# CustomFieldValue stores a value for a specific resource (case or client)
class CustomFieldValue(db.Model):
    __tablename__ = 'custom_field_value'
    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey('custom_field.id'), nullable=False)
    # link to case or client (use nullable ints and only one used depending on target)
    case_id = Column(Integer, ForeignKey('case.id'), nullable=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=True)
    # store as text; for multiple choices store JSON-encoded array
    value = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    field = relationship('CustomField', backref='values')