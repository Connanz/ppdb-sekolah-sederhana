from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models import Form, User, UserRole, Notification
from app import db
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != UserRole.ADMIN.value:
            flash('Anda tidak memiliki akses ke halaman ini.', 'error')
            return redirect(url_for('index_bp.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('admin/dashboard')
@login_required
@admin_required
def dashboard():
    # Get forms by status
    pending_forms = Form.query.filter_by(status='pending').all()
    approved_forms = Form.query.filter_by(status='approved').order_by(Form.verification_date.desc()).all()
    rejected_forms = Form.query.filter_by(status='rejected').order_by(Form.verification_date.desc()).all()
    
    # Get counts
    pending_count = len(pending_forms)
    approved_count = len(approved_forms)
    rejected_count = len(rejected_forms)

    return render_template('parts/admindashboard.html',
                         pending_forms=pending_forms,
                         approved_forms=approved_forms,
                         rejected_forms=rejected_forms,
                         pending_count=pending_count,
                         approved_count=approved_count,
                         rejected_count=rejected_count)

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