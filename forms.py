from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, PasswordField, DateTimeField, SubmitField, FileField, TextAreaField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
import datetime
now = datetime.datetime.utcnow()

class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# --- CaseForm (excerpt) ---
# Update your CaseForm in forms.py to include the criminal fields.

class CaseForm(FlaskForm):
    CASE_TYPE_CHOICES = [
        ('', 'Select case type...'),
        ('personal_injury', 'Personal Injury'),
        ('criminal', 'Criminal'),
        ('estate', 'Probate / Estate Planning'),
        ('other', 'Other / General Matter'),
    ]

    # Common
    style = StringField('Case Style / Title', validators=[DataRequired(), Length(max=200)])
    case_number = StringField('Case Number', validators=[DataRequired(), Length(max=100)])
    judge = StringField('Judge', validators=[Optional(), Length(max=100)])
    filed_date = DateField('Filed Date', format='%Y-%m-%d', validators=[Optional()])
    case_type = SelectField('Case Type', choices=CASE_TYPE_CHOICES, validators=[DataRequired()])
    client_id = SelectField('Client', coerce=int, validators=[DataRequired()])
    user_id = SelectField('Assigned User', coerce=int, validators=[DataRequired()])

    # -----------------------
    # Personal Injury
    # -----------------------
    injuries = TextAreaField('Injuries / Medical Summary', validators=[Optional(), Length(max=4000)])
    accident_date = DateField('Accident Date', format='%Y-%m-%d', validators=[Optional()])
    accident_location = StringField('Accident Location', validators=[Optional(), Length(max=255)])
    treating_physicians = TextAreaField('Treating Physicians / Providers', validators=[Optional(), Length(max=2000)])
    medical_record_refs = TextAreaField('Medical Record References', validators=[Optional(), Length(max=2000)])
    lost_wages = StringField('Lost Wages (note / amount)', validators=[Optional(), Length(max=100)])
    insurance_info = TextAreaField('Insurance Info', validators=[Optional(), Length(max=1000)])
    settlement_amount = StringField('Settlement Amount (if any)', validators=[Optional(), Length(max=100)])

    # -----------------------
    # Criminal
    # -----------------------
    jurisdiction = SelectField('Jurisdiction', choices=[
        ('', 'Select jurisdiction...'),
        ('federal', 'Federal (FLA)'),
        ('state', 'State (FLA)')
    ], validators=[Optional()])
    defendant = StringField('Defendant', validators=[Optional(), Length(max=200)])
    co_defendants = RadioField('Co-defendants?', choices=[('yes','Yes'),('no','No')], validators=[Optional()])
    retained_date = DateField('Date Retained', format='%Y-%m-%d', validators=[Optional()])
    charges = TextAreaField('Charges / Allegations', validators=[Optional(), Length(max=4000)])
    arresting_agency = StringField('Arresting Agency', validators=[Optional(), Length(max=200)])
    case_status = SelectField('Case Status', choices=[
        ('', 'Select status...'),
        ('open', 'Open'),
        ('pretrial', 'Pre-trial'),
        ('plea', 'Plea'),
        ('dismissed', 'Dismissed'),
        ('closed', 'Closed')
    ], validators=[Optional()])

    # -----------------------
    # Probate / Estate Planning
    # -----------------------
    decedent_name = StringField("Decedent's Name", validators=[Optional(), Length(max=200)])
    date_of_death = DateField('Date of Death', format='%Y-%m-%d', validators=[Optional()])
    will_present = RadioField('Will Present?', choices=[('yes','Yes'),('no','No')], validators=[Optional()])
    executor_name = StringField('Executor / Personal Representative', validators=[Optional(), Length(max=200)])
    beneficiaries = TextAreaField('Beneficiaries', validators=[Optional(), Length(max=4000)])
    estate_value = StringField('Estate Value (estimate)', validators=[Optional(), Length(max=100)])
    probate_case_number = StringField('Probate Case Number', validators=[Optional(), Length(max=100)])

    # -----------------------
    # Other / General Matter
    # -----------------------
    matter_description = TextAreaField('Matter Description', validators=[Optional(), Length(max=4000)])
    opposing_party = StringField('Opposing Party', validators=[Optional(), Length(max=200)])
    priority = SelectField('Priority', choices=[('', 'Select...'), ('low','Low'), ('medium','Medium'), ('high','High')], validators=[Optional()])
    court = StringField('Court / Venue', validators=[Optional(), Length(max=200)])

    submit = SubmitField('Save Case')

    def populate_obj(self, obj):
        """
        Populate the SQLAlchemy object with form data.
        Handles conversions (e.g., co_defendants radio => boolean) and keeps nullable behavior.
        """
        super().populate_obj(obj)
        # co_defendants radio field to boolean/None
        if hasattr(self, 'co_defendants'):
            val = self.co_defendants.data
            if val == 'yes':
                obj.co_defendants = True
            elif val == 'no':
                obj.co_defendants = False
            else:
                obj.co_defendants = None

    def validate(self, extra_validators=None):
        """
        Perform normal validation, then run any conditional checks.
        Must accept extra_validators to remain compatible with WTForms internal calls.
        """
        # call parent validate and forward extra_validators
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False

        # Example conditional rule area (keep optional by default).
        # Uncomment/modify to require fields for specific case types if desired.
        # if self.case_type.data == 'criminal' and not self.defendant.data:
        #     self.defendant.errors.append('Defendant name is recommended for criminal cases.')
        #     return False

        return True

class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    address = StringField('Address', validators=[Length(max=250)])
    submit = SubmitField('Save Client')

class DocumentForm(FlaskForm):
    filename = StringField('Document Name', validators=[DataRequired()])
    client_id = SelectField('Client', coerce=int)
    case_id = SelectField('Case', coerce=int)
    file = FileField('Upload File')
    submit = SubmitField('Save Document')

class NoteForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired()])
    date_made = DateTimeField('Date Made', format='%Y-%m-%d %H:%M', default=now)
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    case_id = SelectField('Case/Matter', coerce=int)
    client_id = SelectField('Client', coerce=int)
    event_id = SelectField('Event', coerce=int)
    document_id = SelectField('Document', coerce=int)
    submit = SubmitField('Save Note')

def get_year_choices():
    this_year = datetime.date.today().year
    return [(str(y), str(y)) for y in range(this_year, this_year + 3)]

def get_month_choices():
    return [(str(m).zfill(2), str(m).zfill(2)) for m in range(1, 13)]

def get_day_choices():
    return [(str(d).zfill(2), str(d).zfill(2)) for d in range(1, 32)]

def get_hour_choices():
    return [(str(h).zfill(2), str(h).zfill(2)) for h in range(0, 24)]

def get_minute_choices():
    return [(str(m).zfill(2), str(m).zfill(2)) for m in range(0, 60)]

class CalendarEventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    time_length = StringField('Time Length')
    deadline = BooleanField('Is there a Deadline?', default=False)
    event_datetime = StringField("Event Date & Time")
    deadline = BooleanField("Is Deadline?")
    deadline_datetime = StringField("Deadline Date & Time")
    case_id = SelectField('Case', coerce=int)
    client_id = SelectField('Client', coerce=int)
    document_id = SelectField('Document', coerce=int)
    user_id = SelectField('User', coerce=int)
    completed = BooleanField('Completed')
    submit = SubmitField('Save Event')

# -----------------------
# DOCUMENT / TEMPLATE FORMS
# -----------------------
class TemplateForm(FlaskForm):
    name = StringField('Template Name', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Template Content (Jinja2)', validators=[DataRequired()])
    submit = SubmitField('Save Template')

class GenerateDocumentForm(FlaskForm):
    template_id = SelectField('Template', coerce=int, validators=[DataRequired()])
    case_id = SelectField('Case', coerce=int, validators=[DataRequired()])
    filename = StringField('Output Filename (no extension)', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Generate Document')

# Multi-checkbox helper and Bulk form (if present in your codebase)
from wtforms import widgets, SelectMultipleField
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class BulkGenerateForm(FlaskForm):
    case_id = SelectField('Case', coerce=int, validators=[DataRequired()])
    doc_types = MultiCheckboxField('Documents to Generate', choices=[])
    submit = SubmitField('Generate Selected Documents')