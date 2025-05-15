from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models import Form, db
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

payment_bp = Blueprint('payment_bp', __name__)

def allowed_payment_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_PAYMENT_EXTENSIONS']

@payment_bp.route('/payment/<int:form_id>', methods=['GET', 'POST'])
@login_required
def payment_process(form_id):
    form = Form.query.get_or_404(form_id)
    
    if form.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # Ensure the payment_proofs directory exists
        os.makedirs(current_app.config['PAYMENT_UPLOADS'], exist_ok=True)

        if 'payment_proof' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
            
        file = request.files['payment_proof']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)

        if file and allowed_payment_file(file.filename):
            try:
                # Generate secure filename
                filename = secure_filename(file.filename)
                unique_filename = f"payment_{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config['PAYMENT_UPLOADS'], unique_filename)
                
                # Save the file
                file.save(file_path)
                
                # Update database
                form.payment_proof = unique_filename
                form.payment_status = 'pending_verification'
                db.session.commit()
                
                flash('Bukti pembayaran berhasil diupload!', 'success')
                return redirect(url_for('payment_bp.payment_success'))
            
            except Exception as e:
                current_app.logger.error(f"Payment upload error: {str(e)}")
                flash('Error uploading payment proof', 'error')
                return redirect(request.url)
        else:
            flash('File type not allowed. Please use JPG, JPEG, or PNG', 'error')
            return redirect(request.url)

    return render_template('parts/payment.html', form=form)

@payment_bp.route('/payment/success')
@login_required
def payment_success():
    return render_template('parts/payment_success.html')