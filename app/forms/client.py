from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length
from app.models.client import ClientType


class ClientForm(FlaskForm):
    """Form for creating and editing clients"""
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    client_type = SelectField('Client Type', choices=[
        (ClientType.INDIVIDUAL, 'Individual'),
        (ClientType.BUSINESS, 'Business'),
        (ClientType.NONPROFIT, 'Nonprofit'),
        (ClientType.GOVERNMENT, 'Government')
    ])

    # Contact information
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    city = StringField('City', validators=[Optional(), Length(max=100)])
    state = StringField('State/Province', validators=[Optional(), Length(max=100)])
    postal_code = StringField('Postal Code', validators=[Optional(), Length(max=20)])
    country = StringField('Country', validators=[Optional(), Length(max=100)])

    # Individual-specific fields
    date_of_birth = DateField('Date of Birth', validators=[Optional()], format='%Y-%m-%d')
    ssn_last_four = StringField('Last 4 of SSN', validators=[Optional(), Length(min=4, max=4)])

    # Business-specific fields
    company_name = StringField('Company Name', validators=[Optional(), Length(max=255)])
    industry = StringField('Industry', validators=[Optional(), Length(max=100)])
    tax_id = StringField('Tax ID', validators=[Optional(), Length(max=50)])
    website = StringField('Website', validators=[Optional(), Length(max=255)])

    # Additional information
    referral_source = StringField('Referral Source', validators=[Optional(), Length(max=255)])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=5000)])
    is_active = BooleanField('Active Client', default=True)
    submit = SubmitField('Save Client')


class ClientSearchForm(FlaskForm):
    """Form for searching clients"""
    keywords = StringField('Search', validators=[Optional()])
    client_type = SelectField('Client Type', validators=[Optional()], choices=[
        ('', 'All Types'),
        (ClientType.INDIVIDUAL, 'Individual'),
        (ClientType.BUSINESS, 'Business'),
        (ClientType.NONPROFIT, 'Nonprofit'),
        (ClientType.GOVERNMENT, 'Government')
    ])
    is_active = SelectField('Status', validators=[Optional()], choices=[
        ('', 'All Clients'),
        ('1', 'Active Clients Only'),
        ('0', 'Inactive Clients Only')
    ])
    submit = SubmitField('Search')