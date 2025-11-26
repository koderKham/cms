# cms/custom_fields_admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, CustomField
from wtforms import Form, StringField, SelectField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Optional

admin_bp = Blueprint('custom_fields_admin', __name__, template_folder='templates')

class CustomFieldForm(Form):
    name = StringField('Name (internal)', validators=[DataRequired()])
    slug = StringField('Slug (unique key)', validators=[DataRequired()])
    label = StringField('Label', validators=[DataRequired()])
    target = SelectField('Target', choices=[('case','Case'), ('client','Client')], validators=[DataRequired()])
    field_type = SelectField('Field Type', choices=[('text','Text'),('textarea','Textarea'),('select','Select'),('radio','Radio'),('checkbox','Checkbox'),('boolean','Checkbox (single)'),('date','Date'),('number','Number')], validators=[DataRequired()])
    options = TextAreaField('Options (JSON array or newline list)', validators=[Optional()])
    required = BooleanField('Required')
    help_text = TextAreaField('Help text', validators=[Optional()])
    order = IntegerField('Order', validators=[Optional()])

@admin_bp.route('/admin/custom_fields')
@login_required
def list_custom_fields():
    fields = CustomField.query.order_by(CustomField.target, CustomField.order).all()
    return render_template('admin_custom_fields_list.html', fields=fields)

@admin_bp.route('/admin/custom_fields/create', methods=['GET','POST'])
@login_required
def create_custom_field():
    form = CustomFieldForm(request.form)
    if request.method == 'POST' and form.validate():
        cf = CustomField(
            name=form.name.data,
            slug=form.slug.data,
            label=form.label.data,
            target=form.target.data,
            field_type=form.field_type.data,
            options=form.options.data,
            required=bool(form.required.data),
            help_text=form.help_text.data,
            order=form.order.data or 100,
            visible=True
        )
        db.session.add(cf)
        db.session.commit()
        flash('Custom field created.', 'success')
        return redirect(url_for('custom_fields_admin.list_custom_fields'))
    return render_template('admin_custom_field_form.html', form=form)