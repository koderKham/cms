from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required
from datetime import datetime
from app.models.event import Event, db
from app.forms.event_form import EventForm  # You should create this form as shown in previous messages

calendar_bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@calendar_bp.route('/', methods=['GET'])
@login_required
def index():
    # Optionally filter events by client, case, document, or date range
    try:
        events = Event.query.order_by(Event.datetime.asc()).all()
    except:
        pass
    events = "No events"
    return render_template('calendar/index.html', events=events)

@calendar_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            event_type=form.event_type.data,
            datetime=form.datetime.data,
            case_id=form.case_id.data or None,
            client_id=form.client_id.data or None,
            document_id=form.document_id.data or None
        )
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('calendar.index'))
    return render_template('calendar/add_event.html', form=form)

@calendar_bp.route('/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.event_type = form.event_type.data
        event.datetime = form.datetime.data
        event.case_id = form.case_id.data or None
        event.client_id = form.client_id.data or None
        event.document_id = form.document_id.data or None
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('calendar.index'))
    return render_template('calendar/edit_event.html', form=form, event=event)

@calendar_bp.route('/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('calendar.index'))