from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Optional

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    event_type = SelectField(
        'Event Type',
        choices=[('task', 'Task'), ('important_date', 'Important Date'), ('reminder', 'Reminder')],
        validators=[DataRequired()]
    )
    datetime = DateTimeField(
        'Date & Time',
        format='%Y-%m-%d %H:%M',
        validators=[DataRequired()],
        description='Format: YYYY-MM-DD HH:MM'
    )
    case_id = IntegerField('Case ID', validators=[Optional()])
    client_id = IntegerField('Client ID', validators=[Optional()])
    document_id = IntegerField('Document ID', validators=[Optional()])
    submit = SubmitField('Save')