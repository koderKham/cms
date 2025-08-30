from flask import Blueprint, render_template, request, redirect, url_for, flash
import datetime

from flask_login import login_required

# Define the blueprint
billing_bp = Blueprint('billing', __name__)

# Simulated in-memory storage (replace with database in production)
cases = [
    {'id': 1, 'name': 'Case A'},
    {'id': 2, 'name': 'Case B'},
    {'id': 3, 'name': 'Case C'}
]
fees = []
expenses = []
payments = []

# Route to display billing details for all cases

@billing_bp.route('/index')
@login_required
def index():
    return render_template('billing/index.html', cases=cases, fees=fees, expenses=expenses, payments=payments)

# Route to add or update a fee for a case
@billing_bp.route('/billing/fee/<int:case_id>', methods=['GET', 'POST'])
def manage_fee(case_id):
    case = next((c for c in cases if c['id'] == case_id), None)
    if not case:
        flash('Case not found.', 'danger')
        return redirect(url_for('billing.index'))

    if request.method == 'POST':
        fee_type = request.form.get('fee_type')
        amount = request.form.get('amount')
        hourly_rate = request.form.get('hourly_rate')

        # Remove existing fee for this case
        fees[:] = [fee for fee in fees if fee['case_id'] != case_id]

        # Add the new fee
        fee = {
            'case_id': case_id,
            'fee_type': fee_type,
            'amount': float(amount) if amount else None,
            'hourly_rate': float(hourly_rate) if hourly_rate else None
        }
        fees.append(fee)

        flash('Fee updated successfully.', 'success')
        return redirect(url_for('billing.index'))

    # Get the current fee for this case
    current_fee = next((fee for fee in fees if fee['case_id'] == case_id), None)
    return render_template('billing/manage_fee.html', case=case, current_fee=current_fee)

# Route to record an expense for a case
@billing_bp.route('/billing/expense/<int:case_id>', methods=['GET', 'POST'])
def record_expense(case_id):
    case = next((c for c in cases if c['id'] == case_id), None)
    if not case:
        flash('Case not found.', 'danger')
        return redirect(url_for('billing.index'))

    if request.method == 'POST':
        description = request.form.get('description')
        amount = float(request.form.get('amount'))

        expense = {
            'case_id': case_id,
            'description': description,
            'amount': amount,
            'date': datetime.date.today().isoformat()
        }
        expenses.append(expense)

        flash('Expense recorded successfully.', 'success')
        return redirect(url_for('billing.index'))

    return render_template('billing/record_expense.html', case=case)

# Route to record a payment for a case
@billing_bp.route('/billing/payment/<int:case_id>', methods=['GET', 'POST'])
def record_payment(case_id):
    case = next((c for c in cases if c['id'] == case_id), None)
    if not case:
        flash('Case not found.', 'danger')
        return redirect(url_for('billing.index'))

    if request.method == 'POST':
        amount = float(request.form.get('amount'))

        payment = {
            'case_id': case_id,
            'amount': amount,
            'date': datetime.date.today().isoformat()
        }
        payments.append(payment)

        flash('Payment recorded successfully.', 'success')
        return redirect(url_for('billing.index'))

    return render_template('billing/record_payment.html', case=case)