from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=False)
    date_made = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))