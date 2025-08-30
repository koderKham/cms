from datetime import datetime
from app import db


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    file_path = db.Column(db.String(255))
    dropbox_path = db.Column(db.String(255))
    is_synced_to_dropbox = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(200))  # Comma-separated tags
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = db.Column(db.Text)
    # Associations (nullable, only one should be set)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    notes = db.relationship('Note', backref='document', lazy=True)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'case_id': self.case_id,
            'client_id': self.client_id,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'file_path': self.file_path,
            'dropbox_path': self.dropbox_path,
            'is_synced_to_dropbox': self.is_synced_to_dropbox,
            'tags': self.tags.split(',') if self.tags else [],
            'uploaded_by_id': self.uploaded_by_id,
            'uploaded_at': self.uploaded_at,
            'last_modified': self.last_modified,
            'description': self.description
        }

