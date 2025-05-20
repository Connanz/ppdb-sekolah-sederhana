from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models import Form, User, UserRole, Notification
from app import db
from datetime import datetime
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import func
from collections import Counter
from app.utils.email import send_verification_email

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
    
    # Get payments by status
    pending_payments = Form.query.filter_by(payment_status='pending_verification').all()
    verified_payments = Form.query.filter_by(payment_status='verified').all()
    rejected_payments = Form.query.filter_by(payment_status='rejected').all()
    
    # Get counts
    pending_count = len(pending_forms)
    approved_count = len(approved_forms)
    rejected_count = len(rejected_forms)

    return render_template('parts/admindashboard.html',
                         pending_forms=pending_forms,
                         approved_forms=approved_forms,
                         rejected_forms=rejected_forms,
                         pending_payments=pending_payments,
                         verified_payments=verified_payments,
                         rejected_payments=rejected_payments,
                         pending_count=pending_count,
                         approved_count=approved_count,
                         rejected_count=rejected_count)

# rute untuk memverifikasi formulir pendaftaran oleh admin dari data yang dikirmkan oleh user/siswa-siswi
@admin_bp.route('/verify-form/<int:form_id>', methods=['POST'])
@login_required
@admin_required
def verify_form(form_id):
    form = Form.query.get_or_404(form_id)
    action = request.form.get('action')
    note = request.form.get('note', '')

    if action == 'approve':
        form.status = 'approved'
        form.verified_by = current_user.id
        form.verification_date = datetime.utcnow()
        form.verification_note = note
        form.is_verified = True
        
        # Buat notifikasi
        notification = form.create_notification(
            'Pendaftaran Anda telah diverifikasi dan diterima.'
        )
        
        # Kirim email verifikasi
        if send_verification_email(form.student_email, form.student_name):
            flash('Form diverifikasi dan email pemberitahuan terkirim', 'success')
        else:
            flash('Form diverifikasi tetapi gagal mengirim email', 'warning')
            
        db.session.commit()
        return redirect(url_for('admin_bp.dashboard'))
        
    # Add 'cancel' to valid actions
    if action not in ['approve', 'reject', 'cancel']:
        flash('Aksi tidak valid', 'error')
        return redirect(url_for('admin_bp.dashboard'))

    try:
        if action == 'cancel':
            # Reset form status to pending
            form.status = 'pending'
            form.verified_by = None
            form.verification_date = None
            form.verification_note = None
            form.is_verified = False

            notification_message = f"Status verifikasi pendaftaran untuk {form.student_name} telah dibatalkan dan kembali ke status menunggu verifikasi."
        else:
            # Existing logic for approve/reject
            form.status = 'approved' if action == 'approve' else 'rejected'
            form.verified_by = current_user.id
            form.verification_date = datetime.utcnow()
            form.verification_note = note
            form.is_verified = True if action == 'approve' else False

            notification_message = (
                f"Pendaftaran untuk {form.student_name} telah " + 
                ("disetujui" if action == 'approve' else "ditolak")
            )
            if note:
                notification_message += f". Catatan: {note}"

        # Create notification
        notification = Notification(
            user_id=form.user_id,
            message=notification_message
        )

        # Save changes
        db.session.add(notification)
        db.session.commit()

        if action == 'cancel':
            flash('Status verifikasi berhasil dibatalkan', 'success')
        else:
            flash(f'Formulir telah berhasil di{action}', 'success')

    except Exception as e:
        db.session.rollback()
        flash('Terjadi kesalahan saat memproses verifikasi', 'error')
        current_app.logger.error(f"Error processing form verification: {str(e)}")

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

@admin_bp.route('/profile')
@login_required
@admin_required
def profile():
    return render_template('parts/profile_admin.html')

@admin_bp.route('/change-password', methods=['POST'])
@login_required
@admin_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Verify current password
    if not check_password_hash(current_user.password, current_password):
        flash('Password saat ini salah!', 'error')
        return redirect(url_for('admin_bp.profile'))

    # Verify new passwords match
    if new_password != confirm_password:
        flash('Password baru dan konfirmasi password tidak cocok!', 'error')
        return redirect(url_for('admin_bp.profile'))

    try:
        # Update password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password berhasil diubah!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error changing password: {str(e)}")
        flash('Terjadi kesalahan saat mengubah password', 'error')

    return redirect(url_for('admin_bp.profile'))

@admin_bp.route('/laporan')
@login_required
@admin_required
def laporan():
    # Get total registrations
    total_registrations = Form.query.count()
    
    # Get age statistics as list of tuples
    age_stats_query = db.session.query(
        Form.student_age,
        func.count(Form.student_age).label('count')
    ).group_by(Form.student_age).order_by(Form.student_age).all()
    
    # Convert SQLAlchemy Row objects to lists
    age_stats = [[row[0], row[1]] for row in age_stats_query]
    
    # Calculate age statistics
    if age_stats:
        min_age = min(row[0] for row in age_stats)
        max_age = max(row[0] for row in age_stats)
        total_students = sum(row[1] for row in age_stats)
        avg_age = sum(row[0] * row[1] for row in age_stats) / total_students
    else:
        min_age = max_age = avg_age = 0
        total_students = 0

    # Get school statistics as list of tuples
    school_stats_query = db.session.query(
        Form.school_name,
        func.count(Form.school_name).label('count')
    ).group_by(Form.school_name).order_by(func.count(Form.school_name).desc()).all()
    
    # Convert SQLAlchemy Row objects to lists
    school_stats = [[row[0], row[1]] for row in school_stats_query]
    
    # Get top 5 schools for pie chart
    top_schools = school_stats[:5] if school_stats else []
    
    # Get status statistics
    status_counts = dict(db.session.query(
        Form.status,
        func.count(Form.status)
    ).group_by(Form.status).all())
    
    return render_template('parts/laporan.html',
                         total_registrations=total_registrations,
                         age_stats=age_stats,
                         min_age=min_age,
                         max_age=max_age,
                         avg_age=round(avg_age, 1),
                         school_stats=school_stats,
                         top_schools=top_schools,
                         status_stats=status_counts)