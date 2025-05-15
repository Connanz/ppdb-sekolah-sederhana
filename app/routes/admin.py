from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models import Form, User, UserRole, Notification
from app import db
from datetime import datetime
from functools import wraps

# Inisialisasi blueprint untuk admin
admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')

# Verifikasi yang memastikan hanya admin yag dapat mengakses halaman admin, jika tidak maka akan diarahkan ke halaman utama(index_bp.index)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != UserRole.ADMIN.value:
            flash('Anda tidak memiliki akses ke halaman ini.', 'error')
            return redirect(url_for('index_bp.index'))
        return f(*args, **kwargs)
    return decorated_function

# Rute dashboard untuk admin 
@admin_bp.route('admin/dashboard')
@login_required
@admin_required
def dashboard():
    # Get forms by status
    pending_forms = Form.query.filter_by(status='pending').all()
    approved_forms = Form.query.filter_by(status='approved').order_by(Form.verification_date.desc()).all()
    rejected_forms = Form.query.filter_by(status='rejected').order_by(Form.verification_date.desc()).all()
    
    # Get pending payments
    pending_payments = Form.query.filter_by(payment_status='pending_verification').all()
    
    # Get counts
    pending_count = len(pending_forms)
    approved_count = len(approved_forms)
    rejected_count = len(rejected_forms)

    return render_template('parts/admindashboard.html',
                         pending_forms=pending_forms,
                         approved_forms=approved_forms,
                         rejected_forms=rejected_forms,
                         pending_payments=pending_payments,
                         pending_count=pending_count,
                         approved_count=approved_count,
                         rejected_count=rejected_count)

# rute untuk memverifikasi formulir pendaftaran oleh admin dari data yang dikirmkan oleh user/siswa-siswi
@admin_bp.route('/verify/<int:form_id>', methods=['POST'])
@login_required
@admin_required
def verify_form(form_id):
    form = Form.query.get_or_404(form_id)
    action = request.form.get('action')
    note = request.form.get('note')

    if action not in ['approve', 'reject']:
        flash('Aksi tidak valid', 'error')
        return redirect(url_for('admin_bp.dashboard'))

    try:
        # Update form status
        form.status = 'approved' if action == 'approve' else 'rejected'
        form.verified_by = current_user.id
        form.verification_date = datetime.utcnow()
        form.verification_note = note
        form.is_verified = True if action == 'approve' else False

        # Create notification for the user
        notification_message = (
            f"Pendaftaran untuk {form.student_name} telah " + 
            ("disetujui" if action == 'approve' else "ditolak")
        )
        if note:
            notification_message += f". Catatan: {note}"

        notification = Notification(
            user_id=form.user_id,
            message=notification_message
        )

        # Save changes
        db.session.add(notification)
        db.session.commit()

        flash(f'Formulir telah berhasil di{action}', 'success')

    except Exception as e:
        db.session.rollback()
        flash('Terjadi kesalahan saat memverifikasi formulir', 'error')
        current_app.logger.error(f"Error verifying form: {str(e)}")

    return redirect(url_for('admin_bp.dashboard'))

# rute untuk memverifikasi pembayaran oleh admin dari data yang dikirmkan oleh user/siswa-siswi
@admin_bp.route('/verify-payment/<int:form_id>', methods=['POST'])
@login_required
@admin_required
def verify_payment(form_id):
    form = Form.query.get_or_404(form_id)
    action = request.form.get('action')
    note = request.form.get('note')

    try:
        if action == 'verify':
            form.payment_status = 'verified'
            message = "Pembayaran Anda telah diverifikasi"
        else:
            form.payment_status = 'rejected'
            message = "Pembayaran Anda ditolak"

        if note:
            message += f". Catatan: {note}"

        form.payment_verified_at = datetime.utcnow()
        form.payment_verified_by = current_user.id

        # Create notification
        notification = Notification(
            user_id=form.user_id,
            message=message,
            form_id=form.id
        )
        db.session.add(notification)
        db.session.commit()

        flash(f'Status pembayaran berhasil diperbarui', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Terjadi kesalahan saat memverifikasi pembayaran', 'error')
        current_app.logger.error(f"Error verifying payment: {str(e)}")

    return redirect(url_for('admin_bp.dashboard'))

# Detail User/siswa-siswi yang telah mengirimkan formulir pendaftaran, namun ada verifikasi yang menunjukkan hanya admin yang dapat melihat detail siswa-siswi
@admin_bp.route('/student/<int:form_id>')
@login_required
def student_detail(form_id):
    if not current_user.is_admin():
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.index'))
        
    form = Form.query.get_or_404(form_id)
    return render_template('parts/student_detail.html', form=form)