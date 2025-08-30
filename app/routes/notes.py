from flask import Blueprint, render_template, redirect, url_for, request, flash

from app.forms.note_form import NoteForm

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')

@notes_bp.route('/', methods=['GET'])
def list_notes():
    notes = Note.query.all()
    return render_template('notes/list.html', notes=notes)

@notes_bp.route('/add', methods=['GET', 'POST'])
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            note=form.note.data,
            date_made=form.date_made.data,
            user_id=form.user_id.data,
            case_id=form.case_id.data,
            client_id=form.client_id.data,
            event_id=form.event_id.data,
            document_id=form.document_id.data
        )
        db.session.add(note)
        db.session.commit()
        flash('Note added successfully!', 'success')
        return redirect(url_for('notes.list_notes'))
    return render_template('notes/add.html', form=form)