from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models.person import Person
from app.forms.person import PersonForm
from flask_login import login_required

people = Blueprint('people', __name__)

@people.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = PersonForm()
    if form.validate_on_submit():
        if not (form.email.data or form.phone.data):
            form.email.errors.append('At least one contact (email or phone) is required.')
            return render_template('people/add.html', form=form)
        person = Person(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(person)
        db.session.commit()
        flash('Person added successfully.', 'success')
        return redirect(url_for('people.index'))
    return render_template('people/add.html', form=form)