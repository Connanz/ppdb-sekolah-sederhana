from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models import Form, db
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

payment_bp = Blueprint('payment_bp', __name__, template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@payment_bp.route('/payment/<int:form_id>', methods=['GET', 'POST'])
@login_required
def payment_process(form_id):
    form = Form.query.get_or_404(form_id)
    
    # Ensure the form belongs to the current user
    if form.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.index'))
    
    # Check if payment is already completed
    if form.payment_status == 'verified':
        flash('Pembayaran sudah diverifikasi', 'info')
        return redirect(url_for('form_bp.student_dashboard'))

    if request.method == 'POST':
        if 'payment_proof' not in request.files:
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(request.url)

        file = request.files['payment_proof']
        if file.filename == '':
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            try:
                # Create payment proofs directory if it doesn't exist
                payment_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'payment_proofs')
                os.makedirs(payment_folder, exist_ok=True)

                # Save payment proof
                filename = secure_filename(file.filename)
                unique_filename = f"payment_{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(payment_folder, unique_filename)
                file.save(file_path)

                # Update form payment status
                form.payment_proof = unique_filename
                form.payment_status = 'pending_verification'
                db.session.commit()

                flash('Bukti pembayaran berhasil diunggah', 'success')
                return redirect(url_for('payment_bp.payment_success'))
            
            except Exception as e:
                current_app.logger.error(f"Error in payment process: {str(e)}")
                flash('Terjadi kesalahan saat mengupload bukti pembayaran', 'error')
                return redirect(request.url)
        else:
            flash('Format file tidak diizinkan', 'error')
            return redirect(request.url)

    return render_template('parts/payment.html', form=form)

@payment_bp.route('/payment/success')
@login_required
def payment_success():
    return render_template('parts/payment_success.html')