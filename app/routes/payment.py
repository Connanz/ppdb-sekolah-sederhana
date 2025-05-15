from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Form, db
from datetime import datetime

payment_bp = Blueprint('payment_bp', __name__, template_folder='templates')

@payment_bp.route('/payment/<int:form_id>', methods=['GET', 'POST'])
@login_required
def payment_process(form_id):
    form = Form.query.get_or_404(form_id)
    
    # Ensure the form belongs to the current user
    if form.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        step = request.form.get('step')
        if step == 'confirm_payment':
            # Handle payment confirmation
            payment_proof = request.files.get('payment_proof')
            if payment_proof:
                # Save payment proof logic here
                form.payment_status = 'pending_verification'
                db.session.commit()
                flash('Bukti pembayaran berhasil diunggah', 'success')
                return redirect(url_for('payment_bp.payment_success'))
    
    return render_template('parts/payment.html', form=form)

@payment_bp.route('/payment/success')
@login_required
def payment_success():
    return render_template('parts/payment_success.html')