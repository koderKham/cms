from datetime import datetime
from app import db

class BaseEvent(db.Model):
    __tablename__ = 'base_events'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))  # For polymorphic identity

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Polymorphic assignment fields
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'base_event',
        'polymorphic_on': type
    }