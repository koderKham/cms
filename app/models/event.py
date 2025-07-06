from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from datetime import datetime
from app import db  # adjust import as needed

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_type = db.Column(db.String(50), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.DateTime)

    @classmethod
    def create_event(cls, title, description, event_type, datetime_value, case_id=None, client_id=None, document_id=None):
        event = cls(
            title=title,
            description=description,
            event_type=event_type,
            datetime=datetime_value,
            case_id=case_id,
            client_id=client_id,
            document_id=document_id
        )
        db.session.add(event)
        db.session.commit()
        return event

    def edit_event(self, title=None, description=None, event_type=None, datetime_value=None, case_id=None, client_id=None, document_id=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if event_type is not None:
            self.event_type = event_type
        if datetime_value is not None:
            self.datetime = datetime_value
        if case_id is not None:
            self.case_id = case_id
        if client_id is not None:
            self.client_id = client_id
        if document_id is not None:
            self.document_id = document_id
        db.session.commit()
        return self

    def delete_event(self):
        db.session.delete(self)
        db.session.commit()