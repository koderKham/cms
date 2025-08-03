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
        # Handle duration conversion from string to timedelta
        duration = None
        if form.duration.data:
            try:
                # Parse duration string (e.g., "2:30:00" for 2 hours 30 minutes)
                time_parts = form.duration.data.split(':')
                if len(time_parts) == 3:
                    from datetime import timedelta
                    duration = timedelta(hours=int(time_parts[0]), 
                                       minutes=int(time_parts[1]), 
                                       seconds=int(time_parts[2]))
            except (ValueError, IndexError):
                duration = None
        
        event = Event(
            title=form.title.data,
            description=form.description.data,
            event_type=form.event_type.data,
            datetime=form.datetime.data,
            case_id=form.case_id.data or None,
            client_id=form.client_id.data or None,
            document_id=form.document_id.data or None,
            location=form.location.data,
            duration=duration,
            status=form.status.data,
            priority=form.priority.data,
            is_recurring=form.is_recurring.data,
            recurrence_pattern=form.recurrence_pattern.data,
            notify_before=form.notify_before.data
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
    
    # Set duration field for display if event has duration
    if event.duration and form.duration.data is None:
        # Convert timedelta back to string format for form display
        total_seconds = int(event.duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        form.duration.data = f"{hours}:{minutes:02d}:{seconds:02d}"
    
    if form.validate_on_submit():
        # Handle duration conversion from string to timedelta
        duration = None
        if form.duration.data:
            try:
                # Parse duration string (e.g., "2:30:00" for 2 hours 30 minutes)
                time_parts = form.duration.data.split(':')
                if len(time_parts) == 3:
                    from datetime import timedelta
                    duration = timedelta(hours=int(time_parts[0]), 
                                       minutes=int(time_parts[1]), 
                                       seconds=int(time_parts[2]))
            except (ValueError, IndexError):
                duration = None
        
        event.title = form.title.data
        event.description = form.description.data
        event.event_type = form.event_type.data
        event.datetime = form.datetime.data
        event.case_id = form.case_id.data or None
        event.client_id = form.client_id.data or None
        event.document_id = form.document_id.data or None
        event.location = form.location.data
        event.duration = duration
        event.status = form.status.data
        event.priority = form.priority.data
        event.is_recurring = form.is_recurring.data
        event.recurrence_pattern = form.recurrence_pattern.data
        event.notify_before = form.notify_before.data
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