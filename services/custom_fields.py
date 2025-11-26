# services/custom_fields.py
import json
from wtforms import StringField, TextAreaField, SelectField, RadioField, BooleanField, DateField, IntegerField, FieldList
from wtforms.validators import InputRequired, Optional
from models import CustomField, CustomFieldValue
from flask import current_app
from datetime import datetime

FIELD_TYPE_MAPPING = {
    'text': StringField,
    'textarea': TextAreaField,
    'select': SelectField,
    'radio': RadioField,
    'checkbox': SelectField,  # multi-select represented as SelectField with multiple choices handled specially in template or you can use FieldList
    'boolean': BooleanField,
    'date': DateField,
    'number': IntegerField,
}

def get_custom_fields_for(target):
    """Return visible custom fields for 'case' or 'client' ordered by 'order'."""
    q = CustomField.query.filter_by(target=target, visible=True).order_by(CustomField.order.asc(), CustomField.id.asc())
    return q.all()

def attach_custom_fields_to_form(form, target, owner=None):
    """
    Given an existing WTForms form instance, attach dynamic fields to it in-memory.
    - form: instance (not class) of your form
    - target: 'case' or 'client'
    - owner: an existing Case/Client instance for edit (optional) to populate current values
    Returns: list of CustomField objects attached (in order)
    """
    fields = get_custom_fields_for(target)
    for cf in fields:
        field_name = f'custom_{cf.slug}'
        wtfield_cls = FIELD_TYPE_MAPPING.get(cf.field_type, StringField)

        validators = [InputRequired()] if cf.required else [Optional()]

        # choices for select/radio/checkbox:
        if cf.field_type in ('select', 'radio', 'checkbox'):
            choices = cf.get_options_list()
            # For SelectField with no default, add an empty choice if not required
            if not cf.required:
                choices = [('', '')] + choices
            wtfield = wtfield_cls(cf.label, choices=choices, validators=validators, description=cf.help_text)
        elif cf.field_type == 'boolean':
            wtfield = wtfield_cls(cf.label, validators=validators, description=cf.help_text)
        elif cf.field_type == 'date':
            wtfield = wtfield_cls(cf.label, format='%Y-%m-%d', validators=validators, description=cf.help_text)
        else:
            # text/textarea/number fallback
            wtfield = wtfield_cls(cf.label, validators=validators, description=cf.help_text)

        # attach to form instance
        setattr(form, field_name, wtfield)

        # populate existing value if owner provided
        if owner:
            val = None
            if target == 'case':
                existing = CustomFieldValue.query.filter_by(field_id=cf.id, case_id=getattr(owner, 'id', None)).first()
            else:
                existing = CustomFieldValue.query.filter_by(field_id=cf.id, client_id=getattr(owner, 'id', None)).first()
            if existing:
                # decode JSON arrays for checkbox fields
                v = existing.value
                try:
                    parsed = json.loads(v)
                    form_field_value = parsed
                except Exception:
                    form_field_value = v
                # set attribute value on field (WTForms expects .data)
                getattr(form, field_name).data = form_field_value

    return fields

def save_custom_field_values(owner, target, custom_fields, form):
    """
    Persist custom field values from form to CustomFieldValue rows for owner (Case/Client).
    - owner: Case or Client model instance
    - target: 'case' or 'client'
    - custom_fields: list of CustomField objects (as returned by get_custom_fields_for)
    - form: the form instance that now has fields attached
    """
    # helper to pick owner id field name
    owner_id_name = 'case_id' if target == 'case' else 'client_id'
    for cf in custom_fields:
        field_name = f'custom_{cf.slug}'
        if not hasattr(form, field_name):
            continue
        form_field = getattr(form, field_name)
        raw = form_field.data

        # normalize value to string for storage. For multiple choices (checkbox) ensure JSON array.
        if cf.field_type == 'checkbox':
            # Expect raw to be list-like. Save as JSON
            to_store = json.dumps(raw if raw is not None else [])
        else:
            # boolean -> '1'/'0' or store JSON true/false? We'll store as string via json to preserve types
            # Use json.dumps to preserve booleans and numbers consistently
            try:
                to_store = json.dumps(raw)
            except Exception:
                to_store = str(raw) if raw is not None else None

        # find existing value
        filters = {'field_id': cf.id}
        if target == 'case':
            filters['case_id'] = owner.id
            existing = CustomFieldValue.query.filter_by(**filters).first()
        else:
            filters['client_id'] = owner.id
            existing = CustomFieldValue.query.filter_by(**filters).first()

        if existing:
            existing.value = to_store
            existing.updated_at = datetime.utcnow()
        else:
            kwargs = {'field_id': cf.id, 'value': to_store}
            if target == 'case':
                kwargs['case_id'] = owner.id
            else:
                kwargs['client_id'] = owner.id
            newv = CustomFieldValue(**kwargs)
            db.session.add(newv)
    # commit is caller's responsibility