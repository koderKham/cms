from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association tables for many-to-many relationships
user_event = db.Table('user_event',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

case_event = db.Table('case_event',
    db.Column('case_id', db.Integer, db.ForeignKey('case.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

client_event = db.Table('client_event',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)