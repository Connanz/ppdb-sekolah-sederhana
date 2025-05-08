from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Form, User, UserRole
from app import db
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__, template_folder='templates')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != UserRole.ADMIN.value:
            flash('Anda tidak memiliki akses ke halaman ini.', 'error')
            return redirect(url_for('index.home'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    pending_forms = Form.query.filter_by(status='pending').all()
    return render_template('parts/admindashboard.html', forms=pending_forms)

@admin_bp.route('/verify/<int:form_id>', methods=['POST'])
@login_required
@admin_required
def verify_form(form_id):
    form = Form.query.get_or_404(form_id)
    action = request.form.get('action')
    note = request.form.get('note')

    if action not in ['approve', 'reject']:
        flash('Aksi tidak valid', 'error')
        return redirect(url_for('admin.dashboard'))

    form.status = 'approved' if action == 'approve' else 'rejected'
    form.verified_by = current_user.id
    form.verification_date = datetime.utcnow()
    form.verification_note = note

    try:
        db.session.commit()
        flash(f'Formulir telah berhasil di{action}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Terjadi kesalahan saat memverifikasi formulir', 'error')

    return redirect(url_for('admin.dashboard'))