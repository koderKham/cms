from flask_wtf import FlaskForm
from wtforms import TextAreaField, DateTimeField, IntegerField, SubmitField

class NoteForm(FlaskForm):
    note = TextAreaField('Note')
    date_made = DateTimeField('Date Made', format='%Y-%m-%d %H:%M:%S')
    user_id = IntegerField('User ID')
    case_id = IntegerField('Case ID')
    client_id = IntegerField('Client ID')
    event_id = IntegerField('Event ID')
    document_id = IntegerField('Document ID')
    submit = SubmitField('Submit')