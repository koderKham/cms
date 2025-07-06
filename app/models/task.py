from app.models.base_event import BaseEvent
from app import db

class Task(BaseEvent):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, db.ForeignKey('base_events.id'), primary_key=True)
    completed = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'task',
    }