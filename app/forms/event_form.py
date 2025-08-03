from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField, IntegerField, BooleanField
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
    
    # New fields for enhanced functionality
    location = StringField('Location', validators=[Optional()])
    duration = StringField('Duration', validators=[Optional()], description='Format: 2:30:00 for 2 hours 30 minutes')
    status = SelectField(
        'Status',
        choices=[('active', 'Active'), ('completed', 'Completed'), ('canceled', 'Canceled')],
        default='active',
        validators=[DataRequired()]
    )
    priority = SelectField(
        'Priority',
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        validators=[Optional()]
    )
    is_recurring = BooleanField('Recurring Event', default=False)
    recurrence_pattern = StringField('Recurrence Pattern', validators=[Optional()], 
                                   description='e.g., weekly, daily, monthly')
    notify_before = IntegerField('Notify Before (minutes)', validators=[Optional()],
                               description='Number of minutes before event to send notification')
    
    submit = SubmitField('Save')