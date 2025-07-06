from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, FloatField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from app.models.case import CaseType, CaseStatus


class CaseForm(FlaskForm):
    """Form for creating and editing cases"""
    title = StringField('Case Title', validators=[DataRequired(), Length(max=255)])
    case_number = StringField('Case Number', validators=[Length(max=50)])
    type = SelectField('Case Type', choices=[
        (CaseType.LITIGATION, 'Litigation'),
        (CaseType.CORPORATE, 'Corporate'),
        (CaseType.FAMILY, 'Family Law'),
        (CaseType.CRIMINAL, 'Criminal Defense'),
        (CaseType.ESTATE, 'Estate Planning'),
        (CaseType.REAL_ESTATE, 'Real Estate'),
        (CaseType.IMMIGRATION, 'Immigration'),
        (CaseType.TAX, 'Tax Law'),
        (CaseType.INTELLECTUAL_PROPERTY, 'Intellectual Property'),
        (CaseType.OTHER, 'Other')
    ])
    status = SelectField('Status', choices=[
        (CaseStatus.OPEN, 'Open'),
        (CaseStatus.PENDING, 'Pending'),
        (CaseStatus.CLOSED, 'Closed'),
        (CaseStatus.ARCHIVED, 'Archived')
    ])
    description = TextAreaField('Description', validators=[Optional(), Length(max=5000)])
    court_name = StringField('Court', validators=[Optional(), Length(max=255)])
    judge_name = StringField('Judge', validators=[Optional(), Length(max=100)])
    opposing_counsel = StringField('Opposing Counsel', validators=[Optional(), Length(max=255)])
    filing_date = DateField('Filing Date', validators=[Optional()], format='%Y-%m-%d')
    hearing_date = DateField('Hearing Date', validators=[Optional()], format='%Y-%m-%d')

    # Financial information
    hourly_rate = FloatField('Hourly Rate', validators=[Optional(), NumberRange(min=0)])
    retainer_amount = FloatField('Retainer Amount', validators=[Optional(), NumberRange(min=0)])

    # References
    client_id = SelectField('Client', coerce=int, validators=[DataRequired()])
    lead_attorney_id = SelectField('Lead Attorney', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Save Case')


class CaseSearchForm(FlaskForm):
    """Form for searching cases"""
    keywords = StringField('Search', validators=[Optional()])
    case_type = SelectField('Case Type', validators=[Optional()], choices=[
        ('', 'All Types'),
        (CaseType.LITIGATION, 'Litigation'),
        (CaseType.CORPORATE, 'Corporate'),
        (CaseType.FAMILY, 'Family Law'),
        (CaseType.CRIMINAL, 'Criminal Defense'),
        (CaseType.ESTATE, 'Estate Planning'),
        (CaseType.REAL_ESTATE, 'Real Estate'),
        (CaseType.IMMIGRATION, 'Immigration'),
        (CaseType.TAX, 'Tax Law'),
        (CaseType.INTELLECTUAL_PROPERTY, 'Intellectual Property'),
        (CaseType.OTHER, 'Other')
    ])
    status = SelectField('Status', validators=[Optional()], choices=[
        ('', 'All Statuses'),
        (CaseStatus.OPEN, 'Open'),
        (CaseStatus.PENDING, 'Pending'),
        (CaseStatus.CLOSED, 'Closed'),
        (CaseStatus.ARCHIVED, 'Archived')
    ])
    submit = SubmitField('Search')