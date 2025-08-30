from datetime import datetime
from app import db
from app.models.user import User
from app.models.person import Person

class CaseStatus:
    """Enum for case status values"""
    OPEN = 'open'
    PENDING = 'pending'
    CLOSED = 'closed'
    ARCHIVED = 'archived'


class CaseType:
    """Enum for case type values"""
    LITIGATION = 'litigation'
    CORPORATE = 'corporate'
    FAMILY = 'family'
    CRIMINAL = 'criminal'
    ESTATE = 'estate'
    REAL_ESTATE = 'real_estate'
    IMMIGRATION = 'immigration'
    TAX = 'tax'
    INTELLECTUAL_PROPERTY = 'intellectual_property'
    OTHER = 'other'


class Case(db.Model):
    """Case model representing a legal case in the system"""
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
        # ... other fields ...
    title = db.Column(db.String(255), nullable=False)
    case_number = db.Column(db.String(50), unique=True)
    type = db.Column(db.String(50), default=CaseType.OTHER)
    status = db.Column(db.String(20), default=CaseStatus.OPEN)
    description = db.Column(db.Text)
    court_name = db.Column(db.String(255))
    judge_name = db.Column(db.String(100))
    opposing_counsel = db.Column(db.String(255))
    filing_date = db.Column(db.Date)
    hearing_date = db.Column(db.Date)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=True)
    person = db.relationship('Person', backref='cases')
    # Financial information
    total_billed = db.Column(db.Float, default=0.0)
    total_paid = db.Column(db.Float, default=0.0)
    hourly_rate = db.Column(db.Float)
    retainer_amount = db.Column(db.Float, default=0.0)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    notes = db.relationship('Note', backref='case', lazy=True)
    events = db.relationship('Event', secondary='case_event', back_populates='cases')
    documents = db.relationship('Document', backref='case', lazy=True)
    # We'll add more relationships later (documents, activities, notes)

    def __repr__(self):
        return f'<Case {self.title} ({self.case_number})>'

    def to_dict(self):
        """Convert Case to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'case_number': self.case_number,
            'type': self.type,
            'status': self.status,
            'description': self.description,
            'court_name': self.court_name,
            'judge_name': self.judge_name,
            'opposing_counsel': self.opposing_counsel,
            'filing_date': self.filing_date.isoformat() if self.filing_date else None,
            'hearing_date': self.hearing_date.isoformat() if self.hearing_date else None,
            'total_billed': self.total_billed,
            'total_paid': self.total_paid,
            'hourly_rate': self.hourly_rate,
            'retainer_amount': self.retainer_amount,
            'lead_attorney': self.lead_attorney.name if self.lead_attorney else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }