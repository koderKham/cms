from app.models.base_event import BaseEvent
from app import db

class ImportantDate(BaseEvent):
    __tablename__ = 'important_dates'
    id = db.Column(db.Integer, db.ForeignKey('base_events.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'important_date',
    }