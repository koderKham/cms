from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateTimeField, FileField
from wtforms.validators import DataRequired, Optional, Length

class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[Optional()])
    location = StringField("Location", validators=[Optional(), Length(max=200)])
    category = SelectField("Category", choices=[("Meeting", "Meeting"), ("Personal", "Personal"), ("Work", "Work")], validators=[Optional()])
    priority = SelectField("Priority", choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], default="medium", validators=[Optional()])

    start_time = DateTimeField("Start Time", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    end_time = DateTimeField("End Time", format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    all_day = BooleanField("All Day", validators=[Optional()])

    is_recurring = BooleanField("Recurring", validators=[Optional()])
    recurrence_pattern = SelectField("Recurrence Pattern", choices=[("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly"), ("yearly", "Yearly")], validators=[Optional()])
    recurrence_end_date = DateTimeField("Recurrence End Date", format='%Y-%m-%d %H:%M:%S', validators=[Optional()])

    organizer = StringField("Organizer", validators=[Optional(), Length(max=100)])
    is_private = BooleanField("Private", validators=[Optional()])
    invite_link = StringField("Invite Link", validators=[Optional(), Length(max=200)])

    status = SelectField("Status", choices=[("Scheduled", "Scheduled"), ("Completed", "Completed"), ("Canceled", "Canceled")], default="Scheduled", validators=[Optional()])
    reminder_time = DateTimeField("Reminder Time", format='%Y-%m-%d %H:%M:%S', validators=[Optional()])

    attachments = FileField("Attachments", validators=[Optional()])
    url = StringField("URL", validators=[Optional(), Length(max=200)])

    color = StringField("Color", validators=[Optional(), Length(max=7)])