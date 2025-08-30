from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from datetime import datetime
from app import db  # adjust import as needed

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    time_length = db.Column(db.String(100))
    deadline = db.Column(db.Boolean, default=False)
    deadline_datetime = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)

    cases = db.relationship('Case', secondary='case_event', back_populates='events')
    clients = db.relationship('Client', secondary='client_event', back_populates='events')
    documents = db.relationship('Document', backref='event', lazy=True)
    users = db.relationship('User', secondary='user_event', back_populates='events')
    notes = db.relationship('Note', backref='event', lazy=True)

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