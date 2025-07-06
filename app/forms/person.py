from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, Email, Length

class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Add Person')