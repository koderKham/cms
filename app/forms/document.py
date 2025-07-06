from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Optional

class DocumentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    file = FileField('File', validators=[DataRequired()])
    # Only allow one association
    person_id = IntegerField('Person ID', validators=[Optional()])
    case_id = IntegerField('Case ID', validators=[Optional()])
    event_id = IntegerField('Event ID', validators=[Optional()])
    submit = SubmitField('Save Document')